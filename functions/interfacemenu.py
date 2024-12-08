
import os
import sys
import random
import tkinter

from time import time

import functions.log as log
import functions.game as game
import functions.data as data
import functions.stats as stats
import functions.asset as asset
import functions.common as common
import functions.genproc as genproc
import functions.moveview as moveview
import functions.gameclass as gameclass
import functions.affichage as affichage
import functions.interfacegame as interfacegame

######################### Menu Principale #########################

def mainmenu(gamedata, classmap, option, root):
	# Création de la fenêtre
	mainmenuwin = tkinter.Toplevel(root, height = option.heightWindow, width = option.widthWindow)
	# On centre la fenêtre
	# Pourquoi ?
	log.log.printinfo(f"{option.heightWindow}x{option.widthWindow}+{option.heightWindow//8}+{option.widthWindow//8}")
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
	Button_mainm_QuickPlay = tkinter.Button(fmainm, command = lambda: game.initgame(mainmenuwin, gamedata, classmap, option, root), text = "Partie Rapide")

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
	fplaymenu.grid()
	mainmenuwin.geometry(f"+{option.widthWindow//3}+{option.heightWindow//5}")


	########################\ Minimap \##############################
	# Frame dans lequel on va afficher la version réduite de la carte
	canvasframeminimap = tkinter.Frame(fplaymenu, height = option.heightWindow/4, width = option.widthWindow/4)
	canvasframeminimap.grid(row = 0, columnspan = 5)

	# Canvas de la minimap
	mapcanv = tkinter.Canvas(canvasframeminimap)

	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, option.mapx, option.mapy)
	# Fonction qui gen la mini carte
	previewmap(mapcanv, pic, option.mapx, option.mapy)
	##################################################################

	########################\ Seed \##################################
	#txt variable seed
	tkvar_seed = tkinter.IntVar()
	tkvar_seed.set(gamedata.seed)

	# Button pour générer un nouveau seed ce qui vient update automatiquement la carte
	Button_playmenu_newseed = tkinter.Button(fplaymenu ,command = lambda: regenseed(gamedata, option,tkvar_seed, mapcanv), text = "Genérer nouvelle Seed")
	Button_playmenu_newseed.grid(row = 1, columnspan = 5)


	# Entry widget qui affiche la seed, permet de la modif et de la copier
	entryseed = tkinter.Entry(fplaymenu, textvariable = tkvar_seed)
	entryseed.grid(row = 2, column = 1, columnspan = 2)
	button_entryseed = tkinter.Button(fplaymenu, command = lambda: validate_entry_seed(entryseed, option, gamedata, tkvar_seed, mapcanv), text = "change")
	button_entryseed.grid(row = 2, column = 2, columnspan = 2)
	##################################################################

	########################\ Map Size \##############################
	#txt variable mapx mapy
	tkvar_mapx = tkinter.IntVar()
	tkvar_mapx.set(option.mapx)
	tkvar_mapy = tkinter.IntVar()
	tkvar_mapy.set(option.mapy)

	# Label
	tkinter.Label(fplaymenu, text = "largeur: ").grid(row = 3, column = 0)
	# Entry widget qui affiche la taille en x et y 
	entrymapx = tkinter.Entry(fplaymenu, textvariable = tkvar_mapx)
	entrymapx.grid(row = 3, column = 1)
	tkinter.Label(fplaymenu, text = "hauteur: ").grid(row = 3, column = 2)
	entrymapy = tkinter.Entry(fplaymenu, textvariable = tkvar_mapy)
	entrymapy.grid(row = 3, column = 3)
	button_entrymap = tkinter.Button(fplaymenu, command = lambda: validate_entry_map(entrymapx, entrymapy, option, gamedata, tkvar_mapx, tkvar_mapy, mapcanv), text = "change")
	button_entrymap.grid(row = 3, column = 4)
	##################################################################

	########################\ Liste Seigneurs \#######################
	# On affiche la liste des seigneurs actuellement créer
	tkinter.Label(fplaymenu, text = "liste des Seigneur: ").grid(row = 4, columnspan = 5)

	fplaymenu_frame_listlord = tkinter.Frame(fplaymenu)
	fplaymenu_frame_listlord.grid(row = 6, columnspan = 5)

	#txt variable nom joueur
	tkvar_playername = tkinter.StringVar()
	tkvar_playername.set(gamedata.list_lord[gamedata.playerid].lordname)
	for lord in gamedata.list_lord:
		# Si c'est le joueur on met affiche un label Player est on met en place un Entry afin de pouvoir modifier le nom du Seigneur
		if lord.player == True:
			tkinter.Label(fplaymenu, text = "Player:").grid(row = 5, column = 1)
			entryplayername = tkinter.Entry(fplaymenu, textvariable = tkvar_playername)
			entryplayername.grid(row = 5, column = 2)
			tkinter.Button(fplaymenu, text = "change", command = lambda: validate_entry_lordname(gamedata, tkvar_playername)).grid(row = 5, column = 3)
		else:
			tkinter.Label(fplaymenu_frame_listlord, text = lord.lordname, fg = lord.color).grid(columnspan = 5)
	##################################################################


	# On affiche un bouton pour en créer un nouveau
	button_newlord = tkinter.Button(fplaymenu, text = "Créer un seigneur", command = lambda: playmenucreatelord(gamedata, fplaymenu_frame_listlord))
	button_newlord.grid(columnspan = 5)
	# On affiche un bouton pour supprimer le dernier
	button_deletelastlord = tkinter.Button(fplaymenu, text = "Supprimer le dernier seigneur", command = lambda:playmenudeletelord(gamedata, fplaymenu_frame_listlord))
	button_deletelastlord.grid(columnspan = 5)

	# Button pour lancer une nouvelle partie
	Button_playmenu_play = tkinter.Button(fplaymenu, command = lambda: game.initgame(mainmenuwin, gamedata, classmap, option, root),text = "Jouer")
	Button_playmenu_play.grid(columnspan = 5)

	# Boutton pour revenir en arrière
	Button_playmenu_return = tkinter.Button(fplaymenu, command = lambda: playmenutomainmenu(gamedata, classmap, option, mainmenuwin, root),text = "Retour")
	Button_playmenu_return.grid(columnspan = 5)

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

	for y in range(mapy):
		for x in range(mapx):
			log.log.printinfo(f"picx, picy: {len(pic[0])}, {len(pic)}")
			log.log.printinfo(f"x,y: {x},{y}")
			tl = tuile(pic[y][x])[0]
			mapcanv.create_rectangle((x*2), y*2, (x*2)+2, (y*2)+2, fill=tl, tags = "minimap", outline='black')

	mapcanv.pack(expand = "True",fill="both")

def playmenutomainmenu(gamedata, classmap, option, menu, root):
	mainmenu(gamedata, classmap, option, root)
	menu.destroy()


def playmenucreatelord(gamedata, frame_listlord):
	####################
	# Fonction pour Créer un seigneur dans le menu play
	####################
	log.log.printinfo("On Créer un nouveau Seigneur")
	gamedata.createlord()
	lord = gamedata.list_lord[gamedata.Nb_lord-1]

	log.log.printinfo("On l'ajoute au frame")
	tkinter.Label(frame_listlord, text = gamedata.list_lord[gamedata.Nb_lord-1].lordname, fg = lord.color).grid(columnspan = 5)


def playmenudeletelord(gamedata, frame_listlord):
	####################
	# Fonction pour Suprimer un seigneur dans le menu play
	####################
	if gamedata.Nb_lord-1 != gamedata.playerid:
		log.log.printinfo(f"On supprime le Dernier Seigneur de la liste {gamedata.list_lord[gamedata.Nb_lord-1].lordname}, avec pour id: {gamedata.list_lord[gamedata.Nb_lord-1].idlord}")
		gamedata.deletelord(gamedata.Nb_lord-1)
		log.log.printinfo("On le retire du frame")
		log.log.printinfo(f"{frame_listlord.winfo_children()}")
		# On retire le seigneur de la liste
		frame_listlord.winfo_children()[-1].destroy()

	else:
		log.log.printerror("Il ne reste plus que le joueur")

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




def optionmenu(gamedata, classmap, option):
	# On suprime le frame du menu principale
	mainmenuwin.winfo_children()[0].destroy()

	# On créer le nouveaux frame




	pass



######################### Écran de Fin de Jeu #########################

def eofgamescreen(gamedata, classmap, option):
	###############
	# Fonction appelé pour afficher l'écran de fin de Jeu
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

	frame_eof_screen_up = tkinter.Frame(frame_eof_screen)
	frame_eof_screen_up.grid(row = 0, column = 0, columnspan = 5)
	eofgamescreen_main(gamedata, classmap, option, frame_eof_screen_up)

	# Boutton pour Changer pour un Graphique
	# Graphe Croissance Militaire
	button_military_graph = tkinter.Button(frame_eof_screen ,text = "Croissance Militaire", command = lambda: eof_military_graph(gamedata, classmap, option, frame_eof_screen_up)).grid(row = 4, column = 1)

	# Graphe Croissance Démographique
	button_demography_graph = tkinter.Button(frame_eof_screen ,text = "Croissance Démographique", command = lambda: eof_demography_graph(gamedata, classmap, option, frame_eof_screen_up)).grid(row = 4, column = 2)

	# Graphe Croissance économique
	button_economy_graph = tkinter.Button(frame_eof_screen ,text = "Croissance Économique", command = lambda: eof_economy_graph(gamedata, classmap, option, frame_eof_screen_up)).grid(row = 4, column = 3)

	# Graphe Score
	button_score_graph = tkinter.Button(frame_eof_screen ,text = "Score", command = lambda: eof_score_graph(gamedata, classmap, option, frame_eof_screen_up)).grid(row = 4, column = 4)

	# Graphe des Mort
	button_death_graph = tkinter.Button(frame_eof_screen ,text = "Mort", command = lambda: eof_death_graph(gamedata, classmap, option, frame_eof_screen_up)).grid(row = 4, column = 5)

	# Boutton pour retourner sur le Menu Principale
	button_return_mainmenu = tkinter.Button(frame_eof_screen ,text = "Menu Principale", command = lambda: exit_mainmenu(gamedata, classmap, option)).grid(row = 5, column = 1, columnspan = 2)

	# Boutton pour charger une Save précédente
	button_loadsave = tkinter.Button(frame_eof_screen ,text = "Charger une Sauvegarde").grid(row = 5, column = 3, columnspan = 2)


def eofgamescreen_main(gamedata, classmap, option, frame_eof_screen_up):
	#######
	# Affichage Principale
	#######

	# On gère l'affichage précédent
	lchildren = frame_eof_screen_up.winfo_children()
	print(lchildren)
	while len(lchildren) >= 1:
		frame_eof_screen_up.winfo_children()[0].destroy()
		lchildren = frame_eof_screen_up.winfo_children()

	frame_eof_screen_up_child = tkinter.Frame(frame_eof_screen_up)
	frame_eof_screen_up_child.grid()

	player = gamedata.list_lord[gamedata.playerid]

	# Titre
	# Victoire OU défaite
	tkinter.Label(frame_eof_screen_up_child, text = f"{gamedata.victory} du Seigneur {player.lordname}").grid(row = 0,column = 3)

	# Info de base Principale
	# Nb Tour
	tkinter.Label(frame_eof_screen_up_child, text = f"Nombre de tour: {gamedata.nb_turn}").grid(row = 1, column = 2)
	# Nb Vassaux possèder
	tkinter.Label(frame_eof_screen_up_child, text = f"Nombre de Vassaux: {len(player.vassal)}").grid(row = 2, column = 2)
	# Puissance Militaire
	tkinter.Label(frame_eof_screen_up_child, text = f"Puissance Militaire: {player.power}").grid(row = 3, column = 2)
	# Score
	tkinter.Label(frame_eof_screen_up_child, text = f"Score: ").grid(row = 1, column = 4)
	# Nb Village possèder
	tkinter.Label(frame_eof_screen_up_child, text = f"Nombre de Village: {len(player.fief)}").grid(row = 2, column = 4)
	# Nb Pop
	# On recup la taille totale
	nb_total= 0
	for village in player.fief:
		nb_total += len(village.population)
	tkinter.Label(frame_eof_screen_up_child, text = f"Taille de la Population: {nb_total}").grid(row = 3, column = 4)

def eof_military_graph(gamedata, classmap, option, frame_eof_screen_up):
	#######
	# Affichage Graphe Évolution Militaire
	#######

	# On gère l'affichage précédent
	lchildren = frame_eof_screen_up.winfo_children()
	print(lchildren)
	while len(lchildren) >= 1:
		frame_eof_screen_up.winfo_children()[0].destroy()
		lchildren = frame_eof_screen_up.winfo_children()

	frame_eof_screen_up_child = tkinter.Frame(frame_eof_screen_up)
	frame_eof_screen_up_child.grid()

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"").grid(row = 0,column = 3)

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color).grid(row = 1, column = i)

		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Croissance Militaire").grid(row = 0,column = 0, columnspan = i)

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child)
	canvas.grid(row = 2, column = 0, columnspan = i)

	pass

def eof_demography_graph(gamedata, classmap, option, frame_eof_screen_up):
	#######
	# Affichage Graphe Évolution démographique
	#######

	# On gère l'affichage précédent
	lchildren = frame_eof_screen_up.winfo_children()
	print(lchildren)
	while len(lchildren) >= 1:
		frame_eof_screen_up.winfo_children()[0].destroy()
		lchildren = frame_eof_screen_up.winfo_children()

	frame_eof_screen_up_child = tkinter.Frame(frame_eof_screen_up)
	frame_eof_screen_up_child.grid()

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"").grid(row = 0,column = 3)

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color).grid(row = 1, column = i)

		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Croissance Démographique").grid(row = 0,column = 0, columnspan = i)

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child)
	canvas.grid(row = 2, column = 0, columnspan = i)
	pass

def eof_economy_graph(gamedata, classmap, option, frame_eof_screen_up):
	#######
	# Affichage Graphe Évolution Économique
	#######

	# On gère l'affichage précédent
	lchildren = frame_eof_screen_up.winfo_children()
	print(lchildren)
	while len(lchildren) >= 1:
		frame_eof_screen_up.winfo_children()[0].destroy()
		lchildren = frame_eof_screen_up.winfo_children()

	frame_eof_screen_up_child = tkinter.Frame(frame_eof_screen_up)
	frame_eof_screen_up_child.grid()

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"").grid(row = 0,column = 3)

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color).grid(row = 1, column = i)

		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Croissance Économique").grid(row = 0,column = 0, columnspan = i)

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child)
	canvas.grid(row = 2, column = 0, columnspan = i)
	pass

def eof_score_graph(gamedata, classmap, option, frame_eof_screen_up):
	#######
	# Affichage Graphe Évolution Score
	#######

	# On gère l'affichage précédent
	lchildren = frame_eof_screen_up.winfo_children()
	print(lchildren)
	while len(lchildren) >= 1:
		frame_eof_screen_up.winfo_children()[0].destroy()
		lchildren = frame_eof_screen_up.winfo_children()

	frame_eof_screen_up_child = tkinter.Frame(frame_eof_screen_up)
	frame_eof_screen_up_child.grid()

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"").grid(row = 0,column = 3)

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color).grid(row = 1, column = i)

		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Score").grid(row = 0,column = 0, columnspan = i)

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child)
	canvas.grid(row = 2, column = 0, columnspan = i)
	pass

def eof_death_graph(gamedata, classmap, option, frame_eof_screen_up):
	#######
	# Affichage Graphe Évolution Mort
	#######

	# On gère l'affichage précédent
	lchildren = frame_eof_screen_up.winfo_children()
	print(lchildren)
	while len(lchildren) >= 1:
		frame_eof_screen_up.winfo_children()[0].destroy()
		lchildren = frame_eof_screen_up.winfo_children()

	frame_eof_screen_up_child = tkinter.Frame(frame_eof_screen_up)
	frame_eof_screen_up_child.grid()

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"").grid(row = 0,column = 3)

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color).grid(row = 1, column = i)

		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Mort").grid(row = 0,column = 0, columnspan = i)

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child)
	canvas.grid(row = 2, column = 0, columnspan = i)
	pass

def exit_mainmenu(gamedata, classmap, option):
	#######
	# Fonction pour retourner aux Menu Principale
	#######
	exit()


###########################################################################

######################### Écran de Jeu #########################
def mainscreen(gamedata, classmap, option, root, pic):

	# Création de la fenêtre
	win1 = tkinter.Toplevel(root, height = option.heightWindow, width= option.widthWindow)
	log.log.printinfo(f"taille écran x,y: {root.winfo_screenwidth()}, {root.winfo_screenheight()}")
	win1.geometry(f"+{option.widthWindow//8}+{option.heightWindow//4}")
	win1.title("Medieval Game")


	# Frame Map
	fcanvas = tkinter.Frame(win1, height = (option.heightWindow*0.6), width= option.widthWindow)
	log.log.printinfo(f"Taille de la Frame du Canvas: {fcanvas.winfo_width()}, {fcanvas.winfo_height()}")
	classmap.setlframecanvas(fcanvas)

	# Interface de Jeu
	interfacegame.gameinterface(gamedata, classmap, option, win1)

	fcanvas.pack()

	# Carte de Jeu
	createmap(gamedata, classmap, option, pic, win1)


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
	coordcanvas = common.coordmaptocanvas(gamedata, classmap, option, [village.x, village.y], True)
	# On centre la vue sur le village de départ
	moveview.centerviewcanvas(gamedata, classmap, option, coordcanvas)


	for village in classmap.lvillages:
		infovillage(classmap.listmap[village].village)

	interfacegame.updateinterface(gamedata, classmap)


####################################################################################################

######################### Creation de la Carte Canvas #######################################################
def createmap(gamedata, classmap, option, pic, win1):

	#Si heigthWindow/1.5 le boutton quitter disparait
	mapcanv = tkinter.Canvas(classmap.framecanvas, height = (option.heightWindow*0.6), width= option.widthWindow)
	log.log.printinfo(f"Taille du Canvas:{mapcanv.winfo_width()}, {mapcanv.winfo_height()}")
	# On setup le frame de l'atlas
	asset.atlas.setlframe(classmap.framecanvas)
	# On lie le mapcanvas à classmap
	classmap.setmapcanv(mapcanv)
	# On Créer les Différentes Cases avec le tags tuile pour indiquer et les trouvé plus facilement
	# On ajoute aussi le tags click pour indiquer qu'ils sont clickables
	# On ajoute aussi les tags x et y qui correspond à la casse ou ils est situés
	# ONn ajoute aussi le tag pic[x][y] qui correspond à la valeur de la case gen
	# 2ieme version: ajouter un tag supplémentaire liées aux types

	idtuile = 0

	ts = gamedata.tuilesize

	# !!!!!!
	# Différence position entre map texture et map carré causer par le fait que la map texture utilise les coordonnées donnés comme point centrale et non point en haut à gauche
	# !!!!!!
	for y in range(option.mapy):
		for x in range(option.mapx):

			# On utilise la valeur de la case pour définir la tuile que l'on va créer
			tl = tuile(pic[y][x])

			# Création de la carte avec Rectangle
			#mapcanv.create_rectangle((x*ts), (y*ts), (x*ts)+ts, (y*ts)+ts, fill = tl[0], tags = ["click","tuile",x,y,pic[x][y], tl[1]], outline='black')
			
			##### Version Non-Aléatoire Dico Avec Atlas #####
			
			if tl[1] == "mountains":
				asset.atlas.loadtextureatlas(asset.dico_file, ts, "mountains_inner.png", tl[1])
				texture_name = "mountains_inner.png"
			elif tl[1] == "forest":
				asset.atlas.loadtextureatlas(asset.dico_file, ts, "conifer_forest_inner.png", tl[1])
				texture_name = "conifer_forest_inner.png"
			elif tl[1] == "plains":
				asset.atlas.loadtextureatlas(asset.dico_file, ts, "plains.png", tl[1])
				texture_name = "plains.png"
			elif tl[1] == "ocean":
				asset.atlas.loadtextureatlas(asset.dico_file, ts, "ocean_inner.png", tl[1])
				texture_name = "ocean_inner.png"

			mcanvt = mapcanv.create_image((x*ts)+(ts/2), (y*ts)+(ts/2), image = asset.atlas.dico[texture_name].image, tags = ["img",tl[1],"tuile","click", x, y, pic[y][x], idtuile])
			
			################################

			"""
			##### Version Aléatoire Dico #####
			texture_name = data.randomtexturefromdico(gamedata.dico_file, tl[1])
			# Si la texture afficher n'est pas une texture compléte est que ce n'est pas un ocean
			if tl[1] != "ocean":
				if texture_name not in ["mountains_inner.png", "conifer_forest_inner.png", "ocean_inner.png", "plains.png"]:
					# On affiche en arrière plans une texture background
					gamedata.loadtextureatlas("plains.png", "plains")
					mapcanv.create_image((x*ts)+(ts/2), (y*ts)+(ts/2), image = gamedata.atlas["plains.png"].image, tags = ["img",tl[1],"tuile","click", x, y, pic[x][y], idtuile])
			
			gamedata.loadtextureatlas(texture_name, tl[1])
			mcanvt = mapcanv.create_image((x*ts)+(ts/2), (y*ts)+(ts/2), image = gamedata.atlas[texture_name].image, tags = ["img",tl[1],"tuile","click", x, y, pic[x][y], idtuile])
			"""
			################################

			# On créer une nouvelle instance de la classe tuiles
			instancetuile = data.Classtuiles(texture_name, tl[1], x, y, mcanvt)
			# On le stocker dans la ClassMap
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
	mapcanv.bind('<Shift-ButtonPress-2>', lambda event: moveview.startmoveviewmouse(event))
	mapcanv.bind('<Shift-ButtonRelease-2>', lambda event: moveview.endmoveviewmouse(event))
	mapcanv.bind('<Shift-B2-Motion>', lambda event: moveview.moveviewmouse(event, gamedata, classmap, option))


	#ON lie les différentes Cases à l'action click
	mapcanv.tag_bind("click", "<Button-1>", lambda event: interfacegame.highlightCase(event, gamedata, classmap))

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



def typetoimg(type, ts):
	####################
	# Fonction qui va renvoyer une image selon le type envoyer en entré
	# l'image est resize à la taille d'une tuile
	####################

	img = ""

	if type == "mountains":
		img = data.loadtexture("/asset/texture/terrain/mountains/mountains_inner.png", ts)
	elif type == "forest":
		img = data.loadtexture("/asset/texture/terrain/conifer_forest/conifer_forest_inner.png", ts)
	elif type == "plains":
		img = data.loadtexture("/asset/texture/terrain/plains/plains.png", ts)
	elif type == "ocean":
		img = data.loadtexture("/asset/texture/terrain/ocean/ocean_inner.png", ts)
	return img


def typetoimgdico(dico_file, type, ts):
	####################
	# Fonction qui va renvoyer une image selon le type envoyer en entré et le dico
	# l'image est resize à la taille d'une tuile
	####################

	img = ""

	if type == "mountains":
		img = data.loadtexturefromdico(dico_file, "mountains_inner.png", type, ts)[1]
	elif type == "forest":
		img = data.loadtexturefromdico(dico_file, "conifer_forest_inner.png", type, ts)[1]
	elif type == "plains":
		img = data.loadtexturefromdico(dico_file, "plains.png", type, ts)[1]
	elif type == "ocean":
		img = data.loadtexturefromdico(dico_file, "ocean_inner.png", type, ts)[1]
	return img

###########################################################################

######################### Autre Fonction #########################
def infovillage(village):
	log.log.printinfo(f"village name {village.name}")
	if village.lord != 0:
		log.log.printinfo(f"village lord:  {village.lord.lordname}")
	else:
		log.log.printinfo(f"village lord: Indépendant")
	if village.priest != 0:
		log.log.printinfo(f"village priest:  {village.priest.name}")
	else:
		log.log.printinfo(f"village priest: 0")
	log.log.printinfo(f"village global joy: {village.global_joy}")
	log.log.printinfo(f"village ressource, money:  {village.prod_ressource}, {village.prod_money}")


