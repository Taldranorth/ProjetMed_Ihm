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
		classmap.mapcanv.create_image((posx*ts)+(ts/2), (posy*ts)+(ts/2), tags = ["village","build","tuile","img", "click", posx, posy], image = gamedata.atlas["settlement.png"].image)

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


def printarmy(gamedata, classmap, option):
	##################
	# Fonction pour afficher une armée 
	##################
	pass


def printunit(gamedata, classmap, frame):
	##################
	# Fonction pour afficher les soldat
	##################
	pass
