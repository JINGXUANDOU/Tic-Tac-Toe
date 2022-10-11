import socket
from tkinter import messagebox
from threading import Thread
from time import sleep
from unicodedata import numeric
from gameboard import BoardClass
from startup_dlg import StartupDlg
from game_window import GameWindow
from choice_dlg import ChoiceDlg
import coordinate

RECV_SIZE = 1024    # read at most 1024 bytes
PLAYER1_CHESS = '×'
PLAYER2_CHESS = '◯'
PLAYER2_USERNAME = 'player2'    # The username of player2


class Player2(GameWindow):
    """A class to handle operations of player2.

    Attributes:
        sock: Socket variable object.
        player1_name(str): The username of player1.
        player2_name(str): The username of player2.
        on_move: On move function which is called when chessboard is clicked.
        conn_sock: The accepted socket.
        exit_thread(bool): The boolean variable that controls the loop.
        sock_state(int): The integer of socket state.
    """
    def __init__(self) -> None:
        """Make player1's gameboard."""
        super(Player2, self).__init__(PLAYER2_CHESS)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player1_name = ''
        self.player2_name = PLAYER2_USERNAME
        self.on_move = self.on_player2_move

        self.conn_sock = None
        self.exit_thread = False
        self.sock_state = 0
 

    def setup_server(self) -> bool:
        '''Set up player2(server) with user inputs and wait for player1's(client) connection.

        A valid port information should be an integer that is greater than 1024.

        Returns:
            True if no error occurs, False otherwise.
        '''
        dlg = StartupDlg(False)

        while True:
            if not dlg.run():
                break
            try:
                self.sock.bind(dlg.get_host_info())
                self.sock.listen(1)
                dlg.destroy()
                return True
            except socket.error as msg:     # socket error: fail to sent request
                 messagebox.showwarning("Error", "Socket Error: %s" % msg)
            except TypeError as msg:     # TypeError: wrong information type
                messagebox.showwarning("Error", "Type Error: %s" % msg)
            except OverflowError as msg:     # OverflowError: fail to connect after a long time
                messagebox.showwarning("Error", "Overflow Error: %s" % msg)
            except:  #Error for other unexpected errors
                messagebox.showwarning("Error", "Some unknown error occurs.")

        dlg.destroy()        
        return False


    def recv_player1_move(self) -> None:
        '''Receives player1's move through network and update it on the board.

        Raises:
            ValueError: if the move is out of range.
        '''

        self.enable_set(False)
        self.update_turn("%s's turn" % self.player1_name)

        player1_move = self.conn_sock.recv(RECV_SIZE).decode()     # receive player1's move
        x, y = coordinate.parse_coordinate(player1_move)
        self.gameboard.updateGameBoard(self.player1_name, x, y)
        self.set(x, y, PLAYER1_CHESS)

        if self.gameboard.isWinner() or self.gameboard.boardIsFull():
            self.update_stats(self.gameboard)
            self.sock_state = 3
            self.update_turn("")
        else:
            self.sock_state = 2
            self.enable_set(True)
            self.update_turn("%s's turn" % self.player2_name)



    def on_player2_move(self, x: int, y: int) -> None:
        '''Player2 moves a step and sends the move to player1.

        Args:
            x: The x-coordinate of the slot.
            y: The y-coordinate of the slot.
        '''
        self.conn_sock.sendall("{},{}".format(x, y).encode())
        self.gameboard.updateGameBoard(self.player2_name, x, y)

        if self.gameboard.isWinner() or self.gameboard.boardIsFull():
            self.update_stats(self.gameboard)
            self.sock_state = 3
        else:
            self.sock_state = 1


    def recv_play_again(self) -> bool:
        '''Receives player1's choice for whether the user wants to try again.

        Returns
            True represents yes or False represents no.
        '''
        choice = self.conn_sock.recv(RECV_SIZE).decode()     # receive player1's choice
        if choice == 'Play Again':
            self.gameboard.resetGameBoard()
            self.reset()
            return True
        else:
            self.update_stats(self.gameboard)
            self.reset()
            return False


    def start_socket(self) -> None:
        """The socket thread function that does all the internet operations here."""
        while not self.exit_thread:
            if self.sock_state == 0:        # wait connected
                self.accept()
                self.sock_state = 1
                continue

            if self.sock_state == 1:      # receive player1 move
                self.recv_player1_move()
                continue

            if self.sock_state == 2:       # wait player2 move
                sleep(1)
                continue

            if self.sock_state == 3:      # receive play again choice
                if self.recv_play_again():
                    self.sock_state = 1
                    self.update_turn("%s's turn" % self.player1_name)
                    self.enable_set(True)
                else:
                    self.sock_state = 0
                    self.conn_sock.close()
                    self.conn_sock = None
                continue

        if self.conn_sock:
            self.conn_sock.close()
            self.conn_sock = None


    def accept(self) -> None:
        """Accepts incoming connection, and creates gameboard. """
        try:
            self.conn_sock, addr = self.sock.accept()

            self.player1_name = self.conn_sock.recv(RECV_SIZE).decode() # receive player1_username
            self.conn_sock.sendall(self.player2_name.encode())

            self.gameboard = BoardClass(self.player1_name, self.player2_name, self.player2_name)
            self.update_stats(self.gameboard)
            self.enable_set(False)
            self.update_turn("%s's turn" % self.player1_name)
        except:
            pass


    def play_game(self) -> None:
        '''Two players play the game

        Creates widget and thread, then starts the game.
        '''

        t = Thread(target=self.start_socket)        # create thread, thread function is start_socket
        t.start()                           # start Thread

        self.create_widget()
        self.run()                      # start window mainloop

        self.exit_thread = True

        if self.conn_sock:
            self.conn_sock.close()

        self.sock.close()

        t.join()                # wait thread exit
        self.destroy()


if __name__ == '__main__':
    player = Player2()

    if player.setup_server():
        player.play_game()
    