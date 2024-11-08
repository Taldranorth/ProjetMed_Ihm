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

	# on Créer les tkinter variables que l'on va utiliser 
	#Nb_rssource
	tkvar_nb_ressource = tkinter.IntVar()
	#self.nb_ressource = tkinter.IntVar()
	#self.nb_ressource.set(10)

	#Nb_money
	tkvar_nb_money = tkinter.IntVar()
	#self.nb_money = tkinter.IntVar()
	#self.nb_money.set(10)

	#global_joy
	tkvar_global_joy = tkinter.IntVar()
	#self.global_joy = tkinter.IntVar()
	#self.global_joy.set(10)

	#Nb_tour
	tkvar_nb_tour = tkinter.IntVar()

	# On les set
	tkvar_nb_ressource.set(gamedata.list_lord[0].nb_ressource) 
	tkvar_nb_money.set(gamedata.list_lord[0].nb_money) 
	tkvar_global_joy.set(gamedata.list_lord[0].global_joy)
	tkvar_nb_tour.set(gamedata.Nb_tour) 

	# Info Entête
	# Nb Total Ressource
	ressource_labelt = tkinter.Label(topframe, text = "Ressource Total: ")
	ressource_label = tkinter.Label(topframe, text = "Ressource Total: ", textvariable = tkvar_nb_ressource)
	ressource_labelt.pack(side = "left")
	ressource_label.pack(side = 'left')

	# Nb Total Argent
	money_labelt = tkinter.Label(topframe, text = "Argent Total: ")
	money_label = tkinter.Label(topframe, text = "Argent Total: ", textvariable = tkvar_nb_money)
	money_labelt.pack(side = "left")
	money_label.pack(side = 'left')

	# Humeur Globale de la Population
	global_joy_labelt = tkinter.Label(topframe, text = "Taux de Bonheur: ")
	global_joy_label = tkinter.Label(topframe, text = "Taux de Bonheur: ", textvariable = tkvar_global_joy)
	global_joy_labelt.pack(side = "left")
	global_joy_label.pack(side = 'left')

	# N°Tour
	nb_tour_labelt = tkinter.Label(topframe, text = "Tour N°: ")
	nb_tour_label = tkinter.Label(topframe, text = "Tour N°: ", textvariable = tkvar_nb_tour)
	nb_tour_labelt.pack(side = "left")
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

