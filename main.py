import tkinter
import random

import genproc
import data
import interface
import gameClass
import affichage
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
# - réglé le décalage entre les state et la carte
# 	--> Voir pour modifier moveviewz
#			--> On à un décalage qui se créer à cause de move qui change la position à partir de event.x et event.y
#				--> Cela cause inévitablement un décalage autour event.x et event.y de delta
#					--> ex quand on zoom la première fois avec la souris sur la zone 50,50 on a un décalage de 100,100 qui va se créer à partir de cette coord
#			--> Il faut faire une translation vers le point d'origne du canvas, appliquer le scale puis se repositionner aux coord voulu
#				--> centerview(gamedata, option, mapcanv, [0,0])
#				--> scale()
#				--> centerview(gamedata, option, mapcanv, coordcanv)
#	- Déplacement en mettant la souris sur la bordure extérieur de la carte
# Interface:
# - réglé les tags unbind
# - terminer statewar()
# - terminer staterecruitarmy
# - commencer statesubjugate
# - commencer stateimmigration
# - commencer statetax
# - ajout la création de pop à buildvillage
# - définir les régles de création de village, création d'église
#
# GameClass:
# - définir les particularités des prêtre
#
# Data:
#	- Sauvegarde des données
#########################################################


######################### Menu Principale #########################

def mainmenu(option, gamedata, classmap,root):
	# Création de la fenêtre
	mainmenuwin = tkinter.Toplevel(root, height = option.heightWindow, width = option.widthWindow)
	# On centre la fenêtre
	# Pourquoi ?
	print(f"{option.heightWindow}x{option.widthWindow}+{option.heightWindow//8}+{option.widthWindow//8}")
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
	mainscreen(option, root, pic, gamedata, classmap)

	# Une fois l'initialisation lancé on détruit la fenêtre du menu principale
	mainmenuwin.destroy()

	# On lance la game
	# Actuellement Bloque le process
	#game(gamedata)


###########################################################################




######################### Écran de Jeu #########################
def mainscreen(option, root, pic, gamedata, classmap):

	# Création de la fenêtre
	win1 = tkinter.Toplevel(root, height = option.heightWindow, width= option.widthWindow)
	win1.geometry(f"+{option.widthWindow//8}+{option.heightWindow//4}")


	# Frame Map
	fcanvas = tkinter.Frame(win1)
	fcanvas.pack(expand="True", fill="both")

	# Interface de Jeu
	interface.gameinterface(win1, option, gamedata, classmap, fcanvas)

	# Carte de Jeu
	createmap(gamedata, classmap, option, pic, fcanvas)


	# Genération des Villages
	genproc.genVillage(Map, gamedata, option)

	# Affichage des Villages
	affichage.printvillage(gamedata, Map, option,fcanvas)

	# On rempli les villages de pop
	for village in classmap.lvillages:
		genproc.genpopvillage(option, classmap, gamedata,village, 10)


####################################################################################################





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

	# Frame dans lequel on va afficher la version réduite de la carte
	canvasframeminimap = tkinter.Frame(fplaymenu, height = option.heightWindow/4, width = option.widthWindow/4)
	canvasframeminimap.pack(side="top")

	# Canvas de la minimap
	mapcanv = tkinter.Canvas(canvasframeminimap)

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

	for lord in gamedata.list_lord:
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
			#print(tl, x ,y)
			mapcanv.create_rectangle((x*2), y*2, (x*2)+2, (y*2)+2, fill=tl, tags = "minimap", outline='black')

	mapcanv.pack(expand = "True",fill="both")

def playmenutomainmenu(gamedata, classmap, option, menu, root):
	mainmenu(option, gamedata, classmap, root)
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
		del gamedata.list_lord[gamedata.Nb_lord-1]
		gamedata.Nb_lord -= 1
		gamedata.log.printinfo("On le retire du frame")
		frame_listlord.winfo_children()[gamedata.Nb_lord].destroy()

	else:
		gamedata.log.printerror("Il ne reste plus que le joueur")

###########################################################################


######################### Menu Load #########################

###############
# Fonction appeler pour afficher le menu de chargement des Saves
# On l'affiche par dessus le menu Principale
#
# Ce menu va servir à charger une save parmi la liste proposer
#	- Nom de la save, Nb de tour, nom du seigneur, date de la sauvegarde
#	- 
#	- Tant que l'on aura pas lancer le chargement de la save rien n'est charger en arrière plan
###############




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


######################### Creation de la Carte Canvas #######################################################
def createmap(gamedata, classmap, option, pic, frame):

	#Si heigthWindow/1.5 le boutton quitter disparait
	mapcanv = tkinter.Canvas(frame,height = ((option.heightWindow)*0.6), width = option.widthWindow)
	gamedata.setlframe(tkinter.Frame(frame))
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
			instancetuile = Classtuiles(texture_name, tl[1], x, y, mcanvt)
			# On le stocker dans la ClassMap
			#gamedata.list_tuile += [instancetuile]
			classmap.addtuileinlist(instancetuile)
			idtuile += 1

	#Carrer test
	#mapcanv.create_rectangle(0,0,20,20,tags = "tuile")

	#print("taille atlas: ",len(atlas))
	#On lie Command+molette aux zoom/dézoom
	mapcanv.bind("<MouseWheel>", lambda event: moveviewz(event, gamedata, option))

	#On focus sur le widget sinon il ne prendra pas en compte les entrées des touches fléchés
	mapcanv.focus_set()

	#On lie les touches fléchés aux déplacement de la vue
	mapcanv.bind('<KeyPress-Left>', lambda event, x=1,y=0: moveviewxy(event,x,y))
	mapcanv.bind("<KeyPress-Right>", lambda event, x=-1,y=0: moveviewxy(event,x,y))
	mapcanv.bind("<KeyPress-Up>", lambda event, x=0,y=1: moveviewxy(event,x,y))
	mapcanv.bind("<KeyPress-Down>", lambda event, x=0,y=-1: moveviewxy(event,x,y))

	#On lie le déplacement de la vue au maintient du bouton droit de la souris + motion
	mapcanv.bind('<Shift-ButtonPress-2>', startmoveviewmouse)
	mapcanv.bind('<Shift-B2-Motion>', moveviewmouse)


	#ON lie les différentes Cases à l'action click
	mapcanv.tag_bind("click", "<Button-1>", lambda event:interface.highlightCase(event, gamedata))

	#print(gamedata.list_tuile)
	mapcanv.pack(expand ="True", fill = "y")

####################################################################################################








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

def centerview(gamedata, option, mapcanv, coordcanv):
	##################
	# Fonction pour centrer la vue sur les coordonnées canvas donnés
	##################

	# On position à l'origine du canvas
	movex = mapcanv.canvasx(0)
	movey = mapcanv.canvasy(0)
	print("déplacement de x,y: ", movex, movey)
	mapcanv.move("tuile", +movex, +movey)


	# On se place en coord[0], coord[1]
	# On veut se placer au centre
	# On calcul donc le centre de la window du canvas
	# x = (1200/20)/2 = 30
	# y = ((1200/1.6)/20)//2 = 18
	# On ajoute les coord
	#  movex = coorcanva[0] - tuilesize*30, movey = coorcanva[0] - tuilesize*18

	movex = coordcanv[0] - ((option.widthWindow/gamedata.tuilesize)//2) * gamedata.tuilesize
	movey = coordcanv[1] - (((option.heightWindow/1.6)/gamedata.tuilesize)//2) * gamedata.tuilesize
	print("déplacement de x,y: ", movex, movey)
	mapcanv.move("tuile", -movex, -movey)


#################################### Fonction Calcul de coord ####################################


def coordcanvastomap(option, tuilesize, coord, mapcanv):
	##################
	# Fonction pour traduire les coordonnées du canvas en coordonnées de la carte
	##################
	xorigine = mapcanv.canvasx(0)
	yorigine = mapcanv.canvasy(0)
	print("xorigine: ", xorigine)
	print("yorigine: ", yorigine)
	print("coord: ", coord)

	xmap = (((coord[0] + xorigine) - tuilesize/2)%tuilesize)
	ymap = (((coord[1] + yorigine) - tuilesize/2)%tuilesize)


	return [xmap, ymap]

def coordmaptocanvas(option, tuilesize, coord, mapcanv):
	##################
	# Fonction pour traduire les coordonnées map en coordonnées du canvas
	##################

	# calcul de base
	xcanvas = (coord[0]*tuilesize)+(tuilesize/2)
	ycanvas = (coord[1]*tuilesize)+(tuilesize/2)

	# Maintenant on prend en compte le décalage que créer le zoom/dézoom
	# 20 est la taille de base d'une tuile sans avoir appliquer de zoom/dezoom
	xcanvas = xcanvas + (tuilesize/20) - 1
	ycanvas = ycanvas + (tuilesize/20) - 1

	return [xcanvas, ycanvas]

##########################################################################################



def bordervillage(Gamedata, Classmap, frame):
	##################
	# Fonction pour afficher les frontière des villages
	#
	#
	#
	##################
	pass


def moveunit(gamedata, unit):
	##################
	# Fonction pour bouger les unit
	#	- Doit vérifier que l'unit à suffisament de point de mouvement disponible
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
		#print("mountain")
		img = data.loadtexture("/asset/texture/terrain/mountains/mountains_inner.png", sizetuile)
	elif type == "forest":
		#print("forest")
		img = data.loadtexture("/asset/texture/terrain/conifer_forest/conifer_forest_inner.png", sizetuile)
	elif type == "plains":
		#print("plains")
		img = data.loadtexture("/asset/texture/terrain/plains/plains.png", sizetuile)
	elif type == "ocean":
		#print("ocean")
		img = data.loadtexture("/asset/texture/terrain/ocean/ocean_inner.png", sizetuile)
	return img


def typetoimgdico(dico_file, type, sizetuile):
	####################
	# Fonction qui va renvoyer une image selon le type envoyer en entré et le dico
	# l'image est resize à la taille d'une tuile
	####################

	img = ""

	if type == "mountains":
		#print("mountain")
		img = data.loadtexturefromdico(dico_file, "mountains_inner.png", type, sizetuile)[1]
	elif type == "forest":
		#print("forest")
		img = data.loadtexturefromdico(dico_file, "conifer_forest_inner.png", type, sizetuile)[1]
	elif type == "plains":
		#print("plains")
		img = data.loadtexturefromdico(dico_file, "plains.png", type, sizetuile)[1]
	elif type == "ocean":
		#print("ocean")
		img = data.loadtexturefromdico(dico_file, "ocean_inner.png", type, sizetuile)[1]
	return img


def moveviewz(event, gamedata, option):
	####################
	# Fonction pour zoomer/dézoomer
	# En utilisant la molette de la souris
	#
	# On prend pour valeur min de la taille d'une tuile 5
	#
	# On zoome quand on multiplie par delta
	# On dezoome quand on divise par delta
	#
	#	--- * 2 = ------ 	== Zoom car on agrandit
	#
	# 	--- / 3 = - 		== DeZoom car on réduit
	####################
	# 1°) On recup les point d'origine du canvas
	# 2°) On normalise le delta pour prendre en compte les différentes plateformes
	# 3°) On recup la taille d'une tuile
	# 4°) On scale 
	# 5°) On change les texture des tuiles pour la nouvelles tuiles
	#####################

	idorigine = 0
	while event.widget.type(idorigine) != "image":
		idorigine += 1



	####################\ 1°) \####################

	x0 = int(event.widget.canvasx(event.x))
	y0 = int(event.widget.canvasy(event.y))

	# On recup les coord-canvas de la tuile
	coordcanv = event.widget.coords(event.widget.find_closest(x0,y0))

	print("x0, y0: ", x0, y0)
	print("coord canv tuile plus proche: ", coordcanv[0], coordcanv[1])
	############################################################

	####################\ 2°) \####################
	#Pour éviter les différence entre windows et Mac ont normalise delta
	#Doit prendre en compte linux -_-
	print(event.delta)
	if event.delta <= 0:
		delta = -2
	else:
		delta = 2
	############################################################


	####################\ 3°) \####################
	# On recup la taille d'une tuile
	x = gamedata.tuilesize
	#print("x, event.delta, delta: ",x, event.delta, delta)
	############################################################

	# Doit trouver les valeurs parfaite max et min
	# Zoom = max = x = 320
	# DeZoom = min = x = 5
	# À l'avenir changer la valeur minimum par une valeur calculer a partir de la taille de la carte

	####################\ 4°) \####################
	#Zoom
	print("x avant zoom: ", event.widget.coords(idorigine)[0])
	print("y avant zoom: ", event.widget.coords(idorigine)[1])
	#centerview(gamedata, option, event.widget, [event.widget.canvasx(0),event.widget.canvasy(0)])
	if (x<320) and (delta == 2):
		print("Zoom")
		event.widget.scale("tuile", 0, 0, delta, delta)
		print("x: ", event.widget.canvasx(event.x))
		print("y: ", event.widget.canvasy(event.y))
		#print("x: ", x*delta)
		x = x*delta
	#Dezoom
	elif(x>5) and (delta == -2):
		print("DeZoom")
		#On rend positive le delta sinon il inverse le sens de la carte
		event.widget.scale("tuile", 0, 0, -1/(delta), -1/(delta))
		#print("x: ",x*(-1/(delta)))
		x = x*(-1/(delta))
	centerview(gamedata, option, event.widget, [coordcanv[0], coordcanv[1]])
	# On change la taille des tuiles stocker dans les données globaux
	gamedata.newsizetuile(x)
	############################################################
	print("x après zoom: ", event.widget.coords(idorigine)[0])
	print("y après zoom: ", event.widget.coords(idorigine)[1])



	####################\ 5°) \####################
	#Recalcul des images
	newsize = x
	print("newsize : ", newsize)

	###############################\ !!! À modifier !!! \#############################
	# Trouver un moyen de se débaraser des 4 variables
	# Ne plus utiliser le type de la texture

	###################################################################################
	f = 0
	m = 0
	o = 0
	p = 0
	v = 0
	#Tuile graphique:
	for ele in event.widget.find_withtag("img"):

		type = event.widget.gettags(ele)[1]
		# Version Non-random ou on utilise les texture de bases:
		# Quand la classe des tuile sera implémenter utiliser le nom de la texture
		# Utiliser #gamedata.loadtextureatlas(texture_name, type)
		if type == "forest":
			#Si dans la fonction on n'a pas déjà recalculer la nouvelle image pour le type selectionner
			if f == 0:
				#On recréer l'image
				tk_img = data.loadtexturefromdico(dico_file, "conifer_forest_inner.png", type, int(newsize))
				# On change le label associer à la texture dans l'atlas
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])				
				f = 1
			# On recup le label associer à la texture
			label = gamedata.atlas["conifer_forest_inner.png"]
		elif type == "mountains":
			if m == 0:
				tk_img = data.loadtexturefromdico(dico_file, "mountains_inner.png", type, int(newsize))
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])	
				m = 1
			label = gamedata.atlas["mountains_inner.png"]
		elif type == "ocean":
			if o == 0:
				tk_img = data.loadtexturefromdico(dico_file, "ocean_inner.png", type, int(newsize))
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])						
				o = 1
			label = gamedata.atlas["ocean_inner.png"]
		elif type == "plains":
			if p == 0:
				tk_img = data.loadtexturefromdico(dico_file, "plains.png", type, int(newsize))
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])						
				p = 1
			label = gamedata.atlas["plains.png"]
		elif type == "build":
			if v == 0:
				tk_img = data.loadtexturefromdico(dico_file, "settlement.png", type, int(newsize))
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])
				v = 1
			label = gamedata.atlas["settlement.png"]

		event.widget.itemconfigure(ele,image = label.image)
	############################################################
	print("taille Atlas: ", len(gamedata.atlas))
	############################################################














#################### 
# Ensemble de Fonction pour déplacer la vue en:
# Maintenant le click gauche de la souris √
# En placant le souris sur une extrémité de la caméra
# En appyant sur les touches fléchés √
####################

def moveviewxy(event, deltax, deltay):
	####################
	# Fonction pour déplacer la vue en:
	# Maintenant le click gauche de la souris
	# En placant le souris sur une extrémité de la caméra
	# En appyant sur les touches fléchés 
	####################
	mult = 100

	print("move map arrow")

	################ Déplacement de la vue ################

	event.widget.move("tuile", mult*deltax, mult*deltay)

	#######################################################

def startmoveviewmouse(event):
	####################
	# Fonction pour déplacer la vue en:
	# Maintenant le click droit de la souris
	# Partie 1
	# Utiliser .scan_mark(x, y)
	#
	####################
	#print(startmoveviewmouse)
	event.widget.scan_mark(event.x, event.y)

def moveviewmouse(event):
	####################
	# Fonction pour déplacer la vue en:
	# Maintenant le click droit de la souris
	# Partie 2
	# Utiliser .scan_dragto(x, y)
	# !!!! A cause de l'utilisation de Move est très couteux !!!!
	####################
	#print(moveviewmouse)
	event.widget.scan_dragto(event.x, event.y, gain = 1)


######################### Autre Fonction #########################



###########################################################################


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

# Fonction qui gère la partie
def game(gamedata):

	ingame = True
	nbtoplay = 0
	# Boucle principale du jeu
	while(ingame == True):
		if nbtoplay == gamedata.Nb_lord:
			nbtoplay = 0
			gamedata.Nb_tour += 1

		# On verifie que c'est le tour du joueur
		if gamedata.playerid == nbtoplay:
			playerturn(gamedata)
		else:
			notplayerturn(gamedata, nbtoplay)


		nbtoplay += 1




# Fonction qui gère la fin de partie
def endofgame():
	pass


# Fonction qui gère l'ia des ennemies
def notplayerturn(gamedata, nbtoplay):
	pass



# Fonction qui gère le tour du joueur
def playerturn(gamedata):
	while(gamedata.endturn == False):
		pass
	gamedata.endturn == True

def buildvillage(Classmap, idtuile, player):
	####
	# Fonction pour tester puis créer un village par le joueur 
	#####

	# On vérifie que la construction est possible
	if buildvillagepossible(Options, Classmap, idtuile) == True:
		# Si c'est possible on créer
		Classmap.lvillages += [idtuile]
		Classmap.listmap[idtuile].createvillage()
		Classmap.listmap[idtuile].setpossesor("player")


def moveunit():
	pass







###########################################################################

######################### Def de Classes #########################

class Classmap:
	####################
	# Classe qui va contenir toute les sous-classes tuiles dans une liste associer à un identificateur
	#		--> Une liste ou un dictionnaire ?
	#		--> l'avantage du dictionnaire et de pouvoir balancer l'identificateur pour en recup la tuile
	####################
	def __init__(self):
		# Variable qui vient contenir le canvas de la map
		self.mapcanv = 0
		# liste qui vient contenir le décalage en x et y
		self.gap = [0,0]

		#Dico qui vient contenir les Classtuiles 
		self.listmap = {}
		self.nbtuile = 0

		#Liste qui vient contenir les ids des:
		#	--> Villages
		#	--> Plaines
		self.lvillages = []
		self.lplaines = []

	def addtuileinlist(self, tuile):
		self.listmap[self.nbtuile] = tuile
		tuile.setidtuile(self.nbtuile)
		self.nbtuile += 1

	def setmapcanv(self, mapcanv):
		self.mapcanv = mapcanv


class Classtuiles:
	####################
	# Classe qui va contenir toute les données liée à une tuile:
	#
	#	- N° de la tuile
	#	- Propriétaire de la tuile:
	#		--> Un seigneur ou personne(nature)
	#		--> Quand la tuile est créer personne ne possède la tuile
	#	- Ressource présente
	#	- Ressource particulière
	#		--> Optionnelle, pour après que le projet soit terminer
	#	- Bonus/Malus
	#	- texture file associé
	#			--> On sépare le texture file du texture
	#				--> texture_name = le nom du fichier
	#				--> texture = le fichier charger est resize
	#			--> Selon le type on associe un background
	####################

	def __init__(self, texture_name, type, x, y, canvasobject):
		# N° de la tuile, défini par classmap
		self.id = 0
		#Position de la tuile
		self.x = x
		self.y = y
		self.type = type
		# nom du fichier texture associé
		self.texture_name = texture_name
		self.background = "plains.png"

		# Si c'est un village
		self.village = 0

		# nom du propriétaire de la tuile
		self.possesor = "wild"

		# Objet du canvas associer
		self.canvastuiles = canvasobject

		# Selon le type de la classe on définit:
		#	- le rendement en ressource et argent
		#	- le cout en déplacement pour traverser la tuile

		if type == "plains":

			self.ressourceyield = 0
			self.moneyield = 0
			self.movementcost = 1

		elif type == "forest":

			self.ressourceyield = 0
			self.moneyield = 0
			self.movementcost = 2

		elif type == "mountains":

			self.ressourceyield = 0
			self.moneyield = 0
			self.movementcost = 3

		elif type == "ocean":

			self.ressourceyield = 0
			self.moneyield = 0
			self.movementcost = 4

	def setidtuile(self, id):
		self.id = id

	def setpossesor(self, possesor):
		self.possesor = possesor

	def createvillage(self):
		# On créer un nouveau village que l'on stocke
		self.village = gameClass.Classvillage(self.x, self.y)
		# On set le nom du village
		self.village.setnamevillage(gamedata.randomnametype("Village"))


class ClassGameInterface:
	####################
	# Classe qui va contenir toute les données liée à l'interface Tkinter
	#
	#
	####################

	def __init__(self):
		self.root = tkinter.Tk()



###########################################################################

######################### Main #########################
if __name__ == '__main__':


	#GameInterface = ClassGameInterface()
	#Init de la fenêtre
	root = tkinter.Tk()

	# Chargement des Options:
	option = data.ClassOptions()
	# Initialisation de GameData
	gamedata = data.ClassGameData()

	# Initialisation de la Carte
	Map = Classmap()

	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, option.mapx, option.mapy)
	#Chargement en mémoires des images du dico:
	dico_file = data.assetLoad()
	

	# Menu principale
	mainmenu(option, gamedata, Map, root)
	# Si on veut tester rapidement la boucle de jeu sans passer par le menu principale
	#mainscreen(option, root, pic, gamedata, Map)


	root.mainloop()