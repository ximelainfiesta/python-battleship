import random

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
        Instructions: Guess the Row and the Column of the ship.
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
        for turno in range(4):
            adivina_fila = input("Adivina fila:")
            adivina_columna = input("Adivina columna:")

            if adivina_fila == self.barco_fila and adivina_columna == self.barco_col:
                print "Felicitaciones! Hundiste mi barco!"
                break
            else:
                if (adivina_fila < 0 or adivina_fila > 11) or (adivina_columna < 0 or adivina_columna > 11):
                    print "Vaya, esto ni siquiera esta en el oceano."
                elif(self.board[adivina_fila-1][adivina_columna-1] == "X"):
                    print "Ya dijiste esa."
                else:
                  print "No impactaste mi barco!"
                  self.board[adivina_fila-1][adivina_columna-1] = "X"
                if turno == 3:
                    print "Termino el juego"

            print turno + 1
            self.print_board()

    def call(self):
        self.fill_board()
        self.print_board()
        self.fila_aleatoria()
        self.columna_aleatoria()
        self.ship_variables()
        self.user_entry()


GO = Game()
GO.call()
