# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 22:22:45 2019

@author: Nicolas
"""

#Puissance 4 pour IA
#Aymar Moncorge, Poincheval Alban & Nicolás Pérez 801
#Infos importantes: 
#le tableau est toujours traité dans le sens inverse auquel on le voit, c'est l'intéret de la fonction afficher_le_tableau
#La fonction gagnant ne regarde pas chaque casse, en faite il y a quelques casses où c'est impossible de gagner dans certaines directions
#La fonction gagnant regarde le tableau toujours de gauche vers la droite
#De même pour les fonctions qu'utilise l'IA pour savoir quoi faire

#L'idée de l'IA est que chaque colonne va avoir une valeur spécifique de "Points" positives ou négatives, ces valeurs vont évolué selon l'évolution du jeu, plus une colonne a des pints positives, mieux c'est pour l'IA de jouer là
#C'est l'algorithme du Minimax, l'IA va tester toutes ses possibilités et va choisir la meilleure position pour mettre sa piece.

#Ce code utilise bien l'algorithme du minimax
#On utilise le alpha beta prunning pour faire l'algorithme plus performant.

#Le seul problème retrouvé c'est que l'IA des fois va pas gagner, des fois elle a 3 alignés mais elle préfère mettre la pièce dans une autre part


import numpy as np
import random as rd
#import time 
#import math

Colonnes = 7
Lignes = 6
Longueur_fenêtre = 4

Jeu_Terminé = False
Tour = rd.randint(0,1)  #Alternation de qui commence

Joueur = 0
AI = 1

Piece_J = 1
Piece_IA = 2

Depth = 6   #Cette valeur va définir "L'intelligence" de l'IA, plus elle est élevée, plus elle sera dûr à battre.
            #Valeur limite 6 pour des ordis assez performants, sinon avec 3 ou 4 elle marche assez bien, 5 ou 6 seulement pour des pc assez perfomrants
            #Le nombre de calculs à faire croit exponentiellement, tel que: #Calculs = 7^Depth
            #Avec le alpha prunning le nombre de calcul qu'effectue l'IA est mineur.

def creer_tableau():                    #On crée le tableau
    return np.zeros((Lignes,Colonnes),dtype=int)

def afficher_le_tableau():              #Affiche le tableau dans la bonne direction
    return print(np.flipud(Tableau))    #Ici on tourne inverse le tableau et on l'affiche inversé, pour donner l'impression que les pièces tombent toujours dans la casse la plus base
    
def mettre_une_piece(Tableau, Col, Ligne, piece):    #Permet de mettre la pièce à l'endroit voulut
    Tableau[Ligne][Col] = piece
    
def validation_colonne(Tableau, Col):                #Permet d'éviter mettre des pièces en dehors de la grille
    return Tableau[Lignes-1][Col] == 0
    
def prendre_ligne_suivante(Tableau, Col):            #Crée l'effet de gravité, si la ligne d'en bas est plein, alors il prend la suivante
    for l in range(Lignes):
        if Tableau[l][Col] == 0:
            return l
        
def gagnant(Tableau, piece):
    for l in range(Lignes):     #Regarde chaque ligne si il y a 4 pieces égale alignés
        for c in range(Colonnes-3):
            if Tableau[l][c] == piece and Tableau[l][c+1] == piece and Tableau[l][c+2] == piece and Tableau[l][c+3] == piece:
                return True
                
    for l in range(Lignes-3):       #Regarde chaque colonne si il y a 4 pieces égale alignés
        for c in range(Colonnes):
            if Tableau[l][c] == piece and Tableau[l+1][c] == piece and Tableau[l+2][c] == piece and Tableau[l+3][c] == piece:
                return True 
                
    for l in range(Lignes-3):       #Regarde en diagonale croissante ver la droite si il y a 4 pieces égale alignés
        for c in range(Colonnes-3):
            if Tableau[l][c] == piece and Tableau[l+1][c+1] == piece and Tableau[l+2][c+2] == piece and Tableau[l+3][c+3] == piece:
                return True
                
    for l in range(3, Lignes):      #Regarde en diagonale décroissante ver la droite si il y a 4 pieces égale alignés
        for c in range(Colonnes-3):
            if Tableau[l][c] == piece and Tableau[l-1][c+1] == piece and Tableau[l-2][c+2] == piece and Tableau[l-3][c+3] == piece:
                return True        

def Evaluer_la_fenêtre(Fenêtre,Piece):  #Cette partie va évaluer les valeurs des points pour l'IA
    Points = 0
    
    Piece_Adversaire = Piece_J
    if Piece == Piece_Adversaire:
        Piece_Adversaire = Piece_IA
    
    if Fenêtre.count(Piece) == 4:
        Points += 1000
    elif Fenêtre.count(Piece) == 3 and Fenêtre.count(0) == 1:
        Points += 5
    elif Fenêtre.count(Piece) == 2 and Fenêtre.count(0) == 2:
        Points += 2
        

    if Fenêtre.count(Piece_Adversaire) == 3 and Fenêtre.count(0) == 1:
        Points -= 4

    return Points

def Points_Positions(Tableau, Piece):
    Points = 0

    #Attribution des points de la colonne du milieu
    Formation_Centre = [int(i) for i in list(Tableau[:,Colonnes//2])]
    Points_Centre = Formation_Centre.count(Piece)
    Points += Points_Centre*3
    
    #Attribution des points selon les lignes
    for l in range(Lignes):
        Formation_lignes = [int(i) for i in list(Tableau[l,:])]   #On crée une liste avec les valeurs de chaque ligne
        for c in range(Colonnes-3):
            Fenêtre = Formation_lignes[c:c+Longueur_fenêtre]    #On crée une "Fenetre" de taille 4 où l'IA va regarder combien de pieces propres elle a dans la ligne
            Points += Evaluer_la_fenêtre(Fenêtre,Piece)
                
    #Attribution des points selon les colonnes
    for c in range(Colonnes):
        Formation_colonnes = [int(i) for i in list(Tableau[:,c])]
        for l in range(Lignes-3):
            Fenêtre = Formation_colonnes[l:l+Longueur_fenêtre]  #On crée une "Fenetre" de taille 4 où l'IA va regarder combien de pieces propres elle a dans la colonne
            Points += Evaluer_la_fenêtre(Fenêtre,Piece)

    #Attribution des points selon les diagonales du bas vers le haut
    for l in range(Lignes-3):
        for c in range(Colonnes-3):
            Fenêtre = [Tableau[l+i][c+i] for i in range(Longueur_fenêtre)]
            Points += Evaluer_la_fenêtre(Fenêtre,Piece)

    #Attribution des points selon les diagonales du haut vers le bas
    for l in range(Lignes-3):
        for c in range(Colonnes-3):
            Fenêtre = [Tableau[l+3-i][c+i] for i in range(Longueur_fenêtre)]
            Points += Evaluer_la_fenêtre(Fenêtre,Piece)

    return Points

#Algorithme Minimax (Le pseudocode est sur wikipedia)
def Terminal_node(Tableau):
    return gagnant(Tableau, Piece_J) or gagnant(Tableau,Piece_IA) or len(Obtenir_possibles_locations(Tableau)) == 0
    
def minimax(Tableau, depth, alpha, beta, maximizingPlayer):
    Lieux_vides = Obtenir_possibles_locations(Tableau)
    is_terminal = Terminal_node(Tableau)
    if depth == 0 or is_terminal:
        if is_terminal:
            if gagnant(Tableau, Piece_IA):
                return (None, 10000000000000)
            elif gagnant(Tableau, Piece_J):
                return (None, -10000000000000)
            else:   #Cela correspond aux jeux finis avec toutes las casses pleines
                return(None, 0)
        else: #Depth = 0
            return (None, Points_Positions(Tableau, Piece_IA))
    if maximizingPlayer:
        value = float("-inf")
        Colonne = rd.choice(Lieux_vides)
        for Col in Lieux_vides:
            Ligne = prendre_ligne_suivante(Tableau, Col)
            T_copy = Tableau.copy()
            mettre_une_piece(T_copy, Col,Ligne, Piece_IA)
            Nouveaux_points = minimax(T_copy, depth-1, alpha, beta, False)[1]
            if Nouveaux_points > value:
                value = Nouveaux_points
                Colonne = Col
            alpha = max(alpha,value)
            if alpha >= beta:       #Cette partie correspond à l'alpha prunning, il y a des branches que l'IA n'est pas suceptible de prendre
                break
        return (Colonne,value)
    
    else: #Minimazing player
        value = float("inf")
        Colonne = rd.choice(Lieux_vides)
        for Col in Lieux_vides:
            Ligne = prendre_ligne_suivante(Tableau ,Col)
            T_copy = Tableau.copy()
            mettre_une_piece(T_copy, Col, Ligne, Piece_J)
            Nouveaux_points = minimax(T_copy, depth-1, alpha, beta, True)[1]
            if Nouveaux_points < value:
                value = Nouveaux_points
                Colonne = Col
            beta = min(beta,value)
            if alpha >= beta:
                break
        return (Colonne,value)

def Obtenir_possibles_locations(Tableau):
    Possibles = []
    for Col in range(Colonnes):
        if validation_colonne(Tableau, Col):
            Possibles.append(Col)
    return Possibles

def Choisir_Mouvement(Tableau, Piece):
    Possibles_locations = Obtenir_possibles_locations(Tableau)  #On obtient toutes les possibilités de jeu
    Max_Points = -10000  
    Meilleure_col = rd.choice(Possibles_locations)
    for Col in Possibles_locations:     #On teste toutes les possibilités pour l'IA
        Ligne = prendre_ligne_suivante(Tableau, Col)
        Temp_Tableau = Tableau.copy()   #On crée un deuxième tableau pour tester les différentes jeux de l'IA
        mettre_une_piece(Temp_Tableau,Col,Ligne,Piece)
        Points = Points_Positions(Temp_Tableau, Piece)
        if Points > Max_Points:
            Max_Points = Points
            Meilleure_col = Col

    return Meilleure_col
   
   
Tableau = creer_tableau()
afficher_le_tableau()


while not Jeu_Terminé:
    
    #Faut voir les entrées du joueur 1
    if Tour == Joueur:
        Col = int(input("Choisit la colonne à mettre la pièce (0-6) "))
        
        if validation_colonne(Tableau, Col):
            Ligne = prendre_ligne_suivante(Tableau, Col)
            mettre_une_piece(Tableau,Col,Ligne,Piece_J)
            if gagnant(Tableau, Piece_J):
                print("Félicitations, le joueur 1 a gagné")
                Jeu_Terminé = True

    
    #Faut voir les entrées du joueur 2
    else:
        #Col = int(input("Choisit la colonne à mettre la pièce (0-6) "))
        #Col = rd.randint(0,Colonnes-1)   #L'IA choisit une colonne au hassard
        #Col = Choisir_Mouvement(Tableau, Piece_IA)  #L'IA choisit intelligement
        Col, Points_minimax = minimax(Tableau, Depth, float("-inf"), float("inf"), True)     #Plus la valeur du Depth est haute, plus itelligente elle sera
        print ("Le joueur 2 joue")
        #time.sleep(1)   #Évite que l'IA répond trop vite
        
        if validation_colonne(Tableau, Col):
            Ligne = prendre_ligne_suivante(Tableau, Col)
            mettre_une_piece(Tableau,Col,Ligne, Piece_IA)
            if gagnant(Tableau, Piece_IA):
                print("Félicitations, le joueur 2 a gagné")
                Jeu_Terminé = True
                
        
    #Changement de tour entre le joueur 1 et 2    
    Tour += 1
    Tour = Tour % 2
    afficher_le_tableau()
