import tkinter






######################### Fonction Interface ############################

def gameinterface(win, heightWindow, widthWindow, gamedata):

	####################
	# Fonction qui met en place l'interface en Jeu, voir l'entête
	# HeightWindow et widthWindow sont la taille de la fenêtre de jeu
	# 
	# Actuellement l'interface est défini à l'extérieur
	#
	# ------------------
	#	en tête haut
	# ------------------
	# |				   |
	# |		Canvas	   |
	# |				   |
	# ------------------
	#	en tête bas
	# ------------------
	# A voir pour a terme Ne pas placer à l'extérieur l'interface, avoir un effet de profondeur
	#
	# l'interface doit prendre une taille suffisante mais pas trop grosse
	#	On prend une valeur 
	#
	# A voir pour à terme avoir les bouttons afficher sur un calque transparent
	####################


	# En tête Haut
	topframe = tkinter.Frame(win, height = heightWindow/28, width= widthWindow, background = "grey")
	# En tête Bas
	bottomFrame = tkinter.Frame(win, height = heightWindow/18, width= widthWindow, background = "grey")

	topframe.pack(expand = "True", side = "top")
	bottomFrame.pack(expand = "True", side = "bottom")

	# Info Entête
	# Nb Total Ressource
	ressource_label = tkinter.Label(topframe, text = "Ressource Total: ", textvariable = gamedata.list_lord[0].nb_ressource)
	ressource_label.pack(side = 'right')
	# Nb Total Argent
	money_label = tkinter.Label(topframe, text = "Argent Total: ", textvariable = gamedata.list_lord[0].nb_money)
	money_label.pack(side = 'right')
	# Humeur Globale de la Population
	global_joy_label = tkinter.Label(topframe, text = "Taux de Bonheur: ", textvariable = gamedata.list_lord[0].global_joy)
	global_joy_label.pack(side = 'right')
	# N°Tour
	nb_tour_label = tkinter.Label(topframe, text = "Tour N°: ", textvariable = gamedata.Nb_tour)
	nb_tour_label.pack(side = 'left')

	# Liste de Bouton

	# Button Gauche
	Button_military = tkinter.Button(bottomFrame, text= "Militaire")
	Button_gestion = tkinter.Button(bottomFrame, text= "Gestion")


	# Button Droit

	# Buton pour quitter(A remplacer par un listbutton)
	# Exit, Option, Load, Sauvegarder
	Button_exit = tkinter.Button(bottomFrame, command = exit, text = "Quitter")
	# Button pour acceder à la vue générale
	Button_globalview = tkinter.Button(bottomFrame, text = "Vue Générale")


	# On pack les Button
	Button_gestion.pack(side="left")
	Button_military.pack(side="left")
	Button_exit.pack(side="right")
	Button_globalview.pack(side="right")

#########################################################################

