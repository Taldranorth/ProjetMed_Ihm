
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
import functions.cheat as cheat
import functions.common as common
import functions.savegame as save
import functions.genproc as genproc
import functions.moveview as moveview
import functions.gameclass as gameclass
import functions.affichage as affichage
import functions.interfacegame as interfacegame
import functions.interfacemenu as interfacemenu

######################### Menu Principale #########################

def mainmenu(gamedata, classmap, option, root):
	# Création de la fenêtre
	global mainmenuwin
	mainmenuwin = tkinter.Toplevel(root, height = option.heightWindow, width = option.widthWindow)
	# On centre la fenêtre
	# Pourquoi ?
	log.log.printinfo(f"{option.heightWindow}x{option.widthWindow}+{option.heightWindow//4}+{option.widthWindow//2}")
	mainmenuwin.geometry(f"+{int(option.widthWindow*0.45)}+{option.heightWindow//4}")

	# Création de la frame
	fmainm = tkinter.Frame(mainmenuwin, height = option.heightWindow, width = option.widthWindow)
	fmainm.pack(expand="True", fill="both")

	# Mise en Place des Menus

	# Button Play
	Button_mainm_Play = tkinter.Button(fmainm, command = lambda : playmenu(mainmenuwin, gamedata, classmap, option, root), text = "Jouer")

	# Button Quickplay
	Button_mainm_QuickPlay = tkinter.Button(fmainm, command = lambda: game.initgame(mainmenuwin, gamedata, classmap, option, root, 5), text = "Partie Rapide")

	# Button Load
	#Button_mainm_load = tkinter.Button(fmainm, command=lambda: save.load_game_and_start(gamedata, classmap, option, root, mainmenuwin), text="Load")
	Button_mainm_load = tkinter.Button(fmainm, command = lambda: loadmenu(mainmenuwin, gamedata, classmap, option, root) , text = "Load")

	#Button Options
	Button_mainm_option = tkinter.Button(fmainm, command = lambda: optionmenu(gamedata, classmap, option, root, mainmenuwin), text = "Options")

	#Button Exit
	Button_mainm_exit = tkinter.Button(fmainm, command = exit, text = "Quitter")

	#Pack des Button
	Button_mainm_Play.pack()
	Button_mainm_QuickPlay.pack()
	Button_mainm_load.pack()
	Button_mainm_option.pack()
	Button_mainm_exit.pack()

	tooltip(Button_mainm_Play, "Menu Partie", [])

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
	mainmenuwin.geometry(f"+{option.widthWindow//4}+{option.heightWindow//8}")


	########################\ Minimap \##############################
	# Frame dans lequel on va afficher la version réduite de la carte
	canvasframeminimap = tkinter.Frame(fplaymenu, height = option.heightWindow/4, width = option.widthWindow/4)
	canvasframeminimap.grid(row = 0, columnspan = 5)

	# Canvas de la minimap
	mapcanv = tkinter.Canvas(canvasframeminimap)

	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, classmap.mapx, classmap.mapy)
	# Fonction qui gen la mini carte
	previewmap(mapcanv, pic, classmap.mapx, classmap.mapy)
	##################################################################

	########################\ Seed \##################################
	#txt variable seed
	tkvar_seed = tkinter.IntVar()
	tkvar_seed.set(gamedata.seed)

	# Button pour générer un nouveau seed ce qui vient update automatiquement la carte
	Button_playmenu_newseed = tkinter.Button(fplaymenu ,command = lambda: regenseed(gamedata, classmap, option,tkvar_seed, mapcanv), text = "Genérer nouvelle Seed")
	Button_playmenu_newseed.grid(row = 1, columnspan = 5)

	tkinter.Label(fplaymenu, text = "Graine: ").grid(row = 2, column = 1, columnspan = 2)
	# Entry widget qui affiche la seed, permet de la modif et de la copier
	entryseed = tkinter.Entry(fplaymenu, textvariable = tkvar_seed)
	entryseed.grid(row = 2, column = 2, columnspan = 2)
	button_entryseed = tkinter.Button(fplaymenu, command = lambda: validate_entry_seed(entryseed, gamedata, classmap, option, tkvar_seed, mapcanv), text = "changer")
	button_entryseed.grid(row = 2, column = 3, columnspan = 2)
	##################################################################

	########################\ Map Size \##############################
	#txt variable mapx mapy
	tkvar_mapx = tkinter.IntVar()
	tkvar_mapx.set(classmap.mapx)
	tkvar_mapy = tkinter.IntVar()
	tkvar_mapy.set(classmap.mapy)

	# Label
	tkinter.Label(fplaymenu, text = "Largeur Carte: ").grid(row = 3, column = 0)
	# Entry widget qui affiche la taille en x et y 
	entrymapx = tkinter.Entry(fplaymenu, textvariable = tkvar_mapx)
	entrymapx.grid(row = 3, column = 1)
	tkinter.Label(fplaymenu, text = "Hauteur Carte: ").grid(row = 3, column = 2)
	entrymapy = tkinter.Entry(fplaymenu, textvariable = tkvar_mapy)
	entrymapy.grid(row = 3, column = 3)
	button_entrymap = tkinter.Button(fplaymenu, command = lambda: validate_entry_map(entrymapx, entrymapy, gamedata, classmap, option, tkvar_mapx, tkvar_mapy, mapcanv), text = "changer")
	button_entrymap.grid(row = 3, column = 4)
	##################################################################

	########################\ Village Neutre \########################

	tkvar_neutralvill = tkinter.IntVar()
	tkvar_neutralvill.set(5)
	#Label
	tkinter.Label(fplaymenu, text = "Nb Village Neutre: ").grid(row = 4, column = 1)
	# Entry
	entryneutralvill = tkinter.Entry(fplaymenu, textvariable = tkvar_neutralvill)
	entryneutralvill.grid(row = 4, column = 2)

	##################################################################

	########################\ Liste Seigneurs \#######################
	# On affiche la liste des seigneurs actuellement créer
	tkinter.Label(fplaymenu, text = "liste des Seigneur: ").grid(row = 5, columnspan = 5)

	fplaymenu_frame_listlord = tkinter.Frame(fplaymenu)
	fplaymenu_frame_listlord.grid(row = 7, columnspan = 5)

	#txt variable nom joueur
	tkvar_playername = tkinter.StringVar()
	tkvar_playername.set(gamedata.list_lord[gamedata.playerid].lordname)
	for lord in gamedata.list_lord:
		# Si c'est le joueur on met affiche un label Player est on met en place un Entry afin de pouvoir modifier le nom du Seigneur
		if lord.player == True:
			tkinter.Label(fplaymenu, text = "Seigneur Joueur:").grid(row = 6, column = 1)
			entryplayername = tkinter.Entry(fplaymenu, textvariable = tkvar_playername)
			entryplayername.grid(row = 6, column = 2)
			tkinter.Button(fplaymenu, text = "changer", command = lambda: validate_entry_lordname(gamedata, tkvar_playername, mapcanv)).grid(row = 6, column = 3)
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
	Button_playmenu_play = tkinter.Button(fplaymenu, command = lambda: game.initgame(mainmenuwin, gamedata, classmap, option, root, int(tkvar_neutralvill.get())),text = "Jouer")
	Button_playmenu_play.grid(columnspan = 5)

	# Boutton pour revenir en arrière
	Button_playmenu_return = tkinter.Button(fplaymenu, command = lambda: returntomainmenu(gamedata, classmap, option, mainmenuwin, root),text = "Retour")
	Button_playmenu_return.grid(columnspan = 5)

def validate_entry_map(entrymapx, entrymapy, gamedata, classmap, option, tkvar_mapx, tkvar_mapy, mapcanv):
	classmap.mapx = int(entrymapx.get())
	classmap.mapy = int(entrymapy.get())

	tkvar_mapx.set(classmap.mapx)
	tkvar_mapy.set(classmap.mapy)

	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, classmap.mapx, classmap.mapy)
	previewmap(mapcanv, pic, classmap.mapx, classmap.mapy)
	coordmouse = mapcanv.winfo_pointerxy()
	temp_message(mapcanv, "Changer", 1000, coordmouse, "green")

def validate_entry_seed(entryseed, gamedata, classmap, option, tkvar_seed, mapcanv):
	####################
	# Fonction pour changer automatiquement la seed stocker dans gamedata, tkvar_seed et la minimap
	####################
	gamedata.seed = float(entryseed.get())
	tkvar_seed.set(gamedata.seed)
	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, classmap.mapx, classmap.mapy)
	previewmap(mapcanv, pic, classmap.mapx, classmap.mapy)
	coordmouse = mapcanv.winfo_pointerxy()
	temp_message(mapcanv, "Changer", 1000, coordmouse, "green")

def validate_entry_lordname(gamedata, tkvar_playername, mapcanv):
	####################
	# Fonction pour changer le nom du seigneur player
	####################
	gamedata.list_lord[gamedata.playerid].lordname = tkvar_playername.get()
	coordmouse = mapcanv.winfo_pointerxy()
	temp_message(mapcanv, "Changer", 1000, coordmouse, "green")

def regenseed(gamedata, classmap, option, tkvar_seed, mapcanv):
	####################
	# Fonction associer à un bouton pour random la seed et changer la minimap
	####################

	gamedata.seed = random.random()*time()
	tkvar_seed.set(gamedata.seed)
	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, classmap.mapx, classmap.mapy)
	previewmap(mapcanv, pic, classmap.mapx, classmap.mapy)

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
			tl = tuilesquare(pic[y][x])
			mapcanv.create_rectangle((x*2), y*2, (x*2)+2, (y*2)+2, fill=tl, tags = "minimap", outline='black')

	mapcanv.pack(expand = "True",fill="both")

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
		#log.log.printinfo(f"{frame_listlord.winfo_children()}")
		# On retire le seigneur de la liste
		frame_listlord.winfo_children()[-1].destroy()
	else:
		log.log.printerror("Il ne reste plus que le joueur")

def returntomainmenu(gamedata, classmap, option, menu, root):
	######
	# Fonction Global Pour retourner sur le Menu principale
	######
	mainmenu(gamedata, classmap, option, root)
	menu.destroy()

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

def savemenu(win, gamedata, classmap, option, root):
	######
	# Fonction. pour gérer l'affichage du Menu de Sauvegarde
	######
	# Affiche dans une Listbox toute les Saves trouvés
	# - Un fichier Save porte l'extension .save
	######

	c_d = os.getcwd()
	p_f = c_d + "/user/save"

	# On met en place la fenêtre
	savemenuwin = tkinter.Toplevel()
	# On place la fenêtre
	savemenuwin.geometry(f"+{int(option.widthWindow*0.4)}+{option.heightWindow//4}")
	# On la rend passagère
	savemenuwin.transient(win)

	# On met en place l'interface
	fsavemenu = tkinter.Frame(savemenuwin, height = option.heightWindow, width = option.widthWindow)
	fsavemenu.grid()

	tkinter.Label(fsavemenu, text = "Liste des Sauvegardes").grid(row = 0, column = 0)

	# On setup la Scrollbar de la listbox
	yscrollbar = tkinter.Scrollbar(fsavemenu, orient = tkinter.VERTICAL)
	yscrollbar.grid(row = 1, column = 1, sticky= tkinter.W+ tkinter.N + tkinter.S)

	# On setup la Listbox
	lbsave = tkinter.Listbox(fsavemenu, yscrollcommand = yscrollbar.set)
	lbsave.grid(row = 1, column = 0)

	yscrollbar["command"] = lbsave.yview

	i = 2
	for file in os.listdir(p_f):
		# Si le Fichier est bien une save
		if file[-5:] == ".save":
			# On insert la save dans le Label
			# [NomSave, DateSauvegarde, NomSeigneurJoueur]
			lbsave.insert(0, f"{file[:-5]}")
			i += 1

	# On met en place les bouttons
	Bcreatesave = tkinter.Button(fsavemenu, text = "Créer une Nouvelle Sauvegarde", command = lambda: savemenu_save(gamedata, classmap, option, True, lbsave, p_f))
	Bcreatesave.grid(row = i, column = 0)
	Breplacesave = tkinter.Button(fsavemenu, text = "Écraser la Sauvegarde", command = lambda: savemenu_save(gamedata, classmap, option, False, lbsave, p_f))
	Breplacesave.grid(row = i+1, column = 0)
	# On met en place le Bouttons de Retour
	Breturn = tkinter.Button(fsavemenu, text = "Retour", command = lambda: exitmenu(savemenuwin))
	Breturn.grid(row = i+2, column = 0)

def loadmenu(win, gamedata, classmap, option, root):
	######
	# Fonction pour gèrer l'affichage du Menu de Chargement de Données
	######
	# Affiche dans une Listbox toute les Saves trouvés
	# - Un fichier Save porte l'extension .save
	######

	c_d = os.getcwd()
	p_f = c_d + "/user/save"

	# On met en place la fenêtre
	loadmenuwin = tkinter.Toplevel()
	# On place la fenêtre
	loadmenuwin.geometry(f"+{int(option.widthWindow*0.4)}+{option.heightWindow//4}")
	# On la rend passagère
	loadmenuwin.transient(win)

	# On met en place l'interface
	floadmenu = tkinter.Frame(loadmenuwin, height = option.heightWindow, width = option.widthWindow)
	floadmenu.grid()

	tkinter.Label(floadmenu, text = "Charger Une Sauvegarde").grid(row = 0, column = 0)

	# On setup la Scrollbar de la listbox
	yscrollbar = tkinter.Scrollbar(floadmenu, orient = tkinter.VERTICAL)
	yscrollbar.grid(row = 1, column = 1, sticky= tkinter.W+ tkinter.N + tkinter.S)

	# On setup la Listbox
	lbsave = tkinter.Listbox(floadmenu, yscrollcommand = yscrollbar.set)
	lbsave.grid(row = 1, column = 0)

	yscrollbar["command"] = lbsave.yview

	i = 2
	for file in os.listdir(p_f):
		# Si le Fichier est bien une save
		if file[-5:] == ".save":
			# On insert la save dans le Label
			# [NomSave, DateSauvegarde, NomSeigneurJoueur]
			lbsave.insert(0, f"{file[:-5]}")
			i += 1

	# On met en place les bouttons
	Bload = tkinter.Button(floadmenu, text = "Charger la Sauvegarde", command = lambda: loadmenu_load(gamedata, classmap, option, lbsave, win, loadmenuwin, root, p_f))
	Bload.grid(row = i, column = 0)
	# On met en place le Bouttons de Retour
	Breturn = tkinter.Button(floadmenu, text = "Retour", command = lambda: exitmenu(loadmenuwin))
	Breturn.grid(row = i+1, column = 0)

def savemenu_save(gamedata, classmap, option, newsave:bool, lbsave, savefolderpath):
	####
	# Fonction Pour gérer la Sauvegarde
	####
	# newsave = True si on créer une nouvelle save
	# newsave = False si on écrase une save
	####
	coord = [int(option.widthWindow*0.4), option.heightWindow//8]
	if newsave == False:
		if len(lbsave.curselection()) > 0:
			filename = lbsave.get(lbsave.curselection()[0])
			filename += ".save"
			save.save_game(gamedata, classmap, option, savefolderpath+"/"+filename)
		else:
			interfacemenu.temp_message(classmap.mapcanv, "Pas de fichier de Sauvegarde sélectionner", 2000, coord, "red")
			return
	else:
		player = gamedata.list_lord[gamedata.playerid]
		nb = 0
		# on calcul le nom de la save
		# NomSeigneurJoueur/N°Save/date/Automatique
		# On recup le nombre de save que le joueur possède avec se nom de seigneur
		for file in os.listdir(savefolderpath):
			if player.lordname in file:
				nb += 1
		# On créer la chaîne de charac
		filename = player.lordname + f"{nb}"+"manuel"+".save"
		# On lance la save
		save.save_game(gamedata, classmap, option, savefolderpath+"/"+filename)
		# On update la listbox
		lbsave.insert(0, f"{filename[:-5]}")

	coord = [option.widthWindow//2, option.heightWindow//8]
	interfacemenu.temp_message(classmap.mapcanv, "Fichier Sauvegarder", 2000, coord, "green")



def loadmenu_load(gamedata, classmap, option, lbsave, win, winmenu, root, filepath):
	####
	# Fonction Pour gérer le Chargement de la Save Selon la listbox
	####
	coord = [option.widthWindow//2, option.heightWindow//8]
	if len(lbsave.curselection())>0:
		# On recup le nom du fichier
		filename = lbsave.get(lbsave.curselection()[0])
		filename += ".save"
		# On lance le chargement de la save
		save.load_game_and_start(gamedata, classmap, option, root, win, filepath + "/" + filename)
		# On détruit l'écran de chargement de save
		exitmenu(winmenu)

	else:
		interfacemenu.temp_message(classmap.mapcanv, "Pas de fichier de Sauvegarde sélectionner", 2000, coord, "red")
		return

def exitmenu(win):
	#####
	# Fonction générale pour quitter un menu
	#####
	win.destroy()



###########################################################################

######################### Menu Option #########################

###############
# Fonction appeler pour afficher le menu des Options 
# On l'affiche par dessus le menu Principale
#
###############


def optionmenu(gamedata, classmap, option, root, win):
	#####
	# Fonction appeler pour afficher le menu des Options 
	#####
	# Ce menu va servir à configurer les paramètre globaux de l'application ainsi que les touches, voir à afficher les Combinaisons de touches
	#####
	c_d = os.getcwd()

	# On met en place la fenêtre
	optionmenuwin = tkinter.Toplevel()
	# On place la fenêtre
	optionmenuwin.geometry(f"+{int(option.widthWindow*0.4)}+{option.heightWindow//4}")
	# On la rend passagère
	optionmenuwin.transient(win)

	foptionmenu = tkinter.Frame(optionmenuwin)
	foptionmenu.grid()

	tkinter.Label(foptionmenu, text = "Résolution").grid(row = 1, column = 0)
	# Tvariable nécessaires au Menu Boutton
	Tvar_res = tkinter.StringVar()
	Tvar_res.set(f"{option.widthWindow}x{option.heightWindow}")

	# On affiche un Menu Boutton pour les résolutions
	Bmenures = tkinter.Menubutton(foptionmenu, textvariable = Tvar_res)
	Bmenures.grid(row = 2, column = 0)
	# On créer un Menu pour les résolutions
	menures = tkinter.Menu(Bmenures)
	Bmenures["menu"] = menures
	# On config le menu
	for res in ([800,600],[1280,800],[1440,900],[1920,1200],[2560,1440]):
		menures.add_command(label = f"{res[0]}x{res[1]}", command = lambda: option_change_res(option, res[0], res[1], Tvar_res))

	# On permet à l'utilisateur d'entré par lui même une résolution


	# On affiche la résolution conseillé par tkinter
	tkinter.Label(foptionmenu, text = f"Résolution Conseillé: {win.winfo_screenwidth()}x{win.winfo_screenheight()}").grid(row = 4, column = 0)
	# On affiche un boutton pour reset
	Breset_res = tkinter.Button(foptionmenu, text = "Reset Résolution", command = lambda: option_reset_res(option, root, Tvar_res))
	Breset_res.grid(row = 5, column = 0)



	tkinter.Label(foptionmenu, text = "DebugMenu On/off").grid(row = 6, column = 0)
	# Boutton pour Activer/Désactiver le menu Debug
	tkinter.Radiobutton(foptionmenu, text = "On", command = lambda: cheat.changestate(gamedata, classmap, option, root, True)).grid(row = 7, column = 0)
	tkinter.Radiobutton(foptionmenu, text = "off", command = lambda: cheat.changestate(gamedata, classmap, option, root, False)).grid(row = 8, column = 0)

	# Boutton pour sauvegarder les options
	Bsave_option = tkinter.Button(foptionmenu, text = "Sauvegarder Option", command = lambda: option.saveoption(c_d+"/user/"+"config.ini"))
	Bsave_option.grid(row = 9, column = 0)

	# Boutton pour quitter
	Bexit = tkinter.Button(foptionmenu, text = "retour", command = lambda: exitmenu(optionmenuwin))
	Bexit.grid(row = 10, column = 0)

def option_change_res(option, newwidth, newheight, Tvar_res):
	#####
	# Fonction pour changer la résolution stocker dans option, l'appliqué et changer la variable Tvar
	#####

	# On change les variables
	option.widthWindow = newwidth
	option.heightWindow = newheight
	log.log.printinfo(f"Nouvelle Résolution: {option.widthWindow}x{option.heightWindow}")
	# On applique le changement de Résolution


	# On update la Tvar
	Tvar_res.set(f"{option.widthWindow}x{option.heightWindow}")

def option_reset_res(option, root, Tvar_res):
	#####
	# Fonction pour reset la résolution stocker
	#####

	if (len(sys.argv) >= 2 ) and (str(sys.argv[1]) == "-SR"):
		[height, width] = [1400, 1440]
	else:
		[height, width] = [root.winfo_screenheight(),root.winfo_screenwidth()]

	option.widthWindow = width
	option.heightWindow = height


	# On update la Tvar
	Tvar_res.set(f"{option.widthWindow}x{option.heightWindow}")

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

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child, height = (0.4* option.heightWindow)+10, width = (0.6*option.widthWindow)+10)
	canvas.grid(row = 2, column = 0, columnspan = len(gamedata.list_lord))

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color, command = lambda name = lord.lordname: disablegraph(canvas, name)).grid(row = 1, column = i)
		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Croissance Militaire").grid(row = 0,column = 0, columnspan = i)

	# On récupère le nbmax de tour
	if gamedata.nb_turn > 20:
		turnmax = gamedata.nb_turn
	else:
		turnmax = 20
	# On calcul la taille d'une case en X
	sqx = ((0.6*option.widthWindow))//turnmax
	print("sizesquarex: ", sqx)
	# échelle 5
	# On calcul la taille d'une case en Y
	sqy = (0.4* option.heightWindow)//100

	# On créer l'échelle haut
	for x in range(1, turnmax+1):
		canvas.create_text(x*sqx, (0.4* option.heightWindow), text = x)

	# On créer l'échelle bas
	for y in range(5,100,5):
		canvas.create_text(10, ((0.4* option.heightWindow)-10)-(y*sqy), text = y)

	for lord in gamedata.list_lord:
		color = lord.color
		for turn in stats.dico_stat.dico_stat[lord.lordname]:
			# On recup le tour
			t = turn[0]
			# On recup la stat Militaire du tour
			power = turn[1]["Military"][0]
			nbarmy = turn[1]["Military"][1]
			x = (t*sqx)+20
			y = (0.4* option.heightWindow)-10
			x2 = (t*sqx)+sqx+20
			print(x,x2)
			y2 = ((0.4* option.heightWindow)-20) - ((power*sqy) + 20)
			square = canvas.create_rectangle( x, y, x2, y2, outline = color, tags = [lord.lordname])

	# On créer un Cadre
	canvas.create_rectangle(20, 20,(0.6*option.widthWindow), (0.4* option.heightWindow)-10)

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

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child, height = (0.4* option.heightWindow)+10, width = (0.6*option.widthWindow)+10)
	canvas.grid(row = 2, column = 0, columnspan = len(gamedata.list_lord))

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color, command = lambda name = lord.lordname: disablegraph(canvas, name)).grid(row = 1, column = i)
		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Croissance Démographique").grid(row = 0,column = 0, columnspan = i)

	# On récupère le nbmax de tour
	if gamedata.nb_turn > 20:
		turnmax = gamedata.nb_turn
	else:
		turnmax = 20
	# On calcul la taille d'une case en X
	sqx = ((0.6*option.widthWindow))//turnmax
	print("sizesquarex: ", sqx)
	# échelle 5
	# On calcul la taille d'une case en Y
	sqy = (0.4* option.heightWindow)//100

	# On créer l'échelle haut
	for x in range(1, turnmax+1):
		canvas.create_text(x*sqx, (0.4* option.heightWindow), text = x)

	# On créer l'échelle bas
	for y in range(5,100,5):
		canvas.create_text(10, ((0.4* option.heightWindow)-20)-(y*sqy), text = y)

	for lord in gamedata.list_lord:
		color = lord.color
		for turn in stats.dico_stat.dico_stat[lord.lordname]:
			#print("turn: ",turn)
			# On recup le tour
			t = turn[0]
			# On recup la stat Militaire du tour
			nbpop = turn[1]["Demography"][0]
			x = (t*sqx)+20
			y = (0.4* option.heightWindow)-10
			x2 = (t*sqx)+sqx+20
			print(x,x2)
			y2 = ((0.4* option.heightWindow)-20) - ((nbpop*sqy) + 20)
			square = canvas.create_rectangle( x, y, x2, y2, outline = color, tags = [lord.lordname])

	# On créer un Cadre
	canvas.create_rectangle(20, 20,(0.6*option.widthWindow), (0.4* option.heightWindow)-10)

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

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child, height = (0.4* option.heightWindow)+10, width = (0.6*option.widthWindow)+10)
	canvas.grid(row = 2, column = 0, columnspan = len(gamedata.list_lord))

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color, command = lambda name = lord.lordname: disablegraph(canvas, name)).grid(row = 1, column = i)
		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Croissance Économique").grid(row = 0,column = 0, columnspan = i)

	# On récupère le nbmax de tour
	if gamedata.nb_turn > 20:
		turnmax = gamedata.nb_turn
	else:
		turnmax = 20
	# On calcul la taille d'une case en X
	sqx = ((0.6*option.widthWindow))//turnmax
	print("sizesquarex: ", sqx)
	# échelle 5
	# On calcul la taille d'une case en Y
	sqy = (0.4* option.heightWindow)//100

	# On créer l'échelle haut
	for x in range(1, turnmax+1):
		canvas.create_text(x*sqx, (0.4* option.heightWindow), text = x)

	# On créer l'échelle bas
	for y in range(5,100,5):
		canvas.create_text(10, ((0.4* option.heightWindow)-20)-(y*sqy), text = y)

	for lord in gamedata.list_lord:
		color = lord.color
		for turn in stats.dico_stat.dico_stat[lord.lordname]:
			#print("turn: ",turn)
			# On recup le tour
			t = turn[0]
			# On recup la stat Militaire du tour
			power = turn[1]["Military"][0]
			nbarmy = turn[1]["Military"][1]
			x = (t*sqx)+20
			y = (0.4* option.heightWindow)-10
			x2 = (t*sqx)+sqx+20
			print(x,x2)
			y2 = ((0.4* option.heightWindow)-20) - ((power*sqy) + 20)
			square = canvas.create_rectangle( x, y, x2, y2, outline = color, tags = [lord.lordname])

	# On créer un Cadre
	canvas.create_rectangle(20, 20,(0.6*option.widthWindow), (0.4* option.heightWindow)-10)

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

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child, height = (0.4* option.heightWindow)+10, width = (0.6*option.widthWindow)+10)
	canvas.grid(row = 2, column = 0, columnspan = len(gamedata.list_lord))

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color, command = lambda name = lord.lordname: disablegraph(canvas, name)).grid(row = 1, column = i)
		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Score").grid(row = 0,column = 0, columnspan = i)

	# On récupère le nbmax de tour
	if gamedata.nb_turn > 20:
		turnmax = gamedata.nb_turn
	else:
		turnmax = 20
	# On calcul la taille d'une case en X
	sqx = ((0.6*option.widthWindow))//turnmax
	print("sizesquarex: ", sqx)
	# échelle 5
	# On calcul la taille d'une case en Y
	sqy = (0.4* option.heightWindow)//100

	# On créer l'échelle haut
	for x in range(1, turnmax+1):
		canvas.create_text(x*sqx, (0.4* option.heightWindow), text = x)

	# On créer l'échelle bas
	for y in range(5,100,5):
		canvas.create_text(10, ((0.4* option.heightWindow)-20)-(y*sqy), text = y)

	for lord in gamedata.list_lord:
		color = lord.color
		for turn in stats.dico_stat.dico_stat[lord.lordname]:
			#print("turn: ",turn)
			# On recup le tour
			t = turn[0]
			# On recup la stat Militaire du tour
			score = turn[1]["Score"][0]
			x = (t*sqx)+20
			y = (0.4* option.heightWindow)-10
			x2 = (t*sqx)+sqx+20
			print(x,x2)
			y2 = ((0.4* option.heightWindow)-20) - ((score*sqy) + 20)
			square = canvas.create_rectangle( x, y, x2, y2, outline = color, tags = [lord.lordname])

	# On créer un Cadre
	canvas.create_rectangle(20, 20,(0.6*option.widthWindow), (0.4* option.heightWindow)-10)

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

	# On créer le Canvas
	canvas = tkinter.Canvas(frame_eof_screen_up_child, height = (0.4* option.heightWindow)+10, width = (0.6*option.widthWindow)+10)
	canvas.grid(row = 2, column = 0, columnspan = len(gamedata.list_lord))

	i = 0
	for lord in gamedata.list_lord:
		# On Met en place bouton pour pouvoir désactiver l'affichage de la courbe du Seigneur
		tkinter.Button(frame_eof_screen_up_child, text = lord.lordname, fg = lord.color, command = lambda name = lord.lordname: disablegraph(canvas, name)).grid(row = 1, column = i)
		i +=1

	# Label de la Fenêtre
	tkinter.Label(frame_eof_screen_up_child, text = f"Mort").grid(row = 0,column = 0, columnspan = i)

	# On récupère le nbmax de tour
	if gamedata.nb_turn > 20:
		turnmax = gamedata.nb_turn
	else:
		turnmax = 20
	# On calcul la taille d'une case en X
	sqx = ((0.6*option.widthWindow))//turnmax
	print("sizesquarex: ", sqx)
	# échelle 5
	# On calcul la taille d'une case en Y
	sqy = (0.4* option.heightWindow)//100

	# On créer l'échelle haut
	for x in range(1, turnmax+1):
		canvas.create_text(x*sqx, (0.4* option.heightWindow), text = x)

	# On créer l'échelle bas
	for y in range(5,100,5):
		canvas.create_text(10, ((0.4* option.heightWindow)-20)-(y*sqy), text = y)

	for lord in gamedata.list_lord:
		color = lord.color
		for turn in stats.dico_stat.dico_stat[lord.lordname]:
			#print("turn: ",turn)
			# On recup le tour
			t = turn[0]
			# On recup la stat Militaire du tour
			death = turn[1]["Death"]
			x = (t*sqx)+20
			y = (0.4* option.heightWindow)-10
			x2 = (t*sqx)+sqx+20
			print(x,x2)
			y2 = ((0.4* option.heightWindow)-20) - ((death*sqy) + 20)
			square = canvas.create_rectangle( x, y, x2, y2, outline = color, tags = [lord.lordname])

	# On créer un Cadre
	canvas.create_rectangle(20, 20,(0.6*option.widthWindow), (0.4* option.heightWindow)-10)

def disablegraph(canvas, lordname):
	######
	# Fonction pour désactiver, réactiver le graphe du Seigneur
	######
	lcanvasobject = canvas.find_withtag(lordname)
	#print("lcanvasobject:", lcanvasobject)
	#print(lordname)
	for ele in lcanvasobject:
		if canvas.itemcget(ele,"state") == "hidden":
			canvas.itemconfigure(ele, state = tkinter.NORMAL)
		else:
			canvas.itemconfigure(ele, state = tkinter.HIDDEN)

def exit_mainmenu(gamedata, classmap, option):
	#######
	# Fonction pour retourner aux Menu Principale
	#######

	exit()


###########################################################################

######################### Écran de Jeu #########################
def mainscreen(gamedata, classmap, option, root, pic, NeutralVill, upload_save = False):

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
	interfacegame.gameinterface(gamedata, classmap, option, win1, root)

	fcanvas.pack(expand = True)

	# Carte de Jeu
	createmap(gamedata, classmap, option, pic, win1, upload_save = upload_save)

    # Ne pas regénérer les villages si la partie a déjà été chargée
	if not upload_save:
		# Genération des Villages
		genproc.genVillage(gamedata, classmap, option, NeutralVill)

		# On rempli les villages de pop
		# En début de Game Chaque Village est composé de 10 Pop:
		#	- 8 Paysan
		#	- 2 Artisan
		for village in classmap.lvillages:
			genproc.genpopidvillage(gamedata, classmap, option, village, 8, 2)
	else:
		log.log.printinfo("Chargement de sauvegarde: affichage des villages...	")



	# Affichage des Villages
	affichage.printvillage(gamedata, classmap, option,fcanvas)

	# On affiche les Bordures des villages:
	affichage.bordervillage(gamedata, classmap, option)

	village = gamedata.list_lord[gamedata.playerid].fief[0]
	coordcanvas = common.coordmaptocanvas(gamedata, classmap, option, [village.x, village.y], True)
	# On centre la vue sur le village de départ
	moveview.centerviewcanvas(gamedata, classmap, option, coordcanvas)


	for village in classmap.lvillages:
		infovillage(classmap.listmap[village].village)

	interfacegame.updateinterface(gamedata, classmap)

	# On affiche la légendes des Commandes
	interfacegame.legendginterface(gamedata, classmap, option)

####################################################################################################

######################### Creation de la Carte Canvas #######################################################
def createmap(gamedata, classmap, option, pic, win1, upload_save = False):

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
	
	existing_village = None
	for y in range(classmap.mapy):
		for x in range(classmap.mapx):
			tile_id = common.coordmaptoidtuile(classmap,[x,y])
			# Conservez le village existant s'il y en a un
			existing_tile = classmap.listmap.get(tile_id, None)
			if existing_tile and hasattr(existing_tile, 'village'):
				existing_village = existing_tile.village	
			else:
				None


			##### Version Non-Aléatoire Dico Avec Atlas #####
			#'''
			tl = no_random_tuile(option ,pic, x, y, ts)

			mcanvt = mapcanv.create_image((x*ts)+(ts/2), (y*ts)+(ts/2), image = asset.atlas.dico[tl[0]].image, tags = ["img",tl[1],"tuile","click", x, y, pic[y][x], idtuile])
			#'''
			################################
			##### Version Pseudo-Aléatoire Dico Avec Atlas #####
			'''
			tl = pseudo_random_tuile(option, pic, x, y, ts)
			if tl[1] not in ["mountains_inner.png", "conifer_forest_inner.png", "plains.png", "ocean_inner.png"]:
				asset.atlas.loadtextureatlas(asset.dico_file, ts, "plains.png", "plains")
				mapcanv.create_image((x*ts)+(ts/2), (y*ts)+(ts/2), image = asset.atlas.dico["plains.png"].image, tags = ["img","plains","tuile","click", x, y, pic[y][x], idtuile, "bg"])

			mcanvt = mapcanv.create_image((x*ts)+(ts/2), (y*ts)+(ts/2), image = asset.atlas.dico[tl[0]].image, tags = ["img",tl[1],"tuile","click", x, y, pic[y][x], idtuile])
			'''
			################################

			# On créer une nouvelle instance de la classe tuiles
			instancetuile = data.Classtuiles(tl[0], tl[1], x, y, mcanvt)

			# Si un village existe déjà, l'ajouter
			if existing_village:
				instancetuile.village = existing_village
				print(f"Village {existing_village} restauré sur la tuile")
			else:
				instancetuile.village = None

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
	# Si Mac
	if option.os == "darwin":
		mapcanv.bind('<Shift-ButtonPress-2>', lambda event: moveview.startmoveviewmouse(event))
		mapcanv.bind('<Shift-ButtonRelease-2>', lambda event: moveview.endmoveviewmouse(event))
		mapcanv.bind('<Shift-B2-Motion>', lambda event: moveview.moveviewmouse(event, gamedata, classmap, option))
	else:
		mapcanv.bind('<Shift-ButtonPress-3>', lambda event: moveview.startmoveviewmouse(event))
		mapcanv.bind('<Shift-ButtonRelease-3>', lambda event: moveview.endmoveviewmouse(event))
		mapcanv.bind('<Shift-B3-Motion>', lambda event: moveview.moveviewmouse(event, gamedata, classmap, option))		
	# Si linux

	#ON lie les différentes Cases à l'action click
	mapcanv.tag_bind("click", "<Button-1>", lambda event: interfacegame.highlightCase(event, gamedata, classmap))

	# on termine par pack le mapcanv
	mapcanv.pack(expand ="True", fill = "y")

####################################################################################################

######################### Fonction Création Tuile ############################
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
		return "mountains"
	elif(nb>-0.25 and nb <=0):
		return "forest"
	elif(nb>0 and nb <= 0.25):
		return "plains"
	else:
		return "ocean"

def tuilesquare(nb):
	#####
	# Version qui retourne la carré de la tule
	#####
	if(nb <= -0.25):
		return "grey"
	elif(nb>-0.25 and nb <=0):
		return "green"
	elif(nb>0 and nb <= 0.25):
		return "yellow"
	else:
		return "blue"

def no_random_tuile(option, pic, x, y, ts):
	######
	# Fonction qui charge en mémoire et renvoit la texture de la tuile ciblé + son type
	######

	# On utilise la valeur de la case pour définir la tuile que l'on va créer
	tl = tuile(pic[y][x])

	if tl == "mountains":
		asset.atlas.loadtextureatlas(asset.dico_file, ts, "mountains_inner.png", tl)
		return ["mountains_inner.png", "mountains"]
	elif tl == "forest":
		asset.atlas.loadtextureatlas(asset.dico_file, ts, "conifer_forest_inner.png", tl)
		return ["conifer_forest_inner.png", "forest"]
	elif tl == "plains":
		asset.atlas.loadtextureatlas(asset.dico_file, ts, "plains.png", "plains")
		return ["plains.png", "plains"]
	elif tl == "ocean":
		asset.atlas.loadtextureatlas(asset.dico_file, ts, "ocean_inner.png", tl)
		return ["ocean_inner.png", "ocean"]



def pseudo_random_tuile(option, pic, x, y, ts):
	######
	# Fonction qui charge en mémoire et renvoit la texture de la tuile ciblé + son type
	######

	# On utilise la valeur de la case pour définir la tuile que l'on va créer
	tl = tuile(pic[y][x])

	if tl == "mountains":
		asset.atlas.loadtextureatlas(asset.dico_file, ts, "mountains_inner.png", tl)
		return ["mountains_inner.png", "mountains"]
	elif tl == "forest":
		lntype = neightbours_tuile(option, pic, x, y)
		print(len(lntype[1]))
		print("voisin foret:", lntype[1])
		# Si l'ensemble des coord sont dans forêt alors tout les voisins sont des forêts
		if len(lntype[1]) == (len(lntype[0])+ len(lntype[1]) + len(lntype[2]) + len(lntype[3])):
			asset.atlas.loadtextureatlas(asset.dico_file, ts, "conifer_forest_inner.png", tl)
			return ["conifer_forest_inner.png", "forest"]
		else:
			texture_name = neighbourstotexture(option, x, y, "forest", lntype)
			print("texture: ",texture_name)
			asset.atlas.loadtextureatlas(asset.dico_file, ts, texture_name, "forest")
			return [texture_name, "forest"]
	elif tl == "plains":
		asset.atlas.loadtextureatlas(asset.dico_file, ts, "plains.png", "plains")
		return ["plains.png", "plains"]
	elif tl == "ocean":
		asset.atlas.loadtextureatlas(asset.dico_file, ts, "ocean_inner.png", tl)
		return ["ocean_inner.png", "ocean"]


def neightbours_tuile(option, pic, x, y):
	#####
	# Fonction qui renvoit un tuple qui contient les types des voisin
	# 0 1 2
	# 3   4
	# 5 6 7
	#####
	lntype = [[],[],[],[]]
	for yn in range(-1,2):
		for xn in range(-1,2):
			# On s'assure que les coord ne soit pas hors de la carte
			if(((x+xn) >= 0) and ((x+xn)<classmap.mapx)):
				if(((y+yn) >= 0) and ((y+yn)<classmap.mapy)):
					if ((xn == 0) and (yn == 0)):
						pass
					else:
						#print("x,y: ",xn, yn)
						#print(y+yn, x+xn)
						tl = tuile(pic[y+yn][x+xn])
						if tl == "mountains":
							lntype[0] += [[x+xn,y+yn]]
						elif tl == "forest":
							lntype[1] += [[x+xn,y+yn]]
						elif tl == "plains":
							lntype[2] += [[x+xn,y+yn]]
						elif tl == "ocean":
							lntype[3] += [[x+xn,y+yn]]
	return lntype

def neighbourstotexture(option, x, y , type, lntype):
	#####
	# Fonction qui renvoit une texture selon les voisin et le type
	#####
	# V1: Prend en compte seulement les foret est seulement dans les 4 directions cardinal
	#
	#
	####
	print(x,y)
	print(type)
	print(lntype)
	# Si pour forêt
	if type == "forest":
		print("Type Forêt trouvé")
		# Cardinal North
		if ((y-1) >= 0):
			if [x, y-1] not in lntype[1]:
				print("cardinal North")
				return "conifer_forest_north_1.png"
		# Cardinal Ouest
		if((x-1)>=0):
			if [x-1, y] not in lntype[1]:
				print("cardinal Ouest")
				return "conifer_forest_west_1.png"
		# Cardinal Est
		if ((x+1) < classmap.mapx):
			if [x+1, y] not in lntype[1]:
				print("cardinal Est")
				return "conifer_forest_east_1.png"
		# Cardinal Sud
		if((y+1) < classmap.mapy):
			if [x, y+1] not in lntype[1]:
				print("cardinal Sud")
				return "conifer_forest_south_1.png"
		# Sinon on affiche forêt normal
		print("pas de cardinal trouvé")
		return "conifer_forest_inner.png"


def cardinal(option, x, y, lntype):
	######
	# Fonction qui renvoit une liste contenant les cardinal manquant
	######
	lcardinal = [0,0,0,0,0,0,0,0]
	for yn in range(-1,2):
		for xn in range(-1, 2):
			if((xn== 0) and (yn == 0)):
				pass
			else:
				if (((x+xn)< classmap.mapx) and (x+xn >= 0)):
					if (((y+yn)< classmap.mapy) and (y+yn >= 0)):
						if [x+xn, y+yn] not in lntype:
							pass


######################################################################


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

################## Fonction Pop Up ##################
def tooltip(widget, text, lvariable):
	####
	# Fonction Pour Gérer un tooltip
	####
	# On recup la Top Window
	top_window = widget.winfo_toplevel()
	widget.bind("<Enter>", lambda event: tooltip_create(event, widget, top_window, text, lvariable))

def tooltip_create(event, widget, top_window, text, lvariable):
	####
	# Fonction pour gérer la Création de la fenêtre
	####
	# On recup les coord de la souris
	posmouse = event.widget.winfo_pointerxy()
	# On créer la fenêtre
	windowtooltip = tkinter.Toplevel()
	# On la place
	windowtooltip.geometry(f"+{posmouse[0]+5}+{posmouse[1]+5}")
	# On la rend Transient
	windowtooltip.transient(top_window)
	# On l'overrid
	windowtooltip.overrideredirect(True)
	# On créer le frame dans lequel on ajoute le text
	frame = tkinter.Frame(windowtooltip)
	frame.pack()
	# On traite le texte
	if type(text) == str:
		ch = text
	else:
		ch = ""
		for ele in text:
			if type(ele) == str:
				ch += ele
			else:
				ch += f"{ele}"

	# On y ajoute le texte
	tkinter.Label(frame, text = ch).pack()
	# On bind la destruction quand la souris quitte le widget
	widget.bind("<Leave>", lambda event: tooltip_destroy(event, widget, windowtooltip))
	# On bind la destruction quand le widget est détruit
	widget.bind("<Destroy>", lambda event: tooltip_destroy(event, widget, windowtooltip))

def tooltip_destroy(event, widget, window_tooltip):
	####
	# Fonction pour gérer la destruction de la fenêtre
	####
	#print("On détruit le tooltip")
	window_tooltip.destroy()
	# On retire le Bind
	widget.unbind_all("<Leave>")

################## Fonction Pop Up Canvas ##################
def tooltipcanvas(canvas, idobject, text, lvariable):
	#####
	# Fonction Pour gérer un tooltip Vis à Vis d'un objet
	#####
	# On recup la Top Window
	top_window = canvas.winfo_toplevel()
	canvas.tag_bind(idobject, "<Enter>", lambda event: tooltipcanvas_create(event, canvas, idobject, top_window, text, lvariable))

def tooltipcanvas_create(event, canvas, idobject, top_window, text, lvariable):
	####
	# Fonction pour gérer la Création de la fenêtre
	####
	#print("On créer le Pop-Up")
	# On recup les coord de la souris
	posmouse = event.widget.winfo_pointerxy()
	#print(text)
	#print(lvariable)
	# On créer la fenêtre
	windowtooltip = tkinter.Toplevel()
	# On la place
	windowtooltip.geometry(f"+{posmouse[0]+5}+{posmouse[1]+5}")
	# On la rend Transient
	windowtooltip.transient(top_window)
	# On l'overrid
	windowtooltip.overrideredirect(True)
	# On créer le frame dans lequel on ajoute le text
	frame = tkinter.Frame(windowtooltip)
	frame.pack()
	# On traite le texte
	if type(text) == str:
		ch = text
	else:
		ch = ""
		for ele in text:
			if type(ele) == str:
				ch += ele
			else:
				ch += f"{ele}"

	# On y ajoute le texte
	tkinter.Label(frame, text = ch).pack()
	# On bind la destruction quand la souris quitte le widget
	canvas.tag_bind(idobject, "<Leave>", lambda event: tooltipcanvas_destroy(event, canvas, idobject, windowtooltip))


def tooltipcanvas_destroy(event, canvas, idobject, window_tooltip):
	####
	# Fonction pour gérer la destruction de la fenêtre
	####
	#print("On détruit le tooltip")
	window_tooltip.destroy()
	# On retire le Bind
	canvas.tag_unbind(idobject, "<Leave>")


######################################################

#############\ Fonction Message Temp \################

def temp_message(widget, text, time, coord, color):
	####
	# Fonction pour gérer l'affichage des messages Temporaires
	####
	top_window = widget.winfo_toplevel()
	create_temp_message(widget, top_window, text, time, coord, color)

def create_temp_message(widget, top_window, text, time, coord, color):
	####
	# Fonction Pour créer le Message Temporaire
	####
	# On créer la fenêtre
	window_message = tkinter.Toplevel()
	# On la positionne
	window_message.geometry(f"+{coord[0]}+{coord[1]}")
	# On la transforme en fenêtre Transiant
	window_message.transient(top_window)
	# On override
	window_message.overrideredirect(True)

	frame = tkinter.Frame(window_message)
	frame.pack()
	tkinter.Label(frame, text = text, fg = color, font = ('Helvetica', '16')).pack()

	# On détruit après X temps
	widget.after(time, lambda: destroy_temp_message(window_message))

def destroy_temp_message(window_message):
	####
	# Fonction Pour détruire le message temp
	####
	window_message.destroy()

#############\ Fonction Validation Message \################

def validation_message(widget, text, coord, color):
	####
	# Fonction pour gérer l'affichage des messages Temporaires
	####
	# Prend en Paramètre un tuple tooltip composé du text et des variables utilisé par le text
	#####
	top_window = widget.winfo_toplevel()
	create_validation_message(widget, top_window, text, coord, color)

def create_validation_message(widget, top_window, text, coord, color):
	####
	# Fonction Pour créer le Message à Valider
	####
	# On créer la fenêtre
	window_message = tkinter.Toplevel()
	# On la positionne
	window_message.geometry(f"+{coord[0]}+{coord[1]}")
	# On la transforme en fenêtre Transiant
	window_message.transient(top_window)
	# On override
	window_message.overrideredirect(True)
	# On affiche le Message
	frame = tkinter.Frame(window_message)
	frame.grid()
	tkinter.Label(frame, text = text, fg = color).grid(row = 0, column = 0)
	# On ajoute le Bouton pour valider le Message
	button = tkinter.Button(frame, text = "ok", command = lambda:destroy_validation_message(window_message))
	button.grid(row = 1, column = 0)

def destroy_validation_message(window_message):
	####
	# Fonction Pour détruire le message à Valider
	####
	window_message.destroy()

######################################################


def convertposgraph(coord, heightgraph, widthgraph):
	####
	# Fonction pour obtenir les coordonnés pour afficher sur un Graphe
	####
	posx = coord[0] + 10
	posy = heightgraph - coord[1]


	return [posx,posy]


######################################################
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

