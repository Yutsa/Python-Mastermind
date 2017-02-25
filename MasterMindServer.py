import socket , threading
from initialisations import *
from tourDeJeu import * 

#Jeu
nbCouleur , longueur , essais = 0 , 0 , 0
soluce = 0
count = 1 

####Demarrage du jeu pour le client:
def startGame(conn):
    query = "initGame"
    conn.send(query.encode())
    print("En attente de l'initialisation ...")
    reponse = conn.recv(1024)
    reponse = reponse.decode()
    tab = reponse.split(":")
    global nbCouleur
    nbCouleur = int(tab[0])
    global longueur
    longueur = int(tab[1])
    global essais
    essais = int(tab[2])
    global soluce
    soluce = choseList(nbCouleur,longueur)
    print("essais",essais)
    print("soluce generee : ",soluce)
    play(conn)

def play(conn):
    global count
    global essais
    global soluce
    print("Debut du jeu,essais",essais)
    while essais > 0:
        print("essai n°",count)
        conn.send(("msg_code:Essai n° " + str(count)).encode())
        conn.send("attempt".encode())
        conn.recv(1024) #Confirmation 
        conn.send(str(nbCouleur).encode())
        conn.recv(1024) #Confirmation 
        conn.send(str(longueur).encode())
        conn.recv(1024) #Confirmation
        reponse = conn.recv(1024)
        liste = convert(reponse.decode())
        ###On evalue les bons,mauvais placements
        bons,mals = evaluer(liste,soluce)
        conn.send(("msg_code:"+ str(affichage(bons,mals))).encode())
        print("sent")
        count+=1
        essais -=1
        global longueur
        if(bons == longueur):
            conn.send(("msg_code:Bravo vous avez gagné, la suite etait bien : " + printListe(soluce)).encode())
            conn.close()
    conn.send(("msg_code:Perdu, il fallait trouver : " + printListe(soluce)).encode())
    conn.close()
        
#Convertit le choix (string) en liste d'entiers
def convert(x):
    returned = list()
    for i in x :
        returned.append(int(i))
    return returned

#Thread de lancement du jeu sur chaque client
class ThreadGame(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def run(self):
        startGame(self.connexion)

#Connexion
host = '25.178.91.160' #hebergement de la partie sur machine locale
port = 44000

serverSocket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
try :
    serverSocket.bind((host,port))
except socket.error :
    print("Impossible de bind le socket au port :",port,"interruption . ")
    exit()

print("Serveur initialisé, en attente de connexions...")
serverSocket.listen(5)

while True:
    connexion , adresse = serverSocket.accept()
    print("connection de ",adresse)
    tg = ThreadGame(connexion)
    tg.start()
    


