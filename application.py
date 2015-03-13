import random

tablero = []

for x in range(0,10):
  tablero.append(["O"] * 10)

def print_tablero(tablero):
  for fila in tablero:
    print " ".join(fila)

print "Juguemos batalla naval!"
print_tablero(tablero)

def fila_aleatoria(tablero):
  return random.randint(0,len(tablero)-1)

def columna_aleatoria(tablero):
  return random.randint(0,len(tablero[0])-1)

barco_fila = fila_aleatoria(tablero)
barco_col = columna_aleatoria(tablero)
print barco_fila
print barco_col

for turno in range(4):
    adivina_fila = input("Adivina fila:")
    adivina_columna = input("Adivina columna:")

    if adivina_fila == barco_fila and adivina_columna == barco_col:
        print "Felicitaciones! Hundiste mi barco!"
        break
    else:
        if (adivina_fila < 0 or adivina_fila > 5) or (adivina_columna < 0 or adivina_columna > 5):
            print "Vaya, esto ni siquiera esta en el oceano."
        elif(tablero[adivina_fila-1][adivina_columna-1] == "X"):
            print "Ya dijiste esa."
        else:
          print "No impactaste mi barco!"
          tablero[adivina_fila-1][adivina_columna-1] = "X"
        if turno == 3:
            print "Termino el juego"

    print turno + 1
    print_tablero(tablero)