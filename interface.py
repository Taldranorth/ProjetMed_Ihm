import tkinter
import genproc
import affichage

import main



######################### Fonction Interface ############################

def gameinterface(win, option, gamedata, classmap):

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
	topframe = tkinter.Frame(win, height = (option.heightWindow*0.2), width= option.widthWindow, background = "grey")
	topframe.pack(expand = "True", side = "top")
	# En tête Bas
	bottomFrame = tkinter.Frame(win, height = (option.heightWindow*0.2), width= option.widthWindow, background = "grey")
	bottomFrame.pack(expand = "True", side = "bottom")




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
	ressource_label = tkinter.Label(topframe, text = "Ressource Total: ", textvariable = tkvar_list[0])
	ressource_labelt.pack(side = "left")
	ressource_label.pack(side = 'left')

	# Nb Total Argent
	money_labelt = tkinter.Label(topframe, text = "Argent Total: ")
	money_label = tkinter.Label(topframe, text = "Argent Total: ", textvariable = tkvar_list[1])
	money_labelt.pack(side = "left")
	money_label.pack(side = 'left')

	# Humeur Globale de la Population
	global_joy_labelt = tkinter.Label(topframe, text = "Taux de Bonheur: ")
	global_joy_label = tkinter.Label(topframe, text = "Taux de Bonheur: ", textvariable = tkvar_list[2])
	global_joy_labelt.pack(side = "left")
	global_joy_label.pack(side = 'left')

	# N°Tour
	nb_turn_labelt = tkinter.Label(topframe, text = "Tour N°: ")	
	nb_turn_label = tkinter.Label(topframe, text = "Tour N°: ", textvariable = tkvar_list[3])
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
	Button_globalview = tkinter.Button(bottomFrame, command = lambda: globalviewmenu(win, option, gamedata, classmap), text = "Vue Générale")

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
def globalviewmenu(win ,option, gamedata, classmap):

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


	##############################\ À changer\##############################
	# Frame de la fenêtre
	frame_global_view = tkinter.Frame(win, height = option.heightWindow, width = option.widthWindow)
	frame_global_view.pack()
	canvaswindow = classmap.mapcanv.create_window(option.widthWindow/2, option.heightWindow/4, window = frame_global_view)
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

	if gamedata.state != 0 :
		gamedata.log.printerror(f"déjà dans un état {gamedata.state}")
		return
	else:
		gamedata.state = "interface_recruit_army"
		gamedata.log.printinfo("entre dans un état interface_recruit_army")



	player = gamedata.list_lord[gamedata.playerid]
	xorigine = classmap.mapcanv.canvasx(0)
	yorigine = classmap.mapcanv.canvasy(0)

	# On créer l'interface qui va contenir le frame
	frame_interface_army = tkinter.Frame(classmap.framecanvas)
	frame_interface_army.pack()

	# listbox
	lc_interface_army = tkinter.Listbox(frame_interface_army)

	# On affiche la liste des armées du Joueur uniquement
	for army in player.army:
		lc_interface_army.insert(tkinter.END, army.name)
	#lc_interface_army.bind("<Double-Button-1>",)

	# On créer la window qui va s'afficher sur le canvas
	idwindow = classmap.mapcanv.create_window(xorigine+option.widthWindow/6, yorigine+option.heightWindow/3, window = frame_interface_army)

	# On bind 
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstatestaterecruitarmy(event, gamedata, classmap.mapcanv, idwindow))


def exitstatestaterecruitarmy(event, gamedata, mapcanv, idwindow):
	################
	# Fonction pour quitter l'interface de recrutement d'armé
	################
	gamedata.log.printinfo("On Supprimer l'interface de recretument d'armée '")
	# On nettoye l'interface
	mapcanv.delete(idwindow)
	# On Unbind
	mapcanv.tag_bind("click", "<Button-1>", lambda event: highlightCase(event, gamedata))
	# On remet à 0 l'état
	gamedata.state = 0


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

	if gamedata.state != 0 :
		gamedata.log.printerror(f"déjà dans un état {gamedata.state}")
		return
	else:
		gamedata.state = "interface_war"
		gamedata.log.printinfo("entre dans un état interface_war")

	# Tant que la carte n'est pas dezoom à 20
	while gamedata.tuilesize != 20:
		main.moveviewz(gamedata)





	player = gamedata.list_lord[gamedata.playerid]
	ts = gamedata.tuilesize
	xorigine = classmap.mapcanv.canvasx(0)
	yorigine = classmap.mapcanv.canvasy(0)

	# On se place au centre
	main.centerview(gamedata, option, classmap.mapcanv, [(option.mapx/2)*ts, (option.mapy/2)*ts])

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
	frame_interface_war.pack()

	# On affiche dans une fenêtre liée au canvas
	idwindow = classmap.mapcanv.create_window(xorigine+option.widthWindow/6, yorigine+option.heightWindow/3, window = frame_interface_war)

	# On affiche une liste des alliés, des ennemies et des neutres
	frame_interface_war_list_ally = tkinter.Frame(frame_interface_war)
	frame_interface_war_list_ennemy = tkinter.Frame(frame_interface_war)
	frame_interface_war_list_neutral = tkinter.Frame(frame_interface_war)
	frame_interface_war_list_ally.pack(side = "left")
	frame_interface_war_list_ennemy.pack(side = "left")
	frame_interface_war_list_neutral.pack(side = "left")
	tkinter.Label(frame_interface_war_list_ally, text = "Allié").pack(side = "top")
	tkinter.Label(frame_interface_war_list_ennemy, text = "Ennemie").pack(side = "top")
	tkinter.Label(frame_interface_war_list_neutral, text = "Neutre").pack(side = "top")

	for lord in gamedata.list_lord:
		if lord in player.vassal:
			tkinter.Label(frame_interface_war_list_ally, text = lord.lordname).pack(side = "top")
		elif lord in player.war:
			tkinter.Label(frame_interface_war_list_ennemy, text = lord.lordname).pack(side = "top")
		elif lord.player == False:
			tkinter.Label(frame_interface_war_list_neutral, text = lord.lordname).pack(side = "top")

	# On bind
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: exitstatewar(event, gamedata, classmap.mapcanv, idwindow))

def wardeclaration(gamedata, mapcanv, lord):

	
	pass

def exitstatewar(event, gamedata, mapcanv, idwindow):
	################
	# Fonction pour quitter l'interface de guerre
	################
	gamedata.log.printinfo("On Supprimer le grillage war")
	# On delete les carrer
	mapcanv.delete("interface_war")

	gamedata.log.printinfo("On Supprimer l'interface war")
	# On delete la fenêtre
	mapcanv.delete(idwindow)

	# On unbind
	mapcanv.tag_bind("click", "<Button-1>", lambda event: highlightCase(event, gamedata))

	# On quitter l'état de guerre
	gamedata.state = 0



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

	if gamedata.state != 0 :
		gamedata.log.printerror(f"déjà dans un état {gamedata.state}")
		return
	else:
		gamedata.state = "build_village"
		gamedata.log.printinfo("entre dans un état build_village")


	ts = gamedata.tuilesize
	xorigine = classmap.mapcanv.canvasx(0)
	yorigine = classmap.mapcanv.canvasy(0)

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
			classmap.mapcanv.create_rectangle(xorigine + (x*ts), yorigine + (y*ts) , xorigine + (x*ts)+ts, yorigine + (y*ts)+ts,tag = ["buildvillage","tuile", x, y], fill = "green",outline = "green")

	# On tag au carrer 
	classmap.mapcanv.tag_bind("buildvillage", "<Button-1>", lambda event: buildvillage(event, gamedata, classmap, option))
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event, mc = classmap.mapcanv: exitstatebuildvillage(event, gamedata, mc), add = "+")

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
	classmap.listmap[idtuile].createvillage()
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




def exitstatebuildvillage(event, gamedata, mapcanv):
	# On delete tout les éléments ayant le tag buildvillage
	gamedata.log.printinfo("On Supprimer le grillage constuction")
	mapcanv.delete("buildvillage")
	# On retire le bind
	mapcanv.tag_bind("click", "<Button-1>", lambda event: highlightCase(event, gamedata))

	gamedata.state = 0





############################################# Build Church #############################################


def statebuildchurch(gamedata, classmap, option):
	if gamedata.state != 0:
		gamedata.log.printerror(f"déjà dans un état {gamedata.state}")
		return
	else:
		gamedata.state = "build_church"
		gamedata.log.printinfo("entre dans un état build_church")



	player = gamedata.list_lord[gamedata.playerid]
	ts = gamedata.tuilesize
	xorigine = classmap.mapcanv.canvasx(0)
	yorigine = classmap.mapcanv.canvasy(0)

	# On affiche une interface montrant une liste des villages ou on peut construire + données du village

	# On créer la frame
	frame_interface_church = tkinter.Frame(classmap.framecanvas)
	frame_interface_church.pack()

	# On créer la listbox
	lc_interface_church = tkinter.Listbox(frame_interface_church)
	lc_interface_church.pack()
	# On créer un menu déroulant qui présente les villages éligible à la construction d'une église avec les donnés du villag
	for village in player.fief:
		if village.church == 0:
			lc_interface_church.insert(tkinter.END, village.name)
	# Quand un village est double click on appele la fonction pour centrer la vue sur le village
	lc_interface_church.bind("<Double-Button-1>", lambda event: centervillagechurch(event, gamedata, classmap, option))
			
	#ON créer un window dans le canvas
	idwindow = classmap.mapcanv.create_window(xorigine+option.widthWindow/6, yorigine+option.heightWindow/3, window = frame_interface_church)

	# On bind la fonction d'exit à tout ce qui n'est pas un village construisible
	classmap.mapcanv.tag_bind("click", "<Button-1>",lambda event: exitstatebuildchurch(event, gamedata, classmap, option, idwindow))

	# On affiche en vert tout les villages ou on peut construire une église
	for village in player.fief:
		if village.church == 0:
			x = village.x
			y = village.y
			classmap.mapcanv.create_rectangle((x*ts) - xorigine, (y*ts)- yorigine, (x*ts)+ts - xorigine, (y*ts)+ts - yorigine , tags = ["buildchurch","tuile"], outline = "green")
			# On calcul l'id de la tuile
			idvillage =x + (option.mapx*y)
			# On bind la fonction buildchurch à la tuile du village
			classmap.mapcanv.tag_bind(["village",x, y], "<Button-1>",lambda event: buildchurch(event, gamedata, village))


def centervillagechurch(event, gamedata, classmap, option):
	############
	# Fonction appeler par la listbox lc_interface_church pour centrer la carte sur le village selectionner dans la listbox
	# On sait que les noms des villages sont uniques
	############
	gamedata.log.printinfo("On se déplace vers le village")
	# On recup le village actuellement selectionner dans la listbox
	village_selected = event.widget.curselection()
	
	idvillage = classmap.nametoid(village_selected)
	# On recup les coord du village
	x = classmap.listmap[idvillage].x
	y = classmap.listmap[idvillage].y


	# On centre la vu sur le village
	main.centerview(gamedata, option, classmap.mapcanv, [classmap.mapcanv.canvasx(x),classmap.mapcanv.canvasy(y)])

def buildchurch(event, gamedata, idvillage):
	############
	# Fonction pour construire une église dans un village
	############

	village.buildchurch(gamedata.randomnametype("Nom"))




def exitstatebuildchurch(event, gamedata, classmap, option, idwindow):
	############
	# Fonction pour sortir de l'état build_church et néttoyer l'interface
	############
	gamedata.log.printinfo("On Supprimer le grillage church")
	# On détruit les cases verte
	classmap.mapcanv.delete("buildchurch")
	gamedata.log.printinfo("On Supprimer l'interface build_church'")
	# On détruit l'interface
	classmap.mapcanv.delete(idwindow)
	# On retire le bind exit
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event: highlightCase(event, gamedata))
	# On retir le bind build
	classmap.mapcanv.tag_bind("village","<Button-1>", lambda event, opt = option, gd = gamedata, cm = classmap: villageinterface(event, opt, gd, cm))
	# On sort de l'état build_church
	gamedata.state = 0


def tax():
	pass

def immigration():
	pass



def villageinterface(event, option, gamedata, classmap):
	##################
	# Fonction pour afficher l'interface d'un village
	##################

	# Si le joueur est dans un état ou il a déjà l'interface d'un village ouvert on ne fait rien
	if gamedata.state != 0 :
		gamedata.log.printerror(f"déjà dans un état {gamedata.state}")
		return
	else:
		gamedata.state = "interface_village"
		gamedata.log.printinfo("entre dans un état interface_village")


	# On recup l'origine du canvas
	xorigine = classmap.mapcanv.canvasx(0)
	yorigine = classmap.mapcanv.canvasy(0)

	# On recup l'idée du canvas de la tuile que l'on vient de sélectionner
	idcanvasvillage = event.widget.find_withtag("current")[0]
	# On recup les coord-canvas du village
	coordcanv = event.widget.coords(idcanvasvillage)
	# On recup la pos x et y du village dans la map
	gamedata.log.printinfo(f"{event.widget.gettags(idcanvasvillage)}")
	# Si on à cliqué sur le village
	if event.widget.type(idcanvasvillage) == "image":
		posx = event.widget.gettags(idcanvasvillage)[5]
		posy = event.widget.gettags(idcanvasvillage)[6]
	# Sinon on à cliqué sur le label
	else:
		posx = event.widget.gettags(idcanvasvillage)[3]
		posy = event.widget.gettags(idcanvasvillage)[4]

	# On calcul l'id map du village
	idmapvilage = int(posx)+(option.mapx*int(posy))
	gamedata.log.printinfo(f"{idmapvilage}")
	# On place le village au centre de l'écran
	main.centerview(gamedata, option, classmap.mapcanv, coordcanv)

	gamedata.log.printinfo("On affiche l'interface du village")
	# On fait apparaitre l'interface informative
	# On commence par créer le frame qui vient stocker les infos
	frame_info = tkinter.Frame(classmap.framecanvas)
	# On créer la frame qui vient contenir les actions possibles
	frame_button = tkinter.Frame(classmap.framecanvas)
	frame_info.pack()
	frame_button.pack()

	# On créer les fenêtre
	# Demade un placement précis
	canvas_window_list = []
	# Pour les fenêtre on prend en compte le décalage créer par move()
	# Fenêtre Info
	canvas_window_list += [classmap.mapcanv.create_window(xorigine+option.widthWindow/3, yorigine+option.heightWindow/4, window = frame_info)]
	# Fenêtre Button
	canvas_window_list += [classmap.mapcanv.create_window(xorigine+option.widthWindow/1.5, yorigine+option.heightWindow/4, window = frame_button)]


	# On affiche les infos voulu
	# Le nom du village
	tkinter.Label(frame_info, text = classmap.listmap[idmapvilage].village.name).pack(side = "top")
	gamedata.log.printinfo(f"{classmap.listmap[idmapvilage].village.name}")
	# Le seigneur du village
	if (classmap.listmap[idmapvilage].village.lord == 0):
		tkinter.Label(frame_info, text = "lord").pack(side = "top")
	else:
		tkinter.Label(frame_info, text = classmap.listmap[idmapvilage].village.lord.lordname).pack(side = "top")
	# Le prêtre du village
	if classmap.listmap[idmapvilage].village.priest == 0:
		tkinter.Label(frame_info, text = "priest").pack(side = "top")
	else:
		tkinter.Label(frame_info, text = classmap.listmap[idmapvilage].village.priest.name).pack(side = "top")
	# Le bonheur global
	tkinter.Label(frame_info, textv = classmap.listmap[idmapvilage].village.global_joy).pack(side = "top")
	# les ressources du village
	tkinter.Label(frame_info, text = classmap.listmap[idmapvilage].village.ressource).pack(side = "top")
	# l'argent du village
	tkinter.Label(frame_info, text = classmap.listmap[idmapvilage].village.money).pack(side = "top")

	# On fait apparaitre les boutons
	button_build_church = tkinter.Button(frame_button, text = "Construire Église")
	button_immigration = tkinter.Button(frame_button, text = "Immigration")
	button_tax = tkinter.Button(frame_button, text = "Impôt")
	button_build_church.pack(side="top")
	button_immigration.pack(side="top")
	button_tax.pack(side="top")

	# Si le joueur clique autre part on sort de l'interface
	classmap.mapcanv.tag_bind("click", "<Button-1>",lambda event, mc = classmap.mapcanv, cwl = canvas_window_list: exitvillageinterface(event, gamedata, mc, cwl))


def exitvillageinterface(event, gamedata, mapcanv, lwindow):
	################
	# Fonction pour détruire les fenêtre de l'interface du village
	################
	for id in lwindow:
		mapcanv.delete(id)
	gamedata.log.printinfo("On supprime l'interface du village")
	# On retire le bind sur la fonction
	mapcanv.tag_bind("click", "<Button-1>", lambda event: highlightCase(event, gamedata))

	# On quitte l'état de construction de village
	gamedata.state = 0



def highlightCase(event, gamedata):
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
	print("highlight x,y:",x,y)
	event.widget.create_rectangle(x, y, x + st, y + st, tags=["highlight","tuile"])
	coord(event)



def coord(event):
	print("\n")
	print("coord origine x,y: ", event.widget.canvasx(0), event.widget.canvasy(0))
	print("coord event x,y: ",event.x, event.y)
	print("coord event canvas x,y: ",event.widget.canvasx(event.x), event.widget.canvasy(event.y))
	coord = event.widget.coords(event.widget.find_withtag("current")[0])
	print("coord x,y: ", coord[0], coord[1])
	print(event.widget.gettags("current"))
