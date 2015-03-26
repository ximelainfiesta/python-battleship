#-*- coding: utf-8 -*-
import random
import sys

class Game(object):
    """Creates a class with a player in battleship"""
    def __init__(self):
        """Single Player Battleship"""
        self.board = [] #empty list that will contain the board

    def fill_board(self):
        for x in range(0,10): #for each element 
          self.board.append([" "] * 10) #multiply it 10 times to create board

    def print_board(self):
        """function to print board"""
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
        return random.randit(1,2)

    def fila_aleatoria(self):
        return random.randint(0,len(self.board)-1)

    def columna_aleatoria(self):
        return random.randint(0,len(self.board[0])-1)

    def ship_variables(self):
        self.barco_fila = self.fila_aleatoria()
        self.barco_col = self.columna_aleatoria()

        print self.barco_fila
        print self.barco_col

    def user_entry(self):
        turno = 0
        while turno < 5:
            turno = turno + 1
            print "Turno: ", turno
            adivina_fila = raw_input("Adivina fila: ")
            adivina_columna = raw_input("Adivina columna:")
            try:
                adivina_fila = int(adivina_fila)
                adivina_columna = int(adivina_columna)

                if adivina_fila == self.barco_fila and adivina_columna == self.barco_col:
                    print "Felicitaciones! Hundiste mi barco!"
                    self.play_again()
                else:
                    if (adivina_fila < 0 or adivina_fila >= 10) or (adivina_columna < 0 or adivina_columna >= 10):
                        print "Vaya, esto ni siquiera esta en el oceano."
                    elif(self.board[adivina_fila][adivina_columna] == "X"):
                        print "Ya dijiste esa."
                    else:
                      print "No impactaste mi barco!"
                      self.board[adivina_fila][adivina_columna] = "X"
                    if turno == 5:
                        print "Terminó el juego"
                        self.play_again()
                        
                self.print_board()
            except (ValueError, SyntaxError):
                print "Ingrese solo números"

    def play_again(self):
        while True:
            try:
                user = raw_input("Quieres jugar de nuevo? Y/N: ")
                user = user.lower()
                if user == "y":
                    self.board = []
                    self.call()
                elif user == "n":
                    print "Adiós!!"
                    sys.exit()
                else:
                    print "Solo ingrese Y o N"
            except TypeError:
                print "Opción inválida"

    def call(self):
        self.fill_board()
        self.print_board()
        self.fila_aleatoria()
        self.columna_aleatoria()
        self.ship_variables()
        self.user_entry()

""" Calls Single Player """
GO = Game()
GO.call()
GO.play_again()
