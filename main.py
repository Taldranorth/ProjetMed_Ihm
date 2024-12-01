import tkinter
import random
import sys
import os

import functions.data as data
import functions.interface as interface
import functions.gameclass as gameclass
import functions.affichage as affichage
import functions.moveview as moveview
import functions.genproc as genproc
import functions.ailord as ailord

from time import time

#Doit terminé de faire un Prototype:
# - Ajouter Un moyen de déplacer la vue √
#	--> Doit modifier afin de prendre en compte le non focus sur le widget du canvas
#		--> Doit appliquer le bind des touches à la root
#		--> Doit trouver un moyen de stocker les objets dans une données facilement accesible
#			--> Un dico ?
#			--> Place les bases du stockage de données
#	--> Doit modifier afin d'accèlerer le déplacement avec le maintient de la touche

# !!! Attention pour une grande carte cela ram !!!
# C'est l'affichage de plein de case qui cause la ram, voir si c'est le cache ou l'affichage

# Fait un teste avec le Moniteur d'activité lancer à coté
# L'utilisation de la ram est plutôt équilibrer, entre 130-160mo
# Quand on déplace la vue sur une zone de la carte remplie le proc est utiliser à 70%

# Trop d'appel à la fonction ? X
# J'ai tester avec une valeur incrémenter à chaque fois que la fonction motion est appelé, l'appel à la fonction est relativement léger
# pour une carte de 250*250 on y fait appel que 16* pour aller d'un bout à l'autre de la map

# The canvas has known performance problems when you create lots of canvas items, even if you delete the canvas items.
# Canvas item ids are not recycled, so the list of item ids that the canvas must maintain grows without bounds and makes the canvas slower on each iteration.
#	--> Définir des marges d'id pour les différents objets du canvas
#

# Objectif:
#	Correctif:
#	- Faire la doc de ce qui a était fait
#	- Réduire le lag lors de l'observation d'un grand groupe de cases
#		--> Utilisation du processeurs importante
#			--> Problème uniquement présent sur mac
#
#	- Refactoriser le Code
#		--> Le Nettoyer
#		--> Retirer les Commentaires Inutiles
#
#	- !!! Voir pour ajouter la taille de la texture resize à l'atlas !!!
#	- Prendre en compte linux dans la fonction moveviewz
#
#	Additif:
#	- Landforme
#	- Ajouter du Son
#		--> https://stackoverflow.com/questions/28795859/how-can-i-play-a-sound-when-a-tkinter-button-is-pushed
#
#	- Ajouter de l'animation
#		--> https://stackoverflow.com/questions/53418926/button-motion-animation-in-tkinter
#			--> Semble très gourmand
#				--> Trouver une solution plus performante
#
#	- Changer tout les EXIT pour ajouter une fenêtre de confirmation
#		--> Rappel de la dernière sauvegarde si >1 minute
#
#	Partie Graphique:
#
#	- Centrer la fenêtre du Menu principale
#		--> Ajouter un Fond d'écran un peu joli
#			--> Ajouter un Peu d'anim
#
#	- Changer la police d'écriture
#		--> font = "Police"
#
#	- Changer la souris
#		--> root.config(cursor="") 
#		--> https://stackoverflow.com/questions/66203294/how-to-add-custom-image-to-cursor-when-hovered-over-python-tkinter-window
# !!!!!!
# Faire des fonctions de recherche optimiser
#		--> Cela devrait permettre de réduire l'utilisation de la mémoire
# !!!!!!


######################### Normes #########################
# https://peps.python.org/pep-0008/#package-and-module-names
#	Nom de Variable:
#
#
#	Nom de Class:
#	- CapWords convention
#
#	Method Names and Instance Variables	
#	- lowercase with words separated by underscores as necessary to improve readability
#	- Use one leading underscore only for non-public methods and instance variables
#	Ex: Pour une Class nomer Outer -> self.outer_instance
#
#########################################################


##############################\ !! Objectif Important !!\###########################
#	1°)
#	- Refactorier le Code pour utiliser les normes
#	- Faire Schéma Classes
#	- Faire système de Jeu
#		--> Tour de Jeu
#		--> Condition Défaite/Victoire
#		--> Event/prise de villages
#
#	2°)
#	- Faire système de Sauvegarde/Chargement
####################################################################################

##################\ Doit Faire: \#######################
# Main:
# - Déplacement en mettant la souris sur la bordure extérieur de la carte
# - Améliorer le Zoom/Dezoom
# - Normaliser les Tags
#
# Interface:
# - ajouter la création de pop à buildvillage
# - définir les régles de création de village, création d'église
# - Améliorer l'interface
# - Suprimmer le carrer du village ou l'église a était construite
# - Léger décalage sur la droite lorsque l'on centre la vue
#
# GameClass:
# 	- définir les particularités des prêtre
#
# affichage:
#	- Régler les labels des noms
#		--> Actuellement ils ont tendance à ce couper quand ils sont trop long
#
# Data:
#	- Sauvegarde des données
#	- Faire Résolution Dynamique
#	- Faire Placement Fenêtre Dynamique
#
# Moveview: 
#	- Implémenter une limite sur le déplacement de la vue pour ne pas aller plus loin que nécessaires
#
# Interface:
# - Recalculer toute les positions d'interfaces
#		--> Rentre dans la partie résolution dynamique
# - améliorer interface
# - Ajouter la prise de village et le combat d'armée à l'interface de déplacement d'armée
#	--> Si souris sur armée ennemie alors affiche icône Combat
#	--> Si souris sur village Ennemies alors affiche icône Pillage

#########################################################


# Il y a 2 décalage possible:
#	- c'elle causer par moveviewxy
#		--> décalage de l'affichage sur le canvas
#			--> Réglable par l'utilisation des coord du point d'origine de la map_canvas
#	- c'elle causer par moveviewmouse
#		--> décalage du canvas sur la fenêtre
#			--> Je ne sais pas, je ne vois pas comment la régler

# Décider d'adapter moveviewxy pour utiliser scan_dragto
#	--> Plus performant car liés à l'afichage des coord et non le changement des coord de tout les objets du canvas comme move()

# -> Fix Build Church
#	--> test en permanence si on est dans l'état build
#		--> Aucun retour quand on construit une église
# -> Terminer StateMovearmy
# 	--> Permettre l'attaque d'un village √
#		--> Afficher une Icône quand on à la souris dessus
#	--> Permettre l'attaque d'une armée
#		--> Afficher une Icône quand on à la souris dessus
# -> Revoir la destruction de village
# -> Refactoriser le code pour réduire la réutilisation de même code pour a la place utilisr une fonction commune liée a l'objet utiliser
#	--> Voir la récupération de village selon la position x,y via Classmap
# -> Refactorisation de tout les calculs de Coordonnées pour utiliser les fonctions Commune
# -> Peut être utiliser Bezier pour l'affichage du Pathfinding
# -> Doit tester la prise de Village
# -> Doit tester l'attaque d'armée Adverse
# -> Fix la possetion de multiple armé
#	-->Faire poper aux alentour de la ville la nouvelle armée si la case de la ville est déjà occupé par une armée
# -> Ajouter Bouton Pour annuler Si on déplace une armée mais que l'on veut annuler son déplacement au tour prochain
# -> Rework Interface avec Grid
#	--> Recruit Army √
#	--> Build Church √
#	--> Tax √
#	--> GlobalViewMenu √
#	--> War √
#	--> Interface_Army
#	--> Interface Village √

#####
# - Améliorer le calcul pour récuperer le village dans prises de village
#		--> Cela met en avant un problème global de coord :/
# - Gérer le Déplacement nécessaire

# - Fix la création d'armée pour le nom est la position

# - Changer la gestion de la population d'un village pour un dico qui vient contenir pour le role la pop
# - Mettre en place fin de tour pour les Villages Indépendants

# - La trajectoire d'une armée doit s'afficher quand on clique dessus
# - Fix le clique de la trajectoire qui est bloquer par l'affichage du Pathfinding

# - Fix différence click droit Mac/Linux
# - Besoin d'un Retour utilisateur Quand Action Impossible

# - Réaction au Bonheur
# - Naissance de la Population
#####

####
# - Mettre en Place le Combat entre 2 armée
# - Fix movetakevillage qui ne récupère pas à tout les coup le village voulu
# - Retravailler Interface Village
# - Retravailler Menu Jouer
#	--> Doit Utiliser Grid
#	--> Doit permettre de Définir les Villages Indépendants
#	--> Doit Afficher sur la minimap les villages de départs
# - Graphe de Fin de Partie
# 	--> Comment stocker les données des  différentes étapes ?
#		--> Une liste qui contient en 0 le tour 0 avec les données des différents Seigneur ?
#	--> Quoi stocker qui soit suffisament pertinent ?
#		--> Ne pas stocker des données qui soit calculable


# - Fix la Construction d'église qui tente d'entrée dans l'interface de Village
#		--> Après c'est une erreur Inoffensif

# - Refactoriser le Code
# - Réorganiser le projet
#		--> Déplacer les fonctions de Menu dans le fichier interface_menu.py


# - Mettre en place un level Log Erreur
# - LVL 0: On affiche seulement les critique dans la Console
# - LVL 1: On affiche les critiques et les important dans la Console
# - LVL 2: On affiche tout dans la Console

# - Changer la tax des IA pour être plus précise
# 	--> Si il manque des Ressource alors va chercher des Ressources
#	--> Si il manque des Écus alors va chercher des écus

# - Au niveau Économique séparé la valeur des Ressource et des Écus

# - Rendre aléatoire le placement des villages par l'Ia
#	--> Pré-Remplir une liste de coord entre [0-5] ou il va tirer aléatoirement ?


# - Implémenter les Différents type de Comportement pour l'IA

# - Ajouter une Condition qui vérifie qu'une armée ne soit pas déjà présente sur la case

# - Gérer les armées ennemies quand le Seigneur n'est plus là
#	--> Ont les Supprimer ou ont les ajoute à la liste des Armées Bandit ?

# - Ajouter Seigneur "Wild" qui vient gérer toute les Villages, armées Indépendantes


# - Actuellement cela bloque dans takevillage
# - Changer les Interfaces Pour qu'elle n'utilise plus la texture de "base"

# - Pour l'instant Les Seigneurs IA ne peuvent vassaliser le Joueur
# - Ajouter une Gestion des Couleurs plus pousé aux différents Seigneurs

#####

######## Fonctionnalité Principale à Implémenter
# - Implémenter Event
# - Capacité Prêtre
# - Implémenter Résolutions Dynamique
# - Implémenter les Réactions
########


######## Fonctionnalité Majeur Secondaire
# - Implémenter Sauvegarde et Chargement de Données
# - Implémenter Options
# - Implémenter marché
# - Implémenter Landforme
# - Gestion de la population par case
# - Pousser le Calcule de la Menace
# - Pousser le Combat entre les Armées
########

######## Fonctionnalité Secondaire
# - Faire petite animations qui montre le gain et la perte de Ressource
# - Système de Pop-up d'événement en début de tour En bas à droite Comme Armée qui termine son déplacement ou village qui termine de se construire voir Civ
# - Affiné la prise de Village pour prendre en compte le PIllage de ressource et la mort de Villageois
# - Affiné le Combat entre 2 armée pour prendre en compte l'enfermement du Chevalier Ennemie
# - Implémenter Système de Tooltip (affichage d'info-Bulle)
# - Implémenter à la révolte des villages la révoltes de l'armée locale si le bonheur est mauvais
# - Implémenter la création de Bandit
# - Changer interface entête pour afficher icône boufe et money
# - Implémenter une interface plus pousser d'attaque de village
# - Implémenter une interface plus pousser d'attaque d'armée
# - Ajouter les Entrelac
# - Améliorer le réaffichage d'une bordure
########

#### Landforme ####
# --> Utiliser Octaves Pour générer groupe de Terrain
# --> Repasser un coup de Noise map dans le groupe de Terrain qui vient définir les tuiles
#
#



######################### Menu Principale #########################

def mainmenu(gamedata, classmap, option, root):
	# Création de la fenêtre
	mainmenuwin = tkinter.Toplevel(root, height = option.heightWindow, width = option.widthWindow)
	# On centre la fenêtre
	# Pourquoi ?
	gamedata.log.printinfo(f"{option.heightWindow}x{option.widthWindow}+{option.heightWindow//8}+{option.widthWindow//8}")
	mainmenuwin.geometry(f"+{option.widthWindow//2}+{option.heightWindow//4}")


	# Création de la frame
	fmainm = tkinter.Frame(mainmenuwin, height = option.heightWindow, width = option.widthWindow)
	fmainm.pack(expand="True", fill="both")

	# Mise en Place des Menus

	# Button Play
	# !!! A CORRIGER !!!
	Button_mainm_Play = tkinter.Button(fmainm, command = lambda : playmenu(mainmenuwin, gamedata, classmap, option, root), text = "Jouer")

	# Button Quickplay
	# !!! A CORRIGER !!!
	Button_mainm_QuickPlay = tkinter.Button(fmainm, command = lambda: initgame(mainmenuwin, gamedata, classmap, option, root), text = "Partie Rapide")

	# Button Load
	Button_mainm_load = tkinter.Button(fmainm, text = "Load")

	#Button Options
	Button_mainm_option = tkinter.Button(fmainm, text = "Options")

	#Button Exit
	Button_mainm_exit = tkinter.Button(fmainm, command = exit, text = "Quitter")

	#Pack des Button
	Button_mainm_Play.pack()
	Button_mainm_QuickPlay.pack()
	Button_mainm_load.pack()
	Button_mainm_option.pack()
	Button_mainm_exit.pack()


###########################################################################

######################### Menu Jouer #########################

####
# Menu pour créer une nouvelle game 
#
#
#### Terminer ####
# Terminer entryseed en intégrant un Validate qui vérifie que la seed soit un int est change la variable gamedata.seed
#
#
##################

def playmenu(mainmenuwin, gamedata, classmap, option, root):


	# On suprime le frame du menu principale
	mainmenuwin.winfo_children()[0].destroy()
	# On Créer un nouveau frame
	fplaymenu = tkinter.Frame(mainmenuwin, height = option.heightWindow, width = option.widthWindow)
	fplaymenu.pack(expand="True", fill="both")
	mainmenuwin.geometry(f"+{option.widthWindow//3}+{option.heightWindow//5}")

	# Frame dans lequel on va afficher la version réduite de la carte
	canvasframeminimap = tkinter.Frame(fplaymenu, height = option.heightWindow/4, width = option.widthWindow/4)
	canvasframeminimap.pack(side="top")

	# Canvas de la minimap
	mapcanv = tkinter.Canvas(canvasframeminimap)

	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, option.mapx, option.mapy)
	# Fonction qui gen la mini carte
	previewmap(mapcanv, pic, option.mapx, option.mapy)

	# Frame central
	fplaymenu_center = tkinter.Frame(fplaymenu)
	fplaymenu_center.pack()

	# top du centre
	fplaymenu_center_top = tkinter.Frame(fplaymenu_center)
	fplaymenu_center_top.pack()

	#txt variable seed
	tkvar_seed = tkinter.IntVar()
	tkvar_seed.set(gamedata.seed)

	# Button pour générer un nouveau seed ce qui vient update automatiquement la carte
	Button_playmenu_newseed = tkinter.Button(fplaymenu_center_top,command = lambda: regenseed(gamedata, option,tkvar_seed, mapcanv), text = "Genérer nouvelle Seed")
	Button_playmenu_newseed.pack()


	# Entry widget qui affiche la seed, permet de la modif et de la copier
	entryseed = tkinter.Entry(fplaymenu_center_top, textvariable = tkvar_seed)
	entryseed.pack(side = "left")
	button_entryseed = tkinter.Button(fplaymenu_center_top, command = lambda: validate_entry_seed(entryseed, option, gamedata, tkvar_seed, mapcanv), text = "change")
	button_entryseed.pack(side = "left")

	# Milieu du centre
	fplaymenu_center_center = tkinter.Frame(fplaymenu_center)
	fplaymenu_center_center.pack()

	#txt variable mapx mapy
	tkvar_mapx = tkinter.IntVar()
	tkvar_mapx.set(option.mapx)
	tkvar_mapy = tkinter.IntVar()
	tkvar_mapy.set(option.mapy)


	# Label
	tkinter.Label(fplaymenu_center_center, text = "largeur: ").pack(side = "left")
	# Entry widget qui affiche la taille en x et y 
	entrymapx = tkinter.Entry(fplaymenu_center_center, textvariable = tkvar_mapx)
	entrymapx.pack(side = "left")
	tkinter.Label(fplaymenu_center_center, text = "hauteur: ").pack(side = "left")
	entrymapy = tkinter.Entry(fplaymenu_center_center, textvariable = tkvar_mapy)
	entrymapy.pack(side = "left")
	button_entrymap = tkinter.Button(fplaymenu_center_center, command = lambda: validate_entry_map(entrymapx, entrymapy, option, gamedata, tkvar_mapx, tkvar_mapy, mapcanv), text = "change")
	button_entrymap.pack(side = "left")

	# bottom du centre
	fplaymenu_center_bottom = tkinter.Frame(fplaymenu_center)
	fplaymenu_center_bottom.pack(side = "bottom")
	# On affiche la liste des seigneurs actuellement créer
	tkinter.Label(fplaymenu_center_bottom, text = "liste des Seigneur: ").pack(side ="top")
	fplaymenu_center_bottom_listlord = tkinter.Frame(fplaymenu_center_bottom)
	fplaymenu_center_bottom_listlord.pack()

	#txt variable nom joueur
	tkvar_playername = tkinter.StringVar()
	tkvar_playername.set(gamedata.list_lord[gamedata.playerid].lordname)

	for lord in gamedata.list_lord:
		# Si c'est le joueur on met affiche un label Player est on met en place un Entry afin de pouvoir modifier le nom du Seigneur
		if lord.player == True:
			fplaymenu_center_bottom_listlord_player = tkinter.Frame(fplaymenu_center_bottom_listlord)
			fplaymenu_center_bottom_listlord_player.pack(side = "top")
			tkinter.Label(fplaymenu_center_bottom_listlord_player, text = "Player").pack(side = "left")
			entryplayername = tkinter.Entry(fplaymenu_center_bottom_listlord_player, textvariable = tkvar_playername)
			entryplayername.pack(side = "left")
			tkinter.Button(fplaymenu_center_bottom_listlord_player, text = "change", command = lambda: validate_entry_lordname(gamedata, tkvar_playername)).pack(side = "left")
		else:
			tkinter.Label(fplaymenu_center_bottom_listlord, text = lord.lordname).pack(side = "top")


	fplaymenu_center_bottom_button = tkinter.Frame(fplaymenu_center_bottom)
	fplaymenu_center_bottom_button.pack(side = "bottom")
	# On affiche un bouton pour en créer un nouveau
	button_newlord = tkinter.Button(fplaymenu_center_bottom_button, text = "Créer un seigneur", command = lambda: playmenucreatelord(gamedata, fplaymenu_center_bottom_listlord))
	button_newlord.pack(side = "left")
	# On affiche un bouton pour supprimer le dernier
	button_deletelastlord = tkinter.Button(fplaymenu_center_bottom_button, text = "Supprimer le dernier seigneur", command = lambda:playmenudeletelord(gamedata, fplaymenu_center_bottom_listlord))
	button_deletelastlord.pack(side = "left")

	fplaymenu_bottom = tkinter.Frame(fplaymenu)
	fplaymenu_bottom.pack(side = "bottom")
	# Button pour lancer une nouvelle partie
	Button_playmenu_play = tkinter.Button(fplaymenu_bottom, command = lambda: initgame(mainmenuwin, gamedata, classmap, option, root),text = "Jouer")
	Button_playmenu_play.pack()

	# Boutton pour revenir en arrière
	Button_playmenu_return = tkinter.Button(fplaymenu_bottom, command = lambda: playmenutomainmenu(gamedata, classmap, option, mainmenuwin, root),text = "Retour")
	Button_playmenu_return.pack()

def validate_entry_map(entrymapx, entrymapy, option, gamedata, tkvar_mapx, tkvar_mapy, mapcanv):
	option.mapx = int(entrymapx.get())
	option.mapy = int(entrymapy.get())

	tkvar_mapx.set(option.mapx)
	tkvar_mapy.set(option.mapy)

	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, option.mapx, option.mapy)
	previewmap(mapcanv, pic, option.mapx, option.mapy)


def validate_entry_seed(entryseed, option, gamedata, tkvar_seed, mapcanv):
	####################
	# Fonction pour changer automatiquement la seed stocker dans gamedata, tkvar_seed et la minimap
	####################
	gamedata.seed = float(entryseed.get())
	tkvar_seed.set(gamedata.seed)
	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, option.mapx, option.mapy)
	previewmap(mapcanv, pic, option.mapx, option.mapy)

def validate_entry_lordname(gamedata, tkvar_playername):
	####################
	# Fonction pour changer le nom du seigneur player
	####################
	gamedata.list_lord[gamedata.playerid].lordname = tkvar_playername.get()


def regenseed(gamedata, option, tkvar_seed, mapcanv):
	####################
	# Fonction associer à un bouton pour random la seed et changer la minimap
	####################

	gamedata.seed = random.random()*time()
	tkvar_seed.set(gamedata.seed)
	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, option.mapx, option.mapy)
	previewmap(mapcanv, pic, option.mapx, option.mapy)


def previewmap(mapcanv, pic, mapx, mapy):
	####################
	# Fonction pour afficher une mini version de la map
	# Utilser la version carrer de la map
	####################

	# Si on à déjà afficher une minimap pour un seed différent on efface
	mapcanv.delete("minimap")

	for x in range(mapx):
		for y in range(mapy):
			tl = tuile(pic[x][y])[0]
			mapcanv.create_rectangle((x*2), y*2, (x*2)+2, (y*2)+2, fill=tl, tags = "minimap", outline='black')

	mapcanv.pack(expand = "True",fill="both")

def playmenutomainmenu(gamedata, classmap, option, menu, root):
	mainmenu(gamedata, classmap, option, root)
	menu.destroy()


def playmenucreatelord(gamedata, frame_listlord):
	####################
	# Fonction pour Créer un seigneur dans le menu play
	####################
	gamedata.log.printinfo("On Créer un nouveau Seigneur")
	gamedata.createlord()

	gamedata.log.printinfo("On l'ajoute au frame")
	tkinter.Label(frame_listlord, text = gamedata.list_lord[gamedata.Nb_lord-1].lordname).pack(side = "top")


def playmenudeletelord(gamedata, frame_listlord):
	####################
	# Fonction pour Suprimer un seigneur dans le menu play
	####################
	if gamedata.list_lord[gamedata.Nb_lord-1].player == False:
		gamedata.log.printinfo("On supprime le Dernier Seigneur de la liste")
		gamedata.deletelord(gamedata.Nb_lord-1)
		gamedata.log.printinfo("On le retire du frame")
		# On retire le seigneur de la liste
		frame_listlord.winfo_children()[gamedata.Nb_lord-1].destroy()
		gamedata.Nb_lord -= 1

	else:
		gamedata.log.printerror("Il ne reste plus que le joueur")

###########################################################################




######################### Menu Save/Load #########################

###############
# Fonction appeler pour afficher le menu de chargement des Saves
# On l'affiche par dessus le menu Principale
#
# Ce menu va servir à charger une save parmi la liste proposer
#	- Nom de la save, Nb de tour, nom du seigneur, date de la sauvegarde
#	- 
#	- Tant que l'on aura pas lancer le chargement de la save rien n'est charger en arrière plan
###############

def savemenu():



	pass



def loadmenu():
	# On suprime le frame du menu principale
	mainmenuwin.winfo_children()[0].destroy()




	pass


###########################################################################

######################### Menu Option #########################

###############
# Fonction appeler pour afficher le menu des Options 
# On l'affiche par dessus le menu Principale
#
# Ce menu va servir à configurer les paramètre globaux de l'application ainsi que les touches, voir à afficher les Combinaisons de touches
###############




def optionmenu():
	# On suprime le frame du menu principale
	mainmenuwin.winfo_children()[0].destroy()

	# On créer le nouveaux frame




	pass


###########################################################################


######################### Écran de Fin de Jeu #########################

def eofgamescreen(gamedata, classmap, option):
	###############
	# Fonction appeler pour afficher l'écran de fin de Jeu
	###############
	# 
	#
	#
	###############

	# Frame-Window
	window_eof_screen = tkinter.Frame(classmap.framecanvas)
	window_eof_screen.place(x = (option.widthWindow//20), y = (option.heightWindow//20))

	# Frame Principale
	frame_eof_screen = tkinter.Frame(window_eof_screen)
	frame_eof_screen.grid()

	player = gamedata.list_lord[gamedata.playerid]

	# Titre
	# Victoire OU défaite
	tkinter.Label(frame_eof_screen, text = f"{gamedata.victory} du Seigneur {player.lordname}").grid(row = 0,column = 3)

	# Info de base Principale
	# Nb Tour
	tkinter.Label(frame_eof_screen, text = f"Nombre de tour: {gamedata.Nb_tour}").grid(row = 1, column = 2)
	# Nb Vassaux possèder
	tkinter.Label(frame_eof_screen, text = f"Nombre de Vassaux: {len(player.vassal)}").grid(row = 2, column = 2)
	# Puissance Militaire
	tkinter.Label(frame_eof_screen, text = f"Puissance Militaire: {player.power}").grid(row = 3, column = 2)
	# Score
	tkinter.Label(frame_eof_screen, text = f"Score: ").grid(row = 1, column = 4)
	# Nb Village possèder
	tkinter.Label(frame_eof_screen, text = f"Nombre de Village: {len(player.fief)}").grid(row = 2, column = 4)
	# Nb Pop
	# On recup la taille totale
	nb_total= 0
	for village in player.fief:
		nb_total += len(village.population)
	tkinter.Label(frame_eof_screen, text = f"Taille de la Population: {nb_total}").grid(row = 3, column = 4)


	# Boutton pour Changer pour un Graphique
	# Graphe Croissance Militaire
	button_military_graph = tkinter.Button(frame_eof_screen ,text = "Croissance Militaire").grid(row = 4, column = 1)

	# Graphe Croissance Démographique
	button_demography_graph = tkinter.Button(frame_eof_screen ,text = "Croissance Démographique").grid(row = 4, column = 2)

	# Graphe Croissance économique
	button_economy_graph = tkinter.Button(frame_eof_screen ,text = "Croissance Économique").grid(row = 4, column = 3)

	# Graphe Score
	button_score_graph = tkinter.Button(frame_eof_screen ,text = "Score").grid(row = 4, column = 4)

	# Graphe des Mort
	button_death_graph = tkinter.Button(frame_eof_screen ,text = "Mort").grid(row = 4, column = 5)

	# Boutton pour retourner sur le Menu Principale
	button_return_mainmenu = tkinter.Button(frame_eof_screen ,text = "Menu Principale").grid(row = 5, column = 1, columnspan = 2)

	# Boutton pour charger une Save précédente
	button_loadsave = tkinter.Button(frame_eof_screen ,text = "Charger une Sauvegarde").grid(row = 5, column = 3, columnspan = 2)


###########################################################################

######################### Initiation de la partie #########################

##########
#
# Appeler par Quickplay ou Play depuis le Menu Principale
#
# On initialise le Gamedata:
#	Tour 1:
#		- Chaque Seigneur Possède 10 de Ressource et 10 d'argent
#
#
#
# Doit détruire le MenuPrincipale
#
##########



def initgame(mainmenuwin, gamedata, classmap, option, root):


	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, option.mapx, option.mapy)
	# On lance la création de la game
	mainscreen(gamedata, classmap, option, root, pic)

	# Une fois l'initialisation lancé on détruit la fenêtre du menu principale
	mainmenuwin.destroy()

	# On lance la game
	# Actuellement Bloque le process
	gameloop(gamedata, classmap, option, root)
	root.mainloop()


###########################################################################

######################### Écran de Jeu #########################
def mainscreen(gamedata, classmap, option, root, pic):

	# Création de la fenêtre
	win1 = tkinter.Toplevel(root, height = option.heightWindow, width= option.widthWindow)
	gamedata.log.printinfo(f"taille écran x,y: {root.winfo_screenwidth()}, {root.winfo_screenheight()}")
	win1.geometry(f"+{option.widthWindow//8}+{option.heightWindow//4}")
	win1.title("Medieval Game")


	# Frame Map
	fcanvas = tkinter.Frame(win1, height = (option.heightWindow*0.6), width= option.widthWindow)
	gamedata.log.printinfo(f"Taille de la Frame du Canvas: {fcanvas.winfo_width()}, {fcanvas.winfo_height()}")
	classmap.setlframecanvas(fcanvas)

	# Interface de Jeu
	interface.gameinterface(gamedata, classmap, option, win1)

	fcanvas.pack()

	# Carte de Jeu
	createmap(gamedata, classmap, option, pic)


	# Genération des Villages
	genproc.genVillage(gamedata, classmap, option)

	# Affichage des Villages
	affichage.printvillage(gamedata, classmap, option,fcanvas)

	# On rempli les villages de pop
	# En début de Game Chaque Village est composé de 10 Pop:
	#	- 8 Paysan
	#	- 2 Artisan
	for village in classmap.lvillages:
		genproc.genpopidvillage(gamedata, classmap, option, village, 8, 2)

	# On affiche les Bordures des villages:
	affichage.bordervillage(gamedata, classmap, option)



	village = gamedata.list_lord[gamedata.playerid].fief[0]
	coordcanvas = moveview.coordmaptocanvas(gamedata, classmap, option, [village.x, village.y], True)
	# On centre la vue sur le village de départ
	moveview.centerviewcanvas(gamedata, classmap, option, coordcanvas)


	for village in classmap.lvillages:
		infovillage(classmap.listmap[village].village)

	interface.updateinterface(gamedata, classmap)


####################################################################################################

######################### Creation de la Carte Canvas #######################################################
def createmap(gamedata, classmap, option, pic):

	#Si heigthWindow/1.5 le boutton quitter disparait
	mapcanv = tkinter.Canvas(classmap.framecanvas, height = (option.heightWindow*0.6), width= option.widthWindow)
	gamedata.log.printinfo(f"Taille du Canvas:{mapcanv.winfo_width()}, {mapcanv.winfo_height()}")
	# On setup le frame de l'atlas
	gamedata.setlframe(classmap.framecanvas)
	# On lie le mapcanvas à classmap
	classmap.setmapcanv(mapcanv)
	# On Créer les Différentes Cases avec le tags tuile pour indiquer et les trouvé plus facilement
	# On ajoute aussi le tags click pour indiquer qu'ils sont clickables
	# On ajoute aussi les tags x et y qui correspond à la casse ou ils est situés
	# ONn ajoute aussi le tag pic[x][y] qui correspond à la valeur de la case gen
	# 2ieme version: ajouter un tag supplémentaire liées aux types

	idtuile = 0

	sizetuile = gamedata.tuilesize

	# !!!!!!
	# Différence position entre map texture et map carré causer par le fait que la map texture utilise les coordonnées donnés comme point centrale et non point en haut à gauche
	# !!!!!!
	for y in range(option.mapy):
		for x in range(option.mapx):

			# On utilise la valeur de la case pour définir la tuile que l'on va créer
			tl = tuile(pic[x][y])

			# Création de la carte avec Rectangle
			#mapcanv.create_rectangle((x*sizetuile), (y*sizetuile), (x*sizetuile)+sizetuile, (y*sizetuile)+sizetuile, fill = tl[0], tags = ["click","tuile",x,y,pic[x][y], tl[1]], outline='black')
			
			##### Version Non-Aléatoire Dico Avec Atlas #####
			
			if tl[1] == "mountains":
				gamedata.loadtextureatlas("mountains_inner.png", tl[1])
				texture_name = "mountains_inner.png"
			elif tl[1] == "forest":
				gamedata.loadtextureatlas("conifer_forest_inner.png", tl[1])
				texture_name = "conifer_forest_inner.png"
			elif tl[1] == "plains":
				gamedata.loadtextureatlas("plains.png", tl[1])
				texture_name = "plains.png"
			elif tl[1] == "ocean":
				gamedata.loadtextureatlas("ocean_inner.png", tl[1])
				texture_name = "ocean_inner.png"

			mcanvt = mapcanv.create_image((x*sizetuile)+(sizetuile/2), (y*sizetuile)+(sizetuile/2), image = gamedata.atlas[texture_name].image, tags = ["img",tl[1],"tuile","click", x, y, pic[x][y], idtuile])
			
			################################

			"""
			##### Version Aléatoire Dico #####
			texture_name = data.randomtexturefromdico(gamedata.dico_file, tl[1])
			# Si la texture afficher n'est pas une texture compléte est que ce n'est pas un ocean
			if tl[1] != "ocean":
				if texture_name not in ["mountains_inner.png", "conifer_forest_inner.png", "ocean_inner.png", "plains.png"]:
					# On affiche en arrière plans une texture background
					gamedata.loadtextureatlas("plains.png", "plains")
					mapcanv.create_image((x*sizetuile)+(sizetuile/2), (y*sizetuile)+(sizetuile/2), image = gamedata.atlas["plains.png"].image, tags = ["img",tl[1],"tuile","click", x, y, pic[x][y], idtuile])
			
			gamedata.loadtextureatlas(texture_name, tl[1])
			mcanvt = mapcanv.create_image((x*sizetuile)+(sizetuile/2), (y*sizetuile)+(sizetuile/2), image = gamedata.atlas[texture_name].image, tags = ["img",tl[1],"tuile","click", x, y, pic[x][y], idtuile])
			"""
			################################

			# On créer une nouvelle instance de la classe tuiles
			instancetuile = data.Classtuiles(texture_name, tl[1], x, y, mcanvt)
			# On le stocker dans la ClassMap
			#gamedata.list_tuile += [instancetuile]
			classmap.addtuileinlist(instancetuile)
			idtuile += 1

	#On lie Command+molette aux zoom/dézoom
	# Sur Mac/Windows
	mapcanv.bind("<MouseWheel>", lambda event: moveview.moveviewz(event, gamedata, classmap, option))
	# Sur linux
	mapcanv.bind("<Button-4>", lambda event: moveview.moveviewz(event, gamedata, classmap, option))
	mapcanv.bind("<Button-5>", lambda event: moveview.moveviewz(event, gamedata, classmap, option))

	#On focus sur le widget sinon il ne prendra pas en compte les entrées des touches fléchés
	mapcanv.focus_set()

	#On lie les touches fléchés aux déplacement de la vue
	mapcanv.bind('<KeyPress-Left>', lambda event, x=1,y=0: moveview.moveviewxy(event, x, y, gamedata, classmap, option))
	mapcanv.bind("<KeyPress-Right>", lambda event, x=-1,y=0: moveview.moveviewxy(event, x, y, gamedata, classmap, option))
	mapcanv.bind("<KeyPress-Up>", lambda event, x=0,y=1: moveview.moveviewxy(event, x, y, gamedata, classmap, option))
	mapcanv.bind("<KeyPress-Down>", lambda event, x=0,y=-1: moveview.moveviewxy(event, x, y, gamedata, classmap, option))

	#On lie le déplacement de la vue au maintient du bouton droit de la souris + motion
	mapcanv.bind('<Shift-ButtonPress-2>', moveview.startmoveviewmouse)
	mapcanv.bind('<Shift-B2-Motion>', moveview.moveviewmouse)


	#ON lie les différentes Cases à l'action click
	mapcanv.tag_bind("click", "<Button-1>", lambda event: interface.highlightCase(event, gamedata, classmap))

	# on termine par pack le mapcanv
	mapcanv.pack(expand ="True", fill = "y")

####################################################################################################


######################### Fonction Secondaire ############################
def tuile(nb):
	####################
	# 1er Version qui lier la valeur d'une case à une Couleur,
	# 2eme Version doit lier la valeur de la case à un type qui sera caractériser par un Tag:
	#	blue, Ocean
	#	yellow, plain
	#	green, forest
	#	grey, mountain
	####################
	if(nb <= -0.25):
		return ("grey", "mountains")
	elif(nb>-0.25 and nb <=0):
		return ("green", "forest")
	elif(nb>0 and nb <= 0.25):
		return ("yellow", "plains")
	else:
		return ("blue", "ocean")



def typetoimg(type, sizetuile):
	####################
	# Fonction qui va renvoyer une image selon le type envoyer en entré
	# l'image est resize à la taille d'une tuile
	####################

	img = ""

	if type == "mountains":
		img = data.loadtexture("/asset/texture/terrain/mountains/mountains_inner.png", sizetuile)
	elif type == "forest":
		img = data.loadtexture("/asset/texture/terrain/conifer_forest/conifer_forest_inner.png", sizetuile)
	elif type == "plains":
		img = data.loadtexture("/asset/texture/terrain/plains/plains.png", sizetuile)
	elif type == "ocean":
		img = data.loadtexture("/asset/texture/terrain/ocean/ocean_inner.png", sizetuile)
	return img


def typetoimgdico(dico_file, type, sizetuile):
	####################
	# Fonction qui va renvoyer une image selon le type envoyer en entré et le dico
	# l'image est resize à la taille d'une tuile
	####################

	img = ""

	if type == "mountains":
		img = data.loadtexturefromdico(dico_file, "mountains_inner.png", type, sizetuile)[1]
	elif type == "forest":
		img = data.loadtexturefromdico(dico_file, "conifer_forest_inner.png", type, sizetuile)[1]
	elif type == "plains":
		img = data.loadtexturefromdico(dico_file, "plains.png", type, sizetuile)[1]
	elif type == "ocean":
		img = data.loadtexturefromdico(dico_file, "ocean_inner.png", type, sizetuile)[1]
	return img


######################### Fonction Jeu #########################

#################### 
# Ensemble de Fonction qui vont régir un tour de jeu
#	Phase d'un Tour de jeu:
#		- Calcul du gain de Ressource et d'Argent
#		- Calcul Mort/Viellisement de la population
#		- Event
#		-- Début du tour du Joueur
#		- action - Réaction
#		- Fin du tour quand le Joueur clique sur la case fin de tour
#		- Les Vassaux du joueur Joue
#################### 
# fin de tour:
#	- CP = capacité de production >=2
#	- Chaque roturier produit CP ressource
#	- Chaque roturier consomme 1 ressource
#	- Si 1 roturier atteint le plafond de ressource qu'il peut posséder la ressource produite est vendu
#	- Si 1 roturier n'a plus de ressource il achète 1 ressource
#	- Chaque roturier voit son âge augmenté de 1
#	- Si 1 roturier voit son âge atteindre 100 il meurt et c'est ressource/money son transférer au Seigneur du village
#	- Le bonheur augmente 
####################
#Tcl/Tk applications are normally event-driven, meaning that after initialization, the interpreter runs an event loop (i.e. Tk.mainloop()) and responds to events.
#Because it is single-threaded, event handlers must respond quickly, otherwise they will block other events from being processed.
#To avoid this, any long-running computations should not run in an event handler, but are either broken into smaller pieces using timers, or run in another thread.
#This is different from many GUI toolkits where the GUI runs in a completely separate thread from all application code including event handlers.
####################





def gameloop(gamedata, classmap, option, root):
	####################
	#
	#	Le Retour des Sémaphore :)
	#
	#
	####################

	if gamedata.semaphore == False:
		# si on a fait le tour des joueurs
		if gamedata.Nb_toplay == gamedata.Nb_lord:
			endofturn(gamedata, classmap, option)

		# Si c'est au joueurs de jouer
		if gamedata.Nb_toplay == gamedata.playerid:
			# On entre dans la loop du tour du joueur
			playerturn(gamedata, classmap, option)
		# Sinon c'est à un Ia de jouer
		else:
			# On entre dans la loop de l'ia
			notplayerturn(gamedata, classmap, option)

	# On vérifie que la partie n'est pas terminé
	if gamedata.is_finished == False:
		# Si elle ne l'est pas on rapelle cette fonction dans 
		root.after(50, lambda: gameloop(gamedata, classmap, option, root))



def playerturn(gamedata, classmap, option):
	# Si le joueur à appuier sur le bouton fin de tour
	if gamedata.endturn == True:
		gamedata.log.printinfo("Player hit end of turn button")
		# On incrémente le joueur qui doit jouer
		gamedata.Nb_toplay += 1
		# On indique au joueurs que c'est à l'ia de Jouer

# Fonction qui gère l'ia des ennemies
def notplayerturn(gamedata, classmap, option):
	# On affiche la banderole
	gamedata.semaphore = True
	gamedata.log.printinfo(f"tour de: {gamedata.list_lord[gamedata.Nb_toplay].lordname}, {gamedata.Nb_toplay}")
	# L'ia Joue
	ailord.mainai(gamedata, classmap, option)

def endofturn(gamedata, classmap, option):
	gamedata.semaphore = True
	gamedata.log.printinfo("Il ne reste plus de Seigneur qui doit Jouer, Fin du tour")
	#print("lplaines: ",classmap.lplaines)
	gamedata.Nb_toplay = 0
	# On vérifie que l'on ne soit pas en état de mettre fin aux jeu:
	if victoryordefeat(gamedata, classmap, option) == False:
		# On fait appel à la fonction de fin de tour
		gamedata.endofturn(classmap)
		# Une fois que tout les objets se sont update ont update l'interface d'entête
		interface.updateinterface(gamedata, classmap)
		gamedata.endturn = False
		gamedata.semaphore = False
	else:
		endofgame(gamedata, classmap, option)



# after(time, function)

def victoryordefeat(gamedata, classmap, option):
	#######
	# Fonction pour vérifier si le Joueur est en Victoire ou défaite
	#######
	# Return un Bool et modifie une variable dans gamedata

	player = gamedata.list_lord[gamedata.playerid]

	# Si le joueur ne Possède plus de village Alors Défaite
	if len(player.fief) == 0:
		gamedata.victory = "Défaite"
		return True
	# Si le joueur est un vassal d'un autre Seigneurs Alors Défaite
	for lord in gamedata.list_lord:
		if lord != player:
			if player in lord.vassal:
				gamedata.victory = "Défaite"
				return True

	# Sinon si le joueur possède un Nombre de Vassaux = Nombre de Seigneur-1
	# Alors Victoire
	if len(player.vassal) == (gamedata.Nb_lord - 1):
		gamedata.victory = "Victoire"
		return True

	return False


def endofgame(gamedata, classmap, option):
	#####
	# Fonction qui gère la fin de partie
	#####
	eofgamescreen(gamedata, classmap, option)



###########################################################################


######################### Autre Fonction #########################
def infovillage(village):
	print("village name", village.name)
	if village.lord != 0:
		print("village lord: ", village.lord.lordname)
	else:
		print("village lord: ", 0)
	if village.priest != 0:
		print("village priest: ", village.priest.name)
	else:
		print("village priest: ", 0)
	print("village global joy: ", village.global_joy)
	print("village ressource, money: ", village.prod_ressource, village.prod_money)

######################### Main #########################
if __name__ == '__main__':

	#Init de la fenêtre
	root = tkinter.Tk()
	print("Hauteur de l'écran: ", root.winfo_screenheight())
	print("Largeur de l'écran: ", root.winfo_screenwidth())

	# Chargement des Options:
	option_instance = data.ClassOptions()
	# Initialisation de GameData
	gamedata_instance = data.ClassGameData()
	gamedata_instance.log.printinfo("Initialisation log terminé")

	# Initialisation de la Carte
	map_instance = data.Classmap()

	# Menu principale
	mainmenu(gamedata_instance, map_instance, option_instance, root)
	gamedata_instance.log.printinfo("Initialisation de l'application terminé")

	root.mainloop()


