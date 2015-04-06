#coding:utf-8

"""BATTLESHIP"""

import copy
import random
import os
import time
import pygame

pygame.mixer.init()

###################### SINGLE PLAYER CLASS ######################

class Game_SP(object):
    """ Single Player Modality """

    def __init__(self):
        """Global Variables"""
        self.user_name = []

    def play_again(self):
        """ Asks User to play again """
        self.user_name = []

        ask = raw_input("Do you want to return to the menu? Y/N: ")
        ask = ask.lower()
        if ask == "y":
            GO = Menu()
            GO.start()
        elif ask == "n":
            quit()
        else:
            print "Only enter Y or N"

    def ask_user_name(self):
        """ Asks the user for a name """
        user_name = raw_input("Enter your name: ")
        return self.user_name.append(user_name)

    def print_board(self, single_player, board):
        """ Prints board for single player mode """
        self.clear()

        #find out if you are printing the computer or user board
        player = "Computer"
        if single_player == "u":
            player = self.user_name[0]

        print player + "'s board look like this: \n"

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
                    if board[i][j] == "*" or board[i][j] == "$":
                        print board[i][j],
                    else:
                        print " ",

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
                    print "Can't place a ship there.\nPlease take a look at the board and try again."
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

        single_player_mode()
        self.ask_user_name()
        time.sleep(0.1)

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

        place_ships()

        #ship placement
        user_board = self.user_place_ships(user_board, ships)
        comp_board = self.computer_place_ships(comp_board, ships)

        #game main loop
        while 1:

            #user move
            user_turn()
            self.print_board("c", comp_board)
            comp_board = self.user_move(comp_board)
            time.sleep(1)

            #check if user won
            if comp_board == "WIN":
                user_won()
                self.play_again()

            #display current computer board
            self.print_board("c", comp_board)
            raw_input("To end user turn hit ENTER")

            #computer move
            computer_turn()
            user_board = self.computer_move(user_board)
            time.sleep(1)

            #check if computer move
            if user_board == "WIN":
                computer_won()
                self.play_again()

            #display user board
            self.print_board("u", user_board)
            raw_input("To end computer turn hit ENTER")

###################### MULTI PLAYER INHERITS FROM SINGLE PLAYER ######################

class Game_MP(Game_SP):
    """ Multi Player Modality """

    def __init__(self):
        """Global Variables"""
        self.players_name = []

    def play_again(self):
        """ Asks User to play again """

        ask = raw_input("Do you want to return to the menu? Y/N: ")
        ask = ask.lower()
        if ask == "y":
            board = []
            GO = Menu()
            GO.start()
        elif ask == "n":
            quit()
        else:
            print "Only enter Y or N"

    def ask_user_name(self):
        """ Asks the users for a name """
        p1_name = raw_input("Player One, Enter your name: ")
        p2_name = raw_input("Player Two, Enter your name: ")
        return self.players_name.append(p1_name), self.players_name.append(p2_name)

    def print_board(self, single_player, board):
        """ Prints board """
        self.clear()
        #find out if you are printing the p1 or p2 board
        player = self.players_name[1]
        if single_player == "p1":
            player = self.players_name[0]

        print player + "'s board look like this: \n"

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
                elif single_player == "p1":
                    print board[i][j],
                elif single_player == "p2":
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

    def print_board2(self, single_player, board):
        """ Prints board showing only hits """
        self.clear()
        #find out if you are printing the p1 or p2 board
        player = self.players_name[1]
        if single_player == "p1":
            player = self.players_name[0]

        print player + "'s board look like this: \n"

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
                elif single_player == "p1":
                    if board[i][j] == "*" or board[i][j] == "$":
                        print board[i][j],
                    else:
                        print " ",
                elif single_player == "p2":
                    if board[i][j] == "*" or board[i][j] == "$":
                        print board[i][j],
                    else:
                        print " ",

                if j != 9:
                    print " | ",
            print

            #print a horizontal line
            if i != 9:
                print "   ----------------------------------------------------------"
            else:
                print

    def p1_place_ships(self, board, ships):
        """Get coordinates from user and validates the position"""
        for ship in ships.keys():

            valid = False
            while not valid:

                self.print_board("p1", board)
                print "Placing a/an " + ship
                row, col = self.get_coor()
                ori = self.v_or_h()
                valid = self.validate(board, ships[ship], row, col, ori)
                if not valid:
                    print "Can't place a ship there.\nPlease take a look at the board and try again."
                    raw_input("Hit ENTER to continue")

            #place the ship
            board = self.place_ship(board, ships[ship], ship[0], ori, row, col)
            self.print_board("p1", board)

        raw_input("Done placing user ships. Hit ENTER to continue")
        return board

    def p2_place_ships(self, board, ships):
        """Generates random coordinates and validates the position"""
        for ship in ships.keys():

            valid = False
            while not valid:

                self.print_board("p2", board)
                print "Placing a/an " + ship
                row, col = self.get_coor()
                ori = self.v_or_h()
                valid = self.validate(board, ships[ship], row, col, ori)
                if not valid:
                    print "Can't place a ship there.\nPlease take a look at the board and try again."
                    raw_input("Hit ENTER to continue")

            #place the ship
            board = self.place_ship(board, ships[ship], ship[0], ori, row, col)
            self.print_board("p2", board)

        raw_input("Done placing user ships. Hit ENTER to continue")
        return board

    def p1_move(self, board):
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

    def p2_move(self, board):
        """Generates user coordinates from the user and try to make move"""
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

    def main(self):
        """Initiates my game"""

        multi_player_mode()
        self.ask_user_name()
        time.sleep(1)

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

        #setup p1 and p2 boards
        p1_board = copy.deepcopy(board)
        p2_board = copy.deepcopy(board)

        #add ships as last element in the array
        p1_board.append(copy.deepcopy(ships))
        p2_board.append(copy.deepcopy(ships))

        #ship placement
        p1_place_ships()
        p1_board = self.p1_place_ships(p1_board, ships)
        p2_place_ships()
        p2_board = self.p2_place_ships(p2_board, ships)

        #game main loop
        while 1:

            #p1 move
            p1_turn()
            self.print_board2("p2", p2_board)
            p2_board = self.p1_move(p2_board)
            time.sleep(1)

            #check if user won
            if p2_board == "WIN":
                print p1_won()
                self.play_again()

            #display current p2 board
            self.print_board2("p2", p2_board)
            raw_input("To see your board, hit ENTER")

            #display current p1 board
            self.print_board("p1", p1_board)
            raw_input("To end player one turn hit ENTER")

            #p2 move
            p2_turn()
            self.print_board2("p1", p1_board)
            p1_board = self.p2_move(p1_board)
            time.sleep(1)

            #check if p2 won
            if p1_board == "WIN":
                print p2_won()
                self.play_again()

            #display p1 board
            self.print_board2("p1", p1_board)
            raw_input("To see your board, hit ENTER")

            #display current p2 board
            self.print_board("p2", p2_board)
            raw_input("To end player two turn hit ENTER")

###################### SALVO INHERITES FROM MULTI PLAYER ######################

class Salvo_Mode(Game_MP):
    """ Salvo Modality """

    def main(self):
        """Initiates my game"""

        salvo_mode()
        self.ask_user_name()
        time.sleep(1)

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

        #setup p1 and p2 boards
        p1_board = copy.deepcopy(board)
        p2_board = copy.deepcopy(board)

        #add ships as last element in the array
        p1_board.append(copy.deepcopy(ships))
        p2_board.append(copy.deepcopy(ships))

        #ship placement
        p1_place_ships()
        p1_board = self.p1_place_ships(p1_board, ships)

        p2_place_ships()
        p2_board = self.p2_place_ships(p2_board, ships)

        #game main loop
        while 1:

            #p1 move
            p1_turn()
            turn = 0
            while turn <= 4:
                self.print_board2("p2", p2_board)
                p2_board = self.p1_move(p2_board)
                time.sleep(1)
                turn += 1

            #check if user won
                if p2_board == "WIN":
                    turn = 5
                    print p1_won()
                    self.play_again()

            #display current p2 board
            self.print_board2("p2", p2_board)
            raw_input("To see your board, hit ENTER")

            #display current p1 board
            self.print_board("p1", p1_board)
            raw_input("To end player one turn hit ENTER")

            #p2 move
            p2_turn()
            turn2 = 0
            while turn2 <= 4:
                self.print_board2("p1", p1_board)
                p1_board = self.p2_move(p1_board)
                time.sleep(1)
                turn2 += 1

                #check if p2 won
                if p1_board == "WIN":
                    turn = 5
                    print p2_won()
                    self.play_again()

            #display p1 board
            self.print_board2("p1", p1_board)
            raw_input("To see your board, hit ENTER")

            #display current p2 board
            self.print_board("p2", p2_board)
            raw_input("To end player two turn hit ENTER")

###################### GLOBAL FUNCTIONS WITH IMAGES ######################

def clear():
    """Clears the screen at the terminal. Works on windows and ubuntu."""
    if os.name == "posix":
        os.system("reset")
    elif os.name == "nt":
        os.system("cls")

def title():
    """ The game's title """
    clear()
    print chr(27) + "[1;36m" + """
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
x                                                           x
x       __/\__            __/\__                __/\__      x
x     ~~\____/~~        ~~\____/~~            ~~\____/~~    x
x                                                           x
x               ╔╗ ╔═╗╔╦╗╔╦╗╦  ╔═╗╔═╗╦ ╦╦╔═╗                x
x               ╠╩╗╠═╣ ║  ║ ║  ║╣ ╚═╗╠═╣║╠═╝                x
x               ╚═╝╩ ╩ ╩  ╩ ╩═╝╚═╝╚═╝╩ ╩╩╩                  x
x                                                           x
x       __/\__            __/\__                __/\__      x
x     ~~\____/~~        ~~\____/~~            ~~\____/~~    x
x                                                           x
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
""" + chr(27) + "[0m"
    time.sleep(0.1)
    raw_input("Press ENTER to continue")

def menu():
    """ Game's menu """
    clear()
    print chr(27) + "[1;94m" + """
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
x                                                                 x
x                         ╔╦╗╔═╗╔╗╔╦ ╦                            x
x       __/\__            ║║║║╣ ║║║║ ║            __/\__          x
x     ~~\____/~~          ╩ ╩╚═╝╝╚╝╚═╝          ~~\____/~~        x 
x                                                                 x
x                                                                 x
x         ┬┌┐┌┌─┐┌┬┐┬─┐┬ ┬┌─┐┌┬┐┬┌─┐┌┐┌┌─┐                        x                 
x  1 ───  ││││└─┐ │ ├┬┘│ ││   │ ││ ││││└─┐                        x                 
x         ┴┘└┘└─┘ ┴ ┴└─└─┘└─┘ ┴ ┴└─┘┘└┘└─┘                        x                 
x         ┌─┐┬┌┐┌┌─┐┬  ┌─┐  ┌─┐┬  ┌─┐┬ ┬┌─┐┬─┐  ┌┬┐┌─┐┌┬┐┌─┐      x 
x  2 ───  └─┐│││││ ┬│  ├┤   ├─┘│  ├─┤└┬┘├┤ ├┬┘  ││││ │ ││├┤       x 
x         └─┘┴┘└┘└─┘┴─┘└─┘  ┴  ┴─┘┴ ┴ ┴ └─┘┴└─  ┴ ┴└─┘─┴┘└─┘      x 
x         ┌┬┐┬ ┬┬ ┌┬┐┬  ┌─┐┬  ┌─┐┬ ┬┌─┐┬─┐  ┌┬┐┌─┐┌┬┐┌─┐          x  
x  3 ───  ││││ ││  │ │  ├─┘│  ├─┤└┬┘├┤ ├┬┘  ││││ │ ││├┤           x    
x         ┴ ┴└─┘┴─┘┴ ┴  ┴  ┴─┘┴ ┴ ┴ └─┘┴└─  ┴ ┴└─┘─┴┘└─┘          x    
x         ┌─┐┌─┐┬ ┬  ┬┌─┐  ┌┬┐┌─┐┌┬┐┌─┐                           x                     
x  4 ───  └─┐├─┤│ └┐┌┘│ │  ││││ │ ││├┤                            x                     
x         └─┘┴ ┴┴─┘└┘ └─┘  ┴ ┴└─┘─┴┘└─┘                           x                     
x         ┌─┐─┐ ┬┬┌┬┐                                             x                                      
x  5 ───  ├┤ ┌┴┬┘│ │                                              x                                      
x         └─┘┴ └─┴ ┴                                              x
x                                                                 x
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
""" + chr(27) + "[0m"

def instructions():
    """Game's instructions"""
    clear()
    print chr(27) + "[1;92m" + """

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx      
x                 ╦╔╗╔╔═╗╔╦╗╦═╗╦ ╦╔═╗╔╦╗╦╔═╗╔╗╔╔═╗                          x
x                 ║║║║╚═╗ ║ ╠╦╝║ ║║   ║ ║║ ║║║║╚═╗                          x
x                 ╩╝╚╝╚═╝ ╩ ╩╚═╚═╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝                          x
x                                                                           x
x      The object of Battleship is to try and sink all of the other         x
x      player's ships before they sink all of your ships.                   x
x                                                                           x
x      ┌─┐┬┌┐┌┌─┐┬  ┌─┐  ┌─┐┬  ┌─┐┬ ┬┌─┐┬─┐  ┌┬┐┌─┐┌┬┐┌─┐                   x
x      └─┐│││││ ┬│  ├┤   ├─┘│  ├─┤└┬┘├┤ ├┬┘  ││││ │ ││├┤                    x
x      └─┘┴┘└┘└─┘┴─┘└─┘  ┴  ┴─┘┴ ┴ ┴ └─┘┴└─  ┴ ┴└─┘─┴┘└─┘                   x
x                                                                           x
x      You will play against a computer and place the ships on the board.   x
x      The placement can either be vertical or horizontal.                  x
x                                                                           x
x      The ships are:                                                       x
x                                                                           x
x      Aircraft Carrier - 5 hits                                            x
x      Battleship - 4 hits                                                  x
x      Submarine - 3 hits                                                   x
x      Destroyer - 3 hits                                                   x
x      Patrol Boat - 2 hits                                                 x
x                                                                           x
x      You try and hit them by calling out the coordinates of one           x
x      of the squares on the board.                                         x
x                                                                           x
x      ┌┬┐┬ ┬┬ ┌┬┐┬  ┌─┐┬  ┌─┐┬ ┬┌─┐┬─┐  ┌┬┐┌─┐┌┬┐┌─┐                       x
x      ││││ ││  │ │  ├─┘│  ├─┤└┬┘├┤ ├┬┘  ││││ │ ││├┤                        x
x      ┴ ┴└─┘┴─┘┴ ┴  ┴  ┴─┘┴ ┴ ┴ └─┘┴└─  ┴ ┴└─┘─┴┘└─┘                       x
x                                                                           x
x      The rules are the same as the Single Player Mode, except both        x
x      players have turns and place each other ships, that cannot be        x
x      seen by the other.                                                   x
x                                                                           x
x      ┌─┐┌─┐┬ ┬  ┬┌─┐  ┌┬┐┌─┐┌┬┐┌─┐                                        x
x      └─┐├─┤│ └┐┌┘│ │  ││││ │ ││├┤                                         x
x      └─┘┴ ┴┴─┘└┘ └─┘  ┴ ┴└─┘─┴┘└─┘                                        x
x                                                                           x
x      Battleship rules apply but with a variation: Each player calls       x                                          x
x      out five shots at a time.                                            x
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
""" + chr(27) + "[0m"

def single_player_mode():
    """Title for SP mode"""
    clear()
    print chr(27) + "[1;93m" + """
                ╔═╗╦╔╗╔╔═╗╦  ╔═╗  ╔═╗╦  ╔═╗╦ ╦╔═╗╦═╗  ╔╦╗╔═╗╔╦╗╔═╗
xxxxxxxxxxxxx   ╚═╗║║║║║ ╦║  ║╣   ╠═╝║  ╠═╣╚╦╝║╣ ╠╦╝  ║║║║ ║ ║║║╣    xxxxxxxxxxxxx
                ╚═╝╩╝╚╝╚═╝╩═╝╚═╝  ╩  ╩═╝╩ ╩ ╩ ╚═╝╩╚═  ╩ ╩╚═╝═╩╝╚═╝
""" + chr(27) + "[0m"

def place_ships():
    """Place ships title"""
    clear()
    print chr(27) + "[1;95m" + """
                ╔═╗╦  ╔═╗╔═╗╔═╗  ╔═╗╦ ╦╦╔═╗╔═╗
xxxxxxxxxxxxx   ╠═╝║  ╠═╣║  ║╣   ╚═╗╠═╣║╠═╝╚═╗   xxxxxxxxxxxxx
                ╩  ╩═╝╩ ╩╚═╝╚═╝  ╚═╝╩ ╩╩╩  ╚═╝
    """ + chr(27) + "[0m"
    raw_input("Press Enter to continue")

def user_turn():
    """User turn title"""
    clear()
    print chr(27) + "[1;36m" + """
                ╦ ╦╔═╗╔═╗╦═╗  ╔╦╗╦ ╦╦═╗╔╗╔
xxxxxxxxxxxxx   ║ ║╚═╗║╣ ╠╦╝   ║ ║ ║╠╦╝║║║   xxxxxxxxxxxxx
                ╚═╝╚═╝╚═╝╩╚═   ╩ ╚═╝╩╚═╝╚╝
    """ + chr(27) + "[0m"
    raw_input("Press Enter to continue")

def computer_turn():
    """Computer turn title"""
    clear()
    print chr(27) + "[1;91m" + """
                ╔═╗╔═╗╔╦╗╔═╗╦ ╦╔╦╗╔═╗╦═╗  ╔╦╗╦ ╦╦═╗╔╗╔
xxxxxxxxxxxxx   ║  ║ ║║║║╠═╝║ ║ ║ ║╣ ╠╦╝   ║ ║ ║╠╦╝║║║   xxxxxxxxxxxxx
                ╚═╝╚═╝╩ ╩╩  ╚═╝ ╩ ╚═╝╩╚═   ╩ ╚═╝╩╚═╝╚╝
    """ + chr(27) + "[0m"
    raw_input("Press Enter to continue")

def user_won():
    """User won title"""
    clear()
    print chr(27) + "[1;94m" + """
              |    |    |
             )_)  )_)  )_)
            )___))___))___)
           )____)____)_____)
         _____|____|____|____
         \                   /
        ^^^^^^^^^^^^^^^^^^^^^^^
      ^^      ^^^^     ^^^    ^^
         ^^^^      ^^^    ^^^ 
         ╦ ╦╔═╗╦ ╦  ╦ ╦╔═╗╔╗╔
         ╚╦╝║ ║║ ║  ║║║║ ║║║║
          ╩ ╚═╝╚═╝  ╚╩╝╚═╝╝╚╝
""" + chr(27) + "[0m"

def computer_won():
    """Computer won title"""
    clear()
    print chr(27) + "[1;91m" + """

   __/\__       ╔═╗╔═╗╔╦╗╔═╗╦ ╦╔╦╗╔═╗╦═╗  ╦ ╦╔═╗╔╗╔
 ~~\____/~~     ║  ║ ║║║║╠═╝║ ║ ║ ║╣ ╠╦╝  ║║║║ ║║║║         __/\__ 
                ╚═╝╚═╝╩ ╩╩  ╚═╝ ╩ ╚═╝╩╚═  ╚╩╝╚═╝╝╚╝       ~~\____/~~ 

""" + chr(27) + "[0m"

def multi_player_mode():
    """MP mode title"""
    clear()
    print chr(27) + "[1;93m" + """
                ╔╦╗╦ ╦╦ ╔╦╗╦  ╔═╗╦  ╔═╗╦ ╦╔═╗╦═╗  ╔╦╗╔═╗╔╦╗╔═╗               
xxxxxxxxxxxxx   ║║║║ ║║  ║ ║  ╠═╝║  ╠═╣╚╦╝║╣ ╠╦╝  ║║║║ ║ ║║║╣    xxxxxxxxxxxxx   
                ╩ ╩╚═╝╩═╝╩ ╩  ╩  ╩═╝╩ ╩ ╩ ╚═╝╩╚═  ╩ ╩╚═╝═╩╝╚═╝               
    """ + chr(27) + "[0m"

def p1_place_ships():
    """P1 place ships title"""
    clear()
    print chr(27) + "[1;95m" +  """

               ╔═╗╦  ╔═╗╦ ╦╔═╗╦═╗  ╔═╗╔╗╔╔═╗
               ╠═╝║  ╠═╣╚╦╝║╣ ╠╦╝  ║ ║║║║║╣ 
               ╩  ╩═╝╩ ╩ ╩ ╚═╝╩╚═  ╚═╝╝╚╝╚═╝
xxxxxxxxxxxxx  ╔═╗╦  ╔═╗╔═╗╔═╗  ╔═╗╦ ╦╦╔═╗╔═╗  xxxxxxxxxxxxx
               ╠═╝║  ╠═╣║  ║╣   ╚═╗╠═╣║╠═╝╚═╗ 
               ╩  ╩═╝╩ ╩╚═╝╚═╝  ╚═╝╩ ╩╩╩  ╚═╝
    """ + chr(27) + "[0m"
    raw_input("Press Enter to continue")

def p2_place_ships():
    """P2 place ships title"""
    clear()
    print chr(27) + "[1;95m" +  """

               ╔═╗╦  ╔═╗╦ ╦╔═╗╦═╗  ╔╦╗╦ ╦╔═╗
               ╠═╝║  ╠═╣╚╦╝║╣ ╠╦╝   ║ ║║║║ ║   
xxxxxxxxxxxxx  ╩  ╩═╝╩ ╩ ╩ ╚═╝╩╚═   ╩ ╚╩╝╚═╝   xxxxxxxxxxxxx
               ╔═╗╦  ╔═╗╔═╗╔═╗  ╔═╗╦ ╦╦╔═╗╔═╗
               ╠═╝║  ╠═╣║  ║╣   ╚═╗╠═╣║╠═╝╚═╗ 
               ╩  ╩═╝╩ ╩╚═╝╚═╝  ╚═╝╩ ╩╩╩  ╚═╝
    """ + chr(27) + "[0m"
    raw_input("Press Enter to continue")

def p1_turn():
    """P1 turn title"""
    clear()
    print chr(27) + "[1;36m" + """
                ╔═╗╦  ╔═╗╦ ╦╔═╗╦═╗  ╔═╗╔╗╔╔═╗  ╔╦╗╦ ╦╦═╗╔╗╔
xxxxxxxxxxxxx   ╠═╝║  ╠═╣╚╦╝║╣ ╠╦╝  ║ ║║║║║╣    ║ ║ ║╠╦╝║║║   xxxxxxxxxxxxx 
                ╩  ╩═╝╩ ╩ ╩ ╚═╝╩╚═  ╚═╝╝╚╝╚═╝   ╩ ╚═╝╩╚═╝╚╝
    """ + chr(27) + "[0m"
    raw_input("Press Enter to continue")

def p2_turn():
    """P2 turn title"""
    clear()
    print """
                ╔═╗╦  ╔═╗╦ ╦╔═╗╦═╗  ╔╦╗╦ ╦╔═╗  ╔╦╗╦ ╦╦═╗╔╗╔
xxxxxxxxxxxxx   ╠═╝║  ╠═╣╚╦╝║╣ ╠╦╝   ║ ║║║║ ║   ║ ║ ║╠╦╝║║║   xxxxxxxxxxxxx 
                ╩  ╩═╝╩ ╩ ╩ ╚═╝╩╚═   ╩ ╚╩╝╚═╝   ╩ ╚═╝╩╚═╝╚╝
    """ + chr(27) + "[0m"
    raw_input("Press Enter to continue")

def p1_won():
    """P1 winning message"""
    clear()
    print chr(27) + "[1;36m" + """
                                  ____________
                              _  |____________|  _
                       _=====| | |            | | |==== _
                 =====| |.---------------------------. | |====
   <--------------------'   .  .  .  .  .  .  .  .   '--------------/
     \                                                             /
      \___________________________________________________________/

               ╔═╗╦  ╔═╗╦ ╦╔═╗╦═╗  ╔═╗╔╗╔╔═╗  ╦ ╦╔═╗╔╗╔
               ╠═╝║  ╠═╣╚╦╝║╣ ╠╦╝  ║ ║║║║║╣   ║║║║ ║║║║
               ╩  ╩═╝╩ ╩ ╩ ╚═╝╩╚═  ╚═╝╝╚╝╚═╝  ╚╩╝╚═╝╝╚╝
""" + chr(27) + "[0m"

def p2_won():
    """P2 winning message"""
    clear()
    print chr(27) + "[1;94m" + """
                                  ____________
                              _  |____________|  _
                       _=====| | |            | | |==== _
                 =====| |.---------------------------. | |====
   <--------------------'   .  .  .  .  .  .  .  .   '--------------/
     \                                                             /
      \___________________________________________________________/


               ╔═╗╦  ╔═╗╦ ╦╔═╗╦═╗  ╔╦╗╦ ╦╔═╗  ╦ ╦╔═╗╔╗╔
               ╠═╝║  ╠═╣╚╦╝║╣ ╠╦╝   ║ ║║║║ ║  ║║║║ ║║║║
               ╩  ╩═╝╩ ╩ ╩ ╚═╝╩╚═   ╩ ╚╩╝╚═╝  ╚╩╝╚═╝╝╚╝
""" + chr(27) + "[0m"

def salvo_mode():
    """Salvo Mode title"""
    clear()
    print chr(27) + "[1;93m" + """
                ╔═╗╔═╗╦ ╦  ╦╔═╗  ╔╦╗╔═╗╔╦╗╔═╗
xxxxxxxxxxxxx   ╚═╗╠═╣║ ╚╗╔╝║ ║  ║║║║ ║ ║║║╣    xxxxxxxxxxxxx
                ╚═╝╩ ╩╩═╝╚╝ ╚═╝  ╩ ╩╚═╝═╩╝╚═╝
    """ + chr(27) + "[0m"

###################### MENU CLASS ######################

class Menu(object):
    """ Menu of Battleship that initiates """

    def start(self):
        """ Starts the Game Battleship """

        pygame.mixer.music.load("battleship.mp3")
        pygame.mixer.music.play(-1)
        title()
        menu()

        while True:
            answer = raw_input("Enter Option: ")
            if answer == "1":
                instructions()
                raw_input("Enter to return")
                self.start()
            elif answer == "2":
                SP = Game_SP()
                SP.main()
            elif answer == "3":
                MP = Game_MP()
                MP.main()
            elif answer == "4":
                SM = Salvo_Mode()
                SM.main()
            elif answer == "5":
                quit()
            else:
                print "Only enter valid options"
                time.sleep(0.1)

###################### CALLING THE GAME ######################

if __name__ == "__main__":
    GO = Menu()
    GO.start()