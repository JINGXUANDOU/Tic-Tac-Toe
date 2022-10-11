import tkinter as tk
from tkinter import messagebox
from gameboard import BoardClass


FONT = ('Ariel', 32)            # Typeface and size of chess.

# game window

class GameWindow:
    """A class to do operations of gamewindow.
    
    Attributes:
        chess(str): The chess character of player.
        board(list): The gameboard of the game.
        slot_stat(list of integers): The state of gameboard slots.
        on_move: On move callback function.
        is_enable_set(bool): The boolean flag that allows player to put a chess."""
    def __init__(self, chess: str) -> None:
        """Create a gamewindow"""
        self.chess = chess                  # character of chess
        self.board = [[],[],[]]             # chessboard with grid buttons
        self.slot_stat = [0, 0, 0, 0, 0, 0, 0, 0, 0]        # situation of grids on gameboard. 0 stands for no chess and 1 stands for chess.
        self.on_move = None                 # on_move function which is called after a chess is called.
        self.is_enable_set = False          # whether the grid allows player to put a chess，True stands for yes，False stands for no.


    def create_widget(self) -> None:        # create widgets in window
        """create a widget"""
        self.window = tk.Tk()               # root window
        self.window.resizable(False, False)
        self.window.title("Tic Tac Toe")

        left_frame = tk.Frame(self.window, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT)

        right_frame = tk.Frame(self.window, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT)

        # Fill left frame
        self.current_turn_label = tk.Label(left_frame)
        self.current_turn_label.pack()

        board_area = tk.Frame(left_frame, bg='white')
        board_area.pack()
        self.create_board_area(board_area)

        # Fill right frame
        statistic_area = tk.LabelFrame(right_frame, text="Statistics", width=300, labelanchor="n", padx=10)
        statistic_area.pack()
        statistic_area.pack_propagate(False)
        self.create_statistic_area(statistic_area)

        result_area = tk.LabelFrame(right_frame, text="Game Result", height=50, width=195, labelanchor="n", padx=10)
        result_area.pack()
        result_area.pack_propagate(False)
        self.create_result_area(result_area)

        self.window.geometry('+%d+%d' % ((self.window.winfo_screenwidth()-300)/2, (self.window.winfo_screenheight()-400)/2))


    def create_board_area(self, area: tk.Frame) -> None:
        """create a board area for game"""
        button = tk.Button(area, text="", width=3, font=FONT, command=lambda: self.on_set(0, 0))
        button.grid(row=0, column=0)
        self.board[0].append(button)

        button = tk.Button(area, text="", width=3, font=FONT, command=lambda: self.on_set(0, 1))
        button.grid(row=0, column=1)
        self.board[0].append(button)

        button = tk.Button(area, text="", width=3, font=FONT, command=lambda: self.on_set(0, 2))
        button.grid(row=0, column=2)
        self.board[0].append(button)

        button = tk.Button(area, text="", width=3, font=FONT, command=lambda: self.on_set(1, 0))
        button.grid(row=1, column=0)
        self.board[1].append(button)

        button = tk.Button(area, text="", width=3, font=FONT, command=lambda: self.on_set(1, 1))
        button.grid(row=1, column=1)
        self.board[1].append(button)

        button = tk.Button(area, text="", width=3, font=FONT, command=lambda: self.on_set(1, 2))
        button.grid(row=1, column=2)
        self.board[1].append(button)

        button = tk.Button(area, text="", width=3, font=FONT, command=lambda: self.on_set(2, 0))
        button.grid(row=2, column=0)
        self.board[2].append(button)

        button = tk.Button(area, text="", width=3, font=FONT, command=lambda: self.on_set(2, 1))
        button.grid(row=2, column=1)
        self.board[2].append(button)

        button = tk.Button(area, text="", width=3, font=FONT, command=lambda: self.on_set(2, 2))
        button.grid(row=2, column=2)
        self.board[2].append(button)


    def create_statistic_area(self, area: tk.LabelFrame) -> None:
        """Create statistic board which shows player name, wins and losses.
        
        Args:
            area: The area of showing words.
        """
        tk.Label(area, text="Player1: ").grid(row=0, sticky="w")
        tk.Label(area, text="Player2: ").grid(row=1, sticky="w")
        tk.Label(area, text="User of last move: ").grid(row=2, sticky="w")
        tk.Label(area, text="Number of games: ").grid(row=3, sticky="w")
        tk.Label(area, text="Number of wins: ").grid(row=4, sticky="w")
        tk.Label(area, text="Number of losses: ").grid(row=5, sticky="w")
        tk.Label(area, text="Number of ties: ").grid(row=6, sticky="w")
        
        self.player1_label = tk.Label(area, text='           ')
        self.player1_label.grid(row=0, column=1)

        self.player2_label = tk.Label(area)
        self.player2_label.grid(row=1, column=1)

        self.user_last_move_label = tk.Label(area)
        self.user_last_move_label.grid(row=2, column=1)

        self.number_of_games_label = tk.Label(area)
        self.number_of_games_label.grid(row=3, column=1)

        self.wins_label = tk.Label(area)
        self.wins_label.grid(row=4, column=1)

        self.losses_label = tk.Label(area)
        self.losses_label.grid(row=5, column=1)

        self.ties_label = tk.Label(area)
        self.ties_label.grid(row=6, column=1)


    def create_result_area(self, area: tk.LabelFrame) -> None:
        """Create an area to show results
        
        Args:
            area: The area of showing."""
        self.result_label = tk.Label(area, text="Game is playing!")
        self.result_label.pack()


    def destroy(self) -> None:      # destroy window
        """Destroy the window when finishing."""
        self.window.quit()


    def on_set(self, x: int, y: int) -> None:       # Called when putting a chess
        """Callback function when a chess is put on the board
        
        Args:
            x: The x-coordinate of the chess.
            y: The y-cordinate of the chess.
        """
        if not self.is_enable_set:
            return

        if self.slot_stat[x * 3 + y] == 1:
            return

        self.slot_stat[x * 3 + y] = 1
        self.board[x][y].configure(text=self.chess, font=FONT)
        self.on_move(x + 1, y + 1)


    def enable_set(self, enable: bool) -> None:     # enable slot can be click
        """enable slot to be clicked
        
        Args:
            enable: A boolean that represents whether the slot is able to click.
        """
        self.is_enable_set = enable


    def set(self, x: int, y: int, chess: str) -> None:
        self.board[x-1][y-1].configure(text=chess, font=FONT)
        self.slot_stat[(x-1)*3+y-1] = 1


    def reset(self):        # reset board
        for row in range(3):
            for col in range(3):
                self.board[row][col].configure(text='')
        
        for i in range(9):
            self.slot_stat[i] = 0


    def run(self):
        self.window.mainloop()


    def update_turn(self, msg: str) -> None:        # update turn label，whose turn
        self.current_turn_label.configure(text=msg)


    def update_stats(self, gameboard: BoardClass) -> None:      # update statis and status label
        self.player1_label.configure(text=gameboard.player1_name)
        self.player2_label.configure(text=gameboard.player2_name)
        self.user_last_move_label.configure(text=gameboard.last_player)
        self.number_of_games_label.configure(text=gameboard.num_of_losses + gameboard.num_of_ties + gameboard.num_of_wins)
        self.wins_label.configure(text=gameboard.num_of_wins)
        self.losses_label.configure(text=gameboard.num_of_losses)
        self.ties_label.configure(text=gameboard.num_of_ties)

        self.result_label.configure(text=gameboard.result)

