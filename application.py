import random

class Game(object):
  """Creates a class with a player in battleship"""
  def first_player(self):
    """Single Player Battleship"""
    board = [] #empty list that will contain the board

    for x in range(0,10): #for each element 
      board.append(["O"] * 10) #multiply it 10 times to create board

    def print_board(board):
      """function to print board"""
      for fila in board:
        print " ".join(fila) #join takes the format away and adds a space

    print """
                  Let's play Battleship!
    Instructions: Guess the Row and the Column of the ship.
    """
    print "0|1|2|3|4|5|6|7|8|9"
    print "-------------------\n"
    print_board(board) #prints the image of board

    def fila_aleatoria(board):
      return random.randint(0,len(board)-1)

    def columna_aleatoria(board):
      return random.randint(0,len(board[0])-1)

    barco_fila = fila_aleatoria(board)
    barco_col = columna_aleatoria(board)
    print barco_fila
    print barco_col

    for turno in range(4):
        adivina_fila = input("Adivina fila:")
        adivina_columna = input("Adivina columna:")

        if adivina_fila == barco_fila and adivina_columna == barco_col:
            print "Felicitaciones! Hundiste mi barco!"
            break
        else:
            if (adivina_fila < 0 or adivina_fila > 11) or (adivina_columna < 0 or adivina_columna > 11):
                print "Vaya, esto ni siquiera esta en el oceano."
            elif(board[adivina_fila-1][adivina_columna-1] == "X"):
                print "Ya dijiste esa."
            else:
              print "No impactaste mi barco!"
              board[adivina_fila-1][adivina_columna-1] = "X"
            if turno == 3:
                print "Termino el juego"

        print turno + 1
        print_board(board)

Initiate = Game()
Initiate.first_player()