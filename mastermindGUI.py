#############################################################################
#                        I   M   P   O   R   T   S                          #
#############################################################################
import pygame, socket, threading
from initialisations import *
from tourDeJeu import *
#Centre la fenêtre du jeu
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'


#############################################################################
#                    F   O   N   C   T   I   O   N   S (/procédures)        #
#############################################################################

###Gestion des clics souris
def onClick(event):
    global current_pos
    global essai_actuel
    global grille
    global essais
    global longueur
    global soluce
    global col_result
    global gagne
    global perdu
    global soluceGrid
    #Recherche du clic sur une bille :
    ballClick = getBallClicked(event)
    if ballClick != -1 and not ( gagne or perdu)  :
        placeBall(ballClick)
    #Recherche du clic sur un bouton
    buttonClick = getButtonClicked(event)
    #Bouton recommencer
    if buttonClick == 0 :
        grille = initGrid(essais,longueur)
        current_pos = 0
        essai_actuel = 0
        col_result = initResults()
        soluceGrid = [0]*longueur
        if gagne : ##Si on clique sur recommencé et qu'on a gagné, une nouvelle soluce est générée
            soluce = choseList(6,4)
            gagne = False
        perdu = False
    #Bouton tester ligne
    if buttonClick == 1 and current_pos == longueur :
        liste = grille[essai_actuel]
        bons,mals = evaluer(liste,soluce)
        afficherResultat(col_result,bons,mals)
        essai_actuel +=1
        current_pos = 0
        if bons == longueur :
            gagne = True
    #Bouton supprimer ligne
    if buttonClick == 2 :
        clearLine(essai_actuel)

    #Recherche clic sur "Sauvegarder" ou "Charger"
    x,y = event.pos #pos souris
    global saveRectangle
    if saveRectangle.collidepoint(x,y):
        saveGame()
        
        
    global loadRectangle
    if loadRectangle.collidepoint(x,y):
        loadGame()


def onClickMulti(event):
    global current_pos
    global essai_actuel
    global grille
    global essais
    global longueur
    global soluce
    global col_result
    global gagne
    global perdu
    global soluceGrid
    #Recherche du clic sur une bille :
    ballClick = getBallClicked(event)
    if ballClick != -1 and not ( gagne or perdu)  :
        placeBall(ballClick)
        update_grid(grille)
    #Recherche du clic sur un bouton
    buttonClick = getButtonClicked(event)
    #Bouton tester ligne
    if buttonClick == 1 and current_pos == longueur :
        liste = grille[essai_actuel]
        bons,mals = evaluer(liste,soluce)
        afficherResultat(col_result,bons,mals)
        ###Envoi des infos à l'autre joueur si en multijouer
        sendResult()
        essai_actuel +=1
        current_pos = 0
        if bons == longueur :
            sendWon()#Previent de la victoire en multijoueur
            gagne = True
    #Bouton supprimer ligne
    if buttonClick == 2 :
        clearLine(essai_actuel)
        update_grid(grille) #Envoie sa grile en multijoueur


    ###On envoie a quel tour de jeu on se trouve
    sendTurn()

###Procedure d'effacement d'une ligne du plateau (demandé en consigne) :
def clearLine(essai):
    global grille
    global longueur
    global current_pos
    for i in range(longueur):
        grille[essai][i] = 0
    current_pos = 0
###Place une bille dans la grille
def placeBall(ball_id):
    global longueur
    global current_pos
    global essai_actuel
    global grille
    if current_pos < longueur:
        grille[essai_actuel][current_pos] = ball_id
        current_pos += 1

###Recherche si on a cliqué sur une bille
###Si on a cliqué sur une bille : retourne l'id de la bille ,
###sinon retourne -1
def getBallClicked(event):
    global colorPos
    x,y = event.pos #position souris
    for i in colorPos:
        #verif si le point (x,y) dans le rectangle de collision:
        xPos = colorPos[i][0]
        yPos = colorPos[i][1]
        right = xPos + 32
        bottom = yPos + 32
        if x>xPos and x<right and y > yPos and y<bottom :
            return i
    return -1


###Recherche si on a cliqué sur un boutton: si on a cliqué sur un bouton , retourne l'id du bouton
###sinon retourne -1
def getButtonClicked(event):
    global button_pos
    x,y = event.pos
    for i in range(len(button_pos)):
        if(button_pos[i][1].collidepoint(x,y)):
            return i
    return -1

###Procedure dessin du plateau (demandée en consigne):
def draw(spritebatch):
    ##Dessin du background
    spritebatch.blit(background,(0,0))
    
    #Dessin des billes de couleur
    for i in range(1,len(states)):
        spritebatch.blit(states[i],colorPos[i])
    
    #Dessin de la grille
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            spritebatch.blit(states[grille[i][j]],(50 + j*64, 100 + i*46))

    #Dessin des bouttons
    for i in range(len(button_pos)):
        spritebatch.blit(button_pos[i][0],button_pos[i][1])


    #Dessin de la colonne des résultats
    for i in range(len(col_result)):
        index= 0
        for x in range(2):
            for y in range(2):
                spritebatch.blit(result_states[col_result[i][index]],(nbCouleur*51 + y*8, 108 + i*46 + x*8))
                index +=1

    #(Bonus) Dessin de la fleche indiquant notre tour de jeu
    spritebatch.blit(turn_arrow, (0,essai_actuel *46 + 100))


    #Dessin de la solution
    for i in range(len(soluceGrid)):
        spritebatch.blit(states[soluceGrid[i]],( 50 + i*64 ,582 ))
        
    #Dessin du texte "solution":
    spritebatch.blit(soluceText,soluceRectangle)

    ###Dessin du texte gagné ou perdu
    if gagne :
        spritebatch.blit(gagneText,gagneRectangle)
    if perdu :
        spritebatch.blit(perduText,perduRectangle)

    ###(Bonus) Dessin des boutons sauvegarder et charger
    spritebatch.blit(saveText,saveRectangle)
    spritebatch.blit(loadText,loadRectangle)

#Dessin du jeu en multijoueur
def drawMulti(spritebatch):
    #Dessin du fond d'ecran
    spritebatch.blit(background,(0,0))
    
    #Dessin des billes de couleur
    for i in range(1,len(states)):
        spritebatch.blit(states[i],colorPos[i])
    
    #Dessin de la grille
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            spritebatch.blit(states[grille[i][j]],(50 + j*64, 100 + i*46))

    #Dessin de la grille multijoueur(autre joueur)
    for i in range(len(other_grid)):
        for j in range(len(other_grid[i])):
            spritebatch.blit(states[other_grid[i][j]],(700 + j*64, 100 + i*46))


    #Dessin des bouttons (sauf le recommencer car en multijoueur)
    for i in range(1,len(button_pos)):
        spritebatch.blit(button_pos[i][0],button_pos[i][1])


    #Dessin de la colonne des résultats
    for i in range(len(col_result)):
        index= 0
        for x in range(2):
            for y in range(2):
                spritebatch.blit(result_states[col_result[i][index]],(nbCouleur*51 + y*8, 108 + i*46 + x*8))
                index +=1

    #Dessin de la colonne des résultats multijoueur (autre joueur)
    for i in range(len(other_result)):
        index= 0
        for x in range(2):
            for y in range(2):
                spritebatch.blit(result_states[other_result[i][index]],(660 + y*8, 108 + i*46 + x*8))
                index +=1

    #Dessin de la fleche indiquant notre tour de jeu
    spritebatch.blit(turn_arrow, (0,essai_actuel *46 + 100))

    #Dessin de la fleche du tour de jeu de l'autre joueur (multijoueur)
    spritebatch.blit(ennemy_arrow,(990-32, ennemy_turn*46 +100))

    #Dessin solution et gagné ou perdu
    drawSoluce(spritebatch)
    drawSoluceText(spritebatch)
    drawScore(spritebatch)



#Dessin des billes de solution:
def drawSoluce(spritebatch):
    for i in range(len(soluceGrid)):
        spritebatch.blit(states[soluceGrid[i]],( 50 + i*64 ,582 ))
        
#Dessin du texte "solution":
def drawSoluceText(spritebatch):
    spritebatch.blit(soluceText,soluceRectangle)

###Dessin du texte gagné ou perdu
def drawScore(spritebatch):
    if gagne :
        spritebatch.blit(gagneText,gagneRectangle)
    if perdu :
        spritebatch.blit(perduText,perduRectangle)


###Procedure qui change l'affichage du resultat pour un essai(consigne):
def afficherResultat(col, biens,mals):
    global essai_actuel
    index = 0
    for i in range(biens):
        col[essai_actuel][index] = 2
        index+=1
    for i in range(mals):
        col[essai_actuel][index] = 1
        index +=1
    
        

###Créé la grille de jeu:
def initGrid(x,y):
    return [[0] * y for _ in range(x)]

##Créé la colonne des resultats
def initResults() : 
    col_result = list()
    for i in range(essais):
        tab= [0]*4
        col_result.append(tab)
    return col_result

#############################################################################
#           I   N   I   T   I   A   L   I   S   A   T   I   O   N           #
#############################################################################
pygame.init()
pygame.font.init()
mainSurface = pygame.display.set_mode((990,650))
pygame.display.set_caption("Mastermind")
FPS = 30
fpsClock = pygame.time.Clock()

#Differents menus
current_display = 1
menu_display = 1
multi_menu_display = 2
multi_wait_display = 3
game_solo_display = 4
game_multi_display = 5
multi_host_display = 6
multi_client_display = 7

#Définit si on se trouve en multijoueur
isMultiplayer = False

#Grille de jeu et parametres
nbCouleur = 6
longueur = 4
essais = 10
grille = initGrid(essais,longueur)
essai_actuel = 0 #Ligne sur laquelle on se trouve
current_pos = 0 #Colonne sur laquelle on se trouve
soluce = choseList(6,4)
print(soluce)
#Couleurs
BLACK = (0,0,0)
WHITE = (255,255,255)

#Polices
default_font = pygame.font.Font("freesansbold.ttf",18)
big_font = pygame.font.Font("freesansbold.ttf",34)
title_font = pygame.font.Font("freesansbold.ttf",50)

#Textures
states = [0]*(nbCouleur+1)
for i in range(nbCouleur+1):
    states[i] = pygame.image.load("ressources/img/"+str(i)+".png").convert_alpha()
#Dictionnaire idCouleur - Tuple position des billes :
colorPos = dict()
for i in range(1,len(states)):
        colorPos[i] = (50 +(i-1) * 38 , 20)




### "Boutons" effacer, tester, recommencer
button_text = ["Recommencer","Tester la ligne","Effacer la ligne"]
button_pos = dict()
for i in range(len(button_text)):
    text = default_font.render(button_text[i], True , WHITE , BLACK)
    xPos = nbCouleur*51 + 75
    yPos = 220 + i * 50
    textRect = text.get_rect()
    textRect.topleft = (xPos,yPos)
    text.set_colorkey(BLACK)
    button_pos[i] = (text,textRect)

### Colonne des resultats bons,mauvais
result_states = [0]*3
for i in range(3):
    result_states[i] = pygame.image.load("ressources/img/res"+str(i)+".png").convert_alpha()
col_result = initResults()

###Perdu ou gagné
perdu = False
gagne = False
## Textes "gagné" et "perdu"
gagneText = big_font.render("Gagné !", True , WHITE , BLACK)
gagneRectangle = gagneText.get_rect()
gagneRectangle.topleft = (nbCouleur*51 + 75 , 590)
gagneText.set_colorkey(BLACK)

perduText = big_font.render("Perdu !" , True , WHITE , BLACK)
perduRectangle = perduText.get_rect()
perduRectangle.topleft = (nbCouleur*51 + 75,590)
perduText.set_colorkey(BLACK)


###Ligne de solution et texte "Solution":
soluceGrid = [0]*longueur
soluceText = default_font.render("Solution:",True, WHITE , BLACK)
soluceRectangle = soluceText.get_rect()
soluceRectangle.topleft = (50, 558)
soluceText.set_colorkey(BLACK)


###Arriere plan
background = pygame.image.load("ressources/img/bg_versus.png").convert_alpha()




#############################################################################
#                           B   O   N   U   S                               #
#############################################################################

##On propose en bonus un menu de jeu :
menutext = title_font.render("Menu Principal",True , WHITE, BLACK)
menutext_rec = menutext.get_rect()
menutext_rec.topleft = (mainSurface.get_width()/2 - menutext.get_width()/2, 100)
####Boutons du menu principal  :
playSolo =  big_font.render("Solo",True , WHITE , BLACK)
playSolo_rec = playSolo.get_rect()
playSolo_rec.topleft = (mainSurface.get_width()/2 - playSolo.get_width()/2, 200)
#Bouton jouer multijoueur
playMulti = big_font.render("Multijoueur", True , WHITE , BLACK)
playMulti_rec = playMulti.get_rect()
playMulti_rec.topleft = (mainSurface.get_width()/2 - playMulti.get_width()/2 , 300)
#Bouton quitter
leave = big_font.render("Quitter", True , WHITE , BLACK)
leave_rec = leave.get_rect()
leave_rec.topleft = (mainSurface.get_width()/2 - leave.get_width()/2 , 400)

#Bouton retour
return_button = big_font.render("Retour",True,WHITE,BLACK)
return_button_rec = return_button.get_rect()
return_button_rec.topleft = (mainSurface.get_width()/2 - return_button.get_width()/2, 550)



##Dessin du menu principal
def drawMainMenu(spritebatch):
    #Dessin du titre du menu
    spritebatch.blit(menutext,menutext_rec)
    #Dessin des boutons
    spritebatch.blit(playSolo,playSolo_rec)
    spritebatch.blit(playMulti,playMulti_rec)
    spritebatch.blit(leave,leave_rec)

## Update menu principal
def onClickMainMenu(event):
    x,y = event.pos #position souris
    global current_display
    if(playSolo_rec.collidepoint(x,y)):
        current_display = game_solo_display

    if(playMulti_rec.collidepoint(x,y)): #On redirige vers le menu multijoueur
        current_display= multi_menu_display
        
    if(leave_rec.collidepoint(x,y)):
        pygame.quit()
        exit()

##Menu multijoueur:
hostServer = big_font.render("Heberger une partie", True,WHITE,BLACK)
hostServer_rec = hostServer.get_rect()
hostServer_rec.topleft = (mainSurface.get_width()/2 - hostServer.get_width()/2 , 100)

joinServer = big_font.render("Rejoindre une partie", True , WHITE , BLACK)
joinServer_rec = joinServer.get_rect()
joinServer_rec.topleft = (mainSurface.get_width()/2 - joinServer.get_width()/2  , 200)

spectateServer = big_font.render("Regarder une partie", True, WHITE , BLACK)
spectateServer_rec = joinServer.get_rect()
spectateServer_rec.topleft = (mainSurface.get_width()/2 - spectateServer.get_width()/2 , 500)

return_button = big_font.render("Retour", True, WHITE , BLACK)
return_button_rec = return_button.get_rect()
return_button_rec.topleft = (mainSurface.get_width()/2 - spectateServer.get_width()/2 , 600)

#Dessin menu multijoueur
def drawMultiMenu(spritebatch):
    spritebatch.blit(hostServer,hostServer_rec)
    spritebatch.blit(joinServer,joinServer_rec)
    spritebatch.blit(spectateServer,spectateServer_rec)

#Update menu multijoueur
def onClickMultiMenu(event):
    x,y = event.pos
    global current_display
    if(hostServer_rec.collidepoint(x,y)):
        current_display = multi_host_display
    if(joinServer_rec.collidepoint(x,y)):
        current_display = multi_client_display


##Menu multi host (quand on heberge une partie)
#Bouton héberger
buttonHost = pygame.image.load("ressources/img/host_button.png").convert_alpha()
buttonHost_rec = buttonHost.get_rect()
buttonHost_rec.topleft = (mainSurface.get_width()/2 - buttonHost.get_width()/2 , mainSurface.get_height()/2 - buttonHost.get_height()/2)
#Dessin menu multi host
def drawMultiHostMenu(spritebatch):
    #Bouton héberger
    spritebatch.blit(buttonHost,buttonHost_rec.topleft)
    #Rendu du texte d'information
    info_rendered_text = big_font.render(info_text,True,WHITE,BLACK)
    info_rendered_text_rec = info_rendered_text.get_rect()
    info_rendered_text_rec.topleft = (mainSurface.get_width()/2 - info_rendered_text.get_width()/2, 450)
    info_rendered_text.set_colorkey(BLACK)
    spritebatch.blit(info_rendered_text,info_rendered_text_rec)      
#Update menu multi host
def onClickMultiHostMenu(event):
    x,y = event.pos
    if buttonHost_rec.collidepoint(x,y):
        th = ThreadHost()
        th.start()

##Menu multi client (quand on veut rejoindre une partie)
# TextField
textFieldFrame = pygame.image.load("ressources/img/frame.png").convert_alpha()
text_input = ""
#Bouton join server
buttonJoin = pygame.image.load("ressources/img/join_button.png").convert_alpha()
buttonJoin_rec = buttonJoin.get_rect()
buttonJoin_rec.topleft = (mainSurface.get_width()/2 + textFieldFrame.get_width()/2 + 10,mainSurface.get_height()/2 - buttonJoin.get_height()/2)

#Texte info
info_text = ""


#Dessin menu multi client
def drawMultiClientMenu(spritebatch):
    #Cadre textbox
    spritebatch.blit(textFieldFrame,(mainSurface.get_width()/2 - textFieldFrame.get_width()/2, mainSurface.get_height()/2 - textFieldFrame.get_height()/2))
    #Boutton join
    spritebatch.blit(buttonJoin,buttonJoin_rec.topleft )
    #Rendu du texte dans la textbox
    rendered_text = big_font.render(text_input,True,WHITE,BLACK)
    rendered_text_rec = rendered_text.get_rect()
    rendered_text_rec.topleft = (mainSurface.get_width()/2 - textFieldFrame.get_width()/2 + 5 , mainSurface.get_height()/2 - textFieldFrame.get_height()/2 + 5)
    rendered_text.set_colorkey(BLACK)
    spritebatch.blit(rendered_text,rendered_text_rec)

    #Rendu du texte d'information
    info_rendered_text = big_font.render(info_text,True,WHITE,BLACK)
    info_rendered_text_rec = info_rendered_text.get_rect()
    info_rendered_text_rec.topleft = (mainSurface.get_width()/2 - info_rendered_text.get_width()/2, 450)
    info_rendered_text.set_colorkey(BLACK)
    spritebatch.blit(info_rendered_text,info_rendered_text_rec)

    #Rendu bouton retour
    return_button_rec.topleft = (mainSurface.get_width()/2 - return_button.get_width()/2, 550)
    spritebatch.blit(return_button,return_button_rec)

#Update menu multi client
def onClickMultiClientMenu(event):
    x,y = event.pos
    if buttonJoin_rec.collidepoint(x,y):
        tc = ThreadConnection(text_input)
        tc.start()
    if return_button_rec.collidepoint(x,y):
        global current_display
        current_display = multi_menu_display

#Rempli le champ de texte en fonction des entrées clavier de l'utilisateur
def onKeyMultiClientMenu(event):
    global text_input
    string = pygame.key.name(event.key)
    try:
        # Taille du textfield en caractères
        to_add = str(int(string))
        if(len(text_input)<20):
            text_input+= to_add
    except Exception :
        if(string == "," or string ==".")and (len(text_input)<20):
            text_input+= "."
        elif string == "backspace":
            text_input  = str(text_input[0:len(text_input)-1])

############################En jeu ##############################

###Flèche indiquant sur quelle ligne on se trouve :
turn_arrow = pygame.image.load("ressources/img/arrow.png").convert_alpha()
ennemy_arrow = pygame.image.load("ressources/img/ennemy_arrow.png").convert_alpha()

###Bouton sauvegarde et chargement:
saveText = default_font.render("Sauvegarder", True , WHITE , BLACK)
saveRectangle = gagneText.get_rect()
saveRectangle.topleft = (nbCouleur*51 + 75 ,440)
saveText.set_colorkey(BLACK)

loadText = default_font.render("Charger" , True , WHITE , BLACK)
loadRectangle = perduText.get_rect()
loadRectangle.topleft = (nbCouleur*51 + 75, 480)
loadText.set_colorkey(BLACK)


###Sauvegarde du jeu en cours :
def saveGame():
    global essai_actuel
    global current_pos
    global soluce
    global grille
    save_file = open("game.save", "w")
    save_file.write("check:ok\n") #Ligne verification
    save_file.write(str(essai_actuel)+"\n")
    save_file.write(str(current_pos)+"\n")
    for i in soluce:
        save_file.write(str(i))
    save_file.write("\n")
    ##Ecriture de la grille
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            save_file.write(str(grille[i][j]))
        save_file.write("\n")
    save_file.close()

###Chargement d'un jeu précédent:
def loadGame():
    global essai_actuel
    global current_pos
    global soluce
    global grille
    save_file = open("game.save", "r")
    line_number= 0
    for line in save_file:
        line = line.replace("\n","")
        if line_number == 0 and not line == "check:ok": #Check fichier
            print("erreur") ##Afficher l'erreur dans le jeu
            return
        if line_number == 1 :
            essai_actuel = int(line)
        if line_number == 2 :
            current_pos = int(line)
        if line_number == 3 :
            temp = list()
            for char in line :
                temp.append(int(char))
            soluce = temp
        if line_number > 3 :
            temp = list()
            for char in line :
                temp.append(int(char))
            grille[line_number-4] = temp
        
        line_number +=1
        
    save_file.close()

    ##Il faut recalculer les resultats des lignes complétées
    global col_result
    for i in range(essai_actuel):
        biens,mals = evaluer(grille[i], soluce)
        index = 0
        for j in range(biens):
            col_result[i][index] = 2
            index+=1
        for j in range(mals):
            col_result[i][index] = 1
            index +=1
#Fin chargement

commSocket = None
CLIENT_NAME = ""
####Traitement des requetes reçues
def processRequest(msg):
    req = msg.split(",")
    msg = req[0]
    sender = req[1]
    if "SET" in msg:
        req = msg.split(":")
        if(req[1] == "soluce"): ## Set soluce
            sol = req[2].split(";")
            global soluce
            tab = list()
            for i in sol:
                tab.append(int(i))
            soluce = tab
        if(req[1] == "grid"): ##Set grid
            tab = [[0] * 4 for _ in range(10)]
            grid = req[2].split("|")
            for i in range(len(grid)):
                for j in range(len(grid[i].split(";"))):
                    tab[i][j] = int(grid[i].split(";")[j])
            global other_grid
            other_grid = tab
        if(req[1] == "results"):
            tab = initResults()
            subtab = req[2].split("|")
            for i in range(len(subtab)):
                for j in range(len(subtab[i].split(";"))):
                    tab[i][j] = int(subtab[i].split(";")[j])
            global other_result
            other_result = tab
        if(req[1] == "turn"):
            global ennemy_turn
            ennemy_turn = int(req[2])
        if(req[1] == "won"):
            global ennemy_won
            ennemy_won = True
            global perdu
            perdu = True
        if(req[1] == "lose"):
            global ennemy_lose
            ennemy_lose = True
            global gagne
            gagne = True
        

#Grille de l'autre joueur et resultats autre joueur
other_grid = [[0] * 4 for _ in range(10)]
showResults = True
other_result = initResults()

#Tour de l'autre joueur
ennemy_turn = 0

#Determine si l'autre joueur a gagné ou perdu
ennemy_won = False
ennemy_lose = False


###Update la grille:
def update_grid(grille):
    sub_req = ""
    for i in range(len(grille)):
        substring =""
        for j in range(len(grille[i])):
            string = str(grille[i][j])
            substring+=string
            if(j != len(grille[i])-1):
               substring+=";"
        sub_req+= substring
        if(i != len(grille)-1):
               sub_req+="|"
    req = "SET:grid:"+sub_req
    commSocket.send((req+","+CLIENT_NAME).encode())

###Update des resultats :
def sendResult():
    sub_req = ""
    for i in range(len(col_result)):
        substring =""
        for j in range(len(col_result[i])):
            state = col_result[i][j]
            substring+=str(state)
            if(j!= len(col_result[i])-1):
                substring+=";"
        sub_req+= substring
        if( i!= len(col_result)-1):
            sub_req+="|"
    req = "SET:results:"+sub_req
    commSocket.send((req+","+CLIENT_NAME).encode())

##Update du tour de jeu :
def sendTurn():
    sub_req="SET:turn:"
    global essai_actuel
    sub_req+=str(essai_actuel)
    commSocket.send((sub_req+","+CLIENT_NAME).encode())

##Envoie à l'adversaire qu'on a gagné
def sendWon():
    req="SET:won"
    commSocket.send((req+","+CLIENT_NAME).encode())

##Envoie à l'adversaire qu'on a perdu
def sendLose():
    req = "SET:lose"
    commSocket.send((req+","+CLIENT_NAME).encode())

    
#############################################################################
#      t   h   r   e   a   d        r   e   c   e   p   t   i   o   n       #
#############################################################################
class ThreadReception(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def run(self):
        while True:
            msg = self.connexion.recv(1024)
            processRequest(msg.decode())


#####Methode de lancement du thread de reception
def startGame(clientConnection):
    global commSocket
    commSocket = clientConnection
    tr = ThreadReception(commSocket)
    tr.start()
    if CLIENT_NAME == "Server":##Si on est le server : Redefint la soluce
        translatedSoluce =""
        for i in range(len(soluce)):
            string = str(soluce[i])
            if(i!= len(soluce)-1):
                string+=";"
            translatedSoluce+=string
        commSocket.send(("SET:soluce:"+translatedSoluce+","+CLIENT_NAME).encode())
    global current_display
    current_display = game_multi_display

#############################################################################
#           t   h   r   e   a   d           e   c   o   u   t   e           #
#############################################################################
class ThreadEcoute(threading.Thread):
    def __init__(self,serv):
        threading.Thread.__init__(self)
        self.server = serv
        self.clientCount = 0

    def run(self):
        global info_text
        while self.clientCount < 1 :
            connexion, adresse = self.server.accept()
            info_text = "Connexion de "+ str(adresse) 
            self.clientCount+=1
            startGame(connexion)


#############################################################################
#                        S   E   R   V   E   U   R                          #
#############################################################################

host = 'localhost' #Hôte sur machine locale
port = 44004
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket = None

class ThreadHost(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        launchServer()

def launchServer():
    global info_text #texte d'information sur les opérations en cours
    try:
        info_text = "Initialisation ..."
        serverSocket.bind((host,port))
        info_text = "Serveur initialisé , en attente d'une autre connexion"
        serverSocket.listen(1)
        te = ThreadEcoute(serverSocket)
        te.start()
        CLIENT_NAME = "Server"
    except socket.error :
        info_text = "Impossible de lancer le serveur"
        

class ThreadConnection(threading.Thread):
    def __init__(self,ipaddr):
        threading.Thread.__init__(self)
        self.ipAddress = ipaddr
    def run(self):
        connectToServer(self.ipAddress)

def connectToServer(ipAddress):
    global info_text #texte d'information sur les opérations en cours
    clientSocket = serverSocket #On devient alors client
    try:
        info_text = "Connexion en cours..."
        clientSocket.connect((ipAddress,port))
        CLIENT_NAME = "Client"
        startGame(clientSocket)
        info_text = "Connexion etablie"
    except socket.error:
        info_text = "La connexion a échoué"
        print("erreur")




#############################################################################
#           B    O    U    C    L    E        D    E        J    E   U      #
#############################################################################
while True:
    """Events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN: ## gestion click
            if(current_display == game_solo_display): #Update , en solo
                onClick(event)
            if(current_display ==  game_multi_display): #Update , en multi
                onClickMulti(event)
            if(current_display == menu_display): # Update, main menu
                onClickMainMenu(event)
            if(current_display == multi_menu_display): #Update , multi menu
                onClickMultiMenu(event)
            if(current_display == multi_host_display): #Update , menu host
                onClickMultiHostMenu(event)
            if(current_display == multi_client_display): #Update, menu client
                onClickMultiClientMenu(event)
        if event.type == pygame.KEYDOWN : ## gestion clavier
            if(current_display == multi_client_display):
                onKeyMultiClientMenu(event)
            
            
    ##Verifie si le joueur a perdu:
    if essai_actuel >= essais and not gagne:
        perdu = True

    ##Affiche la solution , en cas de défaite ou victoire
    if gagne or perdu :
        soluceGrid = soluce
        
    """Draw"""
    mainSurface.fill((0,0,0))
    if(current_display == menu_display): #Draw , main menu
        drawMainMenu(mainSurface)
    if(current_display == game_solo_display):#Draw jeu solo
        draw(mainSurface)
    if(current_display ==  game_multi_display):
        drawMulti(mainSurface)
    if(current_display == multi_menu_display): #Draw menu multijoueur
        drawMultiMenu(mainSurface)
    if(current_display == multi_host_display):#Draw menu heberger partie
        drawMultiHostMenu(mainSurface)
    if(current_display == multi_client_display):#Draw menu rejoindre une partie
        drawMultiClientMenu(mainSurface)
        
    pygame.display.update()
    fpsClock.tick(FPS)
