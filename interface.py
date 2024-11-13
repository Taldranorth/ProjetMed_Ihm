import tkinter
import genproc
import affichage





######################### Fonction Interface ############################

def gameinterface(win, option, gamedata, classmap, framecanvas):

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
	menu_military.add_command(label = "Soldat")
	menu_military.add_command(label = "Guerre")


	# On associe les Commandes Gestion
	menu_gestion.add_command(label = "Immigration")
	menu_gestion.add_command(label = "Impôt")
	menu_gestion.add_command(label = "Construire Église")
	menu_gestion.add_command(label = "Construire Village", command = lambda: statebuildvillage(option, gamedata, classmap, framecanvas))



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
		for ele in (village.name, len(village.population), village.lord, village.ressource, village.money, village.priest, village.global_joy):
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

# Fonction lier au bouton de fin de tour
def turnend(gamedata, topframe):
	print("fin de tour ")
	gamedata.endturn = True
	updateinterface(gamedata, topframe)



def villageinterface(event, option, gamedata, classmap, fcanvas):
	##################
	# Fonction pour afficher l'interface d'un village
	##################

	# On recup l'origine du canvas
	xorigine = classmap.mapcanv.canvasx(0)
	yorigine = classmap.mapcanv.canvasy(0)

	# On recup l'idée du canvas de la tuile que l'on vient de sélectionner
	idcanvasvillage = event.widget.find_withtag("current")[0]
	# On recup les coord-canvas du village
	coordcanv = event.widget.coords(idcanvasvillage)
	# On recup la pos x et y du village dans la map
	print(event.widget.gettags(idcanvasvillage))
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
	print(idmapvilage)

	centerview(gamedata, option, classmap.mapcanv, coordcanv)

	print("On affiche l'interface du village")
	# On fait apparaitre l'interface informative
	# On commence par créer le frame qui vient stocker les infos
	frame_info = tkinter.Frame(fcanvas)
	# On créer la frame qui vient contenir les actions possibles
	frame_button = tkinter.Frame(fcanvas)
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
	print(classmap.listmap[idmapvilage].village.name)
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
	classmap.mapcanv.tag_bind("click", "<Button-1>",lambda event, mc = classmap.mapcanv, cwl = canvas_window_list: exitvillageinterface(event, mc, cwl))


def exitvillageinterface(event, mapcanv, lwindow):
	################
	# Fonction pour détruire les fenêtre de l'interface du village
	################
	for id in lwindow:
		mapcanv.delete(id)
	print("On supprime l'interface du village")
	# On retire le bind sur la fonction
	# Comprend pas comment faire donc en attendant remplace avec highlight
	#mapcanv.tag_unbind("click", "<Button-1>", funcid = "exitvillageinterface")
	mapcanv.tag_bind("click", "<Button-1>", highlightCase)




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





def statebuildvillage(option, gamedata, classmap, framecanvas):
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
			classmap.mapcanv.create_rectangle((x*ts) - xorigine, (y*ts)- yorigine, (x*ts)+ts - xorigine, (y*ts)+ts - yorigine,tag = ["buildvillage","tuile", x, y], fill = "green",outline = "green")

	# On tag au carrer 
	classmap.mapcanv.tag_bind("buildvillage", "<Button-1>", lambda event: buildvillage(event, classmap, gamedata, option, framecanvas))
	classmap.mapcanv.tag_bind("click", "<Button-1>", lambda event, mc = classmap.mapcanv: exitstatebuildvillage(event, mc), add = "+")

def buildvillage(event, classmap, gamedata, option, framecanvas):
	############
	# Fonction pour créer un village selon la tuile sélectionner en état de construction
	############

	print("On construit le village")
	# On calcul l'id de la tuile
	xpos = int(event.widget.gettags("current")[2])
	ypos = int(event.widget.gettags("current")[3])
	idtuile = xpos + (option.mapx*ypos)

	# On créer
	classmap.lvillages += [idtuile]
	classmap.listmap[idtuile].createvillage()
	classmap.listmap[idtuile].setpossesor("player")
	gamedata.list_lord[gamedata.playerid].addfief(classmap.listmap[idtuile].village)

	# On retire les ressource 

	# On affiche le nouveau village
	affichage.printvillageunit(gamedata, classmap, option, framecanvas, [xpos,ypos])

def exitstatebuildvillage(event, mapcanv):
	# On delete tout les éléments ayant le tag buildvillage
	print("On Supprimer le grillage constuction")
	mapcanv.delete("buildvillage")
	# On retire le bind
	#mapcanv.tag_unbind()

