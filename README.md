# Tic-Tac-Toe
A Tic Tac Toe system which enables two players to play together

The purpose of this project  is to get you used to networking by using sockets.
(In our case, both the client and the server will be running on our local machine)
The main libraries to be used are the sockets library (socket) and tkinter (or PyGames).

**Program Details:**
Create 3 new modules with the following details:

- *class* BoardClass (gameboard.py)
  - The board game will consist of the following public interface. (Note this module can be imported and used by both player1 and player2 modules
  - The class should have a minimum of the following (you can add more if you need to):
    - Attributes:
      - User name of player 1
      - User name of player 2
      - User name of the last player to have a turn
      - Number of wins
      - Number of ties
      - Number of losses
    - Functions:
      - updateGamesPlayed()
        - Keeps track how many games have started
      - resetGameBoard()
        - Clear all the moves from game board
      - updateGameBoard()
        - Updates the game board with the player's move
      - isWinner()
        - Checks if the latest move resulted in a win
        - Updates the wins and losses count 
      - boardIsFull()
        - Checks if the board is full (I.e. no more moves to make - tie)
        - Updates the ties count
      - computeStats()
        - Computes and returns the following stats:
          - The username of both players
          - The number of games
          - The number of wins
          - The number of losses
          - The number of ties

**Player 1 Module(Module Name: player1.py) - The joining player**

1. 1. As the client, Player 1 will ask the user for the host information of Player 2 to join the game:

      1. Prompt the user for the host name/IP address of Player 2 they want to play with
      2. Prompt the user for the port to use in order to play with Player 2

   2. Using that information they will attempt to connect to Player 2

      1. Upon successful connection they will send Player 2 their username (just alphanumeric username with no special characters)
      2. If the connection cannot be made then the user will be asked if they want to try again:
         1. If the user enters 'y' then you will request the host information from the user again
         2. If the user enters 'n' then you will end the program

   3.  Once Player 1 receives Player 2's username or if the users decides to play again

      1. Player 1 will ask the user for their move using the current player display area. 
      2.  Send the move to player 2.

1. 1. 1. 1. Player 1 will always be x/X
         2. Player 1 will always send the first move to Player 2
            1. Each move will correspond to the area on the board they user clicks on. 

1. 1. 1. 1.  Once player 1 sends their move they will wait for Player 2's move.
         2.  Repeat steps 3.1 - 3.2.3 until the game is over (A game is over when a winner is found or the board is full)
   2. Once a game has finished (win, lose, or tie) the user will indicate if they want to play again using the user interface.
      1. If the user enters 'y' or 'Y' (or clicks a button) then player 2 will send "Play Again" to player 2
      2. If the user enters 'n' or 'N' (or clicks a button) then player 2 will send "Fun Times" to player 2 and end the program
         1. Once the user is done, the module will print all the statistics.

**Player 2 Module (Module Name: player1.py) - The host of the game, or the server**

1. 1.  The user will be asked to provide the host information so that it can establish a socket connection as the server

   2.  Player 2 will accept incoming requests to start a new game

   3.  When a connection request is received and accepted, Player 2 will wait for Player 1 to send their username

   4.  Once Player 2 receives Player 1's user name, then Player 2 will ask the user to enter their username and send it to Player 1 and wait for Player 1 to send their move.

      1. Once Player 2 receives Player 1's move they will ask the user for their move and send it to Player 1 using the current player display area.

      1.  Each move will correspond to the area on the board they user clicks on. 

      2.  Once player 2 sends their move they will wait for Player 1's move.

      3.  Repeat steps 4.1 - 4.2 until the game is over (A game is over when a winner is found or the board is full)

   5.  Once a game has finished (win or tie) player 2 will wait for player 1 to indicate if they want to play again using the user interface.

      1.  If Player 1 wants to play again then Player 2 will wait for player 1's first move.
      2.  If Player 1 does not wants to play again then Player 2 will print the statistics

**User Interface:**

1. 1. You will create a user interface using either the ==Tkinter== library or the ==PyGames== library. **At ==no point== should the user be required to interact with the ==python shell== with the input() or print() functions.** The user interface should include the following components:

1. 1. 1. A text entry for the host information
      2. A text entry for the username
      3. A Tic Tac Toe board that allows the user to select their move by clicking on that
      4. A ==dialog== that asks the user if they want to play again (only on player 1)
      5. A display area where you display the BoardClass's computed statistics when they are done and any other printed information specified in the lab.
      6. An area indicating who's turn it is currently
      7. An area where the final results will be displayed
