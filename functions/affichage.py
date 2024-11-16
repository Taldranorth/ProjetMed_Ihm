import tkinter

import functions.data as data
import functions.interface as interface

#########################
# Fichier qui vient contenir les fonctions liées à l'affichage
#########################

def printvillage(gamedata, classmap, option, frame):
	##################
	# Fonction pour afficher les villages ainsi que leur noms à la création
	##################

	ts = gamedata.tuilesize
	for ele in classmap.lvillages:
		gamedata.loadtextureatlas("settlement.png", "build")
		#On recup la position en x et y 
		posx = classmap.listmap[ele].x
		posy = classmap.listmap[ele].y
		#print(Classmap.listmap[ele].type, Classmap.listmap[ele].x, Classmap.listmap[ele].y)
		# On affiche le village
		classmap.mapcanv.create_image((posx*ts)+(ts/2), (posy*ts)+(ts/2), tags = ["village","build","tuile","img", posx, posy], image = gamedata.atlas["settlement.png"].image)

		# On affiche en dessous le nom du village
		classmap.mapcanv.create_text((posx*ts)+(ts/2), (posy*ts), text = classmap.listmap[ele].village.name,tags = ["label","village","tuile", posx, posy], activefill = "Black")


	# On ajoute lie au tag village la fonction pour ouvrir l'interface des villages
	classmap.mapcanv.tag_bind("village","<Button-1>", lambda event, opt = option, gd = gamedata, cm = classmap: interface.villageinterface(event, gd, cm, opt))


def printvillageunit(gamedata, classmap, option, coordmap):
	##################
	# Fonction pour afficher un unique village avec les coord_map envoyer
	##################	

	posx = coordmap[0]
	posy = coordmap[1]
	idtuile = posx + (option.mapx*posy)

	ts = gamedata.tuilesize
	# On vérifie que la texture est en mémoire
	gamedata.loadtextureatlas("settlement.png", "build")

	# On affiche le village
	classmap.mapcanv.create_image((posx*ts)+(ts/2), (posy*ts)+(ts/2), tags = ["village","build","tuile","img", "click", posx, posy], image = gamedata.atlas["settlement.png"].image)

	# On affiche en dessous le nom du village
	classmap.mapcanv.create_text((posx*ts)+(ts/2), (posy*ts), text = classmap.listmap[idtuile].village.name,tags = ["label","village","tuile", posx, posy], activefill = "Black")

	# On ajoute lie au village la fonction pour ouvrir l'interface
	classmap.mapcanv.tag_bind("village","<Button-1>", lambda event, opt = option, gd = gamedata, cm = classmap: interface.villageinterface(event, gd, cm, opt))

def printarmy(gamedata, classmap, option, army):
	##################
	# Fonction pour afficher une armée 
	##################

	ts = gamedata.tuilesize
	posx = army.x
	posy = army.y

	# On affiche un portrait de chevalier Si l'armée possède un Chevalier
	if army.knight == 0:
		unit = "knight"
	# Sinon on affiche un portrait de Soldat
	else:
		unit = "soldier"
	# On prend une texture aléatoire
	texture_name = data.randomtexturefromdico(gamedata.dico_file, unit)
	# On assigne dans l'armée la texture
	army.texture = texture_name
	# On charge dans l'atlas la texture préparer avec une taille qui correspond à la moitier d'une tuile
	gamedata.loadtextureatlassize(texture_name, unit, ts/2)
	# On créer à l'emplacement voulu
	classmap.mapcanv.create_image((posx*ts)+(ts/2), (posy*ts)+(ts/2), tags = ["army","tuile","img", army.x, army.y], image = gamedata.atlas[texture_name].image)

	# On bind l'interface
	classmap.mapcanv.tag_bind("army", "<Button-1>", lambda event: interface.armyinterface(event, gamedata, classmap, option))


def printunit(gamedata, classmap, frame):
	##################
	# Fonction pour afficher les soldat
	##################
	pass
