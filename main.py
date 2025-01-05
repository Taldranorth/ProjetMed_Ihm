import os
import sys
import random
import tkinter

import functions.log as log
import functions.data as data
import functions.asset as asset
import functions.cheat as cheat
import functions.ailord as ailord
import functions.genproc as genproc
import functions.moveview as moveview
import functions.gameclass as gameclass
import functions.affichage as affichage
import functions.interfacegame as interfacegame
import functions.interfacemenu as interfacemenu

from time import time

####

# - Mettre en place un level Log Erreur
# - LVL 0: On affiche seulement les critique dans la Console
# - LVL 1: On affiche les critiques et les important dans la Console
# - LVL 2: On affiche tout dans la Console

# - Gérer les armées ennemies quand le Seigneur n'est plus là
#	--> On les Supprimer ou ont les ajoute à la liste des Armées Bandit ?

# - Changer les Interfaces Pour qu'elle n'utilise plus la texture de "base"

# - Pour l'instant Les Seigneurs IA ne peuvent tenter de vassaliser le Joueur

# - Définir comment annuler une action ajouter dans la file d'action
#	--> Si c'est une armée on cherche dans la file toute les actions qui ont pour paramètre l'objet Armée

# - AJouter affichage Victoire ou défaite aux combat d'armée
#	--> Utilisé système de Notification
# - Remplir le Menu Debug

# - Pousser la Gestion de la Menace

# -> Ajouter Bouton Pour annuler Si on déplace une armée mais que l'on veut annuler son déplacement au tour prochain
#	--> Annuler retire l'action en cour dans la pile 1 ou 0

# - Réaction au Bonheur
# --> Si le Bonheur d'un vassaux est trop bas alors il tente une révolte
# --> Si le Bonheur d'une armée est trop basse alors elle se révolte
# --> Ajouter Rebellion Vassaux Contre Seigneur

# - Voir comment gérer de manière efficace le Text Tooltip pour que ce soit dynamique
#	--> Liste qui contient des chaines de caractère avec des appels de variable ?
#		--> Non c'est toujours le même problème, actuellement c'est les valeurs qui sont stocké et non l'adresse mémoire qui est accéder
#			--> Il faut envoyé une variable dynamique et non statique
#				--> Putain python fait chier

# - Mettre en Place Fonctions ListBox qui disparait
#####

#### à Faire:
"""
Implémenter:
 - Améliorer Zoom/Dezoom
 	--> Limité à 1 zoom par action
 - Améliorer Geule de l'Interface
 	--> Utiliser Texture/icone
 	--> Définir des couleur gris/chaud 
 - Implémenter Structure Animation
 - Implémenter Structure Notification
 - Ajouter ToolTipe aux Graphes
 - Implémenter Bezier
 - Ajouter Notification début de tour Croissance des Villages
 - Implémenter Garde fous lors d'ailord main
 - Affichage du Pathfinding en cours des armées
 - Implémenter fonction pour retourner au menu depuis la game

Refactoriser:
 - Améliorer Selection de Village Pour la Construction d'église
 	--> 1 clique pour zoom, 2 clique pour sélectionner
 - Interface de Création de Seigneur
 - Refactoriser le Calcul et l'affichage des Graphes en utilisant Bezier
 - Changer Fonctionnement Event mercenary_army Pour pouvoir afficher le prix de l'armée de mercenaire et sa troupe
 - Refactoriser la gestion des noms

Fix:
 - Fix changement de résolution qui ne prend que la dernière résolution de la liste 
 - Tooltipe Canvas qui peuvent rester après la destruction de leur objets
"""
####

#### Objectif Restant ####
# - Refactorisation Option/classmap et Gamedata pour être défini dans data et accéder à partir d'un appel du fichier
# - Implémenter Réactions Armées et Vassaux
# - Implémenter Comportement de l'IA
# - Terminé Graphe Stat
# - Implémenter ToolTip sur Graphe Stat
# - Trouvé un Moyen de Centré les fenêtre d'interfaces
# - Implémenter Image Event
# - Implémenter Menu Options
# - Implémente Gestion de la population par case
# - Optimiser et Refactoriser
# - Graphe Stats par Bezier
######

######
# -> Ajouter Bouton Pour annuler Si on déplace une armée mais que l'on veut annuler son déplacement au tour prochain
######## Fonctionnalité Principale à Implémenter
# - Implémenter les Différents Comportement de l'IA
# - Refactoriser le Code
########

######## Fonctionnalité Majeur Secondaire
# - Implémenter marché
# - Implémenter Landforme
# - Gestion de la population par case
# - Pousser le Calcul de la Menace
# - Pousser le Combat entre les Armées
# - Refactoriser le Code
########

######## Fonctionnalité Mineur Secondaire
# - Faire petite animations qui montre le gain et la perte de Ressource
# - Système de Pop-up d'événement en début de tour En bas à droite Comme Armée qui termine son déplacement ou village qui termine de se construire voir Civ
# - Affiné la prise de Village pour prendre en compte le PIllage de ressource et la mort de Villageois
# - Affiné le Combat entre 2 armée pour prendre en compte la Capture du Chevalier Ennemie et la mort des Soldats
# - Implémenter à la révolte des villages la révoltes de l'armée locale si le bonheur est mauvais
# - Implémenter la création de Bandit
# - Changer interface entête pour afficher icône boufe et money
# - Implémenter une interface plus pousser d'attaque de village
# - Implémenter une interface plus pousser d'attaque d'armée
# - Refactoriser le Code
########

#### Landforme ####
# --> Utiliser Octaves Pour générer groupe de Terrain
# --> Repasser un coup de Noise map dans le groupe de Terrain qui vient définir les tuiles

######################### Main #########################
if __name__ == '__main__':

	#Init de la fenêtre
	root = tkinter.Tk()

	if (len(sys.argv) >= 2 )and (str(sys.argv[1]) == "-SR"):
		[height, width] = [1400, 1440]
	else:
		[height, width] = [int(1.4*root.winfo_screenheight()),root.winfo_screenwidth()]

	log.log.printinfo(f"Hauteur de l'écran:  {height}")
	log.log.printinfo(f"Largeur de l'écran: {width}")
	log.log.printinfo(f"Plateforme: {sys.platform}")

	# Chargement des Options:
	option_instance = data.ClassOptions(height, width)
	# Initialisation de GameData
	gamedata_instance = data.ClassGameData()
	log.log.printinfo("Initialisation log terminé")

	# Initialisation de la Carte
	map_instance = data.Classmap()

	# Menu principale
	interfacemenu.mainmenu(gamedata_instance, map_instance, option_instance, root)
	log.log.printinfo("Initialisation de l'application terminé")

	root.mainloop()
	
