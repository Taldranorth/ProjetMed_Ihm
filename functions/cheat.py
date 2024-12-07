import tkinter


import functions.log as log
import functions.game as game
import functions.interfacemenu as interfacemenu



######################### Menu Cheat #########################

def cheat_menu(gamedata, classmap, option, root):
	###############
	# Fonction pour créer le menu Cheat
	###############
	cheat_window = tkinter.Toplevel(root)

	cheat_menu_frame = tkinter.Frame(cheat_window)
	cheat_menu_frame.grid()

	tkinter.Label(cheat_menu_frame, text= "Menu Cheat").grid(row = 0, column = 0)

	button_victory = tkinter.Button(cheat_menu_frame, text = "Victoire", command = lambda: cheat_victory(gamedata, classmap, option))
	button_victory.grid(row = 1, column = 0)


def cheat_victory(gamedata, classmap, option):
	#####
	# Fonction pour cheat et terminé la partie comme Gagnant
	#####

	gamedata.victory = "Victoire"
	game.endofgame(gamedata, classmap, option)

