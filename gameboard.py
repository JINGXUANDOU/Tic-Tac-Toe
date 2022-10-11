import tkinter as tk
from tkinter import messagebox


class BoardClass:
    '''A class to store and handle information about gameboard.

    Attributes:
        player1_name(str): The username of player1.
        player2_name(str): The username of player2.
        myself_name(str): The username of current user.
        last_player(str): The username of the last player in a game.
        last_x(int): The x-coordinate of the last slot.
        last_y(int): The y-coordinate of the last slot.
        num_of_wins(int): The number of game wins.
        num_of_ties(int): The number of game ties.
        num_of losses(int): The number of game losses.
    '''
    def __init__(self, player1_name: str, player2_name: str, myself_name: str) -> None:
        '''Make a gameboard.

        Args:
            player1_name: The username of player1.
            player2_name: The username of player2.
            myself_name: The username of current user.

        '''
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.myself_name = myself_name
        self.last_player = ''
        self.last_x = 0
        self.last_y = 0
        self.num_of_wins = 0
        self.num_of_ties = 0
        self.num_of_losses = 0
        self.result = ''

        self.gameboard = [['', '', ''], ['', '', ''], ['', '', '']] # set the gameboard as a list of lists, which contains three empty spaces


    def updateGamesPlayed(self) -> int:
        '''Keep track how many games have started.

        Returns:
            An integer represents number of total games that have started.
        '''
        return self.num_of_wins + self.num_of_ties + self.num_of_losses


    def resetGameBoard(self) -> None:
        '''Clear all the moves from game board.
        '''
        self.gameboard = [['', '', ''], ['', '', ''], ['', '', '']] # reset/clear the list gameboard


    def isEmptySlot(self, slot_x: int, slot_y: int) -> bool:
        '''Justify whether the slot is empty.

        Args:
            slot_x: The x-coordinate of the slot
            slot_y: The y-coordinate of the slot

        Returns:
            True if it's empty, False otherwise
        '''
        if 0 < slot_x < 4 and 0 < slot_y < 4:    # Justify whether the slot is valid
            return self.gameboard[slot_x-1][slot_y-1] == ''
        else:
            return False


    def updateGameBoard(self, player_name: str, slot_x: int, slot_y: int) -> None:
        '''Updates the game board with the player's move

        Args:
            player_name: The username of the player
            slot_x: The x-coordinate of the slot
            slot_y: The y-coordinate of the slot

        Raises:
            ValueError: if the slot is invalid
        '''

        if not self.isEmptySlot(slot_x, slot_y):    # Justify whether the slot is empty
            raise ValueError

        self.last_x = slot_x - 1
        self.last_y = slot_y - 1
        self.last_player = player_name

        if player_name == self.player1_name:     # Justify the user
            self.gameboard[self.last_x][self.last_y] = 'x'
        else:
            self.gameboard[self.last_x][self.last_y] = 'o'


    def isWinner(self) -> bool:
        '''Checks if the latest move resulted in a win and updates the wins and losses count

        Returns:
            True when there is a winner, False otherwise
        ''' 
        if self.gameboard[self.last_x][self.last_y] == '':
            return False

        winner = ''

        if self.gameboard[self.last_x][0] == self.gameboard[self.last_x][1] == self.gameboard[self.last_x][2]:   # Justify whether there is one row of same chess
            winner = self.last_player
        elif self.gameboard[0][self.last_y] == self.gameboard[1][self.last_y] == self.gameboard[2][self.last_y]:    # Justify whether there is one column of same chess
            winner = self.last_player
        elif self.gameboard[1][1] != '':
            if self.gameboard[0][0] == self.gameboard[1][1] == self.gameboard[2][2]:   # Justify whether there is one diagonal of same chess
                winner = self.last_player
            elif self.gameboard[2][0] == self.gameboard[1][1] == self.gameboard[0][2]:   # Justify whether there is one diagonal of same chess
                winner = self.last_player

        if winner == '':
            return False
        elif winner == self.myself_name:
            self.num_of_wins += 1
            self.result = '%s win!' % self.myself_name
        else:
            self.num_of_losses += 1
            self.result = '%s lose!' % self.myself_name
        return True


    def boardIsFull(self) -> bool:
        '''Checks if the board is full (I.e. no more moves to make - tie) and updates the ties count

        Returns:
            True when the gameboard is full, False otherwise
        '''
        for row in self.gameboard:
            if row[0] == '' or row[1] == '' or row[2] == '':
                return False

        self.num_of_ties += 1
        self.result = 'This game ended in a tie!'
        return True


    def printStats(self) -> None:
        '''Print several stats of the game
        '''
        print('The player1 is {}, player2 is {}.'.format(self.player1_name, self.player2_name))
        print('The user name of the last person to make a move is {}.'.format(self.last_player))
        print('The number of games is {}.'.format(self.updateGamesPlayed()))
        print('The number of wins is {}.'.format(self.num_of_wins))
        print('The number of losses is {}.'.format(self.num_of_losses))
        print('The number of ties is {}.'.format(self.num_of_ties))


    def printBoard(self) -> None:
        '''Print the current gameboard
        '''
        print('{} move to {}, {}.'.format(self.last_player, self.last_x + 1, self.last_y + 1))
        print('            -------------')

        for row in self.gameboard:
            print('            | {:1} | {:1} | {:1} |'.format(row[0], row[1], row[2]))
            print('            -------------')
