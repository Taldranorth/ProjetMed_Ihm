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
	classmap.mapcanv.create_image((posx*ts)+(ts/2), (posy*ts)+(ts/2), tags = ["village","build","tuile","img", posx, posy], image = gamedata.atlas["settlement.png"].image)

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
	if army.knight != 0:
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
	army.idtcanvas = classmap.mapcanv.create_image((posx*ts)+(ts/2), (posy*ts)+(ts/2), tags = ["army","tuile","img", army.x, army.y], image = gamedata.atlas[texture_name].image)

	# On bind l'interface
	classmap.mapcanv.tag_bind("army", "<Button-1>", lambda event: interface.armyinterface(event, gamedata, classmap, option))

def printupdatearmy(gamedata, classmap, army):
	##################
	# Fonction pour Update l'affichage d'une armée
	##################
	ts = gamedata.tuilesize

	if army.knight != 0:
		unit = "knight"
	else:
		unit = "solider"
	# On recup la texture
	texture_name = data.randomtexturefromdico(gamedata.dico_file, unit)
	# On la stocke dans la class
	army.texture = texture_name
	# On la charge dans l'atlas
	gamedata.loadtextureatlassize(texture_name, unit, ts/2)
	# On recup le Canvas Id de l'armée
	armyId = army.idtcanvas
	# On update l'image
	classmap.mapcanv.itemconfigure(armyId, image = gamedata.atlas[texture_name].image)

def sequencemoveunit(event, gamedata, classmap, option, army):
	##################
	# Fonction pour entamer une séquence de déplacement d'unité
	##################
	# On recup les coord canvas
	posfinalx = classmap.mapcanv.canvasx(event.x)
	posfinaly = classmap.mapcanv.canvasy(event.y)
	# On les transforme en coord map
	coordmap = moveview.coordcanvastomap(gamedata, classmap, option, coord)

	# On calcul les cases par lequel l'armée doit passer
	# Liste dans laquelle on va enregistrer les déplacement nécessaires
	# Algo de Bresenham
	lmovement = brensenham([army.x, army.y], coordmap)

	# Une fois la liste rempli ont éxécute autant que l'on peut
	i = 0
	idtuile = lmovement[i][0]+(option.mapx*lmovement[i][1])
	while army.moveturn - classmap.listmap[idtuile].movementcost >=0:
		while i < len(lmovement):
			moveunit(gamedata, classmap, option, army, lmovement[i])
			i += 1
	# Si la liste n'est pas vide on ajoute dans la liste des séquence à appliquer


def moveunit(gamedata, classmap, option, army, coord):
	##################
	# Fonction pour déplacer une unité à l'emplacement indiqué
	##################

	# On calcul l'id de la tuile
	idtuile = coord[0]+(option.mapx*coord[1])

	# On calcul les nouvelles coord
	x = coord[0] - army.x
	y = coord[1] - army.y

	# On déplace l'objet
	classmap.mapcanv.move(army.idtcanvas, x, y)

	# On change les coord de l'armée
	army.x += x
	army.y += y


	# On réduit la capacité de mouvement du tour
	army.moveturn -= gamedata.listmap[idtuile].movementcost



def brensenham(coord0, coord1):
	##################
	# Fonction pour calculer déplacement cases par cases
	# On utilise Brensenham
	# On ne veut pas de diagonal !!!
	# Si on veut réintéger diagonal 
	##################

	lcase = []

	x = 0
	y = 0
	# On calcul la distance à parcourir
	dx = coord1[0] - coord0[0]
	dy = coord1[1] - coord0[1]

	e = 0

	# On teste dans quel octant se trouve l'arrivé
	# Si dans l'octant haut droite
	if (dx>=0) and (dy>=0):
		if dy > dx:
			e = dy
			while(y != dy):
				# déplacement [1, 1]
				if (e-dx) < 0:
					x += 1
				else:
					y += 1
				lcase += [coord0[0] + x, coord0[1] + y]
		else:
			e = dx
			while(x != dx):
				# déplacement [1, 1]
				if (e-dy) < 0:
					y += 1
				else:
					x += 1
				lcase += [coord0[0] + x, coord0[1] + y]
	# Si dans l'octant bas droite
	elif (dx >=0) and (dy <0):
		if -dy > dx:
			e = dy
			while(y != dy):
				# déplacement [1, -1]
				if (e-dx) <0:
					x += 1
				else:
					y -= 1
				lcase += [coord0[0] + x, coord0[1] + y]
		else:
			e = dx
			while(x != dx):
				# déplacement [1, -1]
				if (e - dy)<0:
					y -= 1
				else:
					x += 1
				lcase += [coord0[0] + x, coord0[1] + y]

	# Si dans l'octant haut gauche
	elif (dx <0) and (dy >= 0):
		if dy > (-dx):
			e = dy
			while(y != dy):
				# déplacement [-1, 1]
				if(e-dx) < 0:
					x -= 1
				else:
					y += 1

				lcase += [coord0[0] + x, coord0[1] + y]
		else:
			e = dx
			while(x != dx):
				# déplacement [-1, 1]
				if (e -dy) <0:
					y += 1
				else:
					x -= 1

				lcase += [coord0[0] + x, coord0[1] + y]
	# Sinon dans l'octant bas gauche
	else:
		if -dy > (-dx):
			e = dy
			while(y != dy):
				# déplacement [-1, -1]
				if (e-dx)<0:
					x -= 1
				else:
					y -= 1
				lcase += [coord0[0] + x, coord0[1] + y]
		else:
			e = dx
			while(x != dx):
				# déplacement [-1, -1]
				if (e-dy) <0:
					y -= 1
				else:
					x -= 1

				lcase += [coord0[0] + x, coord0[1] + y]


	return lcase


def pathfinding():
	##################
	# Fonction pour calculer déplacement d'une unité valable
	# On utilise Brensenham
	##################
	# calcul plusieurs itinéraires possibles
	# On décompose l'itinéraires en plusieurs groupes que l'on utilise

	# On vérifie qu'un itinéraires ne passe pas par une cases interdites

	# compare le cout en déplacement de chaque itinéraires

	# Ressort l'itinéraires avec le cout le plus faibles

	pass
