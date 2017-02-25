from tourDeJeu import *
from initialisations import *
#création des ensembles avec toutes les solutions possibles
liste = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1,7):
                liste.append((i, j, k, l))
                
S = set(liste)
possibles = frozenset(liste)
#création ensemble résultats
liste2 = []
for i in range(5):
    for j in range(5 - i):
        if( i!= 3 or j!=1):
            liste2.append((i, j))
resultats = set(liste2)

def choisirIA(S,possibles,resultats,essai):
    if essai == 1 :
        return [1,1,2,2]
    else :
        ##Si il ne reste qu'un choix
        if(len(S) == 1):
            return S.pop()
        ##Sinon on cherche le meilleur choix
        else:
            ##Maximum H(g)
            maxiHg = 0
            bestChoice = 0
            #Calcul le maximum sur l'ensemble des elem 'x' de "possibles" :
            for x in possibles :
                # Du min sur l'ensemble des elem 'res' de resultat
                Hx = set()
                for res in resultats :
                    Gxz = set()
                    # Du nombre d'elements 's' de S
                    for s in S :
                        #Dont l'evaluation avec 's' est différente de 'res'
                        if evaluer(list(x),list(s)) != res:
                            Gxz.add(s)
                    Hx.add(len(Gxz))
                HxMin = min(Hx)
                #Recherche du maxi parmi les minis (minimax)
                if(HxMin > maxiHg):
                    maxiHg = HxMin
                    bestChoice = x
            return list(bestChoice)
                    
def play():
    global S
    soluce = choseList(6,4)
    essai = 1
    while True:
        c = choisirIA(S,possibles,resultats,essai)
        print("Essai n°",essai)
        print("Choix de l'ordinateur: ",end ="")
        printListe(c)
        i = evaluer(list(c),list(soluce))
        affichage(i[0],i[1])
        if(i[0] == 4):
            print("L'IA a trouvé le resultat ! C'etait bien : ",end= "")
            printListe(soluce)
            input("Appuyez sur Entrer pour continuer...")
            exit()
        else:
            copy = S.copy()
            for elem in S :
                if(evaluer(list(elem),c) != i):
                    copy.remove(elem)
            S = copy.copy()
            essai +=1
    
play()    
