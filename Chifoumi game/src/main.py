# -*- coding: utf-8 -*-

# Nicolas, 2024-02-09
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
from itertools import chain
import tkinter as tk


import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme








# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'grid-chifoumi-map'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 10# frames per second
    game.mainiteration()
    player = game.player
    

def welcome_frame():
    def show_strategies():

        strategies_window = tk.Toplevel(root)
        strategies_window.title("Stratégies")

        strat = tk.Label(strategies_window, text="Stratégies :",
                         font=("Arial", 60))
        strat.pack(pady=40)

        strat1_text = ("Strat 1 : Jouer aléatoirement\n")

        strat1 = tk.Label(strategies_window, text=strat1_text, font=("Arial", 12))
        strat1.pack(pady=40)


        strat2 = tk.Label(strategies_window, text="Strat 2 : Focused ", font=(
            "Arial", 8))
        strat2.pack(pady=40)

        strat3 = tk.Label(strategies_window, text="Strat 3 : Visibilite region", font=(
            "Arial", 8))
        strat3.pack(pady=40)

        strat4 = tk.Label(strategies_window, text="Strat 4 : Choix de recherche ", font=(
            "Arial", 8))
        strat4.pack(pady=40)

        strat5 = tk.Label(strategies_window, text="Strat 5 : Srategie majoritaire ", font=(
            "Arial", 8))
        strat5.pack(pady=40)

        strat6 = tk.Label(strategies_window, text="Strat 6 : Strategie majoritaire Alter",
                          font=("Arial", 8))
        strat6.pack(pady=40)

        strat7 = tk.Label(strategies_window, text="Strat 7 : Specialisation  ", font=(
            "Arial", 8))
        strat7.pack(pady=40)



    # create a window
    root = tk.Tk()
    root.title("Chifoumi")
    root.geometry("800x900")
    root.configure(bg='#d04669')  # Set background color

    # Titre principal
    title = tk.Label(root, text="WELCOME to Chifoumi", font=("Arial", 24), bg='#D04648', fg='white')
    title.pack(pady=20)

    # Texte et boutons pour la sélection de la stratégie du joueur 1
    label_strat1 = tk.Label(root, text="Select the Strategy for Player 0 :", bg='#D04648', fg='white')
    label_strat1.pack()
    strat1 = tk.StringVar()
    strat1.set("Strat 2")  # Stratégie par défaut
    strat1_buttons = tk.Frame(root, bg='#D04648')
    strat1_buttons.pack()
    for i in range(1, 6):
        button = tk.Radiobutton(strat1_buttons, text="Strat " + str(i), variable=strat1, value="Strat " + str(i),
                                bg='#D04648', fg='black', activebackground='#D04648', activeforeground='white')
        button.pack(side="left")

    # Texte et boutons pour la sélection de la stratégie du joueur 2
    label_strat2 = tk.Label(root, text="Select the Strategy for Player 1 :", bg='#D04648', fg='white')
    label_strat2.pack()
    strat2 = tk.StringVar()
    strat2.set("Strat 4")  
    strat2_buttons = tk.Frame(root, bg='#D04648')
    strat2_buttons.pack()
    for i in range(1, 6):
        button = tk.Radiobutton(strat2_buttons, text="Strat " + str(i), variable=strat2, value="Strat " + str(i),
                                bg='#D04648', fg='black', activebackground='#D04648', activeforeground='white')
        button.pack(side="left")

    # texte et bouton pour la sélection du nombre d'itérations
    label_iter = tk.Label(root, text="Select the number of iterations :", bg='#D04648', fg='white')
    label_iter.pack()
    iter = tk.StringVar()
    iter.set("10")  # 10 itérations par défaut
    iter_buttons = tk.Frame(root, bg='#D04648')
    iter_buttons.pack()
    for i in [10,50,150,300]:
        button = tk.Radiobutton(iter_buttons, text=str(i), variable=iter, value=str(i),
                                bg='#D04648', fg='black', activebackground='#D04648', activeforeground='white')
        button.pack(side="left")

    strategies_button = tk.Button(
        root, text="Stratégie infos !", command=show_strategies)
    strategies_button.pack(pady=20)
    
    # Bouton pour lancer la partie
    button = tk.Button(root, text="Que la partie Commence",
                       command=root.destroy, bg='#6DAA2C', fg='white')
    button.pack(pady=20)

    
    
    # Affichage de la fenêtre
    root.mainloop()
    st1 = strat1.get()
    st2 = strat2.get()
    itr = iter.get()

    # Affichage des valeurs sélectionnées
    print(st1)
    print(st2)
    print(itr)

    return st1, st2, itr

    
def main(str1,str2,itr):
    
    def zone(k,pos,placed):
        (x,y) = pos
        if placed:
            if k==0: 
                return (x>2 and x<9 and y>2 and y<10) # zone des flammes
            elif k==1:
                return (x>12 and x<19 and y>2 and y<10) # zone des potions
            elif k==2:
                return (x>12 and x<19 and y>12 and y<19) # zone des citrouilles
        else: 
            if k==0: 
                return (x==0 or x==1) # zone des flammes
            elif k==1:
                return (y==0 or y==1) # zone des potions
            elif k==2:
                return (x==lMax or x==lMax+1) # zone des citrouilles
            
            
    #-------------------------------
    # Fonctions permettant de récupérer les listes des coordonnées
    # d'un ensemble d'objets ou de joueurs
    #-------------------------------
    
    def itemStates(items): 
        # donne la liste des coordonnees des items
        return [o.get_rowcol() for o in items]
    
    def playerStates(players):
        # donne la liste des coordonnees dez joueurs
        return [p.get_rowcol() for p in players]
    
    
    #-------------------------------
    # Fonctions definissant les positions legales et placement de mur aléatoire
    #-------------------------------
    
    def legal_move_position(pos):
        row,col = pos
        # une position legale de deplacement est dans la carte 
        return (row>lMin and row<lMax-1 and col>=cMin and col<cMax)
    
    
    def legal_position(pos):
        row,col = pos
        all_items_placed = items_placed[0] + items_placed[1] + items_placed[2]
        # une position legale est dans la carte et pas sur un objet deja pose ni sur un joueur
        return ((pos not in itemStates(all_items_placed)) and (pos not in playerStates(players)) and row>lMin and row<lMax-1 and col>=cMin and col<cMax)
    
    def legal_position_focused(pos, k):
        row,col = pos
        all_items_placed = []
        for i in range(len(items_placed)):
            if i!=k:
                all_items_placed += items_placed[i]
        # une position legale est dans la carte et pas sur un objet ininteressant
        cond1 = pos not in itemStates(all_items_placed)
        res = (cond1 and row>lMin and row<lMax-1 and col>=cMin and col<cMax)
        return res
    
    def draw_random_location():
        # tire au hasard un couple de position permettant de placer un item
        while True:
            random_loc = (random.randint(lMin,lMax),random.randint(cMin,cMax))
            if legal_position(random_loc):
                return(random_loc)
            
    #-------------------------------
    # Fonctions pour gérer les comportements
    #-------------------------------
            
    def ramassage(joueur_actuel):
        for k in range(nb_types):
            if posPlayers[joueur_actuel] in itemStates(items_placed[k]):
                picked_items[joueur_actuel][k]+=1
                o=players[joueur_actuel].ramasse(game.layers) # on recupere l'objet 
                items_placed[k].remove(o)         # on l'enleve de la liste des objets de ce type
                break
            
    def deplacement(joueur_actuel, curr_pos, next_pos): #Le joueur actuel se deplace de curr_position a next_position
        if not legal_position(next_pos):
            return False
        posPlayers[joueur_actuel]=next_pos
        
        next_row, next_col = next_pos
        players[joueur_actuel].set_rowcol(next_row,next_col)
        
        return True
    
    def deplacement_focused(joueur_actuel, curr_pos, next_pos, i_prefere): #Le joueur actuel se deplace de curr_position a next_position
        if not legal_position_focused(next_pos, i_prefere):
            return False
        
        posPlayers[joueur_actuel]=next_pos
        
        next_row, next_col = next_pos
        players[joueur_actuel].set_rowcol(next_row,next_col)
        
        return True
    

    def strat_aleatoire(joueur_actuel):
        row,col = posPlayers[joueur_actuel]
        
        while True: # tant que pas legal on retire une position
            x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            next_row = row+x_inc
            next_col = col+y_inc
            if deplacement(joueur_actuel, (row, col), (next_row, next_col)):
                break
        
        ramassage(joueur_actuel)

    
    
    def strat_focused(joueur_actuel, i_prefere):
        if adversaire_est_visible(joueur_actuel):
            chifoumi(joueur_actuel)
            return
        
        objet_prefere = items_types[i_prefere]
        row,col = posPlayers[joueur_actuel]
        
        g =np.zeros((nbLignes,nbCols),dtype=bool)    # une matrice remplie par defaut a True  
        
        
        for i in range(row - taille_vision, row + 1 + taille_vision):
            for j in range(col - taille_vision, col + 1 + taille_vision):
                if not (i>=len(g) or j>=len(g[0]) or i<0 or j<0):
                    g[i][j] = True
                    
        
        #recupere les position de tous les objets que l'on ne veut pas ramasser
        pas_flammes = []
        for i_objet in items_types:
            if items_types[i_objet]!=objet_prefere:
                pas_flammes += items_placed[i_objet]
        
        for y,x in itemStates(pas_flammes):      # on met False quand un item
            g[y][x]=False
                    
        
        for i in range(nbLignes):                   # on exclut aussi les bordures du plateau
            g[0][i]=False
            g[1][i]=False
            g[nbLignes-1][i]=False
            g[nbLignes-2][i]=False
            g[i][0]=False
            g[i][1]=False
            g[i][nbLignes-1]=False
            g[i][nbLignes-2]=False
        
        flammes = itemStates(items_placed[i_prefere])
        
        path_min = []
        f_max = "rien"
        len_path_min = 1000000
        for y,x in flammes:
            f = y,x
            if g[y][x]:
                p = ProblemeGrid2D((row,col),f,g,'manhattan')
                path = probleme.astar(p,verbose=False)
                if len(path)<len_path_min:
                    f_max = f
                    path_min = path
                    len_path_min = len(path)
                    
        if len(path_min)>1:
            next_pos = path_min[1]

            deplacement_focused(joueur_actuel, (row, col), next_pos, i_prefere)
            ramassage(joueur_actuel)
        
        else:
            strat_aleatoire(joueur_actuel)

    
    def strategie_focused_flammes(joueur_actuel) :
        return strat_focused(joueur_actuel, 0)

    def strategie_focused_potions(joueur_actuel) :
        return strat_focused(joueur_actuel, 1)

    def strategie_focused_citrouilles(joueur_actuel) :
        return strat_focused(joueur_actuel, 2)

        
    def coup_majoritaire(liste_coups):
        nombres_coups = [0,0,0]
        for c in liste_coups:
            nombres_coups[c] += 1
        return nombres_coups.index(max(nombres_coups))
    
    
    def strat_majorite(joueur_actuel): #cherche l'objet qui correspond au contre du coup le plus joué par l'adversaire
        if adversaire_est_visible(joueur_actuel):
            chifoumi(joueur_actuel)
            return
        
        joueur_adverse = (joueur_actuel+1)%2
        
        if listes_coups[joueur_adverse]==[]: #aleatoire si l'adversaire n'a pas joué de coups
            strat_aleatoire(joueur_actuel)
        else:
            strat_focused(joueur_actuel, ( coup_majoritaire( listes_coups[joueur_adverse] ) +1)%3)
            
            
    def strat_majorite_alter(joueur_actuel): #cherche l'objet qui correspond au contre du coup le plus joué par l'adversaire
        joueur_adverse = (joueur_actuel+1)%2
        coups_pris_en_compte = listes_coups[joueur_adverse][last_defaite[joueur_adverse]:]
    
    
        if adversaire_est_visible(joueur_actuel):
            chifoumi(joueur_actuel)
            return
        
        joueur_adverse = (joueur_actuel+1)%2
        coups_pris_en_compte = listes_coups[joueur_adverse][declench_chifoumi[joueur_adverse]:]
        
        if coups_pris_en_compte==[]:
            strat_majorite(joueur_actuel)
        else:
            strat_focused(joueur_actuel, ( coup_majoritaire( coups_pris_en_compte ) +1)%3)
            
    
    def strat_specialisation(joueur_actuel): #cherche l'objet le plus présent dans son sac
        """
        if picked_items[joueur_actuel]==[0,0,0]:
            strat_aleatoire(joueur_actuel)
            return
        """
        sac = np.array(picked_items[joueur_actuel])
        max_sac = np.max(sac)
        i_objets_max = np.where(sac==max_sac)[0]
        i_objet_choix = i_objets_max[random.randint(0,len(i_objets_max)-1)]
        strat_focused(joueur_actuel, i_objet_choix)
        
    
    
    def adversaire_est_visible(joueur_actuel):
        row, col = posPlayers[joueur_actuel]
        
        joueur_adverse = (joueur_actuel + 1)%2
        row_adv, col_adv = posPlayers[joueur_adverse]
        
        for i in range(row - taille_vision, row + 1 + taille_vision):
            for j in range(col - taille_vision, col + 1 + taille_vision):
                if i==row_adv and j==col_adv:
                    return True
                
        return False
    
    
    
    def tirage_aleatoire(sac):
        if sum(sac)==0:
            sac=[1,1,1]
        somme_totale = sum(sac)
        n = random.randint(0, somme_totale - 1)
        somme = 0
        for i in range(len(sac)):
            somme += sac[i]
            if n<somme:
                return i
        return i
        
        
    def Chifoumi_regret(joueur_actuel) :
        global chifoumi_effectue
        chifoumi_effectue = True
        declench_chifoumi[joueur_actuel] += 1
        
        sac0 = picked_items[0].copy()
        sac1 = picked_items[1].copy()
        coup0 = tirage_aleatoire(sac0)
        coup1 = tirage_aleatoire(sac1)
        listes_coups[0].append(coup0)
        listes_coups[1].append(coup1)
        
        iteration_chifoumi = len(listes_coups[0])
        
        if coup0==(coup1+1)%3:
            scores[0] += 1
            scores[1] += -1
            picked_items[1] = [0,0,0]
            last_defaite[1] = iteration_chifoumi
            res = 0 #victoire de joueur0
        
        elif (coup0+1)%3==coup1:
            scores[0] += -1
            scores[1] += 1
            picked_items[0] = [0,0,0]
            last_defaite[0] = iteration_chifoumi
            res = 1 #victoire de joueur1
        else:
            res = -1 #match nul
        
        return picked_items, res
    
       
    def chifoumi(joueur_actuel):
        global chifoumi_effectue
        chifoumi_effectue = True
        declench_chifoumi[joueur_actuel] += 1
        
        sac0 = picked_items[0].copy()
        sac1 = picked_items[1].copy()
        
        coup0 = tirage_aleatoire(sac0)
        coup1 = tirage_aleatoire(sac1)
        
        print(f"Coups  : joueur0={coup0}, joueur1={coup1}")
        
        listes_coups[0].append(coup0)
        listes_coups[1].append(coup1)
        
        iteration_chifoumi = len(listes_coups[0])
        
        if coup0==(coup1+1)%3:
            scores[0] += 1
            scores[1] += -1
            picked_items[1] = [0,0,0]
            last_defaite[1] = iteration_chifoumi
            print("JOUEUR 0 GAGNANT !")
            res = 0 #victoire de joueur0
        
        elif (coup0+1)%3==coup1:
            scores[0] += -1
            scores[1] += 1
            picked_items[0] = [0,0,0]
            last_defaite[0] = iteration_chifoumi
            print("JOUEUR 1 GAGNANT !")
            res = 1 #victoire de joueur1
        
        else:
            print("MATCH NUL...")
            res = -1 #match nul
        
        return res


    #-------------------------------
    # Initialisation
    #-------------------------------
    iterations = 100 # default
    global taille_vision
    taille_vision = 3
    # on definit les types d'items sur la carte
    items_types = {0:"flamme",1:"potion",2:"pumpkin"}
    i_prefere = random.randint(0,2)
    
    global chifoumi_effectue
    
    scores = [0,0]
    
    picked_items = [[0,0,0],[0,0,0]] # compteur des items de chaque type pour chaque joueur
    
    listes_coups = [[],[]]
    
    declench_chifoumi = [0,0] #compteur des declenchements de chifoumi pour chaque joueur
    
    last_defaite = [-1,-1]
                
    
    for i_partie in range(int(itr)):
        print("------------------------------------------")
        print(f"Début partie {i_partie}")
        
        if len(sys.argv) == 2:
            iterations = int(sys.argv[1])
    
        init()
        
    
        
        #-------------------------------
        # Initialisation partie
        #-------------------------------
        
        nbLignes = game.spriteBuilder.rowsize
        nbCols = game.spriteBuilder.colsize
        assert nbLignes == nbCols # a priori on souhaite un plateau carre
        lMin=2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les objets)
        lMax=nbLignes-2 
        cMin=2
        cMax=nbCols-2
       
        
        players = [o for o in game.layers['joueur']]
        nbPlayers = len(players)
        
        nb_types = len(items_types)
        
        # on localise tous les objets a allouer au hasard
        # sur le layer ramassable
        # ceux deja places, et ceux a placer
        
        items_to_place = [[],[],[]]
        items_to_place[0] = [o for o in game.layers['ramassable'] if zone(0,o.get_rowcol(),False)]
        items_to_place[1] = [o for o in game.layers['ramassable'] if zone(1,o.get_rowcol(),False)]
        items_to_place[2] = [o for o in game.layers['ramassable'] if zone(2,o.get_rowcol(),False)]
    
        items_placed = [[],[],[]]
        items_placed[0] = [o for o in game.layers['ramassable'] if zone(0,o.get_rowcol(),True)]
        items_placed[1] = [o for o in game.layers['ramassable'] if zone(1,o.get_rowcol(),True)]   
        items_placed[2] = [o for o in game.layers['ramassable'] if zone(2,o.get_rowcol(),True)] 
        nbItems = len(items_to_place[0]+items_to_place[1]+items_to_place[2]),len(items_placed[0]+items_placed[1]+items_placed[2])

            
        #-------------------------------
    
    
        #-------------------------------
        # On place tous les items du bord au hasard
        #-------------------------------
                        
        for k in range(nb_types):                 
            for i in range(0,len(items_to_place[k])): 
                o = items_to_place[k][i]
                (x1,y1) = draw_random_location()
                o.set_rowcol(x1,y1)
                items_placed[k].append(o)
                game.mainiteration()
            
    
        #-------------------------------
        # On place tous les joueurs au hasard
        #-------------------------------
         
        for i in range(0,len(players)): 
            (x1,y1) = draw_random_location()
            players[i].set_rowcol(x1,y1)
            game.mainiteration()
        
        
        
        #-------------------------------
        # Boucle principale de déplacements 
        #-------------------------------
        
        posPlayers = playerStates(players)
        chifoumi_effectue = False
        
            
         
        posPlayers = playerStates(players)
        chifoumi_effectue = False
        
        def perform(strategy):
                if strategy == 'Strat 1':
                    strat_aleatoire(playerss)
                elif strategy == 'Strat 2':
                    strat_focused(playerss,i_prefere)
                elif strategy == 'Strat 3':
                    strat_majorite(playerss)
                elif strategy == 'Strat 4':
                    strat_majorite_alter(playerss)
                elif strategy == 'Strat 5':
                    strat_specialisation(playerss)
                else:
                    return "Error"
            
            
        

        all_items_placed = items_placed[0]+items_placed[1] + items_placed[2]
        for i in range(iterations):
            playerss=2
            if i%2==0:
                playerss=0
                perform(str1)
            else:
                playerss=1
                perform(str2)
              
            game.mainiteration()
      
            if chifoumi_effectue:
                break
        
        
        pygame.quit()
       
    print("------------------------------------------")
    print(f"Sacs   : joueur0={picked_items[0]}, joueur1={picked_items[1]}")
    print(f"Scores : joueur0={scores[0]}, joueur1={scores[1]}")
    print(f"Chifoumis déclenchés : joueur0={declench_chifoumi[0]}, joueur1={declench_chifoumi[1]}")
    if scores[0]==scores[1]:
        if declench_chifoumi[0]==declench_chifoumi[1]:
            gagnant = -1
        elif declench_chifoumi[0]>declench_chifoumi[1]:
            gagnant = 0
        else:
            gagnant = 1
    elif scores[0]>scores[1]:
        gagnant = 0
    else:
        gagnant = 1
        
    if gagnant==0:
        strat_gagnant = str1  
    else: 
        strat_gagnant = str2 
        
    print(f"GAGNANT FINAL : JOUEUR {gagnant} {strat_gagnant}")
    return gagnant
    
    
    
    #-------------------------------
    
        
    
    
   
    


if __name__ == '__main__':


    str1, str2, itr = welcome_frame()

    score0 = 0
    score1 = 0
    nuls=0
    for k in range(1):
        gagnant = main(str1,str2,itr)
        if gagnant==0:
            score0 += 1
        if gagnant==1:
            score1 += 1
        if gagnant==-1:
            nuls += 1
        print(f"ACTUEL score0={score0}, score1={score1}, nuls={nuls}")
    print(f"FINAL score0={score0}, score1={score1}, nuls={nuls}")
    
    pygame.quit()
