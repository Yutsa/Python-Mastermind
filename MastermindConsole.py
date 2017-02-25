import initialisations
from initialisations import *
import tourDeJeu
from tourDeJeu import *

nbCouleur , longueur , essais = initGame()
soluce = choseList(nbCouleur,longueur)
count = 1
while(essais > 0):
    print("Essai ",count)
    bons,mals =  evaluer(choice(nbCouleur,longueur),soluce)
    affichage(bons,mals)
    count+=1
    if(bons == longueur):
        print("Bravo vous avez gagné, la suite etait bien ",end="")
        printListe(soluce)
        exit(0)
print("Perdu , il fallait trouver : ",end ="")
printListe(soluce)
