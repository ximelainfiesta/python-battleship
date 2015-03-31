"""BATTLESHIP"""

import copy
import random
import os

class Game(object):

    def print_board(self, single_player, board):
        """ Prints board for single player mode """
        self.clear()
        #find out if you are printing the computer or user board
        player = "Computer"
        if single_player == "u":
            player = "User"

        print "The " + player + "'s board look like this: \n"

        #print the horizontal numbers
        print " ",
        for i in range(10):
            print "  " + str(i+1) + "  ",
        print "\n"

        for i in range(10):

            #print the vertical line number
            if i != 9:
                print str(i+1) + "  ",
            else:
                print str(i+1) + " ",

            #print the board values, and cell dividers
            for j in range(10):
                if board[i][j] == -1:
                    print ' ',
                elif single_player == "u":
                    print board[i][j],
                elif single_player == "c":
                    #if board[i][j] == "*" or board[i][j] == "$":
                    print board[i][j],
                    #else:
                        #print " ",

                if j != 9:
                    print " | ",
            print

            #print a horizontal line
            if i != 9:
                print "   ----------------------------------------------------------"
            else:
                print

    def user_place_ships(self, board, ships):
        """Get coordinates from user and validates the position"""
        for ship in ships.keys():

            valid = False
            while not valid:

                self.print_board("u", board)
                print "Placing a/an " + ship
                row, col = self.get_coor()
                ori = self.v_or_h()
                valid = self.validate(board, ships[ship], row, col, ori)
                if not valid:
                    print "Cannot place a ship there.\nPlease take a look at the board and try again."
                    raw_input("Hit ENTER to continue")

            #place the ship
            board = self.place_ship(board, ships[ship], ship[0], ori, row, col)
            self.print_board("u", board)

        raw_input("Done placing user ships. Hit ENTER to continue")
        return board


    def computer_place_ships(self, board, ships):
        """Generates random coordinates and validates the position"""
        for ship in ships.keys():

            valid = False
            while not valid:

                row = random.randint(1, 10)-1
                col = random.randint(1, 10)-1
                pos = random.randint(0, 1)
                if pos == 0:
                    ori = "v"
                else:
                    ori = "h"
                valid = self.validate(board, ships[ship], row, col, ori)

            #place the ship
            print "Computer placing a/an " + ship
            board = self.place_ship(board, ships[ship], ship[0], ori, row, col)

        return board


    def place_ship(self, board, ship, single_player, ori, row, col):
        """Place ship based on orientation"""
        if ori == "v":
            for i in range(ship):
                board[row+i][col] = single_player
        elif ori == "h":
            for i in range(ship):
                board[row][col+i] = single_player

        return board

    def validate(self, board, ship, row, col, ori):
        """Validates if the ship can be placed at given coordinates"""
        if ori == "v" and row+ship > 10:
            return False
        elif ori == "h" and col+ship > 10:
            return False
        else:
            if ori == "v":
                for i in range(ship):
                    if board[row+i][col] != -1:
                        return False
            elif ori == "h":
                for i in range(ship):
                    if board[row][col+i] != -1:
                        return False

        return True

    def v_or_h(self):
        """Gets ship orientation from user"""
        while True:
            user_input = raw_input("vertical or horizontal (v or h)?: ")
            if user_input == "v" or user_input == "h":
                return user_input
            else:
                print "Invalid input. Please only enter v or h"

    def get_coor(self):
        """Gets ship coordinates from user"""
        while True:
            user_input = raw_input("Please enter coordinates (row,col)?: ")
            try:
                #see that user entered 2 values seprated by comma
                coor = user_input.split(",")
                if len(coor) != 2:
                    raise Exception("Invalid entry, too few/many coordinates.")

                #check that 2 values are integers
                coor[0] = int(coor[0])-1
                coor[1] = int(coor[1])-1

                #check that values of integers are between 1 and 10 for both coordinates
                if coor[0] > 9 or coor[0] < 0 or coor[1] > 9 or coor[1] < 0:
                    raise Exception("Invalid entry. Please use values between 1 to 10 only.")

                #if everything is ok, return coordinates
                return coor

            except ValueError:
                print "Invalid entry. Please enter only numeric values for coordinates"
            except Exception as exce:
                print exce

    def make_move(self, board, row, col):
        """Make a move on the board and return the result, hit, miss or try again for repeat hit"""
        if board[row][col] == -1:
            return "miss"
        elif board[row][col] == '*' or board[row][col] == '$':
            return "try again"
        else:
            return "hit"

    def user_move(self, board):
        """Get coordinates from the user and tries to make a move"""
        #if move is a hit, check ship sunk and win condition
        while True:
            row, col = self.get_coor()
            res = self.make_move(board, row, col)
            if res == "hit":
                print "Hit at " + str(row+1) + "," + str(col+1)
                self.check_sink(board, row, col)
                board[row][col] = '$'
                if self.check_win(board):
                    return "WIN"
            elif res == "miss":
                print "Sorry, " + str(row+1) + "," + str(col+1) + " is a miss."
                board[row][col] = "*"
            elif res == "try again":
                print "Sorry, that coordinate was already hit. Please try again"

            if res != "try again":
                return board

    def computer_move(self, board):
        """Generates user coordinates from the user and try to make move"""
        #if move is a hit, check ship sunk and win condition
        while True:
            row = random.randint(1, 10)-1
            col = random.randint(1, 10)-1
            res = self.make_move(board, row, col)
            if res == "hit":
                print "Hit at " + str(row+1) + "," + str(col+1)
                self.check_sink(board, row, col)
                board[row][col] = '$'
                if self.check_win(board):
                    return "WIN"
            elif res == "miss":
                print "Sorry, " + str(row+1) + "," + str(col+1) + " is a miss."
                board[row][col] = "*"

            if res != "try again":

                return board

    def check_sink(self, board, row, col):
        """Figures out what ship was hit"""

        if board[row][col] == "A":
            ship = "Aircraft Carrier"
        elif board[row][col] == "B":
            ship = "Battleship"
        elif board[row][col] == "S":
            ship = "Submarine"
        elif board[row][col] == "D":
            ship = "Destroyer"
        elif board[row][col] == "P":
            ship = "Patrol Boat"

        #mark cell as hit and check if sunk
        board[-1][ship] -= 1
        if board[-1][ship] == 0:
            print ship + " Sunk"


    def check_win(self, board):
        """Checks all cells in second board"""
        #simple for loop to check all cells in 2d board
        #if any cell contains a char that is not a hit or a miss return false
        for i in range(10):
            for j in range(10):
                if board[i][j] != -1 and board[i][j] != '*' and board[i][j] != '$':
                    return False
        return True

    def clear(self):
        """Clears the screen at the terminal. Works on windows and ubuntu."""
        if os.name == "posix":
            os.system("reset")
        elif os.name == "nt":
            os.system("cls")

    def main(self):
        """Initiates my game"""
        #types of ships
        ships = {"Aircraft Carrier":5,
                 "Battleship":4,
                 "Submarine":3,
                 "Destroyer":3,
                 "Patrol Boat":2}

        #setup blank 10x10 board
        board = []
        for i in range(10):
            board_row = []
            for j in range(10):
                board_row.append(-1)
            board.append(board_row)

        #setup user and computer boards
        user_board = copy.deepcopy(board)
        comp_board = copy.deepcopy(board)

        #add ships as last element in the array
        user_board.append(copy.deepcopy(ships))
        comp_board.append(copy.deepcopy(ships))

        #ship placement
        user_board = self.user_place_ships(user_board, ships)
        comp_board = self.computer_place_ships(comp_board, ships)

        #game main loop
        while 1:

            #user move
            self.print_board("c", comp_board)
            comp_board = self.user_move(comp_board)

            #check if user won
            if comp_board == "WIN":
                print "User WON! :)"
                quit()

            #display current computer board
            self.print_board("c", comp_board)
            raw_input("To end user turn hit ENTER")

            #computer move
            user_board = self.computer_move(user_board)

            #check if computer move
            if user_board == "WIN":
                print "Computer WON! :("
                quit()

            #display user board
            self.print_board("u", user_board)
            raw_input("To end computer turn hit ENTER")

GO = Game()
GO.main()
