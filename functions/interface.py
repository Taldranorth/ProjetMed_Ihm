import tkinter
import random

import functions.genproc as genproc
import functions.affichage as affichage
import functions.moveview as moveview

######################### Fonction Interface ############################

def gameinterface(gamedata, classmap, option, win):

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

	gamedata.log.printinfo(f"Taille de la Frame du top: {topframe.winfo_width()}, {topframe.winfo_height()}")
	gamedata.log.printinfo(f"Taille de la Frame du bas: {bottomFrame.winfo_width()}, {bottomFrame.winfo_height()}")


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

	# On les set
	# Merde c'est pas dynamique
	classmap.tkvar_list[0].set(f"Ressource : {player.nb_ressource} ({prod_g[1] - salaryarmy[1]})")
	classmap.tkvar_list[1].set(f"Argent : {player.nb_money} ({prod_g[0] - salaryarmy[0]})")
	classmap.tkvar_list[2].set(f"Bonheur: {int(player.global_joy)}%")
	classmap.tkvar_list[3].set(f"Tour N°: {gamedata.Nb_tour}")

	# Info Entête
	# Nb Total Ressource
	ressource_label = tkinter.Label(topframe, textvariable = classmap.tkvar_list[0])
	ressource_label.pack(side = 'left')

	# Nb Total Argent
	money_label = tkinter.Label(topframe, textvariable = classmap.tkvar_list[1])
	money_label.pack(side = 'left')

	# Humeur Globale de la Population
	global_joy_label = tkinter.Label(topframe, textvariable = classmap.tkvar_list[2])
	global_joy_label.pack(side = 'left')

	# N°Tour
	nb_turn_label = tkinter.Label(topframe, textvariable = classmap.tkvar_list[3])
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
	menu_military.add_command(label = "Vassaliser", command = lambda: statesubjugate(gamedata, classmap, option))
	menu_military.add_command(label = "Soldat", command = lambda: staterecruitarmy(gamedata, classmap, option))
	menu_military.add_command(label = "Déclarer Guerre", command = lambda: statewar(gamedata, classmap, option))


	# On associe les Commandes Gestion
	menu_gestion.add_command(label = "Immigration", command = lambda: stateimmigration(gamedata, classmap, option))
	menu_gestion.add_command(label = "Impôt", command = lambda: statetax(gamedata, classmap, option))
	menu_gestion.add_command(label = "Construire Église", command = lambda: statebuildchurch(gamedata, classmap, option))
	menu_gestion.add_command(label = "Construire Village", command = lambda: statebuildvillage(gamedata, classmap, option))



	# Button Droit

	# Buton pour quitter(A remplacer par un listbutton)
	# Exit, Option, Load, Sauvegarder
	Button_exit = tkinter.Button(bottomFrame, command = exit, text = "Quitter")
	# Button pour acceder à la vue générale
	Button_globalview = tkinter.Button(bottomFrame, command = lambda: globalviewmenu(gamedata, classmap, option), text = "Vue Générale")

	# Boutton Central
	# Bouton Fin de Tour
	Button_endofturn = tkinter.Button(bottomFrame, command = lambda: turnend(gamedata, classmap), text = "Fin de Tour")


	# On pack les Button
	Menu_Button_gestion.pack(side="left")
	Menu_Button_military.pack(side="left")
	Button_exit.pack(side="right")
	Button_globalview.pack(side="right")
	Button_endofturn.pack()
#########################################################################
# Fonction lier au bouton de fin de tour
def turnend(gamedata, classmap):
	print("fin de tour ")
	gamedata.endturn = True

def updateinterface(gamedata, classmap):
	player = gamedata.list_lord[gamedata.playerid]
	prod_g = player.prod_global()
	salaryarmy = player.total_salaryarmy()
	classmap.tkvar_list[0].set(f"Ressource : {player.nb_ressource} ({prod_g[1] - salaryarmy[1]})")
	classmap.tkvar_list[1].set(f"Argent : {player.nb_money} ({prod_g[0] - salaryarmy[0]})")
	classmap.tkvar_list[2].set(f"Bonheur: {int(player.global_joy)}%")
	classmap.tkvar_list[3].set(f"Tour N°: {gamedata.Nb_tour}")

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
	# , padx = 25, pady = 25
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
	i += 1
	for j in range(6):
		tkinter.Label(frame_global_view, text = "-----------------").grid(row = i, column = j)
	i += 1
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
	i += 1
	for j in range(6):
		tkinter.Label(frame_global_view, text = "-----------------").grid(row = i, column = j)
	i += 1
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
		for ele in (vassal.lordname, vassal.power, len(vassal.fief), 0, vassal.prod_global()[1], vassal.prod_global()[0]):
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
	# On affiche la liste des Seigneurs Indépendents dans une fenêtre
	# 
	#######
	if gamedata.changenewstate("interface_sujugate") == True:
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
				if lord not in (player.vassal):
					lc_subjugate.insert(tkinter.END, lord.lordname)
		# On bind double click
		lc_subjugate.bind("<Double-Button-1>", lambda event: vassal_offer(event, gamedata, classmap, option, window_interface_subjugate, lc_subjugate))


		# On bind l'exit
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [window_interface_subjugate]))

def vassal_offer(event, gamedata, classmap, option, wis, lc):
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
	button_vassalage_offer = tkinter.Button(frame_interface_offer, command = lambda: b_vassal_offer(gamedata, classmap, option, lc, lord, frame_interface_offer, succes), text = "Envoyer Proposition")
	button_vassalage_offer.grid(row = 5, column = 1)

def b_vassal_offer(gamedata, classmap, option, lc, lord, frame, succes):
	################
	# Fonction pour gérer l'envoit d'une demande de Vassalisation
	################

	player = gamedata.list_lord[gamedata.playerid]

	# On teste la probabilité
	# On genère un chiffre entre 1 et 100
	r = random.randrange(0,100)
	# On addition le succes
	r += succes
	gamedata.log.printinfo(f"Valeur obtenu après lancer de dé: {r}")
	# On vérifie si c'est >= 100
	# Si c'est réussi on ajoute à la liste des Vassaux
	if r >= 100:
		gamedata.log.printinfo("Succès")
		# On ajoute le Seigneur à la liste des Vassaux
		player.addvassal(lord)
		# On ajoute les vassaux du Seigneur à la liste des Vassaux
		for vassal in lord.vassal:
			# On retire de la liste des Vassaux du Seigneur les vassaux qu'il possède
			lord.removevassal(vassallord)
			player.addvassal(vassal)
		print("Liste des vassaux du Joueurs: ",player.vassal)
	# Sinon on déclare la guerre
	else:
		gamedata.log.printinfo("Echecs")
		player.addwar(lord)
		lord.addwar(player)

	# On update la Listbox
	lc.delete(lc.curselection()[0])

	# On update l'affichage de la carte
	affichage.bordervillage(gamedata, classmap, option)

	# On update l'entête
	updateinterface(gamedata, classmap)

	# On détruit la fenêtre Une fois la demande faite
	frame.destroy()

def vassal_try(gamedata, lord, lord2):
	################
	# Fonction qui calcul le % de chance de réussite que le Seigneur1 vassalise le Seigneur2 par une tentative
	################
	# On calcul selon plusieurs facteurs:
	# - La puissance Militaire de Chacun
	# - Le Nombre de (Village * Nb_pop) de Chacun
	# - Le Nombre de (Vassaux*(power+Village * Nb_pop)) de Chacun
	# L'ensemble permet d'obtenir un Score qui va être comparer
	################

	# On ajoute la puissance Militaire
	lord_score1 = lord.power
	lord_score2 = lord2.power
	# On ajoute la puissance Démographique

	for village in lord.fief:
		lord_score1 += len(village.population)

	for village in lord2.fief:
		lord_score2 += len(village.population)

	# On ajoute la puissance Diplomatique
	diplo_power = 0
	for vassal in lord.vassal:
		diplo_power += lord.power
		for village in vassal.fief:
			diplo_power += len(village.population)

	lord_score1 += diplo_power

	diplo_power = 0
	for vassal in lord2.vassal:
		diplo_power += lord2.power
		for village in vassal.fief:
			diplo_power += len(village.population)

	lord_score2 += diplo_power	


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

	if gamedata.changenewstate("interface_recruit_army") == True:
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

		# On bind 
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [window_interface_army]))

def buttoncreatearmy(gamedata, classmap, option, lc_interface_army):


	player = gamedata.list_lord[gamedata.playerid]
	lastarmy = len(player.army)

	# On vérifie que le joueur possède les ressource nécessaire pour recruter 1 Soldata
	if player.verifcost(2,2) == True:
		gamedata.log.printinfo("Le Joueur Créer une armée")

		village = player.fief[0]
		# On vérifie qu'il n'y a pas déjà une armée à cette position
		x = village.x
		y = village.y
		inpos = False
		for army in player.army:
			if (army.x == x) and (army.y == y):
				inpos = True
		if inpos == True:
			x = x+1

		# On créer la nouvelle armée
		player.createarmy(village.name, x, y)
		# On ajoute 1 Soldat
		player.sub_money(2)
		player.sub_ressource(2)
		player.army[lastarmy].recruitsoldier(gamedata.randomnametype("Nom"))
		# On affiche la nouvelle armée
		affichage.printarmy(gamedata, classmap, option, player.army[lastarmy])
		# On update l'interface de la listbox
		lc_interface_army.insert(tkinter.END, player.army[lastarmy].name)
		# On update l'interface entête
		updateinterface(gamedata, classmap)

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
	tkvar_power = tkinter.IntVar()
	tkvar_power.set(army.power)

	tkvar_knight = tkinter.IntVar()
	if army.knight == 0:
		tkvar_knight.set(army.knight)
	else:
		tkvar_knight.set(army.knight.name)

	tkvar_lenunit = tkinter.IntVar()
	tkvar_lenunit.set(len(army.unit))

	tkvar_list = [tkvar_power, tkvar_knight, tkvar_lenunit]

	# On affiche les Infos de l'armée
	# La puissance de l'armée
	tkinter.Label(frame_interface_army_right, textvariable = tkvar_list[0]).grid(column = 1)
	# Le nombre de Chevalier
	tkinter.Label(frame_interface_army_right, textvariable = tkvar_list[1]).grid(column = 1)
	# Le nombre de Soldat
	tkinter.Label(frame_interface_army_right, textvariable = tkvar_list[2]).grid(column = 1)

	# On créer un bouttons pour recruter un Chevalier
	button_recruit_knight = tkinter.Button(frame_interface_army_right, command = lambda unit="knight": button_recruit(gamedata, classmap, tkvar_list, army, unit), text = "Recruter Chevalier")
	button_recruit_knight.grid(column = 1)

	# On créer un bouttons pour recruter un soldat
	button_recruit_soldier = tkinter.Button(frame_interface_army_right, command = lambda unit="soldier": button_recruit(gamedata, classmap, tkvar_list, army, unit), text = "Recruter soldat")
	button_recruit_soldier.grid(column = 1)

def centerarmy(event, gamedata, classmap, option):
	############
	# Fonction appeler par la listbox lc_interface_army pour centrer la vue sur l'armée sélectionner
	############
	gamedata.log.printinfo("On se déplace vers l'armée ")
	# On recup le village actuellement selectionner dans la listbox
	army_selected = event.widget.get(event.widget.curselection()[0])
	
	point_army_object = 0
	# On recup l'objet army
	for army in (gamedata.list_lord[gamedata.playerid].army):
		if army.name == army_selected:
			point_army_object = army


	#print("x,y: ", x, y)
	coord = moveview.coordmaptocanvas(gamedata, classmap, option, [army.x, army.y], True)


	# On centre la vu sur le village
	moveview.centerviewcanvas(gamedata, classmap, option, coord)

def button_recruit(gamedata, classmap, tkvar_list, army, unit):
	################
	# Fonction appeler pour recruter
	################
	player = gamedata.list_lord[gamedata.playerid]

	# On recrute l'unité
	if (unit == "knight") and (type(tkvar_list[1].get()) != str):
		# On verif que le joueur possède les ressources
		if player.verifcost(10,10) == True:
			army.recruitknight(gamedata.randomnametype("Surnom"))
			tkvar_list[1].set(army.knight.name)
			player.sub_money(10)
			player.sub_ressource(10)

	elif unit == "soldier":
		if player.verifcost(2,2) == True:
			army.recruitsoldier(gamedata.randomnametype("Nom"))
			tkvar_list[2].set(len(army.unit))
			player.sub_money(2)
			player.sub_ressource(2)			

	# On update l'armée
	if gamedata.searchtexturetypeindico(army.texture) != "knight":
		affichage.printupdatearmy(gamedata, classmap, army)

	# On update l'interface de l'armée
	tkvar_list[0].set(army.power)
	# On update l'interface de l'entête
	updateinterface(gamedata, classmap)


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

	if gamedata.changenewstate("interface_war") == True :
		# Tant que la carte n'est pas dezoom à 10
		while gamedata.tuilesize != 10:
			if gamedata.tuilesize > 10:
				moveview.moveviewzcenter(gamedata, classmap, option, -2)
			else:
				moveview.moveviewzcenter(gamedata, classmap, option, 2)

		player = gamedata.list_lord[gamedata.playerid]
		ts = gamedata.tuilesize
		xorigine = classmap.mapcanv.canvasx(0)
		yorigine = classmap.mapcanv.canvasy(0)

		# On se place au centre
		moveview.centerviewcanvas(gamedata, classmap, option, [(option.mapx/2)*ts, (option.mapy/2)*ts])

		# On affiche les territoire 
		# On se balade dans la liste des territoire
		for nblord in range(len(gamedata.list_lord)):
			color = "white"
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
					if color == "white":
						print("village neutre: ", village.name)
					elif color == "re":
						print("village ennemie: ", village.name)


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

def warcentervillage(event, gamedata, classmap, option, list_LC, iwd):
	############
	# Fonction appeler par Lb_neutral, Lb_ally ou Lb_ennemy pour centrer la vue sur le village principale du joueur Sélectionner
	############
	# On recup le joueur
	player = gamedata.list_lord[gamedata.playerid]

	# On recup le nom du seigneur Selectionner
	lordname = event.widget.get(event.widget.curselection()[0])
	gamedata.log.printinfo(f"lordname: , {lordname}")
	# On recup son id
	lordid = gamedata.lordnametoid(lordname)
	gamedata.log.printinfo(f"lordid: , {lordid}")
	# On recup l'objet lord
	lord = gamedata.list_lord[lordid]
	# On recup son village principale
	city = lord.fief[0]

	# On convertit les coord Map de l'objet en coord Canvas
	coord = moveview.coordmaptocanvas(gamedata, classmap, option, [city.x, city.y], True)

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
	# On supprimer l'affichage des anciens territoire du Seigneurs
	classmap.mapcanv.delete(["tuile", "border", lord.lordname])
	# Village gérer directement par le seigneur Ennemie
	for village in lord.fief:
		affichage.bordervillageunit(gamedata, classmap, option, village)
	for vassal in lord.vassal:
		classmap.mapcanv.delete(["tuile", "border", vassal.lordname])
		for vassal_village in vassal.fief:
			affichage.bordervillageunit(gamedata, classmap, option, vassal_village)

def wardeclaration(gamedata, lord1, lord2):
	############
	# Fonction appeler pour déclarer la gerre entre 2 Seigneurs
	############
	gamedata.log.printinfo(f"Déclaration de guerre entre: {lord1.lordname} et {lord2.lordname}")

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

	if gamedata.changenewstate("build_village") == True :

		ts = gamedata.tuilesize
		xoriginewindow = classmap.mapcanv.canvasx(0)
		yoriginewindow = classmap.mapcanv.canvasy(0)
		originecanvas = classmap.mapcanv.coords(classmap.listmap[0].canvastuiles)

		# Pour toute les tuiles de plaines
		for idtuile in classmap.lplaines:
			# Si on peut constuire un village
			if genproc.buildvillagepossible(option, classmap, idtuile) == True:
				# On calcul les coord x et y
				x = idtuile%option.mapx
				y = idtuile//option.mapx
				# On créer un carrer clickable avec un bord vert
				#print(xorigine,yorigine)
				#print("coord: ", (x*ts) + xorigine, (y*ts) + yorigine, (x*ts)+ts + xorigine, (y*ts)+ts + yorigine)
				classmap.mapcanv.create_rectangle(originecanvas[0]+(x*ts)-(ts/2), originecanvas[1]+(y*ts)-(ts/2), originecanvas[0]+(x*ts)+ts-(ts/2), originecanvas[1]+(y*ts)+ts-(ts/2), tag = ["buildvillage","tuile", x, y], fill = "green",outline = "green")

		# On tag au carrer 
		classmap.mapcanv.tag_bind("buildvillage", "<Button-1>", lambda event: buildvillage(event, gamedata, classmap, option))
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], ["buildvillage"]))

	# Si on appuie sur esc on quitte automatiquement le mode de construction

def buildvillage(event, gamedata, classmap, option):
	############
	# Fonction pour créer un village selon la tuile sélectionner en état de construction
	############

	player = gamedata.list_lord[gamedata.playerid]
	print("On construit le village")
	# On calcul l'id de la tuile
	xpos = int(event.widget.gettags("current")[2])
	ypos = int(event.widget.gettags("current")[3])
	idtuile = xpos + (option.mapx*ypos)

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
		genproc.genpopvillage(gamedata, classmap, option, classmap.listmap[idtuile].village, 2, 2)

		# On retire les ressource 

		# On affiche le nouveau village
		affichage.printvillageunit(gamedata, classmap, option, [xpos,ypos])

		# On affiche la bordure du nouveau village
		affichage.bordervillageunit(gamedata, classmap, option, classmap.listmap[idtuile].village)

		# On update la carte des villages possible
		updatestatbuildvillage(classmap, option)

def updatestatbuildvillage(classmap, option):
	############
	# Fonction pour update la carte des Construction possible
	############
	liste_carrer = classmap.mapcanv.find_withtag("buildvillage")
	for tuile in liste_carrer:
		# On calcul l'id
		xpos = int(classmap.mapcanv.gettags(tuile)[2])
		ypos = int(classmap.mapcanv.gettags(tuile)[3])
		idtuile = xpos + (option.mapx*ypos)

		# On test si la tuile est toujours valable
		# Si elle ne l'est pas on la suicide
		if genproc.buildvillagepossible(option, classmap, idtuile) == False:
			classmap.mapcanv.delete(tuile)

############################################# Build Church #############################################

def statebuildchurch(gamedata, classmap, option):
	######
	# Fonction Appeler par le menu pour construire une église
	######

	if gamedata.changenewstate("build_church") == True:

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
		lc_interface_church = tkinter.Listbox(frame_interface_church)
		lc_interface_church.grid(row = 1, column = 0)
		# On créer un menu déroulant qui présente les villages éligible à la construction d'une église avec les donnés du villag
		for village in player.fief:
			if village.church == 0:
				lc_interface_church.insert(tkinter.END, village.name)
		# Quand un village est double click on appele la fonction pour centrer la vue sur le village
		lc_interface_church.bind("<Double-Button-1>", lambda event: centervillagechurch(event, gamedata, classmap, option))

		# On affiche en vert tout les villages ou on peut construire une église
		for village in player.fief:
			if village.church == 0:
				x = village.x
				y = village.y
				classmap.mapcanv.create_rectangle(originecanvas[0]+(x*ts)-(ts/2), originecanvas[1]+(y*ts)-(ts/2), originecanvas[0]+(x*ts)+ts-(ts/2), originecanvas[1]+(y*ts)+ts-(ts/2), tags = ["buildchurch","tuile"], outline = "green")

		# On bind la fonction buildchurch à la tuile du village
		idbuildchurch = classmap.mapcanv.tag_bind("village", "<Button-1>", lambda event: triggerbuildchurch(event, gamedata, classmap, option), add = "+")

		# On bind la fonction d'exit à tout ce qui n'est pas un village
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event, lsequ = [["village","<Button-1>"]], lf = [idbuildchurch], lidw = [window_interface_church, "buildchurch"]: exitstate(gamedata, classmap, option, lsequ, lf, lidw))


def centervillagechurch(event, gamedata, classmap, option):
	############
	# Fonction appeler par la listbox lc_interface_church pour centrer la carte sur le village selectionner dans la listbox
	# On sait que les noms des villages sont uniques
	############
	gamedata.log.printinfo("On se déplace vers le village")
	# On recup le village actuellement selectionner dans la listbox
	village_selected = event.widget.get(event.widget.curselection()[0])
	
	idvillage = classmap.nametoid(village_selected)
	# On recup les coord du village
	x = classmap.listmap[idvillage].x
	y = classmap.listmap[idvillage].y

	coord = moveview.coordmaptocanvas(gamedata, classmap, option, [x, y], True)

	# On centre la vu sur le village
	moveview.centerviewcanvas(gamedata, classmap, option, coord)

def triggerbuildchurch(event, gamedata, classmap, option):
	############
	# Fonction pour construire une église dans un village
	############
	print(classmap.mapcanv.gettags("current"))

	# On récup l'id de la tuile ou se trouve le village
	# Si c'est le label
	if classmap.mapcanv.gettags("current")[0] == "label":
		x = int(classmap.mapcanv.gettags("current")[3])
		y = int(classmap.mapcanv.gettags("current")[4])
	# Si c'est l'image
	elif classmap.mapcanv.gettags("current")[0] == "village":
		x = int(classmap.mapcanv.gettags("current")[4])
		y = int(classmap.mapcanv.gettags("current")[5])
	# Si c'est la tuile
	elif classmap.mapcanv.gettags("current")[0] == "img":
		x = int(classmap.mapcanv.gettags("current")[4])
		y = int(classmap.mapcanv.gettags("current")[5])


	idvillage = x + (option.mapx * y)
	village = classmap.listmap[idvillage].village
	player = gamedata.list_lord[gamedata.playerid]

	# On vérife que le village appartient au joueur
	if village in player.fief:
		# On Verfie que le joueur possède l'argent nécessaire
		if player.verifcost(10,10):
			village.buildchurch(gamedata.randomnametype("Nom"))
			player.sub_money(10)
			player.sub_ressource(10)
		# On retire le carrer 
################################################  Tax  #################################################

def statetax(gamedata, classmap, option):
	if gamedata.changenewstate("tax") == True:
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
			taxtemp2 = calculate_tax_village(village)
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
	coord = moveview.coordmaptocanvas(gamedata, classmap, option, [x, y], True)
	moveview.centerviewcanvas(gamedata, classmap, option, coord)


	# On met en places l'interfaces
	frame_tax_collect = tkinter.Frame(wit)
	frame_tax_collect.grid(row = 0, column = 1)
	# On affiche plus d'info sur la populations

	tax = calculate_tax_village(village)
	tkvar_money = tkinter.StringVar()
	tkvar_money.set(f"Collecter {tax[0]} écus")
	tkvar_ressource = tkinter.StringVar()
	tkvar_ressource.set(f"Collecter {tax[1]} ressource")

	tkvar_list = [tkvar_money, tkvar_ressource]
	button_collect_tax_money = tkinter.Button(frame_tax_collect, textvariable = tkvar_list[0], command=lambda: collect_taxes_village(gamedata, classmap, village, "money", frame_tax_collect, tkvar_list))
	button_collect_tax_money.grid(row = 3, column = 1)

	button_collect_tax_ressource = tkinter.Button(frame_tax_collect, textvariable = tkvar_list[1], command=lambda: collect_taxes_village(gamedata, classmap, village, "ressource", frame_tax_collect, tkvar_list))
	button_collect_tax_ressource.grid(row = 4, column = 1)

def collect_taxes_village(gamedata, classmap, village, type_tax, frame, tkvar_list):
	#####
	# Fonction associer au Bouton pour collecter taxes 
	#####

	# On recup le joueur
	player = gamedata.list_lord[gamedata.playerid]

	# Si argent on tax l'argent
	if type_tax == "money":
		# On se balade parmi les roturier du village
		for roturier in village.population:
			# ON les faits payer leur taxes
			roturier.pay_tax_money(player)
		tax = calculate_tax_village(village)
		# On update l'interface
		tkvar_list[0].set(f"Collecter {tax[0]} écus")
	# Si ressource on tax les ressources
	else:
		# On se balade parmi les roturier du village
		for roturier in village.population:
			# ON les faits payer leur taxes
			roturier.pay_tax_ressource(player)
		tax = calculate_tax_village(village)
		# On update l'interface
		tkvar_list[1].set(f"Collecter {tax[1]} ressource")
	# On update l'entête
	updateinterface(gamedata, classmap)

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
	coord = moveview.coordmaptocanvas(gamedata, classmap, option, [x, y], True)
	moveview.centerviewcanvas(gamedata, classmap, option, coord)


	# On met en places l'interfaces
	frame_tax_collect = tkinter.Frame(wit)
	frame_tax_collect.grid(row = 0, column = 1)
	# On affiche plus d'info sur la populations

	tax = calculate_tax_vassal(vassal)


	tkvar_tax = tkinter.StringVar()
	tkvar_tax.set(f"Collecter {tax[0]} écus et {tax[1]} ressource")

	button_collect_tax_money = tkinter.Button(frame_tax_collect, textvariable = tkvar_tax, command=lambda: collect_taxes_vassal(gamedata, classmap, vassal, frame_tax_collect, tkvar_tax))
	button_collect_tax_money.grid(row = 3, column = 1)

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

	if gamedata.changenewstate("immigration") == True:
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
	
	coord = moveview.coordmaptocanvas(gamedata, classmap, option, [x, y], True)
	#On déplace la vue de la carte sur ce village
	moveview.centerviewcanvas(gamedata, classmap, option, coord)
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

def button_add_population(gamedata, classmap, option, village, role, tkvar_list):
	################
	# Fonctions liées aux button pour ajouter de la pop dans l'interface d'immigration
	################
	player = gamedata.list_lord[gamedata.playerid]

	if (role == "paysan"):
		# On verifie que le joueuer à suffisament en stock
		if player.verifcost(1, 1) == True:
			# On ajoute la pop
			genproc.genpopvillage(gamedata, classmap, option, village, 1, 0)
			tkvar_list[1].set(f"Nb Paysan: {village.nb_paysan}")
			# On retire au joueur
			player.sub_ressource(1)
			player.sub_money(1)

	elif role == "artisan":
		if player.verifcost(4, 4) == True:
			genproc.genpopvillage(gamedata, classmap, option, village, 0, 1)
			tkvar_list[2].set(f"Nb artisan: {village.nb_artisan}")
			player.sub_ressource(4)
			player.sub_money(4)

	# On update l'interface Immigration
	tkvar_list[0].set(f"Nb Pop: {len(village.population)}")
	# On update l'interface Entête
	updateinterface(gamedata, classmap)




###############################################################################################

##############################################\ Interface Objet \########################################


def villageinterface(event, gamedata, classmap, option):
	##################
	# Fonction pour afficher l'interface d'un village
	##################

	# Si le joueur est dans un état ou il a déjà l'interface d'un village ouvert on ne fait rien
	if gamedata.changenewstate("interface_village") == True :

		# On recup l'idée du canvas de la tuile que l'on vient de sélectionner
		idcanvasvillage = event.widget.find_withtag("current")[0]
		# On recup les coord-canvas du village
		coordcanv = event.widget.coords(idcanvasvillage)
		# On recup la pos x et y du village dans la map
		gamedata.log.printinfo(f"{event.widget.gettags(idcanvasvillage)}")
		# Si on à cliqué sur le village
		if event.widget.gettags(idcanvasvillage)[0] == "village":
			posx = event.widget.gettags(idcanvasvillage)[4]
			posy = event.widget.gettags(idcanvasvillage)[5]
		# Sinon on à cliqué sur le label
		else:
			posx = event.widget.gettags(idcanvasvillage)[3]
			posy = event.widget.gettags(idcanvasvillage)[4]
		# On calcul l'id map du village
		idmapvillage = int(posx)+(option.mapx*int(posy))
		gamedata.log.printinfo(f"{idmapvillage}")

		####################\ Comment j'ai fait ???? \########################
		# On place le village au centre de l'écran
		moveview.centerviewcanvas(gamedata, classmap, option, coordcanv)
		######################################################################


		####################\ Affichage de l'interface \########################

		# On recup l'origine du canvas
		xorigine = classmap.mapcanv.canvasx(0)
		yorigine = classmap.mapcanv.canvasy(0)

		gamedata.log.printinfo("On affiche l'interface du village")
		# On fait apparaitre l'interface informative
		# On commence par créer le frame qui vient stocker les infos
		frame_info = tkinter.Frame(classmap.framecanvas)
		# On créer la frame qui vient contenir les actions possibles
		frame_button = tkinter.Frame(classmap.framecanvas)
		frame_info.place(x = (option.widthWindow/4), y = (option.heightWindow*0.2))
		frame_button.place(x = (option.widthWindow/1.5), y = (option.heightWindow*0.2))

		# On créer les fenêtre
		# Demade un placement précis
		canvas_window_list = [frame_info, frame_button]

		# Si le village appartient au joueur on affiche l'interface Button
		# On vérifie que l'objet village est présent dans la liste de fief du joueur
		if classmap.listmap[idmapvillage].village in gamedata.list_lord[gamedata.playerid].fief:
			# On fait apparaitre les boutons
			button_build_church = tkinter.Button(frame_button, text = "Construire Église")
			button_immigration = tkinter.Button(frame_button, text = "Immigration")
			button_tax = tkinter.Button(frame_button, text = "Impôt")
			button_build_church.pack(side="top")
			button_immigration.pack(side="top")
			button_tax.pack(side="top")


		# On affiche les infos voulu
		# Le nom du village
		tkinter.Label(frame_info, text = classmap.listmap[idmapvillage].village.name).pack(side = "top")
		gamedata.log.printinfo(f"{classmap.listmap[idmapvillage].village.name}")
		# Le seigneur du village
		if (classmap.listmap[idmapvillage].village.lord == 0):
			tkinter.Label(frame_info, text = "lord").pack(side = "top")
		else:
			tkinter.Label(frame_info, text = classmap.listmap[idmapvillage].village.lord.lordname).pack(side = "top")
		# Le prêtre du village
		if classmap.listmap[idmapvillage].village.priest == 0:
			tkinter.Label(frame_info, text = "priest").pack(side = "top")
		else:
			tkinter.Label(frame_info, text = classmap.listmap[idmapvillage].village.priest.name).pack(side = "top")
		# Le bonheur global
		tkinter.Label(frame_info, textv = classmap.listmap[idmapvillage].village.global_joy).pack(side = "top")
		# les ressources du village
		tkinter.Label(frame_info, text = classmap.listmap[idmapvillage].village.prod_ressource).pack(side = "top")
		# l'argent du village
		tkinter.Label(frame_info, text = classmap.listmap[idmapvillage].village.prod_money).pack(side = "top")

		######################################################################

		# Si le joueur clique autre part on sort de l'interface
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event, cwl = canvas_window_list: exitstate(gamedata, classmap, option, [], [], cwl))


def armyinterface(event, gamedata, classmap, option):
	################
	# Fonction créer la fenêtre de l'interface de l'armée selectionné
	################

	if gamedata.changenewstate("interface_army") == True:

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

		# On affiche le nom
		tkinter.Label(frame_interface_army, text = army.name).grid(row = 0, column = 0)
		# On affiche la puissance
		tkinter.Label(frame_interface_army, text = "Puissance: ").grid(row = 0, column = 1)
		tkinter.Label(frame_interface_army, text = army.power).grid(row = 0, column = 2)

		tkinter.Label(frame_interface_army, text = "Movement").grid(row = 0, column = 3)
		# On affiche la capacité de déplacement max
		tkinter.Label(frame_interface_army, text = army.movecapacity).grid(row = 0, column = 4)
		# On affiche la capacité de déplacement possible
		tkinter.Label(frame_interface_army, text = army.moveturn).grid(row = 0, column = 5)

		# On créer le bouton pour se déplacer
		Button_move_army = tkinter.Button(frame_interface_army, text = "Déplacement", command = lambda: statemovearmy(gamedata, classmap, option, army, window_interface_army))
		Button_move_army.grid(row = 0, column = 6)

		# Si on clique droit sur une armée non allié alors que l'on à selectionner une armée on attaque

		# Si on clique sur autre chose on quitte l'interface
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [window_interface_army]))



def statemovearmy(gamedata, classmap, option, army, fra):
	##################
	# Fonction pour Entréer le joueur dans un état de déplacement d'armé Si il clique sur le bouton déplacer dabs l'interface d'armée
	##################

	# On bind l'affiche de la trajectoire sur l'emplacement de la souris quand elle est sur le canvas
	funcpath = classmap.mapcanv.tag_bind("click","<Motion>", lambda event: showpathfinding(event, gamedata, classmap, option, army), add= "+")

	# On debind le exitstate
	classmap.mapcanv.tag_unbind("click", "<Button-1>")

	# On bind le click gauche sur aller 
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: startsequencemoveunit(event, gamedata, classmap, option, army))

	# On bind sur les villages l'attaque
	funcvillage =  classmap.mapcanv.tag_bind("village", "<Button-1>", lambda event: movetakevillage(event, gamedata, classmap, option, army), add= "+")

	# On bind sur les armées l'attaque
	funcarmy = classmap.mapcanv.tag_bind("army", "<Button-1>", lambda event: movefight(event, gamedata, classmap, army), add= "+")

	# On bind l'exit de l'état aux clic gauche
	classmap.mapcanv.tag_bind("click", "<Button-2>", lambda event: cancelmovearmy(event, gamedata, classmap, option, [funcpath, funcvillage, funcarmy], fra))




def showpathfinding(event, gamedata, classmap, option, army):
	################
	# Fonction qui affiche le chemin que va parcourir l'armée pour atteindre la case
	# Elle affiche en vert le chemin que l'armée parcoura ce tour
	# Elle affiche en rouge le chemin que l'armée ne parcoura pas ce tour
	################

	# On recup les coord Canvas
	posx = event.widget.canvasx(event.x)
	posy = event.widget.canvasy(event.y)
	# On transforme en coord Map
	coord1 = moveview.coordcanvastomap(gamedata, classmap, option, [posx, posy])

	# On calcul la meilleur trajectoire
	sequ = affichage.pathfinding(gamedata, classmap, option,[army.x, army.y], coord1, 45)

	# On détruit la précédante trajectoire afficher
	event.widget.delete("path")

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
			classmap.mapcanv.create_text((sequ[i][0]*ts)+ts/2, (sequ[i][1]*ts)+ts/2, tags = "path", text = turn, fill = color)
		else:
			#On calcule la tuile à partir des coord Map
			idtuile = sequ[i][0]+(option.mapx*sequ[i][1])
			idtuile2 = sequ[i+1][0]+(option.mapx*sequ[i+1][1])
			if color == "green":
				if(move - classmap.listmap[idtuile2].movementcost) < 0:
					classmap.mapcanv.create_oval((sequ[i][0]*ts), (sequ[i][1]*ts), (sequ[i][0]*ts)+ts, (sequ[i][1]*ts)+ts, width = 2, tags = "path", outline = color)
					classmap.mapcanv.create_text((sequ[i][0]*ts)+ts/2, (sequ[i][1]*ts)+ts/2, tags = "path", text = turn, fill = color)
					color = "red"
					move = army.moveturn
				else:
					move -= classmap.listmap[idtuile].movementcost	
			else:
				if (move - classmap.listmap[idtuile].movementcost) >= 0:
					move -= classmap.listmap[idtuile].movementcost	
				else:
					turn += 1
					move = army.moveturn
					classmap.mapcanv.create_oval((sequ[i][0]*ts), (sequ[i][1]*ts), (sequ[i][0]*ts)+ts, (sequ[i][1]*ts)+ts, width = 2, tags = "path", outline = color)
					classmap.mapcanv.create_text((sequ[i][0]*ts)+ts/2, (sequ[i][1]*ts)+ts/2, tags = "path", text = turn, fill = color)

			classmap.mapcanv.create_line((sequ[i][0]*ts), (sequ[i][1]*ts), (sequ[i+1][0]*ts), (sequ[i+1][1]*ts), width = 2, tags = "path", fill = color)
		i += 1

def startsequencemoveunit(event, gamedata, classmap, option, army):
	##################
	# Fonctions pour entamer le déplacement d'une armée vers la case clicker
	##################

	# On recup les coord canvas de la tuile Viser
	posfinalx = classmap.mapcanv.canvasx(event.x)
	posfinaly = classmap.mapcanv.canvasy(event.y)
	# On les transforme en coord map
	coordmap = moveview.coordcanvastomap(gamedata, classmap, option, [posfinalx, posfinaly])
	gamedata.log.printinfo(f"coordmap: ,{coordmap}")
	affichage.sequencemoveunit(gamedata, classmap, option, army, coordmap)



def cancelmovearmy(event, gamedata, classmap, option, lfuncpath, fra):
	################
	# Fonction pour annuler le déplacement d'une armée
	################
	print("exit movearmy")
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
	classmap.mapcanv.tag_unbind("click", "<Button-2>")


def movefight(event, gamedata, classmap, army):
	##################
	# Fonction qui gérer le déplacement d'une armée puis le combat avec une autre
	##################

	# On calcul l'armé adverse
	pass



def movetakevillage(event, gamedata, classmap, option, army):
	##################
	# Fonction qui gérer le déplacement d'une armée puis la prise d'un village
	##################
	# V1 on ne prend pas en compte la vassalisation d'un Seigneur
	#
	######

	# On recup les coord Canvas de la tuile 
	posx = event.widget.canvasx(event.x)
	posy = event.widget.canvasy(event.y)
	# On transforme en coord Map
	coord = moveview.coordcanvastomap(gamedata, classmap, option, [posx, posy])
	idvillage = moveview.coordmaptoidtuile(option, coord)
	print("idvillage: ",idvillage)

	# On recup l'objet village
	village = classmap.idtovillage(idvillage)
	gamedata.log.printinfo(f"Objet village trouvé pour les coord({coord}): {village}")

	# On prend le contrôle du village
	TakeVillage(gamedata, classmap, option, army, village, False)

def fight(gamedata, classmap, army1 , army2):
	##################
	# Fonction pour gérer le combat entre 2 armée
	##################
	# Prend en entrée l'objet armée1 et l'objet armée2
	# - Renvoit True Si Armée1 gagne le combat
	# - Renvoit False Si Armée2 gagne le Combat
	# Selon certaines Conditions Armée 1 gagne le Combat
	# SI army1.power > army2.power
	#
	if army1.power > army2.power:
		return True
	else:
		return False

def TakeVillage(gamedata, classmap, option, army, village, subjugate):
	##################
	# Fonction pour gérer la prise de Village par le Joueur
	##################
	# Subjugate vient définir 2 comportement:
	# Si C'est le Seul Village Du Seigneur Ennemie:
	#	- Soit ajoute au domaine personelle de l'attaquant 	(subjugate == False)
	#	- Soit Vassaliser le Seigneur Ennemie				(subjufate == True)
	# Si ce n'est pas le Seul Village du Seigneur Ennemie:
	#	- Ajoute au domaine personelle de l'attaquant
	# Si le Seigneur Ennemie possède des Vassaux ils sont soit libérer soit ajouté a c'est vassaux
	#	- On prend comme cas de figure standars la prise de contrôle immédiate des Vassaux

	player = gamedata.list_lord[gamedata.playerid]
	gamedata.log.printinfo(f"prise de {village.name} par {player.lordname}")

	# Si le village n'est pas indépendant
	if village.lord != 0:
		Ennemielord = village.lord

		# Si le Seigneur Ennemies possède Encore plus d'1 Village
		if len(Ennemielord.fief) > 1:
			gamedata.log.printinfo(f"Le Seigneur {Ennemielord.lordname} possède plus de 1 village")
			# On debind le Village du Seigneur Ennemie
			Ennemielord.removefief(village)
			# ON Prend le contrôle du village
			player.addfief(village)
		# Sinon On Vassalise le Seigneur ou on le détruit et récupère le village
		else:
			gamedata.log.printinfo(f"C'est le dernier village de: {Ennemielord.lordname}")
			# on retire le seigneur et c'est vassaux de la liste War
			player.removewar(Ennemielord)
			# On retire le joueur de la liste war du Seigneurs Ennemie et de c'est vassaux
			Ennemielord.removewar(player)
			# On transfert le controle des Vassaux du Seigneurs Ennemie aux joueur
			for vassallord in Ennemielord.vassal:
				# On retire le vassal de la liste du seigneurs Ennemie
				Ennemielord.removevassal(vassallord)
				# On l'ajoute à la liste du Joueur
				player.addvassal(vassal)
				gamedata.log.printinfo(f"{vassal.lordname} subjuger")
			gamedata.log.printinfo(f"{player.lordname} à pris le contrôle de tout les Vassaux Ennemie")
			# On Vassalise le Seigneur
			if subjugate == True:
				# On Vassalise le Seigneurs Ennemie
				player.addvassal(Ennemielord)
				gamedata.log.printinfo(f"{Ennemielord.lordname} subjuger")
			# On détruit le Seigneur
			else:
				# On transfert le contrôle du Village du Seigneur Ennemies
				Ennemielord.removefief(village)
				player.addfief(village)
				gamedata.log.printinfo(f"{Ennemielord.lordname} ANÉHANTIE")
				# ON LE DELETE NIARK NIARK NIARK NIARK
				gamedata.deletelord(Ennemielord.idlord)
	else:
		player.addfief(village)

	# On update l'affichage du territoire
	# On supp
	classmap.mapcanv.delete("border")
	# On recréer
	affichage.bordervillage(gamedata, classmap, option)
	# On update l'affichage de l'entête
	updateinterface(gamedata, classmap)


def banderole(gamedata, classmap, option):
	################
	# Fonction pour afficher une banderole aux joueurs qui indique qu'elle AI est entrain de jouer
	################

	# On créer le Frame
	frame_banderole = tkinter.Frame(classmap.framecanvas)
	frame_banderole.pack()

	# On lie le frame au canvas principale
	idwindow = classmap.mapcanv.create_window(option.widthWindow/2 , option.widthWindow/4, window = frame_banderole, tags = "interface")

	# On créer le canvas utiliser pour gérer l'affichage
	canvas_banderole = tkinter.Canvas(frame_banderole)
	canvas_banderole.pack()

	tkinter.Label(canvas_banderole, text = f"C'est au Seigneur N°{gamedata.Nb_toplay} {gamedata.list_lord[gamedata.Nb_toplay].lordname} de jouer").pack()

	return idwindow


def destroybanderole(gamedata, classmap, idwindow):
	classmap.mapcanv.delete(idwindow)





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
		#print(type(idw), idw)
		if (type(idw) == int) or (type(idw) == str):
			classmap.mapcanv.delete(idw)
		else:
			idw.destroy()

	# On unbind les fonctions
	i = 0
	while(i < len(lfuncid)):
		classmap.mapcanv.tag_unbind(lsequbind[i][0], lsequbind[i][1], lfuncid[i])
		i += 1

	# De manière générale on vient remplacer le bin click par le highlight case
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: highlightCase(event, gamedata, classmap))

	# On quitte l'état
	gamedata.statenull()



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
	print("\n")
	print("highlight x,y:",x,y)
	event.widget.create_rectangle(x, y, x + st, y + st, tags=["highlight","tuile"])
	coord(event, classmap)



def coord(event, classmap):
	print("coord tuile (0,0) dans canvas x,y: ", classmap.mapcanv.coords(classmap.listmap[0].canvastuiles))
	print("coord Window (0,0) dans canvas x,y:", classmap.mapcanv.canvasx(0), classmap.mapcanv.canvasy(0))
	print("coord event x,y: ",event.x, event.y)
	print("coord event canvas x,y: ",event.widget.canvasx(event.x), event.widget.canvasy(event.y))
	coord = event.widget.coords(event.widget.find_withtag("current")[0])
	print("coord x,y: ", coord[0], coord[1])
	print(event.widget.gettags("current"))


