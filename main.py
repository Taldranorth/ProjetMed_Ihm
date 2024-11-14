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

# Objectif:
#	Correctif:
#	- Faire la doc de ce qui a était fait
#	- Réduire le lag lors de l'observation d'un grand groupe de cases
#		--> Utilisation du processeurs importante
#
#	- Refactoriser le Code
#		--> Le Nettoyer
#		--> Retirer les Commentaires Inutiles
#	- !!!! Commencer a s'entrainer avec les CLasses !!!!
#
#	- !!! Voir pour ajouter la taille de la texture resize à l'atlas !!!
#	- Prendre en compte linux dans la fonction moveviewz
#
#	Additif:
#	- Landforme
#	- Préparer Système de la Boucle Principale
#	- Recup Texture.png des Batiment, Unités, Event, Blason
#		--> Recup Image Event depuis CK 2 ou 3
#	- Ajouter du Son
#		--> https://stackoverflow.com/questions/28795859/how-can-i-play-a-sound-when-a-tkinter-button-is-pushed
#
#	- Ajouter de l'animation
#		--> https://stackoverflow.com/questions/53418926/button-motion-animation-in-tkinter
#			--> Semble très gourmand
#				--> Trouver une solution plus performante
#
#	- Doit changer la carte pour remplacer l'utilisation des tags par des classes pour la tuile
#		--> Doit changer tout ce qui utiliser les tags
#		--> Vérifier le cout en perf et garder l'ancien système dans un coin au cas ou
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
# - réglé le décalage entre les state et la carte √
# - Déplacement en mettant la souris sur la bordure extérieur de la carte
# - Pouvoir renommer le Seigneur Joueur √
#	--> Remplacer par un Entry √
# - ajouter dans les options quickplay 3 Seigneurs √
# - Ajouter un lord devant les noms des Seigneurs √
# - Définir le système de tour de jeu √
# - Changer MainMenu pour utiliser create_window
#		--> C'est une fonction uniquement liéer aux Canvas -_-
#			--> En créer un et l'utiliser seulement pour cela ?
#			--> Comme cela on à juste à détruire le canvas quand ont veut revenir en arrière
#			--> Et on a pas à créer une nouvelle fenêtre de 0 totalement séparé
# - Améliorer le Zoom/Dezoom
# - Retirer Move de centerviewcanvas
#
#
# Interface:
# - réglé les tags unbind
#		--> C'est de la merde
#			--> à la place on remet le tags highlight
#				--> Peut être utiliser funcid = .execute(func)
# - terminer statewar
# - terminer staterecruitarmy
# - commencer statesubjugate
# - commencer stateimmigration
# - commencer statetax
# - ajouter la création de pop à buildvillage
# - définir les régles de création de village, création d'église
# - terminer centervillagechurch
# - Voir pour une fonction exitstate générale
#
# GameClass:
# - définir les particularités des prêtre
#
# affichage:
# - Régler les labels des noms
#	--> Actuellement ils ont tendance à ce couper
#
# Data:
#	- Sauvegarde des données
#
# Projet:
# - Placer dans un sous-dossier fonctions les fonctions.py √
# - Placer dans un sous-dossier doc les fichiers docs √
#
# Main:
# - Réarranger par ordre d'execution √
#
# Gameclass:
# - Créer une methode pour vérifier l'etat
# - Régler le problème de sauvegarde du log
#		--> Il faut f.close()
#			--> Créer un fonction dans gamedata appeler quand on quitte l'application
# - Ajouter une Methode de Formatage du log qui gère les sauts à la ligne, le time code etc ....
# 
# Interface:
# - remplacer les vérification de state par une methode de Gameclass pour 
#
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


# !!!!! Doit modifier centerviewcanvas pour retirer le move() !!!!!
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





	pass


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
	gamedata.log.printinfo(f"taille écran x,y: , {root.winfo_screenwidth()}, {root.winfo_screenheight()}")
	win1.geometry(f"+{option.widthWindow//8}+{option.heightWindow//4}")


	# Frame Map
	fcanvas = tkinter.Frame(win1)
	fcanvas.pack(expand="True", fill="both")
	classmap.setlframecanvas(fcanvas)

	# Interface de Jeu
	interface.gameinterface(win1, option, gamedata, classmap)

	# Carte de Jeu
	createmap(gamedata, classmap, option, pic)


	# Genération des Villages
	genproc.genVillage(gamedata, classmap, option)

	# Affichage des Villages
	affichage.printvillage(gamedata, classmap, option,fcanvas)

	# On rempli les villages de pop
	for village in classmap.lvillages:
		genproc.genpopvillage(option, classmap, gamedata,village, 10)


####################################################################################################

######################### Creation de la Carte Canvas #######################################################
def createmap(gamedata, classmap, option, pic):

	#Si heigthWindow/1.5 le boutton quitter disparait
	mapcanv = tkinter.Canvas(classmap.framecanvas,height = ((option.heightWindow)*0.6), width = option.widthWindow)
	# On setup le frame de l'atlas
	gamedata.setlframe(tkinter.Frame(classmap.framecanvas))
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
	mapcanv.bind("<MouseWheel>", lambda event: moveview.moveviewz(event, gamedata, classmap, option))

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


def bordervillage(Gamedata, Classmap, frame):
	##################
	# Fonction pour afficher les frontière des villages
	##################
	pass


def movearmy(gamedata, unit):
	##################
	# Fonction pour bouger les unit
	#	- Doit vérifier que l'armée à suffisament de point de mouvement disponible
	#	- 
	#	- 
	##################
	pass

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
			endofturn(gamedata)

		# Si c'est au joueurs de jouer
		if gamedata.Nb_toplay == gamedata.playerid:
			# On entre dans la loop du tour du joueur
			playerturn(gamedata)
		# Sinon c'est à un Ia de jouer
		else:
			# On entre dans la loop de l'ia
			notplayerturn(gamedata)

	# On vérifie que la partie n'est pas terminé
	if gamedata.is_finished == False:
		# Si elle ne l'est pas on rapelle cette fonction dans 
		root.after(50, lambda: gameloop(gamedata, classmap, option, root))



def playerturn(gamedata):
	# Si le joueur à appuier sur le bouton fin de tour
	if gamedata.endturn == True:
		gamedata.log.printinfo("Player hit end of turn button")
		# On incrémente le joueur qui doit jouer
		gamedata.Nb_toplay += 1
		# On indique au joueurs que c'est à l'ia de Jouer

# Fonction qui gère l'ia des ennemies
def notplayerturn(gamedata):
	gamedata.semaphore = True
	gamedata.log.printinfo(f"tour de: , {gamedata.list_lord[gamedata.Nb_toplay].lordname}, {gamedata.Nb_toplay}")
	# L'ia Joue

	gamedata.Nb_toplay += 1
	gamedata.semaphore = False

def endofturn(gamedata):
	gamedata.semaphore = True
	gamedata.Nb_toplay = 0
	gamedata.endofturn()
	gamedata.endturn = False
	gamedata.semaphore = False



# after(time, function)

# Fonction qui gère la fin de partie
def endofgame():
	pass


###########################################################################




def printunit(gamedata, classmap, frame):
	##################
	# Fonction pour afficher les soldat
	##################
	pass


def infovillage(village):
	print("village name", village.name)
	print("village lord: ", village.lord.name)
	print("village priest: ", village.priest.name)
	print("village global joy: ", village.global_joy)
	print("village ressource, money: ", village.ressource, village.money)

######################### Autre Fonction #########################

######################### Main #########################
if __name__ == '__main__':

	#Init de la fenêtre
	root = tkinter.Tk()

	# Chargement des Options:
	option_instance = data.ClassOptions()
	# Initialisation de GameData
	gamedata_instance = data.ClassGameData()

	# Initialisation de la Carte
	map_instance = data.Classmap()

	# Menu principale
	mainmenu(gamedata_instance, map_instance, option_instance, root)


	root.mainloop()


