import tkinter
import random


import functions.log as log
import functions.asset as asset
import functions.common as common
import functions.savegame as save
import functions.genproc as genproc
import functions.moveview as moveview
import functions.gameclass as gameclass
import functions.affichage as affichage
import functions.notification as notification
import functions.warfunctions as warfunctions
import functions.interfacemenu as interfacemenu


######################### Fonction Interface ############################

def gameinterface(gamedata, classmap, option, win, root):

	####################
	# Fonction qui met en place l'interface en Jeu, voir l'entête
	# HeightWindow et widthWindow sont la taille de la fenêtre de jeu
	# 
	# Actuellement l'interface est défini à l'extérieur
	#
	# ------------------
	#	en tête haut	= option.heightwindow * 0.2
	# ------------------
	# |				   |
	# |		Canvas	   |= option.heightwindow * 0.6
	# |				   |
	# ------------------
	#	en tête bas 	= option.heightwindow * 0.2
	# ------------------
	# A voir pour a terme Ne pas placer à l'extérieur l'interface, avoir un effet de profondeur
	#
	# l'interface doit prendre une taille suffisante mais pas trop grosse
	#	On prend une valeur 
	#
	# A voir pour à terme avoir les bouttons afficher sur un calque transparent
	####################


	# En tête Haut
	topframe = tkinter.Frame(win, height = (option.heightWindow*0.4), width= option.widthWindow)
	topframe.pack(expand = "True", fill = "none", side = "top")
	# En tête Bas
	bottomFrame = tkinter.Frame(win, height = (option.heightWindow*0.2), width= option.widthWindow)
	bottomFrame.pack(expand = "True", fill = "none", side = "bottom")

	log.log.printinfo(f"Taille de la Frame du top: {topframe.winfo_width()}, {topframe.winfo_height()}")
	log.log.printinfo(f"Taille de la Frame du bas: {bottomFrame.winfo_width()}, {bottomFrame.winfo_height()}")


	# on Créer les tkinter variables que l'on va utiliser
	tkvar_list = []
	#Nb_rssource
	tkvar_nb_ressource = tkinter.StringVar()

	#Nb_money
	tkvar_nb_money = tkinter.StringVar()

	#global_joy
	tkvar_global_joy = tkinter.StringVar()

	#Nb_tour
	tkvar_nb_turn = tkinter.StringVar()

	classmap.tkvar_list +=[tkvar_nb_ressource, tkvar_nb_money, tkvar_global_joy, tkvar_nb_turn]

	player = gamedata.list_lord[gamedata.playerid]
	prod_g = player.prod_global()
	salaryarmy = player.total_salaryarmy()
	efficiency = player.total_efficiency()

	# On les set
	# Merde c'est pas dynamique
	classmap.tkvar_list[0].set(f"Ressource : {player.nb_ressource} ({efficiency[0]})")
	classmap.tkvar_list[1].set(f"Écus : {player.nb_money} ({efficiency[1]})")
	classmap.tkvar_list[2].set(f"Bonheur: {int(player.global_joy)}%")
	classmap.tkvar_list[3].set(f"Tour N°: {gamedata.nb_turn}")

	# Info Entête
	# Nb Total Ressource
	ressource_label = tkinter.Label(topframe, textvariable = classmap.tkvar_list[0], font = ('Helvetica', '14'))
	ressource_label.pack(side = 'left')

	# Nb Total Argent
	money_label = tkinter.Label(topframe, textvariable = classmap.tkvar_list[1], font = ('Helvetica', '14'))
	money_label.pack(side = 'left')

	# Humeur Globale de la Population
	global_joy_label = tkinter.Label(topframe, textvariable = classmap.tkvar_list[2], font = ('Helvetica', '14'))
	global_joy_label.pack(side = 'left')

	# N°Tour
	nb_turn_label = tkinter.Label(topframe, textvariable = classmap.tkvar_list[3], font = ('Helvetica', '14'))
	nb_turn_label.pack(side = 'left')

	# On Bind tooltip
	lvariable = [player.prod_global(), player.total_salaryarmy()]
	interfacemenu.tooltip(ressource_label, ["Produit: ", lvariable[0][0], "\nConsommé: ", lvariable[1][0]], lvariable)
	interfacemenu.tooltip(money_label, ["Produit: ", lvariable[0][0], "\nConsommé: ", lvariable[1][0]], lvariable)

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
	menu_military.add_command(label = "Vassaliser", command = lambda: statesubjugate(gamedata, classmap, option))
	menu_military.add_command(label = "Soldat", command = lambda: staterecruitarmy(gamedata, classmap, option))
	menu_military.add_command(label = "Déclarer Guerre", command = lambda: statewar(gamedata, classmap, option))


	# On associe les Commandes Gestion
	menu_gestion.add_command(label = "Immigration", command = lambda: stateimmigration(gamedata, classmap, option))
	menu_gestion.add_command(label = "Impôt", command = lambda: statetax(gamedata, classmap, option))
	menu_gestion.add_command(label = "Construire Église", command = lambda: statebuildchurch(gamedata, classmap, option))
	menu_gestion.add_command(label = "Construire Village", command = lambda: statebuildvillage(gamedata, classmap, option))



	# Button Droit
	"""
	# Buton pour quitter(A remplacer par un listbutton)
	# Exit, Option, Load, Sauvegarder
	Button_exit = tkinter.Button(bottomFrame, command = exit, text = "Quitter")
	# Button pour acceder à la vue générale
	"""
	#Lisbutton
	Menu_Button_option = tkinter.Menubutton(bottomFrame, text= "Options")
	menu_option = tkinter.Menu(Menu_Button_option)

	#On lie les button au menu
	Menu_Button_option["menu"] = menu_option

	# On associe les Commandes Militaires
	menu_option.add_command(label = "Réglage", command = lambda:interfacemenu.optionmenu(gamedata, classmap, option, root, win))
	menu_option.add_command(label = "Load", command = lambda: interfacemenu.loadmenu(win, gamedata, classmap, option, root))
	menu_option.add_command(label = "Save", command = lambda: interfacemenu.savemenu(win, gamedata, classmap, option, root))
	menu_option.add_command(label = "Quitter", command = lambda: exitwindow(classmap, option))
	
	
	Button_globalview = tkinter.Button(bottomFrame, command = lambda: globalviewmenu(gamedata, classmap, option), text = "Info Générale")


	# Boutton Central
	# Bouton Fin de Tour
	Button_endofturn = tkinter.Button(bottomFrame, command = lambda: turnend(gamedata, classmap, option), text = "Fin de Tour")


	# On pack les Button
	Menu_Button_gestion.pack(side="left",fill='x',expand=True)
	Menu_Button_military.pack(side="left",padx="1mm",fill='x',expand=True)
	Button_endofturn.pack(side="left",padx='1m',fill='x',expand=True)
	Button_globalview.pack(side="left",padx="1mm")
	#Button_exit.pack(side="right",padx="1mm")	
	Menu_Button_option.pack(side="right",padx="1mm")
#########################################################################
# Fonction lier au bouton de fin de tour
def turnend(gamedata, classmap, option):
	log.log.printinfo("fin de tour ")
	# On affiche un Retour
	coord = [int(option.widthWindow//2), int(option.heightWindow*0.15)]
	interfacemenu.temp_message(classmap.mapcanv, "Fin du Tour", 2000, coord, "green")

	# Si on est dans un état on quitte l'état
	if len(gamedata.exit)>0:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[1], gamedata.exit[2])
	gamedata.endturn = True

def updateinterface(gamedata, classmap):
	player = gamedata.list_lord[gamedata.playerid]
	efficiency = player.total_efficiency()
	classmap.tkvar_list[0].set(f"Ressource : {player.nb_ressource} ({efficiency[0]})")
	classmap.tkvar_list[1].set(f"Écu : {player.nb_money} ({efficiency[1]})")
	classmap.tkvar_list[2].set(f"Bonheur: {int(player.global_joy)}%")
	classmap.tkvar_list[3].set(f"Tour N°: {gamedata.nb_turn}")


def exitwindow(classmap, option):
	#####
	# Fonction pour afficher la boite de dialogue afin de valider l'exit
	#####
	# On créer la boite 
	top_window = classmap.mapcanv.winfo_toplevel()
	# On créer la fenêtre
	window_exit = tkinter.Toplevel()
	# On la positionne
	window_exit.geometry(f"+{int(option.widthWindow*0.45)}+{option.heightWindow//4}")
	# On la rend Transient
	window_exit.transient(top_window)
	# On retire le contour
	window_exit.overrideredirect(True)
	# On Créer le frame
	frame = tkinter.Frame(window_exit)
	frame.grid()
	# On affiche le Message
	tkinter.Label(frame, text = "Voulez-vous Quitter l'application ?").grid(row = 0, column = 0, columnspan = 2)
	# On créer les boutons
	tkinter.Button(frame, text = "Oui", command = exit).grid(row = 1, column = 0)
	tkinter.Button(frame, text = "Non", command = lambda: exitwindow_destroy(window_exit)).grid(row = 1, column = 1)

def exitwindow_destroy(window):
	window.destroy()

def legendginterface(gamedata, classmap, option):
	#####
	# Fonction Pour afficher la légende des commandes
	#####

	# On créer l'interface
	window_interface_legend_command = tkinter.Frame(classmap.framecanvas)
	# On la place
	window_interface_legend_command.place(x = (option.widthWindow*0.01), y = (option.heightWindow*0.45))

	# On créer la frame
	frame = tkinter.Frame(window_interface_legend_command)
	frame.grid()
	# On affiche le titre de la fenêtre
	tkinter.Label(frame, text = "Commande:").grid(row = 0, column = 0)
	# On la rempli avec la légende
	# Déplacement vue avec touche fléché
	tkinter.Label(frame, text = "Déplacé Vue XY: Touche Fléchée").grid(row = 1, column = 0)
	# Déplacement vue avec souris
	tkinter.Label(frame, text = "Déplacé Vue XY: SHIFT + Click DROIT").grid(row = 2, column = 0)
	# Zoom/Dezoom
	tkinter.Label(frame, text = "Zoom/DeZoom: Molette").grid(row = 3, column = 0)
	tkinter.Label(frame, text = "Zoom(X)").grid(row = 0, column = 1)
	# Scale Zoom/Dezoom
	zoomscall = tkinter.Scale(frame, orient = tkinter.VERTICAL, from_ = 0, to = 6)
	zoomscall.grid(row = 1, column = 1, rowspan = 4, sticky = tkinter.NS)
	# On set à la valeur de base (20 = 3)
	zoomscall.set(3)

	# On configure la commande du Scall
	zoomscall.configure(command = lambda event: scalezoom(gamedata, classmap, option, int(event)))

def scalezoom(gamedata, classmap, option, scallvalue):
	####
	# Fonction liée aux scale pour gérer le zoom/dezoom
	####
	print("scallvalue: ",scallvalue)
	# On calul le delta selon le scallvalue
	ts = 5* (2**scallvalue)
	print("new ts: ",ts)
	print("ts: ", gamedata.tuilesize)
	if ts < gamedata.tuilesize:
		delta = -2
	else:
		delta = 2


	moveview.moveviewzcenter(gamedata, classmap, option, delta)

######################### Menu Vue Globale #########################


###############
# Une Fenêtre qui va afficher une liste de l'ensemble des villages avec la population, le seigneur, l'argent produit, les ressources produites
# 
# Comment gérer l'affichage de fenêtre par dessus ?
#  .transient(parent=None) ?
# 
###############
def globalviewmenu(gamedata, classmap, option):

	# ------------------
	#	Village
	# ------------------
	# |				   |
	# |				   |
	# |				   |
	# ------------------
	#	Vassaux
	# ------------------
	# |				   |
	# |				   |
	# |				   |
	# |				   |
	# ------------------
	#	Armée
	# ------------------

	# Window de la fenêtre
	window_global_view = tkinter.Frame(classmap.framecanvas, height = option.heightWindow, width = option.widthWindow, padx = 25, pady = 25)
	window_global_view.place(x = (option.widthWindow/5), y = (option.heightWindow/10))

	player = gamedata.list_lord[gamedata.playerid]

	frame_global_view = tkinter.Frame(window_global_view)
	frame_global_view.grid()

	# Affichage des Village
	# legend
	j = 0
	for legend in ("Village","Population","Production de Ressource","Production d'argent","Prêtre","Bonheur"):
		tkinter.Label(frame_global_view, text = legend).grid(row = 0,column = j)
		j += 1

	i = 1
	for village in player.fief:
		j = 0
		for ele in (village.name, len(village.population), village.prod_ressource, village.prod_money, village.priest, village.global_joy):
			if ele == village.priest:
				if ele != 0:
					tkinter.Label(frame_global_view, text = ele.name).grid(row = i, column = j)
				else:
					tkinter.Label(frame_global_view, text = ele).grid(row = i, column = j)
			else:
				tkinter.Label(frame_global_view, text = ele).grid(row = i, column = j)
			j += 1
		i += 1

	# Séparateur
	i += 2
	for j in range(6):
		tkinter.Label(frame_global_view, text = "-----------------").grid(row = i, column = j)
	i += 2
	#########

	# affichage des Armées
	# legend
	j = 0
	for legend in ("Armée", "Puissance", "Chevalier", "Nombre de Soldat"):
		tkinter.Label(frame_global_view, text = legend).grid(row = i, column = j)
		j += 1
	i += 1
	for army in player.army:
		j = 0
		for ele in (army.name, army.power, army.knight, len(army.unit)):
			if ele == army.knight:
				if ele != 0:
					tkinter.Label(frame_global_view, text = ele.name).grid(row = i, column = j)
				else:
					tkinter.Label(frame_global_view, text = ele).grid(row = i, column = j)
			else:
				tkinter.Label(frame_global_view, text = ele).grid(row = i, column = j)
			j += 1
		i += 1

	# Séparateur
	i += 2
	for j in range(6):
		tkinter.Label(frame_global_view, text = "-----------------").grid(row = i, column = j)
	i += 2
	#########

	# Affichage des Vassaux
	# legend
	j = 0
	for legend in ("Vassaux", "Puissance", "Nombre de Village", "Nombre de Pop", "Production de Ressource", "Production d'argent"):
		tkinter.Label(frame_global_view, text = legend).grid(row = i, column = j)
		j += 1

	i += 1
	for vassal in player.vassal:
		j = 0
		for ele in (vassal.lordname, vassal.power, len(vassal.fief), vassal.total_pop(), vassal.prod_global()[1], vassal.prod_global()[0]):
			tkinter.Label(frame_global_view, text = ele).grid(row = i, column = j)
			j += 1
		i += 1

	i += 1

	# Bouton pour quitter le menu
	Button_exit = tkinter.Button(frame_global_view, text= "Quitter", command = lambda: destroyglobalviewmenu(window_global_view))
	Button_exit.grid(row = i, column = 3)

def destroyglobalviewmenu(window_global_view):
	 window_global_view.destroy()

##############################################################\ Militaire  \###########################################################################

def statesubjugate(gamedata, classmap, option):
	#######
	# Fonction pour ouvrir l'interface de vassalisations
	#######

	# Si on est déjà dans un état
	if len(gamedata.exit)>0:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[1], gamedata.exit[2])

	player = gamedata.list_lord[gamedata.playerid]

	# On créer l'interface qui va contenir la frame
	window_interface_subjugate = tkinter.Frame(classmap.framecanvas)
	window_interface_subjugate.place(x = (option.widthWindow/20), y = (option.heightWindow/20))

	frame_interface_subjugate = tkinter.Frame(window_interface_subjugate)
	frame_interface_subjugate.grid()

	tkinter.Label(frame_interface_subjugate, text = "Choisissez un Seigneur:").grid(row = 0, column = 0)
	# On affiche une liste de tout les Seigneurs qui ne sont pas Vassaux:
	lc_subjugate = tkinter.Listbox(frame_interface_subjugate)
	lc_subjugate.grid(row = 1, column = 0)
	for lord in gamedata.list_lord:
		if lord.player == False:
			# On n'affiche pas les vassaux
			if lord not in (player.vassal):
				# On n'affiche pas ceux avec qui nous somme en guerre
				if lord not in (player.war):
					lc_subjugate.insert(tkinter.END, lord.lordname)
	# On bind double click
	lc_subjugate.bind("<Double-Button-1>", lambda event: l_vassal_offer(event, gamedata, classmap, option, window_interface_subjugate, lc_subjugate))

	# On bind l'exit
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [window_interface_subjugate]))
	gamedata.exit = [[], [], [window_interface_subjugate]]


def l_vassal_offer(event, gamedata, classmap, option, wis, lc):
	################
	# Fonction pour affiche interface pour Afficher les Infos sur le Seigneur est confirmer la proposition de Vassalisation
	################
	# On recup le Seigneur
	lordname = event.widget.get(event.widget.curselection()[0])
	lordid = gamedata.lordnametoid(lordname)
	lord = gamedata.list_lord[lordid]
	player = gamedata.list_lord[gamedata.playerid]


	frame_interface_offer = tkinter.Frame(wis)
	frame_interface_offer.grid(row = 0, column = 1)

	succes = vassal_try(gamedata, player, lord)

	#On affiche les Infos du Seigneur
	# Sa puissance
	tkvar_power = tkinter.StringVar()
	tkvar_power.set(f"Puissance Militaire: {lord.power}")
	tkinter.Label(frame_interface_offer, textvariable = tkvar_power).grid(row = 1,column = 1)

	# Le Nombre de Village qu'il possède
	tkvar_nb_village = tkinter.StringVar()
	tkvar_nb_village.set(f"Nb Village: {len(lord.fief)}")
	tkinter.Label(frame_interface_offer, textvariable = tkvar_nb_village).grid(row = 2,column = 1)

	# Le Nombre de Vassaux qu'il possède
	tkvar_nb_vassal = tkinter.StringVar()
	tkvar_nb_vassal.set(f"Nb Vassal: {len(lord.vassal)}")
	tkinter.Label(frame_interface_offer, textvariable = tkvar_nb_vassal).grid(row = 3,column = 1)

	# Le % de chance qu'il accepte sa vassalisation
	tkvar_succes = tkinter.StringVar()
	tkvar_succes.set(f"Proba de Réussite: {succes}%")
	tkinter.Label(frame_interface_offer, textvariable = tkvar_succes).grid(row = 4,column = 1)

	# Le Boutton pour envoyer la proposition de Vassalisation
	button_vassalage_offer = tkinter.Button(frame_interface_offer, command = lambda: b_vassal_offer(gamedata, classmap, option, lc, player, lord, frame_interface_offer, succes), text = "Envoyer Proposition")
	button_vassalage_offer.grid(row = 5, column = 1)

def b_vassal_offer(gamedata, classmap, option, lc, lord, lord2, frame, succes):
	################
	# Fonction pour gérer l'envoit d'une demande de Vassalisation et l'update de l'écran
	################

	# On appel la fonction qui gérer l'envoit et les répercusion
	result = vassal_offer(gamedata, classmap, option, lord, lord2, succes)

	# On update la Listbox
	lc.delete(lc.curselection()[0])

	# On détruit la fenêtre Une fois la demande faite
	frame.destroy()
	if result == True:
		coord = [option.widthWindow//2, option.heightWindow//4]
		interfacemenu.validation_message(classmap.mapcanv, f"{lord2.lordname} A accepté notre Demande de Vassalisation !", coord, "green")
	else:
		coord = [option.widthWindow//2, option.heightWindow//4]
		interfacemenu.validation_message(classmap.mapcanv, f"{lord2.lordname} A refusé notre demande de Vassalisation !\n Il nous a déclaré la guerre !", coord, "red")

def vassal_offer(gamedata, classmap, option, lord, lord2, succes):
	################
	# Fonction pour gérer l'envoit d'une demande de Vassalisation et l'affichage des répercution
	################
	# Return True Si c'est une réussite
	# Return False Si c'est un Échec
	#######
	result = False
	# On teste la probabilité
	# On genère un chiffre entre 1 et 100
	r = random.randrange(0,100)
	# On addition le succes
	r += succes
	log.log.printinfo(f"Valeur obtenu après lancer de dé: {r}")
	# On vérifie si c'est >= 100
	# Si c'est réussi on ajoute à la liste des Vassaux
	if r >= 100:
		log.log.printinfo("Succès")
		# On ajoute le Seigneur à la liste des Vassaux
		lord.addvassal(lord2)
		# On ajoute les vassaux du Seigneur à la liste des Vassaux
		for vassal in lord2.vassal:
			# On retire de la liste des Vassaux du Seigneur les vassaux qu'il possède
			lord2.removevassal(vassal)
			lord.addvassal(vassal)
		log.log.printinfo(f"Liste des vassaux du Joueurs: {lord.vassal}")
		result = True
	# Sinon on déclare la guerre
	else:
		log.log.printinfo("Echecs")
		lord.addwar(lord2)
		lord2.addwar(lord)

	# On update l'affichage de la carte
	affichage.bordervillage(gamedata, classmap, option)

	# On update l'entête
	updateinterface(gamedata, classmap)
	return result


def vassal_try(gamedata, lord, lord2):
	################
	# Fonction qui calcul le % de chance de réussite que le Seigneur1 vassalise le Seigneur2 par une tentative
	################

	# On ajoute la puissance Militaire
	lord_score1 = lord.score()
	lord_score2 = lord2.score()

	# On compare les 2 Scores
	rs = ((lord_score1 - lord_score2)/100)*100

	# On retourne le résultat
	return rs


############################################# Recrut Army #############################################

def staterecruitarmy(gamedata, classmap, option):
	################
	# Fonction pour ouvrir l'interface des armée
	################
	# On affiche la liste des armée dans une fenêtre
	# On créer un boutton pour en créer une
	################

	if len(gamedata.exit)>0:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[2], gamedata.exit[2])

	player = gamedata.list_lord[gamedata.playerid]

	# On créer l'interface qui va contenir le frame
	window_interface_army = tkinter.Frame(classmap.framecanvas, height = 200, width = 300)
	window_interface_army.place(x = (option.widthWindow/6), y = (option.heightWindow*0.2))

	frame_interface_army = tkinter.Frame(window_interface_army)
	frame_interface_army.grid()

	# listbox
	lc_interface_army = tkinter.Listbox(frame_interface_army)
	lc_interface_army.grid(row = 0, column = 0)

	# On affiche la liste des armées du Joueur uniquement
	for army in player.army:
		lc_interface_army.insert(tkinter.END, army.name)
	# On bind l'objet à une fonction pour center sur l'armée selectionner
	lc_interface_army.bind("<Double-Button-1>", lambda event: interfacerecruit(event, gamedata, classmap, option, frame_interface_army))
	# On créer un boutton pour créer une nouvelle armée
	button_createarmy = tkinter.Button(frame_interface_army, text= "Nouvelle Armée", command = lambda: buttoncreatearmy(gamedata, classmap, option, lc_interface_army))
	button_createarmy.grid(row = 1, column = 0)

	# Bind Tooltipe
	interfacemenu.tooltip(button_createarmy, f"Demande 2 ressource, 2 écus",[])

	# On bind 
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [window_interface_army]))
	exit = [[],[], [window_interface_army]]

def buttoncreatearmy(gamedata, classmap, option, lc_interface_army):


	player = gamedata.list_lord[gamedata.playerid]
	lastarmy = len(player.army)

	# On vérifie que le joueur possède les ressource nécessaire pour recruter 1 Soldata
	if player.verifcost(2,2) == True:
		log.log.printinfo("Le Joueur Créer une armée")
		result = createarmy(gamedata, classmap, option, player, 1, 0)
		if result == 1:
			# On ajoute 1 Soldat
			player.sub_money(2)
			player.sub_ressource(2)
			# On update l'interface de la listbox
			lc_interface_army.insert(tkinter.END, player.army[lastarmy].name)
			# On update l'interface entête
			updateinterface(gamedata, classmap)
	else:
		coord = [option.widthWindow//2, option.heightWindow//8]
		interfacemenu.temp_message(classmap.mapcanv, "Pas Assez de Ressource\n Besoin de 2 R,2 Écus", 2000, coord, "red")

def searchposition(gamedata, classmap, option, village):
	#####
	# Fonction qui renvoit la 1er position non occupé par une armée pour le village sélectionner Dans un Rayon de 1
	# Renvoit 0 si il ne trouve pas
	#####
	xvill = village.x
	yvill = village.y
	idvillage = common.coordmaptoidtuile(classmap, [xvill, yvill])
	# On teste sur la case du village
	if classmap.listmap[idvillage].armyintuile == 0:
		return [village.x, village.y]

	# on test dans un rayon de 1 cases autour du village
	lcase = []
	# On rempli une liste de coord
	for x in range(-1, 1):
		for y in range(-1, 1):
			# On vérifie que les coordonnées sont dans la carte
			if ((xvill+x) > 0) and ((xvill+x) < classmap.mapx):
				if ((yvill+y) > 0) and ((yvill+y) < classmap.mapy):
					lcase += [[xvill + x, yvill + y]]

	if len(lcase) > 0:
		# On tire aléatoirement les coord
		r = random.randrange(len(lcase))
		coord = lcase[r]
		idtuile = common.coordmaptoidtuile(classmap,lcase[r])
		# On vérifie que les coord soit correctes
		while((classmap.listmap[idtuile].armyintuile != 0) and (len(lcase)>0)):
			r = random.randrange(len(lcase))
			coord = lcase[r]
			idtuile = common.coordmaptoidtuile(classmap, lcase[r])
			lcase = lcase[:r] + lcase[r+1:]
		# Si Correcte alors ont renvoit
		if (classmap.listmap[idtuile].armyintuile == 0):
			return coord
	return 0

def interfacerecruit(event, gamedata, classmap, option, frame_interface_army):
	################
	# Fonction pour afficher le Sous-Menu afin de recruter des Troupes pour une Armées particulières
	################

	# On recup l'armée
	army_selected = event.widget.get(event.widget.curselection()[0])

	point_army_object = 0
	# On recup l'objet army
	for army in (gamedata.list_lord[gamedata.playerid].army):
		if army.name == army_selected:
			point_army_object = army


	# On centre la vue sur l'armée selectionner
	centerarmy(event, gamedata, classmap, option)

	# On créer l'interface pour recruter
	frame_interface_army_right = tkinter.Frame(frame_interface_army)
	frame_interface_army_right.grid(row = 0, column = 1)


	# On créer les variables pour l'affichage
	tkvar_power = tkinter.StringVar()
	tkvar_power.set(f"Puissance: {army.power}")

	tkvar_knight = tkinter.StringVar()
	if army.knight == 0:
		tkvar_knight.set(f"Chevalier: 0")
	else:
		tkvar_knight.set(f"Chevalier: {army.knight.name}")

	tkvar_lenunit = tkinter.StringVar()
	tkvar_lenunit.set(f"Soldat: {len(army.unit)}")

	tkvar_list = [tkvar_power, tkvar_knight, tkvar_lenunit]

	# On affiche les Infos de l'armée
	# La puissance de l'armée
	tkinter.Label(frame_interface_army_right, textvariable = tkvar_list[0]).grid(column = 1)
	# Le nombre de Chevalier
	tkinter.Label(frame_interface_army_right, textvariable = tkvar_list[1]).grid(column = 1)
	# Le nombre de Soldat
	tkinter.Label(frame_interface_army_right, textvariable = tkvar_list[2]).grid(column = 1)

	# On créer un bouttons pour recruter un Chevalier
	button_recruit_knight = tkinter.Button(frame_interface_army_right, command = lambda unit="knight": button_recruit(gamedata, classmap, option, tkvar_list, army, unit), text = "Recruter Chevalier")
	button_recruit_knight.grid(column = 1)

	# On créer un bouttons pour recruter un soldat
	button_recruit_soldier = tkinter.Button(frame_interface_army_right, command = lambda unit="soldier": button_recruit(gamedata, classmap, option, tkvar_list, army, unit), text = "Recruter soldat")
	button_recruit_soldier.grid(column = 1)

	# On bind les tooltipe
	interfacemenu.tooltip(button_recruit_knight, f"Demande 10 ressources et 10 écus", [])
	# On bind les tooltipe
	interfacemenu.tooltip(button_recruit_soldier, f"Demande 2 ressources et 2 écus", [])

def centerarmy(event, gamedata, classmap, option):
	############
	# Fonction appeler par la listbox lc_interface_army pour centrer la vue sur l'armée sélectionner
	############
	log.log.printinfo("On se déplace vers l'armée ")
	# On recup le village actuellement selectionner dans la listbox
	army_selected = event.widget.get(event.widget.curselection()[0])
	
	point_army_object = 0
	# On recup l'objet army
	for army in (gamedata.list_lord[gamedata.playerid].army):
		if army.name == army_selected:
			point_army_object = army


	#print("x,y: ", x, y)
	coord = common.coordmaptocanvas(gamedata, classmap, option, [army.x, army.y], True)


	# On centre la vu sur le village
	moveview.centerviewcanvas(gamedata, classmap, option, coord)

def button_recruit(gamedata, classmap, option, tkvar_list, army, unit):
	################
	# Fonction appeler pour recruter
	################
	player = gamedata.list_lord[gamedata.playerid]

	# On recrute l'unité
	if (unit == "knight"):
		if (army.knight == 0):
			# On verif que le joueur possède les ressources
			if player.verifcost(10,10) == True:
				army.recruitknight(asset.dico_name.randomnametype("Surnom"))
				tkvar_list[1].set(f"Chevalier: {army.knight.name}")
				player.sub_money(10)
				player.sub_ressource(10)
			else:
				coord = [option.widthWindow//2, option.heightWindow//8]
				interfacemenu.temp_message(classmap.mapcanv, "Pas Assez de Ressource\n Besoin de 10 R,10 Écus", 2000, coord, "red")
			# On update l'affichage de l'armée
			if asset.atlas.searchtexturetypeindico(asset.dico_file, army.texture) != "knight":
				affichage.printupdatearmy(gamedata, classmap, army)
		else:
			coord = [option.widthWindow//2, option.heightWindow//8]
			interfacemenu.temp_message(classmap.mapcanv, "L'armée possède déjà un Chevalier", 2000, coord, "red")

	if unit == "soldier":
		if player.verifcost(2,2) == True:
			army.recruitsoldier(asset.dico_name.randomnametype("Nom"))
			tkvar_list[2].set(f"Soldat: {len(army.unit)}")
			player.sub_money(2)
			player.sub_ressource(2)		
		else:
			coord = [option.widthWindow//2, option.heightWindow//8]
			interfacemenu.temp_message(classmap.mapcanv, "Pas Assez de Ressource\n Besoin de 2 R,2 Écus", 2000, coord, "red")



	# On update l'interface de l'armée
	tkvar_list[0].set(f"Puissance: {army.power}")
	# On update l'interface de l'entête
	updateinterface(gamedata, classmap)

def createarmy(gamedata, classmap, option, lord, nbsoldat, knight):
	#####
	# Fonction pour créer une armée pour le Seigneur lord avec nb soldat et 0 ou 1 knight
	# On ne prend pas en compte le cout de création
	#####
	village = lord.fief[0]
	idvillage = common.coordmaptoidtuile(classmap, [village.x, village.y])
	# Récupère les coord de la 1er cases libres
	coord = searchposition(gamedata, classmap, option, village)
	if coord != 0:
		i = len(lord.army)
		# Créer l'armée
		lord.createarmy(village.name, coord[0], coord[1])
		classmap.listmap[idvillage].setarmyinplace(lord.army[i])
		# Recrute Soldat
		for x in range(nbsoldat):
			lord.army[i].recruitsoldier(asset.dico_name.randomnametype("Nom"))
		if knight == 1:
			lord.army[i].recruitknight(asset.dico_name.randomnametype("Surnom"))
		idtuile = common.coordmaptoidtuile(classmap, coord)
		# On indique qu'une armée est présente sur la tuile
		classmap.listmap[idtuile].setarmyinplace(lord.army[i])
		# Affiche l'armée
		affichage.printarmy(gamedata, classmap, option, lord.army[i], lord)
		log.log.printinfo(f"{lord.lordname} A créer l'armée {lord.army[i].name} à la position {lord.army[i].x}, {lord.army[i].y}")
		return 1
	else:
		log.log.printerror(f"{lord.lordname} N'a pas de place libre autour de {village.name} pour créer une armée")
		coord = [option.widthWindow//2, option.heightWindow//8]
		interfacemenu.temp_message(classmap.mapcanv, f"Pas Assez de Place autour de {village.name}", 2000, coord, "red")
		return 0

############################################# War #############################################

def statewar(gamedata, classmap, option):
	################
	# Fonction pour ouvrir l'interface de guerre
	################
	# Doit :
	#	- dezoom la vue a 20
	#	- Centrer la carte
	#	- Afficher en blanc les territoires neutre
	#	- Afficher en rouge les territoires ennemies
	#	- Afficher une interface pour définir le seigneur dont ont veut déclarer la guerre
	#		--> Donncer plusieurs information importante comme les vasaux du seigneur est sa puissance totale
	#	- Quand on place la souris sur le nom du seigneur sont terriroire passe ennemies et est donc afficher en rouge
	#
	#################

	# Si on est déjà dans un état on quitte l'état
	if len(gamedata.exit)>0:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[1], gamedata.exit[2])

	ts = gamedata.tuilesize
	# Tant que la carte n'est pas dezoom à 10
	while ts != 5:
		if ts > 5:
			moveview.moveviewzcenter(gamedata, classmap, option, -2)
		else:
			moveview.moveviewzcenter(gamedata, classmap, option, 2)
		ts = gamedata.tuilesize

	player = gamedata.list_lord[gamedata.playerid]
	xorigine = classmap.mapcanv.canvasx(0)
	yorigine = classmap.mapcanv.canvasy(0)

	# On se place au centre
	moveview.centerviewcanvas(gamedata, classmap, option, [(classmap.mapx/2)*ts, (classmap.mapy/2)*ts])

	# On affiche les territoire 
	# On se balade dans la liste des territoire
	for nblord in range(len(gamedata.list_lord)):
		color = gamedata.list_lord[nblord].color
		# Si c'est un joueur actuellement en guerre on change la couleur en rouge
		if gamedata.list_lord[nblord] in player.war:
			color = "red"
		# Si c'est un vassal on affiche en vert
		elif gamedata.list_lord[nblord] in player.vassal:
			color = "green"
		if nblord != gamedata.playerid:
			for village in gamedata.list_lord[nblord].fief:
				x = village.x
				y = village.y
				classmap.mapcanv.create_rectangle((x*ts), (y*ts), (x*ts)+ts, (y*ts)+ts, tag = ["interface_war","tuile", x, y], outline = color)
				classmap.mapcanv.create_text((x*ts), (y*ts)-(3*ts), tag = ["interface_war","tuile"], text = gamedata.list_lord[nblord].lordname, fill = color)

	############# Interface ############
	frame_interface_war = tkinter.Frame(classmap.framecanvas)
	frame_interface_war.place(x = (option.widthWindow/20), y = (option.heightWindow*0.01))

	# On créer l'interface War déclaration
	# Elle reste cacher tant qu'ont la pas appeler 
	interface_war_declaration = tkinter.Frame(classmap.framecanvas)
	interface_war_declaration.place(x = (option.widthWindow/1.5), y = (option.heightWindow*0.05))

	# Version avec .grid
	frame_interface_war_main = tkinter.Frame(frame_interface_war)
	frame_interface_war_main.grid()
	
	frame_interface_war_list_ally = tkinter.Frame(frame_interface_war_main)
	frame_interface_war_list_ennemy = tkinter.Frame(frame_interface_war_main)
	frame_interface_war_list_neutral = tkinter.Frame(frame_interface_war_main)
	frame_interface_war_list_ally.grid(row = 0, column = 0)
	frame_interface_war_list_ennemy.grid(row = 0, column = 1)
	frame_interface_war_list_neutral.grid(row = 0, column = 2)

	tkinter.Label(frame_interface_war_list_ally, text = "Allié").grid(row = 0)
	tkinter.Label(frame_interface_war_list_ennemy, text = "Ennemie").grid(row = 0)
	tkinter.Label(frame_interface_war_list_neutral, text = "Neutre").grid(row = 0)

	# On créer les menu déroulant
	Lb_ally = tkinter.Listbox(frame_interface_war_list_ally)
	Lb_ally.grid(row = 1)
	Lb_ennemy = tkinter.Listbox(frame_interface_war_list_ennemy)
	Lb_ennemy.grid(row = 1)
	Lb_neutral = tkinter.Listbox(frame_interface_war_list_neutral)
	Lb_neutral.grid(row = 1)
	# On les remplis
	for lord in gamedata.list_lord:
		# On vérifie que ce soit pas le joueur:
		if lord.player == False:
			# Si dans la liste des Ennemies
			if lord in player.war:
				Lb_ennemy.insert(tkinter.END, lord.lordname)
			# Sinon Si il est dans les liste des Vassaux
			elif lord in player.vassal:
				Lb_ally.insert(tkinter.END, lord.lordname)
			# Sinon il est neutre
			else:
				Lb_neutral.insert(tkinter.END, lord.lordname)
	list_LC = [Lb_ally, Lb_ennemy, Lb_neutral]
	Lb_ally.bind("<Double-Button-1>", lambda event, iwd = interface_war_declaration: warcentervillage(event, gamedata, classmap, option, list_LC, iwd))
	Lb_ennemy.bind("<Double-Button-1>", lambda event, iwd = interface_war_declaration: warcentervillage(event, gamedata, classmap, option, list_LC, iwd))
	Lb_neutral.bind("<Double-Button-1>", lambda event, iwd = interface_war_declaration: warcentervillage(event, gamedata, classmap, option, list_LC, iwd))

	# On bind
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [frame_interface_war, interface_war_declaration, "interface_war"]))
	gamedata.exit = [[], [], [frame_interface_war, interface_war_declaration, "interface_war"]]



def warcentervillage(event, gamedata, classmap, option, list_LC, iwd):
	############
	# Fonction appeler par Lb_neutral, Lb_ally ou Lb_ennemy pour centrer la vue sur le village principale du joueur Sélectionner
	############
	# On recup le joueur
	player = gamedata.list_lord[gamedata.playerid]

	# On recup le nom du seigneur Selectionner
	lordname = event.widget.get(event.widget.curselection()[0])
	log.log.printinfo(f"lordname: , {lordname}")
	# On recup son id
	lordid = gamedata.lordnametoid(lordname)
	log.log.printinfo(f"lordid: , {lordid}")
	# On recup l'objet lord
	lord = gamedata.list_lord[lordid]
	# On recup son village principale
	city = lord.fief[0]

	# On convertit les coord Map de l'objet en coord Canvas
	coord = common.coordmaptocanvas(gamedata, classmap, option, [city.x, city.y], True)

	# On centre la vue sur le village
	moveview.centerviewcanvas(gamedata, classmap, option, coord)

	# On créer une interface War déclaration

	# Si elle existe déjà on supprime l'ancienne
	# FFFFFFLLLLLLEEEEEMMMMMMMMEEEEE
	if len(iwd.winfo_children()) > 0:
		iwd.winfo_children()[0].destroy()

	frame_war_decl = tkinter.Frame(iwd)
	frame_war_decl.grid()

	# On ajoute les Info sur le Seigneur Ennemie:
	# Nb vassaux, Nb Village, Nb armée, Puissance
	# Power
	tkinter.Label(frame_war_decl, text = "Power:").grid(row = 0, column = 0)
	tkinter.Label(frame_war_decl, text = lord.power).grid(row = 0, column = 1)
	# NB Armée
	tkinter.Label(frame_war_decl, text = "Armée:").grid(row = 1, column = 0)
	tkinter.Label(frame_war_decl, text = len(lord.army)).grid(row = 1, column = 1)

	# Nb Villgae
	tkinter.Label(frame_war_decl, text = "Village:").grid(row = 2, column = 0)
	tkinter.Label(frame_war_decl, text = len(lord.fief)).grid(row = 2, column = 1)

	# Nb vassaux
	tkinter.Label(frame_war_decl, text = "Vassaux:").grid(row = 3, column = 0)
	tkinter.Label(frame_war_decl, text = len(lord.vassal)).grid(row = 3, column = 1)


	# On créer un bouton pour déclarer la guerre
	button_war_declaration = tkinter.Button(frame_war_decl, command = lambda: buttonwardeclaration(gamedata, classmap, option, list_LC, player, lord), text = "Déclarer Guerre")
	button_war_declaration.grid(row = 4, column = 0, columnspan = 2)

def buttonwardeclaration(gamedata, classmap, option, list_LC, player, lord):
	############
	# Fonction appeler par le button de déclarer Guerre
	############

	# Les 2 seigneurs se déclare la guerre
	wardeclaration(gamedata, player, lord)
	# On update l'interface
	# On retire le Seigneur des Neutre
	lineid = list_LC[2].curselection()[0]
	lordname = list_LC[2].get(lineid)
	list_LC[2].delete(lineid)

	# On l'ajoute à ceux en guerre
	list_LC[1].insert(tkinter.END, lordname)

	# On change l'affichage du territoire pour indiquer qu'il est en guerre
	# Village gérer directement par le seigneur Ennemie
	for village in lord.fief:
		affichage.bordervillageunit(gamedata, classmap, option, village)
	for vassal in lord.vassal:
		for vassal_village in vassal.fief:
			affichage.bordervillageunit(gamedata, classmap, option, vassal_village)

def wardeclaration(gamedata, lord1, lord2):
	############
	# Fonction appeler pour déclarer la gerre entre 2 Seigneurs
	############
	log.log.printinfo(f"Déclaration de guerre entre: {lord1.lordname} et {lord2.lordname}")

	lord1.addwar(lord2)
	lord2.addwar(lord1)


##############################################################\ Gestion  \###########################################################################

############################################# Build Village #############################################

def statebuildvillage(gamedata, classmap, option):
	############
	# Fonction appeler quand on clique sur Construire Village
	# 	- Fait rentrer le joueur dans un état "Construction de Village"
	#	- Place un village là ou la texture pointe
	#	- Affiche en rouge la texture si ce n'est pas possible
	#	- Affiche en vert si c'est possible
	#	- Si on appuie sur ESC on annule
	#	- Doit afficher une legende
	############
	# - Affiche avec un carrer vert toute les tuiles ou ont peut constuire un village
	#
	#
	############
	# On permet de sélectionner la case ou on veut constuire un village
	#classmap.mapcanv.tag_bind("click", "Button-1", lambda event, option, gamedata: statbuildvillage(event, option, gamedata))

	if len(gamedata.exit)>0:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[1], gamedata.exit[2])

	ts = gamedata.tuilesize
	xoriginewindow = classmap.mapcanv.canvasx(0)
	yoriginewindow = classmap.mapcanv.canvasy(0)
	originecanvas = classmap.mapcanv.coords(classmap.listmap[0].canvastuiles)

	# Pour toute les tuiles de plaines
	for idtuile in classmap.lplaines:
		# Si on peut constuire un village
		if genproc.buildvillagepossible(option, classmap, idtuile) == True:
			coord = common.idtuiletocoordmap(classmap, idtuile)
			# On calcul les coord x et y
			x = coord[0]
			y = coord[1]
			# On créer un carrer clickable avec un bord vert
			idobject = classmap.mapcanv.create_rectangle(originecanvas[0]+(x*ts)-(ts/2), originecanvas[1]+(y*ts)-(ts/2), originecanvas[0]+(x*ts)+ts-(ts/2), originecanvas[1]+(y*ts)+ts-(ts/2), tag = ["buildvillage","tuile", x, y], fill = "green",outline = "green")

	# On tag au square
	classmap.mapcanv.tag_bind("buildvillage", "<Button-1>", lambda event: buildvillage(event, gamedata, classmap, option))
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], ["buildvillage"]))
	gamedata.exit = [[], [], ["buildvillage"]]

def buildvillage(event, gamedata, classmap, option):
	############
	# Fonction pour créer un village selon la tuile sélectionner en état de construction
	############

	player = gamedata.list_lord[gamedata.playerid]
	log.log.printinfo("On construit le village")
	# On calcul l'id de la tuile
	xpos = int(event.widget.gettags("current")[2])
	ypos = int(event.widget.gettags("current")[3])
	idtuile = xpos + (classmap.mapx*ypos)

	if player.verifcost(15,15) == True:
		# On retire
		player.sub_money(15)
		player.sub_ressource(15)

		# On créer
		# On ajoute l'id de la tuile à la liste des villages
		classmap.lvillages += [idtuile]
		# On créer le village
		classmap.listmap[idtuile].createvillage(gamedata)
		classmap.listmap[idtuile].setpossesor("player")
		# On ajoute l'instance de vilalge à la liste de fief du lord
		player.addfief(classmap.listmap[idtuile].village)
		# On rempli le village de pop
		genproc.genpopvillage(gamedata, classmap, option, classmap.listmap[idtuile].village, 8, 2)

		# On retire les ressource 

		# On affiche le nouveau village
		affichage.printvillageunit(gamedata, classmap, option, [xpos,ypos])

		# On affiche la bordure du nouveau village
		affichage.bordervillageunit(gamedata, classmap, option, classmap.listmap[idtuile].village)

		# On update la carte des villages possible
		updatestatbuildvillage(classmap, option)

		# On update l'entête
		updateinterface(gamedata, classmap)
	else:
		coord = [option.widthWindow//2, option.heightWindow//8]
		interfacemenu.temp_message(event.widget, "Pas Assez de Ressource\n Besoin de 15 R,15 Écus", 2000, coord, "red")

def updatestatbuildvillage(classmap, option):
	############
	# Fonction pour update la carte des Construction possible
	############
	liste_carrer = classmap.mapcanv.find_withtag("buildvillage")
	for tuile in liste_carrer:
		# On calcul l'id
		xpos = int(classmap.mapcanv.gettags(tuile)[2])
		ypos = int(classmap.mapcanv.gettags(tuile)[3])

		idtuile = xpos + (classmap.mapx*ypos)

		# On test si la tuile est toujours valable
		# Si elle ne l'est pas on la suicide
		if genproc.buildvillagepossible(option, classmap, idtuile) == False:
			classmap.mapcanv.delete(tuile)

############################################# Build Church #############################################

def statebuildchurch(gamedata, classmap, option):
	######
	# Fonction Appeler par le menu pour construire une église
	######

	if len(gamedata.exit)>0:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[1], gamedata.exit[2])

	player = gamedata.list_lord[gamedata.playerid]
	ts = gamedata.tuilesize
	xoriginewindow = classmap.mapcanv.canvasx(0)
	yoriginewindow = classmap.mapcanv.canvasy(0)
	originecanvas = classmap.mapcanv.coords(classmap.listmap[0].canvastuiles)

	# On affiche une interface montrant une liste des villages ou on peut construire + données du village

	# On créer la frame
	window_interface_church = tkinter.Frame(classmap.framecanvas)
	window_interface_church.place(x = (option.widthWindow/6), y = (option.heightWindow*0.2))

	frame_interface_church = tkinter.Frame(window_interface_church)
	frame_interface_church.grid()

	# On créer la listbox
	tkinter.Label(frame_interface_church, text = "Village").grid(row = 0, column = 0)
	tkinter.Label(frame_interface_church, text = "Cout: 10 Ressource, 10 Écus").grid(row = 1, column = 0)
	tkinter.Label(frame_interface_church, text = f"Église gratuite: {player.freechurch}").grid(row = 2, column = 0)
	lc_interface_church = tkinter.Listbox(frame_interface_church)
	lc_interface_church.grid(row = 3, column = 0)
	# On créer un menu déroulant qui présente les villages éligible à la construction d'une église avec les donnés du villag
	for village in player.fief:
		if village.church == 0:
			lc_interface_church.insert(tkinter.END, village.name)
			# On affiche en vert tout les villages ou on peut construire une église
			x = village.x
			y = village.y
			classmap.mapcanv.create_rectangle(originecanvas[0]+(x*ts)-(ts/2), originecanvas[1]+(y*ts)-(ts/2), originecanvas[0]+(x*ts)+ts-(ts/2), originecanvas[1]+(y*ts)+ts-(ts/2), tags = ["buildchurch","tuile"], outline = "green", width = 2)
	# Quand un village est double click on appele la fonction pour centrer la vue sur le village
	lc_interface_church.bind("<Double-Button-1>", lambda event: centervillagechurch(event, gamedata, classmap, option))

	# On bind la fonction buildchurch à la tuile du village
	idbuildchurch = classmap.mapcanv.tag_bind("village", "<Button-1>", lambda event: triggerbuildchurch_statebchurch(gamedata, classmap, option), add = "+")
	# On bind la fonction buildchurch au square
	classmap.mapcanv.tag_bind("buildchurch", "<Button-1>",lambda event: triggerbuildchurch_statebchurch(gamedata, classmap, option))

	# On bind la fonction d'exit à tout ce qui n'est pas un village
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event, lsequ = ["village","<Button-1>"], lf = [idbuildchurch], lidw = [window_interface_church, "buildchurch"]: exitstate(gamedata, classmap, option, lsequ, lf, lidw))
	gamedata.exit = [[["village","<Button-1>"]], [idbuildchurch], [window_interface_church, "buildchurch"]]


def centervillagechurch(event, gamedata, classmap, option):
	############
	# Fonction appeler par la listbox lc_interface_church pour centrer la carte sur le village selectionner dans la listbox
	# On sait que les noms des villages sont uniques
	############
	log.log.printinfo("On se déplace vers le village")
	# On recup le village actuellement selectionner dans la listbox
	village_selected = event.widget.get(event.widget.curselection()[0])
	
	idvillage = classmap.nametoid(village_selected)
	# On recup les coord du village
	x = classmap.listmap[idvillage].x
	y = classmap.listmap[idvillage].y

	coord = common.coordmaptocanvas(gamedata, classmap, option, [x, y], True)

	# On centre la vu sur le village
	moveview.centerviewcanvas(gamedata, classmap, option, coord)

def triggerbuildchurch_statebchurch(gamedata, classmap, option):
	############
	# Fonction pour actionner la construction d'église depuis l'état build church
	############
	# On recup les coord Canvas de la tuile:
	coord = classmap.mapcanv.coords("current")
	# On les transforme en coord map
	coordmap = common.coordcanvastomap(gamedata, classmap, option, coord)
	idvillage = common.coordmaptoidtuile(classmap, coordmap)
	village = classmap.listmap[idvillage].village

	triggerbuildchurch(gamedata ,classmap, option, village)

def triggerbuildchurch(gamedata, classmap, option, village):
	############
	# Fonction pour construire une église dans un village
	############

	player = gamedata.list_lord[gamedata.playerid]

	ts = gamedata.tuilesize

	# On vérife que le village appartient au joueur
	if village in player.fief:
		if village.church == 0:
			# On Verifie que le joueur possède l'argent nécessaire
			if ((player.verifcost(10,10)) or (player.freechurch >= 1)):
				# On construit
				village.buildchurch(asset.dico_name.randomnametype("Nom"))
				# Si on à une église gratuite On ne perd pas de ressource
				if player.freechurch >= 1:
					player.freechurch -= 1
				else:
				# On retire l'argent Si on à pas d'église gratuite
					player.sub_money(10)
					player.sub_ressource(10)
				# On update l'interface
				updateinterface(gamedata, classmap)
				coord = [option.widthWindow//2, option.heightWindow//8]
				interfacemenu.temp_message(classmap.mapcanv, f"Église Construite\nCapacité du Prêtre:{village.priest.ability}", 2000, coord, "green")
			else:
				coord = [option.widthWindow//2, option.heightWindow//8]
				interfacemenu.temp_message(classmap.mapcanv, "Pas Assez de Ressource", 2000, coord, "red")
		else:
			coord = [option.widthWindow//2, option.heightWindow//8]
			interfacemenu.temp_message(classmap.mapcanv, "Ce Village possède déjà Une église", 2000, coord, "red")		
	else:
		coord = [option.widthWindow//2, option.heightWindow//8]
		interfacemenu.temp_message(classmap.mapcanv, "Va te faire foutre c'est pas ton Village !", 2000, coord, "red")

def deltuilecoordcanvas(gamedata, classmap, option, tag, coord):
	############
	# Fonction pour détruire une tuile du Canvas avec le tag sélectionner
	############
	# On recup la liste des tuile
	ltuile = classmap.mapcanv.find_withtag(tag)
	# On se balade dedans
	for tuile in ltuile:
		coordtuile = classmap.mapcanv.coords(tuile)
		if (coordtuile[0] == coord[0]) and (coordtuile[1] == coord[1]):
			classmap.mapcanv.delete(tuile)
			return

################################################  Tax  #################################################

def statetax(gamedata, classmap, option):

	if len(gamedata.exit)>0:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[1], gamedata.exit[2])

	player = gamedata.list_lord[gamedata.playerid]
	# Crée la (window) frame de l'interface pour afficher les taxes
	window_interface_tax = tkinter.Frame(classmap.framecanvas)
	window_interface_tax.place( x=(option.widthWindow/6), y=(option.heightWindow*0.2))

	# Crée la frame de l'interface
	frame_interface_tax = tkinter.Frame(window_interface_tax)
	frame_interface_tax.grid()

	# On affiche Village
	tkinter.Label(frame_interface_tax, text = "village:").grid(row = 0)

	# Crée la listbox pour afficher les villages que l'on peut taxer
	lc_village_tax = tkinter.Listbox(frame_interface_tax)
	lc_village_tax.grid(row = 1)

	# On affiche Vassal
	tkinter.Label(frame_interface_tax, text = "Vassaux:").grid(row = 2)
	# Crée la listbox pour afficher les vassaux que l'on peut taxer
	lc_vassal_tax = tkinter.Listbox(frame_interface_tax)
	lc_vassal_tax.grid(row = 3)

	# On affiche les taxes des villages du joueur
	for village in player.fief:
		lc_village_tax.insert(tkinter.END, village.name)

	# On affiche pour les vassaux:
	for vassal in player.vassal:
		lc_vassal_tax.insert(tkinter.END, vassal.lordname)

	# On bind pour les villages
	lc_village_tax.bind("<Double-Button-1>", lambda event, wit = window_interface_tax: taxcentervillage(event, gamedata, classmap, option, wit))
	# On bind pour les vassaux
	lc_vassal_tax.bind("<Double-Button-1>", lambda event, wit = window_interface_tax: taxcentervassal(event, gamedata, classmap, option, wit))
	# Exit la fonction si l'utilisateur clique ailleurs (sur la carte)
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [window_interface_tax]))
	gamedata.exit = [[], [], [window_interface_tax]]


def calculate_tax_village(village):
	#####
	# Fonctions qui renvoit une liste contenant en position 0 l'Argent total et en position 1 les Ressources total que peut récolter le seigneurs dans le village donner
	#####
	tax_m = 0
	tax_r = 0
	# On se balade dans la liste des villageois
	for roturier in village.population:
		tax_m += roturier.tax_money()
		tax_r += roturier.tax_ressource()

	return [tax_m, tax_r]

def calculate_tax_vassal(vassal):
	#####
	# Fonctions qui renvoit une liste contenant en position 0 l'Argent total et en position 1 les Ressources total que peut récolter le seigneurs pour la vassal donner
	#####
	tax = [ int(vassal.nb_money*(1/4)), int(vassal.nb_ressource*(1/4))]
	if (tax[0] == 0) or (tax[1] == 0):
		taxtemp = [0,0]
		for village in vassal.fief:
			taxtemp2 = village.calculate_tax_village()
			taxtemp[0] += taxtemp2[0]
			taxtemp[1] += taxtemp2[1]
		if tax[0] == 0:
			tax[0] = taxtemp[0]
		if tax[1] == 0:
			tax[1] = taxtemp[1]
	return tax

def taxcentervillage(event, gamedata, classmap, option, wit):
	##########
	# Fonction qui place le village selectioner dans la listbox au centre de l'écran est affiche une interface pour taxer soit l'argent soit les ressources
	##########

	# On recup le nom du village
	village_selected = event.widget.get(event.widget.curselection()[0])
	# On calcul son id
	idvillage = classmap.nametoid(village_selected)
	# On recup l'objet village
	village = classmap.listmap[idvillage].village
	# On récupère les coordonnées du village
	x = classmap.listmap[idvillage].x
	y = classmap.listmap[idvillage].y
	# On déplace la vue de la carte sur ce village
	coord = common.coordmaptocanvas(gamedata, classmap, option, [x, y], True)
	moveview.centerviewcanvas(gamedata, classmap, option, coord)

	# On met en place l'interface
	taxwindow_village(gamedata, classmap, option, wit, village)

def taxcentervassal(event, gamedata, classmap, option, wit):
	##########
	# Fonction qui place le village selectioner dans la listbox au centre de l'écran est affiche une interface pour taxer soit l'argent soit les ressources
	##########

	# On recup le nom du vassal
	vassal_selected = event.widget.get(event.widget.curselection()[0])
	# On calcul son id
	idvassal = gamedata.lordnametoid(vassal_selected)
	# On recup l'objet vassal
	vassal = gamedata.list_lord[idvassal]
	# On récupère les coordonnées du village principal du vassal
	x = vassal.fief[0].x
	y = vassal.fief[0].y
	# On déplace la vue de la carte sur ce village
	coord = common.coordmaptocanvas(gamedata, classmap, option, [x, y], True)
	moveview.centerviewcanvas(gamedata, classmap, option, coord)

	# On met en place l'interface 
	taxwindow_vassal(gamedata, classmap, option, wit, vassal)

def taxwindow_village(gamedata, classmap, option, wit, village):
	######
	# Fonction Pour mettre en place l'interface
	######
	# On met en places l'interfaces
	frame_tax_collect = tkinter.Frame(wit)
	frame_tax_collect.grid(row = 0, column = 1)
	# On affiche plus d'info sur la populations
	tkinter.Label(frame_tax_collect, text = "Taxe:").grid(row = 0, column = 1)

	tax = village.calculate_tax_village()
	tkvar_money = tkinter.StringVar()
	tkvar_money.set(f"Collecter {tax[0]} écus")
	tkvar_ressource = tkinter.StringVar()
	tkvar_ressource.set(f"Collecter {tax[1]} ressource")

	tkvar_list = [tkvar_money, tkvar_ressource]
	button_collect_tax_money = tkinter.Button(frame_tax_collect, textvariable = tkvar_list[0], command=lambda: collect_taxes_village(gamedata, classmap, option, village, "money", frame_tax_collect, tkvar_list))
	button_collect_tax_money.grid(row = 3, column = 1)

	button_collect_tax_ressource = tkinter.Button(frame_tax_collect, textvariable = tkvar_list[1], command=lambda: collect_taxes_village(gamedata, classmap, option, village, "ressource", frame_tax_collect, tkvar_list))
	button_collect_tax_ressource.grid(row = 4, column = 1)

	interfacemenu.tooltip(button_collect_tax_money, f"Taxe en Ressource:\n 1/4 les Artisans\n 1/2 les Paysan", [])
	interfacemenu.tooltip(button_collect_tax_ressource, f"Taxe en Écus:\n 1/4 les Artisans\n 1/2 les Paysan", [])

	# Boutton pour quitter
	tkinter.Button(frame_tax_collect, text = "retour", command = lambda: global_exit_window(frame_tax_collect)).grid(row = 5, column = 1)

def global_exit_window(window):
	######
	# Fonction global pour quitter quitter une fenêtre ou une frame
	######
	window.destroy()

def taxwindow_vassal(gamedata, classmap, option, wit, vassal):
	######
	# Fonction Pour mettre en place l'interface
	######
	# On met en places l'interfaces
	frame_tax_collect = tkinter.Frame(wit)
	frame_tax_collect.grid(row = 0, column = 1)
	# On affiche plus d'info sur la populations

	tax = calculate_tax_vassal(vassal)

	tkvar_tax = tkinter.StringVar()
	tkvar_tax.set(f"Collecter {tax[0]} écus et {tax[1]} ressource")

	button_collect_tax_money = tkinter.Button(frame_tax_collect, textvariable = tkvar_tax, command=lambda: collect_taxes_vassal(gamedata, classmap, vassal, frame_tax_collect, tkvar_tax))
	button_collect_tax_money.grid(row = 3, column = 1)

def collect_taxes_village(gamedata, classmap, option, village, type_tax, frame, tkvar_list):
	#####
	# Fonction associer au Bouton pour collecter taxes 
	#####

	# On recup le joueur
	player = gamedata.list_lord[gamedata.playerid]
	taxinit = village.calculate_tax_village()

	# Si argent on tax l'argent
	if type_tax == "money":
		# On se balade parmi les roturier du village
		for roturier in village.population:
			# ON les faits payer leur taxes
			roturier.pay_tax_money(player)
		tax = village.calculate_tax_village()
		# On update l'interface
		tkvar_list[0].set(f"Collecter {tax[0]} écus")
		addsubinterface(gamedata, classmap, option, taxinit[0], 0)

	# Si ressource on tax les ressources
	else:
		# On se balade parmi les roturier du village
		for roturier in village.population:
			# ON les faits payer leur taxes
			roturier.pay_tax_ressource(player)
		tax = village.calculate_tax_village()
		# On update l'interface
		tkvar_list[1].set(f"Collecter {tax[1]} ressource")
		addsubinterface(gamedata, classmap, option, 0, taxinit[1])

	# On update les infos du village
	village.updateinfo()
	# On update l'entête
	updateinterface(gamedata, classmap)

def collect_taxes_vassal(gamedata, classmap, vassal, frame, tkvar_tax):
	#####
	# Fonction associer au Bouton pour collecter taxes 
	#####

	# On recup le joueur
	player = gamedata.list_lord[gamedata.playerid]

	# Le vassal paye la tax
	vassal.tax(player)

	# On recalcul ce qu'il peut payer
	tax = calculate_tax_vassal(vassal)

	# On update l'interface
	tkvar_tax.set(f"Collecter {tax[0]} écus et {tax[1]} ressource")
	# On update l'entête
	updateinterface(gamedata, classmap)

############################################# Immigration ##############################################

def stateimmigration(gamedata, classmap, option):
	######
	#
	######

	if len(gamedata.exit)>0:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[1], gamedata.exit[2])

	player = gamedata.list_lord[gamedata.playerid]
	#Crée la frame de l'interface pour afficher les villages
	window_interface_immigration = tkinter.Frame(classmap.framecanvas)
	window_interface_immigration.place(x=(option.widthWindow/6), y=(option.heightWindow* 0.2))

	frame_interface_immigration = tkinter.Frame(window_interface_immigration)
	frame_interface_immigration.grid()

	# On affiche Village
	tkinter.Label(frame_interface_immigration, text = "Village").grid(row = 0, column = 0)
	#Crée la listbox pour afficher les villages du joueur
	lc_interface_immigration = tkinter.Listbox(frame_interface_immigration)
	lc_interface_immigration.grid(row = 1, column = 0)

    #On affiche les villages appartenant au joueur
	for village in player.fief:
		lc_interface_immigration.insert(tkinter.END, village.name)
	lc_interface_immigration.bind("<Double-Button-1>", lambda event: centervillage_immigration(event, gamedata, classmap, option, window_interface_immigration))
        #Quitte l'interface si l'utilisateur clique ailleurs
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [window_interface_immigration]))
	gamedata.exit = [[], [], [window_interface_immigration]]

def centervillage_immigration(event, gamedata, classmap, option, wii):
	#######
	#
	#######
	village_selected = event.widget.get(event.widget.curselection()[0])
	idvillage = classmap.nametoid(village_selected)
	village = classmap.listmap[idvillage].village
	#on récupère les coordonnées du village et centre la vue
	x = village.x
	y = village.y
	
	coord = common.coordmaptocanvas(gamedata, classmap, option, [x, y], True)
	#On déplace la vue de la carte sur ce village
	moveview.centerviewcanvas(gamedata, classmap, option, coord)
	# On affiche l'interface
	immigrationwindow(gamedata, classmap, option, wii, village)

def button_add_population(gamedata, classmap, option, village, role, tkvar_list):
	################
	# Fonctions liées aux button pour ajouter de la pop dans l'interface d'immigration
	################
	player = gamedata.list_lord[gamedata.playerid]
	coord = [option.widthWindow//2, option.heightWindow//8]

	if (role == "paysan"):
		# On verifie que le joueuer à suffisament en stock
		if player.verifcost(1, 1) == True:
			# On ajoute la pop
			genproc.genpopvillage(gamedata, classmap, option, village, 1, 0)
			# On retire au joueur
			player.sub_ressource(1)
			player.sub_money(1)
			if village.priest != 0:
				if village.priest.ability == "Bonus_Immigration":
					log.log.printinfo(f"la Capacité {village.priest.ability} de {village.priest.name} s'active !")
					genproc.genpopvillage(gamedata, classmap, option, village, 1, 0)

			addsubinterface(gamedata, classmap, option, -1, -1)
		else:
			interfacemenu.temp_message(classmap.mapcanv, "Pas Assez de Ressource\n Besoin de 1 Ressources et 1 écus", 2000, coord, "red")


	elif role == "artisan":
		if player.verifcost(4, 4) == True:
			genproc.genpopvillage(gamedata, classmap, option, village, 0, 1)
			player.sub_ressource(4)
			player.sub_money(4)
			if village.priest != 0:
				if village.priest.ability == "Bonus_Immigration":
					log.log.printinfo(f"la Capacité {village.priest.ability} de {village.priest.name} s'active !")
					genproc.genpopvillage(gamedata, classmap, option, village, 1, 0)
			addsubinterface(gamedata, classmap, option, -4, -4)
		else:
			interfacemenu.temp_message(classmap.mapcanv, "Pas Assez de Ressource\n Besoin de 4 Ressources et 4 écus", 2000, coord, "red")


	# On update l'interface Immigration
	tkvar_list[0].set(f"Nb Pop: {len(village.population)}")
	tkvar_list[1].set(f"Nb Paysan: {village.nb_paysan}")
	tkvar_list[2].set(f"Nb artisan: {village.nb_artisan}")
	# On update l'interface Entête
	updateinterface(gamedata, classmap)



def immigrationwindow(gamedata, classmap, option, wii, village):
	#####
	# Fonction Pour afficher la fenêtre d'immigration
	#####

	# Frame
	frame_immigration = tkinter.Frame(wii)
	frame_immigration.grid(row = 0, column = 1)

	# Info
	# Nb pop du village
	tkvar_nbpop = tkinter.StringVar()
	tkvar_nbpop.set(f"Nb Pop: {len(village.population)}")
	tkinter.Label(frame_immigration, textvariable = tkvar_nbpop).grid(row = 1,column = 1)
	# Nb paysan
	tkvar_nb_paysan = tkinter.StringVar()
	tkvar_nb_paysan.set(f"Nb Paysan: {village.nb_paysan}")
	tkinter.Label(frame_immigration, textvariable = tkvar_nb_paysan).grid(row = 2,column = 1)

	# Nb Artisan
	tkvar_nb_artisan = tkinter.StringVar()
	tkvar_nb_artisan.set(f"Nb artisan: {village.nb_artisan}")
	tkinter.Label(frame_immigration, textvariable = tkvar_nb_artisan).grid(row = 3,column = 1)


	tkvar_list = [tkvar_nbpop, tkvar_nb_paysan, tkvar_nb_artisan]

	#Ajout des bouton pour gérer l'immigration
	#Bouton pour ajouter un paysan
	button_add_paysan = tkinter.Button(frame_immigration,text="Ajouter un Paysan",command=lambda: button_add_population(gamedata, classmap, option, village, "paysan", tkvar_list))
	button_add_paysan.grid(row = 4, column = 1)
	#Bouton pour ajouter un artisan
	button_add_artisan = tkinter.Button(frame_immigration,text="Ajouter un Artisan",command=lambda: button_add_population(gamedata, classmap, option, village, "artisan", tkvar_list))
	button_add_artisan.grid(row = 5, column = 1)

	# On ajoute les tooltip
	interfacemenu.tooltip(button_add_paysan, "Demande 1 ressources et 1 écus",[])
	interfacemenu.tooltip(button_add_artisan, "Demande 4 ressources et 4 écus",[])


	tkinter.Button(frame_immigration ,text = "retour", command = lambda: global_exit_window(frame_immigration)).grid(row = 6, column = 1)

###############################################################################################

##############################################\ Interface Objet \########################################

def villageinterface(event, gamedata, classmap, option):
	##################
	# Fonction pour afficher l'interface d'un village
	##################

	# Si le joueur est dans un état ou il a déjà l'interface d'un village ouvert on ne fait rien
	#if gamedata.changenewstate("interface_village") == False:
	#monkey patch
	if len(gamedata.exit)>0:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[1], gamedata.exit[2])
		gamedata.changenewstate("build_village")

	# On recup les coord-canvas du village
	coordcanv = event.widget.coords("current")
	print(classmap.mapcanv.gettags("current"))
	print(len(classmap.mapcanv.gettags("current")))
	# On recup l'idMapvillage
	# Si objet village
	if (len(classmap.mapcanv.gettags("current")) > 5):
		idmapvillage = int(classmap.mapcanv.gettags("current")[4])
	# Si objet Label
	else:
		idmapvillage = int(classmap.mapcanv.gettags("current")[3])
	log.log.printinfo(f"idvillage : {idmapvillage}")

	####################\ Comment j'ai fait ???? \########################
	# On place le village au centre de l'écran
	moveview.centerviewcanvas(gamedata, classmap, option, coordcanv)
	######################################################################

	####################\ Affichage de l'interface \########################

	# On recup l'origine du canvas
	xorigine = classmap.mapcanv.canvasx(0)
	yorigine = classmap.mapcanv.canvasy(0)

	log.log.printinfo("On affiche l'interface du village")
	# On fait apparaitre l'interface informative
	# On commence par créer le frame qui vient stocker les infos
	window_info = tkinter.Frame(classmap.framecanvas)
	# On créer la frame qui vient contenir les actions possibles
	window_button = tkinter.Frame(classmap.framecanvas)
	window_info.place(x = (option.widthWindow//4), y = (option.heightWindow*0.2))
	window_button.place(x = int(option.widthWindow*0.6), y = (option.heightWindow*0.2))

	frame_info = tkinter.Frame(window_info)
	frame_info.grid()

	frame_button = tkinter.Frame(window_button)
	frame_button.grid()

	# On créer les fenêtre
	# Demande un placement précis
	canvas_window_list = [window_info, window_button]

	# On recup l'objet village
	village = classmap.listmap[idmapvillage].village

	# On affiche les infos voulu
	llabel_village = []
	# Le nom du village
	tkinter.Label(frame_info, text = village.name).grid(row = 0, column = 0)
	log.log.printinfo(f"{village.name}")
	# Le seigneur du village
	if (classmap.listmap[idmapvillage].village.lord == 0):
		lordlabel = tkinter.Label(frame_info, text = "Village Indépendant")
		lordlabel.grid(row = 1, column = 0)
	else:
		lordlabel = tkinter.Label(frame_info, text = f"Seigneur: {village.lord.lordname}")
		lordlabel.grid(row = 1, column = 0)
	llabel_village += [lordlabel]
	# Le prêtre du village
	if village.priest == 0:
		priestlabel = tkinter.Label(frame_info, text = "Prêtre: Aucun")
		priestlabel.grid(row = 2, column = 0)
	else:
		priestlabel = tkinter.Label(frame_info, text = f"Prêtre: {village.priest.name}")
		priestlabel.grid(row = 2, column = 0)
	llabel_village += [priestlabel]

	# Le bonheur global
	joylabel = tkinter.Label(frame_info, text = f"Humeur: {village.global_joy}%")
	joylabel.grid(row = 3, column = 0)
	llabel_village += [joylabel]

	# les ressources du village
	ressourcelabel = tkinter.Label(frame_info, text = f"Produit: {village.prod_ressource} ressources")
	ressourcelabel.grid(row = 4, column = 0)
	llabel_village += [ressourcelabel]
	# l'argent du village
	moneylabel = tkinter.Label(frame_info, text = f"Produit: {village.prod_money} écus")
	moneylabel.grid(row = 5, column = 0)
	llabel_village += [moneylabel]
	# Boutton Vue détaillée
	tkinter.Button(frame_info, text = "Vue détaillée", command = lambda: b_village_stat(gamedata, classmap, option, village, frame_info)).grid(row = 6, column = 0)


	# Si le village appartient au joueur on affiche l'interface Button
	# On vérifie que l'objet village est présent dans la liste de fief du joueur
	if village in gamedata.list_lord[gamedata.playerid].fief:
		tkinter.Label(frame_button, text = "Action").grid(row = 0, column = 0)
		# On fait apparaitre les boutons
		button_build_church = tkinter.Button(frame_button, text = "Construire Église", command = lambda: triggerbuildchurch_statevinterface(gamedata, classmap, option, village, llabel_village))
		button_immigration = tkinter.Button(frame_button, text = "Immigration", command = lambda: immigrationwindow(gamedata, classmap, option, window_button, village))
		button_tax = tkinter.Button(frame_button, text = "Impôt", command = lambda: taxwindow_village(gamedata, classmap, option, window_button, village))

		button_build_church.grid(row = 1, column = 0)
		button_immigration.grid(row = 2, column = 0)
		button_tax.grid(row = 3, column = 0)

	######################################################################

	# Si le joueur clique autre part on sort de l'interface
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event, cwl = canvas_window_list: exitstate(gamedata, classmap, option, [], [], cwl))
	gamedata.exit = [[], [], canvas_window_list]


def b_village_stat(gamedata, classmap, option, village, frame_info):
	################
	# Fonction créer pour afficher la Fenêtre de Vue détaillée du village
	################
	# On créer la fenêtre
	window_village_stat = tkinter.Frame(classmap.framecanvas, pady = (option.heightWindow/20))
	window_village_stat.place(x = (option.widthWindow/8), y = (option.heightWindow/20))
	# On créer la frame
	frame_village_stat = tkinter.Frame(window_village_stat)
	frame_village_stat.grid()

	i = 0
	# On Affiche les Infos de base du Village
	for legend in ("Village", "Population", "Bonheur", "Production de Ressource", "Production d'argent", "Prêtre", "Capacité du Prêtre"):
		tkinter.Label(frame_village_stat, text = legend).grid(row = 0, column = i)
		i += 1
	i = 0
	for ele in (village.name, len(village.population), village.global_joy, village.prod_ressource, village.prod_money, village.priest):
		if ele == village.priest:
			if ele != 0:
				tkinter.Label(frame_village_stat, text = village.priest.name).grid(row = 1, column = i)
				tkinter.Label(frame_village_stat, text = village.priest.ability).grid(row = 1, column = i+1)
			else:
				tkinter.Label(frame_village_stat, text = "X").grid(row = 1, column = i)
				tkinter.Label(frame_village_stat, text = "X").grid(row = 1, column = i+1)
		else:
			tkinter.Label(frame_village_stat, text = ele).grid(row = 1, column = i)
		i += 1

	for j in range(7):
		tkinter.Label(frame_village_stat, text = "-----------------").grid(row = 2, column = j)


	# On affiche les Artisans
	i = 0
	for legend in ("Role", "Nom", "Bonheur", "Ressource", "Écus", "Capacité Production", "CP Bonus", "CP Malus"):
		tkinter.Label(frame_village_stat, text = legend).grid(row = 3,column = i)
		i += 1

	i = 4
	for pop in village.population:
		j = 0
		for ele in (pop.role, pop.name, pop.joy, pop.ressource, pop.money, pop.cp, pop.cpbonus, pop.cpmalus):
			tkinter.Label(frame_village_stat, text = ele).grid(row = i, column = j)
			j += 1
		i += 1
	tkinter.Button(frame_village_stat, text = "Quitter", command = lambda: exit_village_stat(window_village_stat)).grid(row = i, columnspan = 7, sticky = tkinter.S)
	# Si le frame_info au dessus est détruit on quitte
	frame_info.bind("<Destroy>", lambda event: exit_village_stat(window_village_stat))

def exit_village_stat(wvs):
	#######
	# Fonction pour quitter l'interface Village stat
	#######
	wvs.destroy()

def triggerbuildchurch_statevinterface(gamedata, classmap, option, village, llabel_village):
	############
	# Fonction pour actionner la construction d'église depuis l'état village interface
	############

	triggerbuildchurch(gamedata ,classmap, option, village)
	# On update l'interface du village
	llabel_village[1].configure(text = f"Prêtre: {village.priest.name}")



########################\ Interface Armée \##########################################

def armyinterface(event, gamedata, classmap, option):
	################
	# Fonction créer la fenêtre de l'interface de l'armée selectionné
	################

	if gamedata.changenewstate("interface_army") == False:
		exitstate(gamedata, classmap, option, gamedata.exit[0], gamedata.exit[1], gamedata.exit[2])
	# On créer le frame
	window_interface_army = tkinter.Frame(classmap.framecanvas)
	window_interface_army.place(x = (option.widthWindow/3), y = (option.heightWindow/2))

	frame_interface_army = tkinter.Frame(window_interface_army)
	frame_interface_army.grid()

	ts = gamedata.tuilesize
	# on recup les coord (0,0) de la window
	xorigine = classmap.mapcanv.canvasx(0)
	yorigine = classmap.mapcanv.canvasy(0)

	# On recup les coord canvas
	posx = classmap.mapcanv.coords(classmap.mapcanv.find_withtag("current"))[0]
	posy = classmap.mapcanv.coords(classmap.mapcanv.find_withtag("current"))[1]
	# On recup l'objet army
	army = gamedata.coordtoarmy(gamedata.playerid, [int((posx-ts/2)/ts), int((posy-ts/2)/ts)])

	# Si l'armée à un déplacement en cours On affiche la Trajectoire
	#if gamedata.inactionfile(army, "army") == True:
	#	On recup les coord ciblé
	#	coord = 
	#	showpathfindingCoord(coord, gamedata, classmap, option, army)

	if army != False:
		# On affiche le nom
		tkinter.Label(frame_interface_army, text = army.name).grid(row = 0, column = 0)
		# On affiche la puissance
		tkinter.Label(frame_interface_army, text = "Puissance: ").grid(row = 0, column = 1)
		tkinter.Label(frame_interface_army, text = army.power).grid(row = 0, column = 2)

		tkinter.Label(frame_interface_army, text = "Movement").grid(row = 0, column = 3)

		# On affiche la capacité de déplacement max/déplacement du tour
		label_movement = tkinter.Label(frame_interface_army, text = f"{army.moveturn}/{army.movecapacity}")
		label_movement.grid(row = 0, column = 4)

		# On créer le bouton pour se déplacer
		Button_move_army = tkinter.Button(frame_interface_army, text = "Déplacement", command = lambda: statemovearmy(gamedata, classmap, option, army, window_interface_army, label_movement))
		Button_move_army.grid(row = 0, column = 6)

		# Si on clique sur autre chose on quitte l'interface
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [window_interface_army]))
		gamedata.exit = [[], [], [window_interface_army]]
	else:
		exitstate(gamedata, classmap, option, [], [], [window_interface_army])



def statemovearmy(gamedata, classmap, option, army, fra, label_movement):
	##################
	# Fonction pour Entréer le joueur dans un état de déplacement d'armé Si il clique sur le bouton déplacer dabs l'interface d'armée
	##################

	# On bind l'affiche de la trajectoire sur l'emplacement de la souris quand elle est sur le canvas
	funcpath = classmap.mapcanv.tag_bind("click","<Motion>", lambda event: showpathfinding(event, gamedata, classmap, option, army), add= "+")

	# On debind le exitstate
	classmap.mapcanv.tag_unbind("click", "<Button-1>")

	# On bind le click gauche sur aller 
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: startstartsequencemoveunit(event, gamedata, classmap, option, army, label_movement))

	# On bind sur les villages l'attaque
	funcvillage =  classmap.mapcanv.tag_bind("village", "<Button-1>", lambda event: startsequencemovetakevillage(event, gamedata, classmap, option, army), add= "+")

	# On bind sur les armées l'attaque
	funcarmy = classmap.mapcanv.tag_bind("army", "<Button-1>", lambda event: startsequencemovefight(event, gamedata, classmap, option, army), add= "+")

	# On bind l'exit de l'état aux clic droit (ET MERDE SUR LINUX C'EST PAS LE MÊME)
	if option.os == "darwin":
		classmap.mapcanv.bind("<Button-2>", lambda event: cancelmovearmy(event, gamedata, classmap, option, [funcpath, funcvillage, funcarmy], fra))
	else:
		classmap.mapcanv.bind("<Button-3>", lambda event: cancelmovearmy(event, gamedata, classmap, option, [funcpath, funcvillage, funcarmy], fra))

def showpathfinding(event, gamedata, classmap, option, army):
	################
	# Fonction liée a l'event de tkinter pour afficher le Pathfinding
	################

	# On recup les coord Canvas
	posx = event.widget.canvasx(event.x)
	posy = event.widget.canvasy(event.y)
	# On transforme en coord Map
	coord1 = common.coordcanvastomap(gamedata, classmap, option, [posx, posy])

	showpathfindingCoord(coord1, gamedata, classmap, option, army)

def showpathfindingCoord(coord1, gamedata, classmap, option, army):
	################
	# Fonction qui affiche le chemin que va parcourir l'armée pour atteindre la case
	# Elle affiche en vert le chemin que l'armée parcoura ce tour
	# Elle affiche en rouge le chemin que l'armée ne parcoura pas ce tour
	################
	# On calcul la meilleur trajectoire
	sequ = affichage.pathfinding(gamedata, classmap, option,[army.x, army.y], coord1, 45)

	# On détruit la précédante trajectoire afficher
	classmap.mapcanv.delete("path")

	ts = gamedata.tuilesize

	# On affiche la trajectoire
	move = army.moveturn
	turn = 0
	color = "green"
	i = 0
	lensequ = len(sequ)
	while i < (lensequ-1):
		# On place l'oval à la dernière coord
		if i+1 == (lensequ-1):
			classmap.mapcanv.create_oval((sequ[i][0]*ts), (sequ[i][1]*ts), (sequ[i][0]*ts)+ts, (sequ[i][1]*ts)+ts, width = 2, tags = "path", outline = color)
		else:
			#On calcule la tuile à partir des coord Map
			idtuile = common.coordmaptoidtuile(classmap, sequ[i])
			idtuile2 = common.coordmaptoidtuile(classmap, sequ[i+1])
			if color == "green":
				if(move - classmap.listmap[idtuile2].movementcost) < 0:
					classmap.mapcanv.create_oval((sequ[i][0]*ts), (sequ[i][1]*ts), (sequ[i][0]*ts)+ts, (sequ[i][1]*ts)+ts, width = 2, tags = "path", outline = color)
					classmap.mapcanv.create_text((sequ[i][0]*ts)+ts/2, (sequ[i][1]*ts)+ts/2, tags = "path", text = turn, fill = color)
					color = "red"
					move = army.movecapacity
				else:
					move -= classmap.listmap[idtuile].movementcost	
			else:
				if (move - classmap.listmap[idtuile].movementcost) >= 0:
					move -= classmap.listmap[idtuile].movementcost	
				else:
					turn += 1
					move = army.movecapacity
					classmap.mapcanv.create_oval((sequ[i][0]*ts), (sequ[i][1]*ts), (sequ[i][0]*ts)+ts, (sequ[i][1]*ts)+ts, width = 2, tags = "path", outline = color)
					classmap.mapcanv.create_text((sequ[i][0]*ts)+ts/2, (sequ[i][1]*ts)+ts/2, tags = "path", text = turn, fill = color)

			classmap.mapcanv.create_line((sequ[i][0]*ts), (sequ[i][1]*ts), (sequ[i+1][0]*ts), (sequ[i+1][1]*ts), width = 2, tags = "path", fill = color)
		i += 1

def startstartsequencemoveunit(event, gamedata, classmap, option, army, label_movement):
	######
	# Fonction pour gérer le lancement du mouvement de l'armée
	######
	# On lance la sequence
	startsequencemoveunit(event, gamedata, classmap, option, army)
	# On update l'interface
	label_movement.config(text = f"{army.moveturn}/{army.movecapacity}")
	# On update le Pathfinding
	showpathfinding(event, gamedata, classmap, option, army)

def startsequencemoveunit(event, gamedata, classmap, option, army):
	##################
	# Fonctions pour entamer le déplacement d'une armée vers la case clicker
	##################
	gamedata.removeactionfile(army)
	# On recup les coord canvas de la tuile Viser
	posfinalx = classmap.mapcanv.canvasx(event.x)
	posfinaly = classmap.mapcanv.canvasy(event.y)
	# On les transforme en coord map
	coordmap = common.coordcanvastomap(gamedata, classmap, option, [posfinalx, posfinaly])
	log.log.printinfo(f"coordmap: ,{coordmap}")
	affichage.sequencemoveunit(gamedata, classmap, option, army, coordmap)



def cancelmovearmy(event, gamedata, classmap, option, lfuncpath, fra):
	################
	# Fonction pour annuler l'état de déplacement d'armée déplacement d'une armée
	################
	log.log.printinfo("exit movearmy")
	# On debind l'affichage
	classmap.mapcanv.tag_unbind("click", "<Motion>", lfuncpath[0])

	# On debind l'attaque de village
	classmap.mapcanv.tag_unbind("village", "<Button-1>", lfuncpath[1])

	# On debind l'attaque d'armée
	classmap.mapcanv.tag_unbind("army", "<Button-1>", lfuncpath[2])

	# On détruit les chemins afficher
	classmap.mapcanv.delete("path")

	# On rebind la destruction de l'interface de l'armée
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [fra]))
	# On debind le click Gauche
	if option.os == "darwin":
		classmap.mapcanv.unbind("<Button-2>")
	else:
		classmap.mapcanv.unbind("<Button-3>")

def startsequencemovefight(event, gamedata, classmap, option, army):
	##################
	# Fonction pour entamer le déplacement vers l'armé adverse puis le combat
	##################
	log.log.printinfo(f"startsequencemovefight")
	gamedata.removeactionfileturn(army)
	# On recupère les coord
	posx = event.widget.canvasx(event.x)
	posy = event.widget.canvasy(event.y)
	log.log.printinfo(f"pos:  {posx}, {posy}")
	coord1 = common.coordcanvastomap(gamedata, classmap, option, [posx, posy])
	log.log.printinfo(f"coord:  {coord1}")
	# On récupère l'armée adverse
	army2 = 0
	i = 0
	while((army2 == 0) and (i< len(gamedata.list_lord))):
		army2 = gamedata.list_lord[i].coordtoobject(coord1, "army")
		i += 1

	if army2 != 0:
		log.log.printinfo(f"On à trouvé l'armée 2: {army2.name}")
		sequencemovefight(gamedata, classmap, option, army, army2)
	else:
		log.log.printinfo(f"On n'a pas trouvé l'armée 2 pour les coord:{coord1}")


def sequencemovefight(gamedata, classmap, option, army1, army2):
	##################
	# Fonction qui gérer le déplacement d'une armée puis le combat avec une autre
	##################
	log.log.printinfo(f"sequencemovefight")
	# On vérifie que les 2 armées existe toujours
	if (army1 != 0) and (army2 != 0):
		# On recup les coord Map
		coord1 = [army2.x, army2.y]
		# On récupère l'itinéraire la plus efficace
		itinéraire = affichage.pathfinding(gamedata, classmap, option, [army1.x, army1.y], coord1, 45)
		# On retire le dernier déplacement car ils nous placent sur la case ou se trouve l'armée adverse
		itinéraire = itinéraire[:-1]

		# On déplace autant que l'on peut
		i = 0
		idtuile = common.coordmaptoidtuile(classmap, itinéraire[0])
		idtuile0 = idtuile
		while (army1.moveturn - classmap.listmap[idtuile].movementcost >=0) and (i < len(itinéraire)):
			idtuile = common.coordmaptoidtuile(classmap, itinéraire[i])
			affichage.moveunit(gamedata, classmap, option, army1, itinéraire[i])
			i += 1
		classmap.listmap[idtuile0].removearmyinplace()
		classmap.listmap[idtuile].setarmyinplace(army1)
		# Si l'armée à porté on attaque
		if army1.moveturn > 0:
			log.log.printinfo(f"l'armée {army2.name} est à porté de {army1.name}")
			# Si l'armée 1 est vainqueur On détruit l'armée 2
			if(warfunctions.fight(gamedata, classmap, army1, army2)) == True:
				log.log.printinfo(f"l'armée {army1.name} à remporté le combat contre: {army2.name}")
				log.log.printinfo(f"l'armée {army2.name} est détruite")
				# On déréférence toute les unités de l'armée
				army2.destroyarmy()
				# On retire l'armée de la liste du Seigneur
				# On recupère le Seigneur affilié à l'armée
				lord = 0
				i = 0
				while((lord == 0) and (i<len(gamedata.list_lord))):
					if gamedata.list_lord[i].coordtoobject(coord1, "army") != 0:
						lord = gamedata.list_lord[i]
					i += 1
				# On retirer du Registre du Seigneur l'armée
				if lord != 0:
					lord.removearmy(army2)
				# On détruit l'objet du canvas
				classmap.mapcanv.delete(classmap.mapcanv.find_withtag(army2.name)[0])
				# On détruit l'armée
				del army2
			# Sinon On détruit l'armée 1
			else:
				log.log.printinfo(f"l'armée {army2.name} à remporté le combat contre: {army1.name}")
				log.log.printinfo(f"l'armée {army1.name} est détruite")
				# On déréférence toute les unités de l'armée
				army1.destroyarmy()
				# On retire l'armée de la liste du Seigneur
				lord = 0
				i = 0
				while((lord == 0) and (i<len(gamedata.list_lord))):
					if gamedata.list_lord[i].coordtoobject([army1.x, army1.y], "army") != 0:
						lord = gamedata.list_lord[i]
					i += 1
				if lord != 0:
					lord.removearmy(army1)
				# On détruit l'objet du canvas
				classmap.mapcanv.delete(classmap.mapcanv.find_withtag(army1.name)[0])
				# On détruit l'armée
				del army1

		# Sinon on met en mémoire
		else:
			# On met en mémoire 
			log.log.printinfo(f"l'armée {army2.name} n'est pas à porté de {army1.name}")
			gamedata.addactionfile(["sequencemovefight", gamedata, classmap, option, army1, army2], 1)
	else:
		if army2 == 0:
			log.log.printinfo(f"l'armée viser n'existe plus, on annule l'action")
		elif army1 == 0:
			log.log.printinfo(f"l'armée n'existe plus, on annule l'action")

def startsequencemovetakevillage(event, gamedata, classmap, option, army):
	##################
	# Fonction qui entame le déplacement d'une armée vers la prise d'un village
	##################

	gamedata.removeactionfileturn(army)

	player = gamedata.list_lord[gamedata.playerid]

	# On recup les coord Canvas de la tuile 
	posx = event.widget.canvasx(event.x)
	posy = event.widget.canvasy(event.y)
	log.log.printinfo(f"pos: {posx}, {posy}")
	# On transforme en coord Map
	coord = common.coordcanvastomap(gamedata, classmap, option, [posx, posy])
	idvillage = common.coordmaptoidtuile(classmap, coord)
	log.log.printinfo(f"idvillage: {idvillage}")
	# On recup l'objet village
	village = classmap.idtovillage(idvillage)
	log.log.printinfo(f"Objet village trouvé pour les coord({coord}): {village}")

	# On lance la sequence
	sequencemovetakevillage(gamedata, classmap, option, player, army, village)


def sequencemovetakevillage(gamedata, classmap, option, lord, army, village):
	##################
	# Fonction qui gérer le déplacement d'une armée puis la prise d'un village
	##################
	# V1 on ne prend pas en compte la vassalisation d'un Seigneur
	#
	######
	if (village not in lord.fief) and (army != 0):
		# On Recup les coordonnées Map du village
		coord1 = [village.x, village.y]

		# On récupère l'itinéraire la plus efficace
		itinéraire = affichage.pathfinding(gamedata, classmap, option, [army.x, army.y], coord1, 45)
		log.log.printinfo(f"itinéraire: {itinéraire}")

		# On déplace autant que l'on peut
		i = 0
		idtuile = common.coordmaptoidtuile(classmap, itinéraire[0])
		idtuile0 = idtuile
		while (army.moveturn - classmap.listmap[idtuile].movementcost >=0) and (i < len(itinéraire)):
			idtuile = common.coordmaptoidtuile(classmap, itinéraire[i])
			affichage.moveunit(gamedata, classmap, option, army, itinéraire[i])
			i += 1
		classmap.listmap[idtuile0].removearmyinplace()
		classmap.listmap[idtuile].setarmyinplace(army)

		# Si on est a porté on prend le contrôle du village
		# On prend le contrôle du village
		if army.moveturn > 0:
			log.log.printinfo(f"Le Village {village.name} est à porté de {army.name}")
			warfunctions.TakeVillage(gamedata, classmap, option, lord, army, village, False)
		# Sinon on met en mémoire la séquence
		else:
			log.log.printinfo(f"Le Village {village.name} n'est pas à porté de {army.name}")
			gamedata.addactionfile(["sequencemovetakevillage", gamedata, classmap, option, lord, army, village], 1)
	else:
		log.log.printinfo(f"Action annulé")
		if army == 0:
			log.log.printinfo(f"l'armée attaquante du Seigneur {lord.lordname} à était détruite")
		else:
			log.log.printinfo(f"{village.name} à déjà était pris le Seigneur: {lord.lordname}")

def addsubinterface(gamedata, classmap, option, money, ressource):
	################
	# Fonction pour afficher l'augmentation et la décrémentation des ressources
	################

	if money < 0:
		# On affiche la décrémentation
		coord = [int(option.widthWindow*0.48), int(option.heightWindow*0.05)]
		interfacemenu.temp_message(classmap.mapcanv, f"-{money}", 2000, coord, "red")
	elif money > 0:
		# On affiche l'incrémentation
		coord = [int(option.widthWindow*0.48), int(option.heightWindow*0.05)]
		interfacemenu.temp_message(classmap.mapcanv, f"+{money}", 2000, coord, "green")

	if ressource < 0:
		# On affiche la décrémentation
		coord = [int(option.widthWindow*0.42), int(option.heightWindow*0.05)]
		interfacemenu.temp_message(classmap.mapcanv, f"-{ressource}", 2000, coord, "red")
	elif ressource > 0:
		# On affiche l'incrémentation
		coord = [int(option.widthWindow*0.42), int(option.heightWindow*0.05)]
		interfacemenu.temp_message(classmap.mapcanv, f"+{ressource}", 2000, coord, "green")




def banderole(gamedata, classmap, option):
	################
	# Fonction pour afficher une banderole aux joueurs qui indique qu'elle AI est entrain de jouer
	################

	# On créer la WindowFrame
	window_banderole = tkinter.Frame(classmap.framecanvas)
	window_banderole.place(x = option.widthWindow//2, y = option.heightWindow//8)

	# On créer le frame
	frame = tkinter.Frame(window_banderole)
	frame.pack()
	# On ajoute le text
	tkinter.Label(frame, text = f"C'est au Seigneur N°{gamedata.Nb_toplay} {gamedata.list_lord[gamedata.Nb_toplay].lordname} de jouer").pack()

	return window_banderole


def destroybanderole(gamedata, classmap, window):
	window.destroy()

def exitstate(gamedata, classmap, option, lsequbind, lfuncid, lidwindow):
	################
	# Fonction générale pour détruire l'interface, unbind les touches et sortir de l'état
	# demande:
	# - une liste qui contient les séquence du bind ["tag" , "Button"]
	# - une liste qui contient les funcid du bind
	# - une liste qui contient les idwindow ou canvas à détruire
	################

	# On détruit l'idwindow
	for idw in lidwindow:
		# Si objet du Canvas
		# print(type(idw), idw)
		if (type(idw) == int) or (type(idw) == str):
			classmap.mapcanv.delete(idw)
		else:
			idw.destroy()

	# On unbind les fonctions
	i = 0
	while(i < len(lfuncid)):
		classmap.mapcanv.tag_unbind(lsequbind[i][0], lsequbind[i][1], lfuncid[i])
		i += 1

	# De manière générale on vient remplacer le bind click par le highlight case
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: highlightCase(event, gamedata, classmap))

	# On quitte l'état
	gamedata.statenull()
	# On nettoye la variable
	gamedata.exit = []
	# On replace le focus
	classmap.mapcanv.focus_set()



def highlightCase(event, gamedata, classmap):
	####################
	# Fonction qui ilumine la tuile sur laquelle est présente la souris
	# 	--> On ne peut pas "illuminer" une tuile
	#		--> À moins de créer une animations -_-
	#	--> A la place on va créer une bordure ?
	#		--> Pas de fonction de bordure pour une image
	#			--> Tout simplement créer un canvas rectangle afin d'encercler la tuile
	#
	#	--> Après avoir déplacer la carte sur une axe xy la sélection en fonctione plus correctement
	#	--> N'illumine pas les villages
	#
	####################



	# On recup l'id de la tuiles selectionner
	idcurrent = event.widget.find_withtag("current")
	# On recup les coords
	coords = event.widget.coords(idcurrent)


	# On recup la taille d'une tuile
	st = gamedata.tuilesize
	# On supprime l'ancien rectangle highlight si présent
	event.widget.delete("highlight")
	# On créer le nouveau
	x = coords[0] - (st/2)
	y = coords[1] - (st/2)
	log.log.printinfo(f"highlight x,y:{x} {y}")
	event.widget.create_rectangle(x, y, x + st, y + st, tags=["highlight","tuile"])
	coord(event, classmap)



def coord(event, classmap):
	log.log.printinfo(f"coord tuile (0,0) dans canvas x,y:  {classmap.mapcanv.coords(classmap.listmap[0].canvastuiles)}")
	log.log.printinfo(f"coord Window (0,0) dans canvas x,y: {classmap.mapcanv.canvasx(0), classmap.mapcanv.canvasy(0)}")
	log.log.printinfo(f"coord event x,y: {event.x}, {event.y}")
	log.log.printinfo(f"coord event canvas x,y: {event.widget.canvasx(event.x)}, {event.widget.canvasy(event.y)}")
	coord = event.widget.coords(event.widget.find_withtag("current")[0])
	log.log.printinfo(f"coord x,y:  {coord[0]}, {coord[1]}")
	log.log.printinfo(f"{event.widget.gettags("current")}")


