def choice(nbCouleur,long):
    correcte = False
    while(not correcte):
        proposition = list(input("Entrez votre proposition : "))
        for i in range(len(proposition)) :
            proposition[i] = int(proposition[i])
        correcte =  len(proposition) == long
        if(correcte):
            for i in proposition:
                if not ( i>= 1 and i<= nbCouleur):
                    correcte = False
                    break
    return proposition


def evaluer(prop,soluce):
    propC = prop.copy()
    soluceC = soluce.copy()
    bons = 0
    malPlaces = 0
    count = 0
    #On verifie d'abord toutes les valeurs bien placées
    for i in range(len(propC)):
        if propC[i-count] == soluceC[i-count] :
            bons += 1
            #On sort ses valeurs de chaque liste
            propC.pop(i-count)
            soluceC.pop(i-count)
            count += 1     
    #On verifie ensuite ceux qui sont mals placés
    count = 0
    for i in range(len(propC)):
        if propC[i-count] in soluceC:
            soluceC.remove(propC[i-count])
            propC.pop(i-count)
            malPlaces +=1
            count +=1
    return bons,malPlaces

def affichage(bien,mal):
    print(bien , "bien placé(s), et " , mal , "mal placé(s)")

def printListe(liste):
    resultat = ""
    for i in liste :
        resultat += str(i)
    print(resultat)
        
