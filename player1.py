import socket
from tkinter import messagebox
from threading import Thread
from time import sleep
from gameboard import BoardClass
from startup_dlg import StartupDlg
from game_window import GameWindow
from choice_dlg import ChoiceDlg
import coordinate

RECV_SIZE = 1024    # read at most 1024 bytes
PLAYER1_CHESS = '×'     # player1's chess is 'X'
PLAYER2_CHESS = '◯'    # player1's chess is 'O'

# class Player1, GameWindow
class Player1(GameWindow):
    """A class to handle operations of player1.

    Attributes:
        sock: Socket variable object.
        player1_name(str): The username of player1.
        player2_name(str): The username of player2.
        on_move: On move function which is called when chessboard is clicked.
        exit_thread(bool): The boolean variable that controls the loop.
        sock_state(int): The integer of socket state.
    """
    def __init__(self) -> None:
        """Make player1's gameboard."""
        super(Player1, self).__init__(PLAYER1_CHESS)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player1_name = ''
        self.player2_name = ''
        self.on_move = self.on_player1_move     # on_move function，calls when chessboard is clicked
        self.exit_thread = False                # thread marker，True represents getting out from thread loop
        self.sock_state = 0                     # the socket state at present


    def connect(self) -> bool:
        '''Connect player1(client) to player2(server) with user inputs.

        A valid port information should be an integer that is greater than 1024.
        A valid choice information should be either 'y' or 'n'.

        Returns:
            True if no error occurs, False otherwise.
        '''
        user_choice = ''   # Set up a variable 'user_choice' that would be used later
        dlg = StartupDlg(True)

        while user_choice != 'n':    # Stop connection when user input 'n', continue otherwise
            if not dlg.run():
                break

            try:
                self.sock.connect(dlg.get_host_info())   # Connect to player2
                self.player1_name = dlg.get_user_name()
                self.sock_state = 1
                dlg.destroy()
                return True
            except socket.error as msg:     # socket error: fail to sent request
                choice_dlg = ChoiceDlg('Connect fail: %s.\n\nDo you want to try again?' % msg)
                user_choice = choice_dlg.run()
                choice_dlg.destroy()
            except TypeError as msg:     # TypeError: wrong information type
                messagebox.showwarning("Error", "Type Error: %s" % msg)
            except OverflowError as msg:     # OverflowError: fail to connect after a long time
                messagebox.showwarning("Error", "Overflow Error: %s" % msg)
            except:  #Error for other unexpected errors
                messagebox.showwarning("Error", "Some unknown error occurs.")

        dlg.destroy()
        return False


    def check_play_again(self) -> bool:
        '''Check the user input choice for whether the user wants to play again.

        Returns:
            True represents yes or False represents no.
        '''
        dlg = ChoiceDlg('Would you want to play again?')
        play_again_choice = dlg.run() 
        dlg.destroy()

        if play_again_choice == 'y':     # Justify whether player1 wants to start a new game
            self.sock.sendall('Play Again'.encode())
            self.gameboard.resetGameBoard()
            self.reset()
            return True
        else:
            self.sock.sendall('Fun Times'.encode())
            self.exit_thread = True
            self.destroy()
            return False


    def on_player1_move(self, x: int, y: int) -> None:
        '''Player1 moves a step and sends the move to player2.

        The methon is called when click a slot.

        Args:
            x(int): The x-coordinate of player1's move.
            y(int): The y-coordinate of player1's move.

        '''
        self.sock.sendall("{},{}".format(x, y).encode())
        self.gameboard.updateGameBoard(self.gameboard.player1_name, x, y)

        if self.gameboard.isWinner() or self.gameboard.boardIsFull():
            self.sock_state = 3
            self.update_stats(self.gameboard)
        else:
            self.sock_state = 2

        self.enable_set(False)


    def recv_player2_move(self) -> None:
        '''Receives player2's move through network and update it on the board.

        Raises:
            ValueError: if the move is out of range.  
        '''
        self.enable_set(False)
        self.update_turn("%s's turn" % self.player2_name)

        player2_move = self.sock.recv(RECV_SIZE).decode()    #Receives player2's move
        x, y = coordinate.parse_coordinate(player2_move)
        self.gameboard.updateGameBoard(self.player2_name, x, y)
        self.set(x, y, PLAYER2_CHESS)

        if self.gameboard.isWinner() or self.gameboard.boardIsFull():
            self.update_stats(self.gameboard)
            self.update_turn("")
            self.sock_state = 3
        else:
            self.sock_state = 1
            self.update_turn("%s's turn" % self.player1_name)
            self.enable_set(True)


    def start_socket(self) -> None:     # socket thread function
        """The socket thread function that does all the internet operations here."""
        while not self.exit_thread:
            if self.sock_state == 1:        # wait player1 move
                sleep(1)
                continue

            if self.sock_state == 2:      # receive player2 move
                self.recv_player2_move()
                continue

            if self.sock_state == 3:    # check play again
                if not self.check_play_again():
                    break

                self.update_turn("%s's turn" % self.player1_name)
                self.enable_set(True)
                self.sock_state = 1


    def play_game(self) -> None:
        '''Two players play the game

        Creates widget, gameboard and thread, then starts the game.
        '''
        self.create_widget()
        self.sock.sendall(self.player1_name.encode())
        self.player2_name = self.sock.recv(RECV_SIZE).decode()     # Receives player2's username

        self.gameboard = BoardClass(self.player1_name, self.player2_name, self.player1_name)
        self.update_stats(self.gameboard)
        self.enable_set(True)
        self.update_turn("%s's turn" % self.player1_name)

        t = Thread(target=self.start_socket)        # create thread, thread function is start_socket
        t.start()                           # start Thread

        self.run()                      # start window mainloop

        self.exit_thread = True
        self.sock.close()

        t.join()                # wait thread exit


if __name__ == '__main__':
    player = Player1()

    if player.connect():
        player.play_game()
    