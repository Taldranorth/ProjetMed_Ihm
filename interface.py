import tkinter






######################### Fonction Interface ############################

def gameinterface(win, option, gamedata):

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
	topframe = tkinter.Frame(win, height = option.heightWindow/28, width= option.widthWindow, background = "grey")
	# En tête Bas
	bottomFrame = tkinter.Frame(win, height = option.heightWindow/18, width= option.widthWindow, background = "grey")

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
	tkvar_nb_turn = tkinter.IntVar()

	# On les set
	tkvar_nb_ressource.set(gamedata.list_lord[0].nb_ressource) 
	tkvar_nb_money.set(gamedata.list_lord[0].nb_money) 
	tkvar_global_joy.set(gamedata.list_lord[0].global_joy)
	tkvar_nb_turn.set(gamedata.Nb_tour) 

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
	nb_turn_labelt = tkinter.Label(topframe, text = "Tour N°: ")
	nb_turn_label = tkinter.Label(topframe, text = "Tour N°: ", textvariable = tkvar_nb_turn)
	nb_turn_labelt.pack(side = "left")
	nb_turn_label.pack(side = 'left')


	# Liste de Bouton Bas


	# Menu Button Gauche
	Menu_Button_military = tkinter.Menubutton(bottomFrame, text= "Militaire")
	Menu_Button_gestion = tkinter.Menubutton(bottomFrame, text= "Gestion")

	# Menu
	menu_military = tkinter.Menu(Menu_Button_military)
	menu_gestion = tkinter.Menu(Menu_Button_gestion)

	#On lie les button au menu
	Menu_Button_military["menu"] = menu_military
	Menu_Button_gestion["menu"] = menu_gestion

	# On associe les Commandes Militaires
	menu_military.add_command(label = "Vassaliser")
	menu_military.add_command(label = "Soldat")
	menu_military.add_command(label = "Guerre")


	# On associe les Commandes Gestion
	menu_gestion.add_command(label = "Immigration")
	menu_gestion.add_command(label = "Église")
	menu_gestion.add_command(label = "Impôt")



	# Button Droit

	# Buton pour quitter(A remplacer par un listbutton)
	# Exit, Option, Load, Sauvegarder
	Button_exit = tkinter.Button(bottomFrame, command = exit, text = "Quitter")
	# Button pour acceder à la vue générale
	Button_globalview = tkinter.Button(bottomFrame, text = "Vue Générale")

	# Boutton Central
	# Bouton Fin de Tour
	Button_endofturn = tkinter.Button(bottomFrame, command = lambda: turnend(gamedata), text = "Fin de Tour")


	# On pack les Button
	Menu_Button_gestion.pack(side="left")
	Menu_Button_military.pack(side="left")
	Button_exit.pack(side="right")
	Button_globalview.pack(side="right")
	Button_endofturn.pack()

#########################################################################

# Fonction lier au bouton de fin de tour
def turnend(gamedata):
	print("fin de tour ")
	gamedata.endturn = True


def citiesinteface():
	pass


def unitinterface():
	pass






def menu_military():
	pass


def menu_gestion():
	pass

# Fonction Militaire

def vassalisation():
	pass

def addsoldier():
	pass

def war():
	pass


# Fonction Gestion

def buildchurch():
	pass

def tax():
	pass

def immigration():
	pass

def buildvillage():
	pass



"""
def mainscreen(heightWindow,widthWindow):

	#Init de la fenêtre
	root = tkinter.Tk()

	#Création de la fenêtre
	win1 = tkinter.Toplevel(root, height = heightWindow, width= widthWindow)


	#label
	tkinter.Label(win1)


	#frame qui prend la taille de la fenêtre
	f1 = tkinter.Frame(win1)
	f1.pack(expand="True",fill="both")


	################ Canvas ########################
	#frame canvas
	fcanvas = tkinter.Frame(win1)
	fcanvas.pack(side = "bottom")
	#Canvas qui prend la moitier de la frame 
	canv = tkinter.Canvas(fcanvas,height = (heightWindow/2),width = (widthWindow/2), bg = "white")
	canv.pack(side = "top")
	#On associe Event draw à ctrl+click gauche 
	canv.bind("<Control-Motion>", draw)
	canv.bind("<Button-1>", moveline)
	########################################


	################ Menu Fichier ########################

	#Button Fichier en entête
	#Menu button
	Button_file = tkinter.Menubutton(f1, text = "fichier")
	Button_file.pack(side = "left")

	#Menu associé au boutton file
	Menu_file = tkinter.Menu(Button_file)
	#On lie le menu_file au button
	Button_file["menu"] = Menu_file

	#On ajoute les commandes
	Menu_file.add_command(label = "ouvrir", command = command_open)
	Menu_file.add_command(label = "nouveau", command = lambda: command_new(canv))
	Menu_file.add_command(label = "sauvegarder", command = command_save, state = tkinter.DISABLED)
	Menu_file.add_command(label = "quitter", command = lambda: command_exit(root))


	########################################

	#Button Aide en entête
	Button_help = tkinter.Button(f1, text = "Aide")
	Button_help.pack(side = "right")

	if False:
		Menu_file.entryconfigure(2, state = tkinter.ACTIVE)
	root.mainloop()

def command_open():
	pass


def command_new(canvas):
	canvas.delete("all")

def command_save():
	pass


def command_exit(root):
	root.destroy()


def text_help():
	ch = "Merde"
	tkinter.Message(ch)


def draw(event):
	#saisie trace main levée
	#Ctrl( Control) + clic gauche (button[1])
	# coord + _flatten 
	print("draw on ", event.widget)
	line = event.widget.create_line(event.x, event.y, event.x+5, event.y+5, fill = "black")
	#if .entrycget(2, state) == tkinter.DISABLED:
	#	.entryconfigure(2, state = tkinter.ACTIVE)

	print(line)
	print(event.widget.coords(line))
	print(tkinter._flatten(event.widget.coords(line)))
	print(event.widget.find_all())

def moveline(event):
	#event.widget.find_closest(event.x,event.y)
	pass

"""



