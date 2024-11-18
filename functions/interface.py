import tkinter

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
	tkvar_nb_ressource = tkinter.IntVar()

	#Nb_money
	tkvar_nb_money = tkinter.IntVar()

	#global_joy
	tkvar_global_joy = tkinter.IntVar()

	#Nb_tour
	tkvar_nb_turn = tkinter.IntVar()

	tkvar_list +=[tkvar_nb_ressource, tkvar_nb_money, tkvar_global_joy, tkvar_nb_turn]	


	# On les set
	# Merde c'est pas dynamique
	tkvar_list[0].set(gamedata.list_lord[0].nb_ressource)
	tkvar_list[1].set(gamedata.list_lord[0].nb_money)
	tkvar_list[2].set(gamedata.list_lord[0].global_joy)
	tkvar_list[3].set(gamedata.Nb_tour)

	# Info Entête
	# Nb Total Ressource
	ressource_labelt = tkinter.Label(topframe, text = "Ressource Total: ")
	ressource_label = tkinter.Label(topframe, textvariable = tkvar_list[0])
	ressource_labelt.pack(side = "left")
	ressource_label.pack(side = 'left')

	# Nb Total Argent
	money_labelt = tkinter.Label(topframe, text = "Argent Total: ")
	money_label = tkinter.Label(topframe, textvariable = tkvar_list[1])
	money_labelt.pack(side = "left")
	money_label.pack(side = 'left')

	# Humeur Globale de la Population
	global_joy_labelt = tkinter.Label(topframe, text = "Taux de Bonheur: ")
	global_joy_label = tkinter.Label(topframe, textvariable = tkvar_list[2])
	global_joy_labelt.pack(side = "left")
	global_joy_label.pack(side = 'left')

	# N°Tour
	nb_turn_labelt = tkinter.Label(topframe, text = "Tour N°: ")	
	nb_turn_label = tkinter.Label(topframe, textvariable = tkvar_list[3])
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
	menu_military.add_command(label = "Soldat", command = lambda: staterecruitarmy(gamedata, classmap, option))
	menu_military.add_command(label = "Guerre", command = lambda: statewar(gamedata, classmap, option))


	# On associe les Commandes Gestion
	menu_gestion.add_command(label = "Immigration")
	menu_gestion.add_command(label = "Impôt")
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
	Button_endofturn = tkinter.Button(bottomFrame, command = lambda: turnend(gamedata, tkvar_list), text = "Fin de Tour")


	# On pack les Button
	Menu_Button_gestion.pack(side="left")
	Menu_Button_military.pack(side="left")
	Button_exit.pack(side="right")
	Button_globalview.pack(side="right")
	Button_endofturn.pack()
#########################################################################
# Fonction lier au bouton de fin de tour
def turnend(gamedata, topframe):
	print("fin de tour ")
	gamedata.endturn = True
	updateinterface(gamedata, topframe)


def updateinterface(gamedata, tkvar_list):
	tkvar_list[0].set(gamedata.list_lord[0].nb_ressource) 
	tkvar_list[1].set(gamedata.list_lord[0].nb_money) 
	tkvar_list[2].set(gamedata.list_lord[0].global_joy)
	tkvar_list[3].set(gamedata.Nb_tour)

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

	xpos = classmap.mapcanv.canvasx(0)
	ypos = classmap.mapcanv.canvasy(0)

	##############################\ À changer\##############################
	# Frame de la fenêtre
	frame_global_view = tkinter.Frame(classmap.framecanvas, height = option.heightWindow, width = option.widthWindow)
	frame_global_view.pack()
	canvaswindow = classmap.mapcanv.create_window(xpos +option.widthWindow/2, ypos + option.heightWindow/4, window = frame_global_view, tags = "interface")
	###########################################################################
	playerdata = gamedata.list_lord[gamedata.playerid]



	# On créer la légende au dessus
	# Frame qui va contenir la légende
	frame_global_view_legend = tkinter.Frame(frame_global_view)
	frame_global_view_legend.pack(side="top")

	for legend in ("Village","Population","Seigneur","Production de Ressource","Production d'argent","Prêtre","Bonheur"):
		tkinter.Label(frame_global_view_legend, text = legend).pack(side="left")

	# Frame qui va contenir les Infos Centraux
	frame_global_view_info = tkinter.Frame(frame_global_view)
	frame_global_view_info.pack()
	# affichage des Villages directement gérer le joueur
	i = 0
	frame_global_view_info_list = []
	for village in playerdata.fief:
		# Pour chaque village on va créer un sous frame
		frame_global_view_info_list += [tkinter.Frame(frame_global_view_info)]
		for ele in (village.name, len(village.population), village.lord.lordname, village.ressource, village.money, village.priest, village.global_joy):
			if ele == village.priest:
				if ele != 0:
					tkinter.Label(frame_global_view_info_list[i], text = ele.name).pack(side="left")
				else:
					tkinter.Label(frame_global_view_info_list[i], text = ele).pack(side="left")
			else:
				tkinter.Label(frame_global_view_info_list[i], text = ele).pack(side="left")
		frame_global_view_info_list[i].pack(side = "top")
		i += 1

	# affichage des Armées

	# Frame qui va contenir le boutton pour quitter
	frame_global_view_exit = tkinter.Frame(frame_global_view)
	frame_global_view_exit.pack(side ="bottom")

	# Bouton pour quitter le menu
	Button_exit = tkinter.Button(frame_global_view_exit, text= "Quitter", command = lambda: destroyglobalviewmenu(classmap.mapcanv, canvaswindow))
	Button_exit.pack()

def destroyglobalviewmenu(canvas, canvaswindow):
	canvas.delete(canvaswindow)

###########################################################################

def menu_military():
	pass


def menu_gestion():
	pass

##############################################################\ Militaire  \###########################################################################

def vassalisation():
	pass
############################################# Recrut Army #############################################

def staterecruitarmy(gamedata, classmap, option):
	################
	# Fonction pour ouvrir l'interface des armée
	################
	# On affiche la liste des armée dans une fenêtre
	# On créer un boutton pour en créer une
	#
	#
	################

	if gamedata.changenewstate("interface_recruit_army") == True:
		player = gamedata.list_lord[gamedata.playerid]
		xorigine = classmap.mapcanv.canvasx(0)
		yorigine = classmap.mapcanv.canvasy(0)

		# On créer l'interface qui va contenir le frame
		frame_interface_army = tkinter.Frame(classmap.framecanvas, height = 200, width = 300)
		frame_interface_army.place(x = (option.widthWindow/6), y = (option.heightWindow*0.2))

		# listbox
		lc_interface_army = tkinter.Listbox(frame_interface_army)
		lc_interface_army.place(relx = 0, rely = 0, width = 150, anchor = tkinter.NW)

		# On affiche la liste des armées du Joueur uniquement
		for army in player.army:
			lc_interface_army.insert(tkinter.END, army.name)
		# On bind l'objet à une fonction pour center sur l'armée selectionner
		lc_interface_army.bind("<Double-Button-1>", lambda event: interfacerecruit(event, gamedata, classmap, option, frame_interface_army))
		# On créer un boutton pour créer une nouvelle armée
		button_createarmy = tkinter.Button(frame_interface_army, text= "Nouvelle Armée", command = lambda: interfacecreatearmy(gamedata, classmap, option, lc_interface_army))
		button_createarmy.place(x=30, y=200, anchor = tkinter.SW)

		# On bind 
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [frame_interface_army]))

def interfacecreatearmy(gamedata, classmap, option, lc_interface_army):


	player = gamedata.list_lord[gamedata.playerid]
	lastarmy = len(player.army)

	gamedata.log.printinfo("Le Joueur Créer une armée")
	# On créer la nouvelle armée
	player.createarmy(player.fief[0])

	# On affiche la nouvelle armée
	affichage.printarmy(gamedata, classmap, option, player.army[lastarmy])
	# On update l'interface de la listbox
	lc_interface_army.insert(tkinter.END, player.army[lastarmy].name)

def interfacerecruit(event, gamedata, classmap, option, frame_interface_army):

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
	frame_interface_army_right.place(x = 150, rely = 0 )


	# On créer les variables pour l'affichage
	tkvar_power = tkinter.IntVar()
	tkvar_power.set(army.power)

	tkvar_lenknight = tkinter.IntVar()
	tkvar_lenknight.set(army.knight)

	tkvar_lenunit = tkinter.IntVar()
	tkvar_lenunit.set(len(army.unit))

	tkvar_list = [tkvar_power, tkvar_lenknight, tkvar_lenunit]

	# On affiche les Infos de l'armée
	frame_interface_army_right_top = tkinter.Frame(frame_interface_army_right)
	frame_interface_army_right_top.pack(side = "top")

	# La puissance de l'armée
	tkinter.Label(frame_interface_army_right_top, textvariable = tkvar_list[0]).pack()
	# Le nombre de Chevalier
	tkinter.Label(frame_interface_army_right_top, textvariable = tkvar_list[1]).pack()
	# Le nombre de Soldat
	tkinter.Label(frame_interface_army_right_top, textvariable = tkvar_list[2]).pack()

	# On créer un bouttons pour recruter un soldat
	button_recruit_soldier = tkinter.Button(frame_interface_army_right, command = lambda unit="soldier": button_recruit(gamedata, classmap, tkvar_list, army, unit), text = "Recruter soldat")
	button_recruit_soldier.pack(side = "bottom")

	# On créer un bouttons pour recruter un Chevalier
	button_recruit_knight = tkinter.Button(frame_interface_army_right, command = lambda unit="knight": button_recruit(gamedata, classmap, tkvar_list, army, unit), text = "Recruter Chevalier")
	button_recruit_knight.pack(side = "bottom")

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
	coord = moveview.coordmaptocanvas(gamedata, classmap, option, [army.x, army.y])
	#print("Coord Canvas: ", coord[0], coord[1])


	# On centre la vu sur le village
	moveview.centerviewcanvas(gamedata, classmap, option, coord)

def button_recruit(gamedata, classmap, tkvar_list, army, unit):
	################
	# Fonction appeler pour recruter
	################


	# On recrute l'unité
	if unit == "knight":
		army.recruitknight(gamedata.randomnametype("Surnom"))
		tkvar_list[1].set(army.knight.name)
	elif unit == "soldier":
		army.recruitsoldier(gamedata.randomnametype("Nom"))
		tkvar_list[2].set(len(army.unit))
	# On update l'armée
	if gamedata.searchtexturetypeindico(army.texture) != "knight":
		affichage.printupdatearmy(gamedata, classmap, army)

	# On update l'interface
	tkvar_list[0].set(army.power)




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
			moveview.moveviewzcenter(gamedata, classmap, option)

		player = gamedata.list_lord[gamedata.playerid]
		ts = gamedata.tuilesize
		xorigine = classmap.mapcanv.canvasx(0)
		yorigine = classmap.mapcanv.canvasy(0)

		# On se place au centre
		moveview.centerviewcanvas(gamedata, classmap, option, [(option.mapx/2)*ts, (option.mapy/2)*ts])

		# On affiche les territoire 
		# On se balade dans la liste des térritoire
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
					classmap.mapcanv.create_rectangle((x*ts) - xorigine, (y*ts)- yorigine, (x*ts)+ts - xorigine, (y*ts)+ts - yorigine, tag = ["interface_war","tuile", x, y], outline = color)
					if color == "white":
						print("village neutre: ", village.name)
					elif color == "re":
						print("village ennemie: ", village.name)

		# On créer l'interface
		frame_interface_war = tkinter.Frame(classmap.framecanvas)
		frame_interface_war.place(x = (option.widthWindow/6), y = (option.heightWindow*0.2))

		frame_interface_war_list_ally = tkinter.Frame(frame_interface_war)
		frame_interface_war_list_ennemy = tkinter.Frame(frame_interface_war)
		frame_interface_war_list_neutral = tkinter.Frame(frame_interface_war)
		frame_interface_war_list_ally.pack(side = "left")
		frame_interface_war_list_ennemy.pack(side = "left")
		frame_interface_war_list_neutral.pack(side = "left")

		frame_interface_war_list_ally_top = tkinter.Frame(frame_interface_war_list_ally)
		frame_interface_war_list_ennemy_top = tkinter.Frame(frame_interface_war_list_ennemy)
		frame_interface_war_list_neutral_top = tkinter.Frame(frame_interface_war_list_neutral)

		frame_interface_war_list_ally_top.pack(side = "top")
		frame_interface_war_list_ennemy_top.pack(side = "top")
		frame_interface_war_list_neutral_top.pack(side = "top")


		tkinter.Label(frame_interface_war_list_ally_top, text = "Allié").pack(side = "top")
		tkinter.Label(frame_interface_war_list_ennemy_top, text = "Ennemie").pack(side = "top")
		tkinter.Label(frame_interface_war_list_neutral_top, text = "Neutre").pack(side = "top")

		for lord in gamedata.list_lord:
			if lord in player.vassal:
				tkinter.Label(frame_interface_war_list_ally, text = lord.lordname).pack(side = "top")
			elif lord in player.war:
				tkinter.Label(frame_interface_war_list_ennemy, text = lord.lordname).pack(side = "top")
			elif lord.player == False:
				tkinter.Label(frame_interface_war_list_neutral, text = lord.lordname).pack(side = "top")

		# On bind
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [frame_interface_war, "interface_war"]))

def wardeclaration(gamedata, mapcanv, lord):

	
	pass

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

	print("On construit le village")
	# On calcul l'id de la tuile
	xpos = int(event.widget.gettags("current")[2])
	ypos = int(event.widget.gettags("current")[3])
	idtuile = xpos + (option.mapx*ypos)

	# On créer
	# On ajoute l'id de la tuile à la liste des villages
	classmap.lvillages += [idtuile]
	# On créer le village
	classmap.listmap[idtuile].createvillage(gamedata)
	classmap.listmap[idtuile].setpossesor("player")
	# On ajoute l'instance de vilalge à la liste de fief du lord
	gamedata.list_lord[gamedata.playerid].addfief(classmap.listmap[idtuile].village)
	# On rempli le village de pop
	#classmap.listmap[idtuile].village

	# On retire les ressource 

	# On affiche le nouveau village
	affichage.printvillageunit(gamedata, classmap, option, [xpos,ypos])

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

	if gamedata.changenewstate("build_church") == True:

		player = gamedata.list_lord[gamedata.playerid]
		ts = gamedata.tuilesize
		xoriginewindow = classmap.mapcanv.canvasx(0)
		yoriginewindow = classmap.mapcanv.canvasy(0)
		originecanvas = classmap.mapcanv.coords(classmap.listmap[0].canvastuiles)

		# On affiche une interface montrant une liste des villages ou on peut construire + données du village

		# On créer la frame
		frame_interface_church = tkinter.Frame(classmap.framecanvas)
		frame_interface_church.place(x = (option.widthWindow/6), y = (option.heightWindow*0.2))

		# On créer la listbox
		lc_interface_church = tkinter.Listbox(frame_interface_church)
		lc_interface_church.pack()
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
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event, lsequ = [["village","<Button-1>"]], lf = [idbuildchurch], lidw = [frame_interface_church, "buildchurch"]: exitstate(gamedata, classmap, option, lsequ, lf, lidw))


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

	coord = moveview.coordmaptocanvas(gamedata, classmap, option, [x, y])

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

	# On vérife que le village appartient au joueur
	if village in gamedata.list_lord[gamedata.playerid].fief:
		village.buildchurch(gamedata.randomnametype("Nom"))
		# On retire le carrer 

def tax():
	pass

def immigration():
	pass

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
		tkinter.Label(frame_info, text = classmap.listmap[idmapvillage].village.ressource).pack(side = "top")
		# l'argent du village
		tkinter.Label(frame_info, text = classmap.listmap[idmapvillage].village.money).pack(side = "top")

		######################################################################

		# Si le joueur clique autre part on sort de l'interface
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event, cwl = canvas_window_list: exitstate(gamedata, classmap, option, [], [], cwl))


def armyinterface(event, gamedata, classmap, option):
	################
	# Fonction créer la fenêtre de l'interface de l'armée selectionné
	################

	if gamedata.changenewstate("interface_army") == True:

		# On créer le frame
		frame_interface_army = tkinter.Frame(classmap.framecanvas)
		frame_interface_army.place(x = (option.widthWindow/3), y = (option.heightWindow/2))

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
		tkinter.Label(frame_interface_army, text = army.name).pack(side = "left")
		# On affiche la puissance
		tkinter.Label(frame_interface_army, text = "Puissance: ").pack(side = "left")
		tkinter.Label(frame_interface_army, text = army.power).pack(side = "left")

		tkinter.Label(frame_interface_army, text = "Movement").pack(side = "left")
		# On affiche la capacité de déplacement max
		tkinter.Label(frame_interface_army, text = army.movecapacity).pack(side = "left")
		# On affiche la capacité de déplacement possible
		tkinter.Label(frame_interface_army, text = army.moveturn).pack(side = "left")

		# On créer le bouton pour se déplacer
		Button_move_army = tkinter.Button(frame_interface_army, text = "Déplacement", command = lambda: statemovearmy(gamedata, classmap, option, army))
		Button_move_army.pack(side="left")

		# Si on clique droit sur une armée non allié alors que l'on à selectionner une armée on attaque

		# Si on clique sur autre chose on quitte l'interface
		classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstate(gamedata, classmap, option, [], [], [frame_interface_army]))



def statemovearmy(gamedata, classmap, option, army):
	##################
	# Fonction pour Entréer le joueur dans un état de déplacement d'armé Si il clique sur le bouton déplacer dabs l'interface d'armée
	##################

	# On change la souris Pour l'icone de déplacement
	# On charge en mémoire dans l'atlas la texture préparer
	#gamedata.loadtextureatlas("rally_point.png", "other")
	# On change la souris afficher dans la toplevel Window
	# On recup la fenêtre
	root =  classmap.framecanvas.winfo_toplevel()
	# On config la fenêtre 
	root.config(cursor = "man")

	# On bind l'affiche de la trajectoire sur l'emplacement de la souris quand elle est sur le canvas
	#funcpath = classmap.mapcanv.tag_bind("click","<Motion>", lambda event: showpathfinding(event, gamedata), add= "+")

	# On debind le exitstate
	classmap.mapcanv.tag_unbind("click", "<Button-1>")

	# On bind le click gauche sur aller 
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: affichage.sequencemoveunit(event, gamedata, classmap, option, army))

	# On bind l'exit de l'état aux clic gauche
	#classmap.mapcanv.tag_bin("click", "<Button-2>", lambda: exitstate(gamedata, classmap, option, [["click","<Move>"]], [funcpath], ["path"]) )

def showpathfinding(event, gamedata):
	# On calcul la meilleur trajectoire
	sequ = affichage.pathfinding(coord0, coord1)

	# On détruit la précédante trajectoire afficher
	event.widget.destroy("Path")

	ts = gamedata.tuilesize
	# On affiche la trajectoire
	for cases in sequ:
		classmap.mapcanv.create_line( (sequ[0]*ts), (sequ[1]*ts), (sequ[0]*ts)+ts, (sequ[1]*ts)+ts, width = 5, tags = "path")




def exitstatemovearmy():



	pass




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


