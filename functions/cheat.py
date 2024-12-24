import tkinter

import functions.log as log
import functions.game as game
import functions.common as common
import functions.genproc as genproc
import functions.affichage as affichage
import functions.interfacemenu as interfacemenu

import matplotlib.pyplot as plt

global active
global cheat_window

######################### Menu Cheat #########################

def changestate(gamedata, classmap, option, root, state):
	global active
	global cheat_window
	active = state

	if classmap.mapcanv != 0:
		if active == True:
			cheat_menu(gamedata, classmap, option, root, classmap.mapcanv.winfo_toplevel())
		else:
			destroy_cheat_menu(cheat_window)


def cheat_menu(gamedata, classmap, option, root, win):
	###############
	# Fonction pour créer le menu Cheat
	###############
	global cheat_window
	cheat_window = tkinter.Toplevel(root)
	cheat_window.transient(win)

	cheat_menu_frame = tkinter.Frame(cheat_window)
	cheat_menu_frame.grid()

	tkinter.Label(cheat_menu_frame, text= "Menu Debug").grid(row = 0, column = 0)

	button_victory = tkinter.Button(cheat_menu_frame, text = "Victoire", command = lambda: cheat_victory(gamedata, classmap, option))
	button_victory.grid(row = 1, column = 0)

	button_destroy = tkinter.Button(cheat_menu_frame, text = "Détruire Capitale", command = lambda: cheat_destroy(gamedata, classmap, option, gamedata.list_lord[gamedata.playerid]))
	button_destroy.grid(row = 2, column = 0)

	button_plotlibpic = tkinter.Button(cheat_menu_frame, text = "afficher NoiseMap Plotlib", command = lambda: plotlib(gamedata, classmap, option))
	button_plotlibpic.grid(row = 3, column = 0)

def cheat_victory(gamedata, classmap, option):
	#####
	# Fonction pour cheat et terminé la partie comme Gagnant
	#####

	gamedata.victory = "Victoire"
	game.endofgame(gamedata, classmap, option)

def cheat_destroy(gamedata, classmap, option, lord):
	#####
	# Fonction pour cheat et détruire le village principale du  Seigneur donné
	#####
	log.log.printinfo(f"On supprime la capitale du Seigneur {lord.lordname}")
	village = lord.fief[0]
	# On supprime sa Bordure
	affichage.delborder(classmap, village)
	idvillage = common.coordmaptoidtuile(classmap, [village.x, village.y])
	lord.removefief(village)
	classmap.removeidvillage(idvillage)


def plotlib(gamedata, classmap, option):
	#####
	# Fonction pour cheat qui affiche la noise map via Plotlib
	#####
	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, classmap.mapx, classmap.mapy)
	plt.imshow(pic, cmap='gray')
	plt.show()


def destroy_cheat_menu(cheat_window):
	#####
	# Fonction pour détruire le menu de cheat
	#####
	cheat_window.destroy()




######\ Main \######
active = True




