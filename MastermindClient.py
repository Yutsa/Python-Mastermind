import socket, threading
from initialisations import *
from tourDeJeu import *

##Convertit le choix(liste) en entier:
def convert(x):
    toConvert = ""
    for i in x:
        toConvert+= str(i)
    return int(toConvert)

###Demarrage d'une connection avec le client
host = "25.178.91.160"
port = 44000

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Tentative de connexion ...")
try:
    clientSocket.connect((host, port))
except socket.error:
    print ("La connexion a échoué.")
    exit()    
print ("Connexion établie avec le serveur.")

####Boucle de communication
while True:
    reponse = clientSocket.recv(1024)
    if not reponse:
        break
    query = reponse.decode()
    if query.lower() == 'initgame': ##Code envoyé par le serveur pour initGame()
        nbCouleur , longueur , essais = initGame()
        soluce = choseList(nbCouleur,longueur)
        query = ""
        query+= str(nbCouleur) + ":"
        query+= str(longueur) + ":"
        query+= str(essais) 
        clientSocket.send(query.encode())
    if query.lower() == 'attempt': ##Code envoyé par le serveur pour une proposition
        clientSocket.send("ok".encode())#Methode pour confirmer avant renvoi
        nbCouleur = int((clientSocket.recv(1024)).decode())
        clientSocket.send("ok".encode())#Confirmation
        longueur = int((clientSocket.recv(1024)).decode())
        clientSocket.send("ok".encode())#Confirmation
        choix = choice(nbCouleur,longueur)
        choix = convert(choix)
        query = str(choix)
        clientSocket.send(query.encode())
    elif "msg_code:" in query: ##Message du serveur non interprété
        print(query.replace("msg_code:",""))
clientSocket.close()

input("Appuyez sur entrer pour continuer")
