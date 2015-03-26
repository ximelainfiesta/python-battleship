#-*- coding: utf-8 -*-
""" BATTLESHIP """
import random
import sys

class Game(object):
    """Creates a class with a player in battleship"""
    def __init__(self):
        """Single Player Battleship"""
        self.board = [] #empty list that will contain the board
        self.ships = {"Carrier":5, "Battleship":4, "Cruiser":3, "Submarine":3, "Destroyer":2}

    def fill_board(self):
        """Fills board with numbers 0-9"""
        for i in range(0, 10): #for each element
            self.board.append([" "] * 10) #multiply it 10 times to create board

    def print_board(self):
        """Prints board"""
        print """
                      Let's play Battleship!
        Instructions: Guess the Row and the Column of the ship. You have 5 turns
        """
        print "   |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |"
        print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  \n"

        cont = 0
        for i in self.board:
            print str(cont) + "  |  " + "  |  ".join(i) + "  |"
            print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
            cont += 1

    def position(self):
        """Generates a random position to determine H or V direction"""
        return random.randit(1, 2)

    def row_random(self):
        """Generates a random row number"""
        return random.randint(0, len(self.board)-1)

    def column_random(self):
        """Generates a random column number"""
        return random.randint(0, len(self.board[0])-1)

    def ship_variables(self):
        """ Calls my functions above in a variable """
        self.ship_row = self.row_random() #this should be defined in init
        self.ship_col = self.column_random()
        print self.ship_row
        print self.ship_col

    def put_ship(self):


    def user_entry(self):
        turn = 0
        while turn < 5:
            turn = turn + 1
            print "Turn: ", turn
            guess_row = raw_input("Guess Row: ")
            guess_column = raw_input("Guess Column:")
            try:
                guess_row = int(guess_row)
                guess_column = int(guess_column)

                if guess_row == self.ship_row and guess_column == self.ship_col:
                    print "Congratulations, you sank my ship!"
                    self.play_again()
                else:
                    if (guess_row < 0 or guess_row >= 10)or(guess_column < 0 or guess_column >= 10):
                        print "Wow, this is not even in the ocean."
                    elif self.board[guess_row][guess_column] == "X":
                        print "You already said that."
                    else:
                        print "You did not hit my ship!"
                        self.board[guess_row][guess_column] = "X"
                    if turn == 5:
                        print "Game Over"
                        self.play_again()

                self.print_board()
            except (ValueError, SyntaxError):
                print "Enter only numbers"

    def play_again(self):
        """ Option to repeat the game """
        while True:
            try:
                user = raw_input("Do you want to play again? Y/N: ")
                user = user.lower()
                if user == "y":
                    self.board = []
                    self.call()
                elif user == "n":
                    print "Good-Bye!!"
                    sys.exit()
                else:
                    print "Only enter Y o N"
            except TypeError:
                print "Invalid Option"

    def clear():
        """Clears the screen at the terminal. Works on windows and ubuntu."""
        if os.name == "posix":
            os.system("reset")
        elif os.name == "nt":
            os.system("cls")

    def call(self):
        """ Calls the functions in order """
        self.fill_board()
        self.print_board()
        self.row_random()
        self.column_random()
        self.ship_variables()
        self.user_entry()



""" Calls Single Player """
GO = Game()
GO.call()
GO.play_again()
