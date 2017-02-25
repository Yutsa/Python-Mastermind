import random
from random import *

def initGame():
    nbCouleur = -1
    longueur = -1
    essais = -1
    while(nbCouleur < 2):
        nbCouleur = int(input("Entrez le nombre de couleurs existantes"))
    while(longueur < 2):
        longueur = int(input("Entrez la longueur de la suite à deviner"))
    while(essais < 5):
        essais = int(input("Entrez le nombre d'essais possibles "))
    return nbCouleur,longueur,essais
        
def choseList(nb , long):
    liste = list()
    for i in range(long):
        liste.append(randrange(1,nb+1))
    return liste
