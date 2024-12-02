import functions.data as data

import functions.common as common

#########################
# Fichier qui vient contenir les fonctions liées aux déplacement du canvas
#########################



########################################\ Fonction Déplacement Vue \##################################################

#################### 
# Ensemble de Fonction pour déplacer la vue en:
# Maintenant le click gauche de la souris √
# En placant le souris sur une extrémité de la caméra
# En appyant sur les touches fléchés √
####################
#
# Bon bon bon, alors scan_dragto déplace le canvas dans la fenêtre de la X, Y différent stocker dans 
# scan_mark
# !!!! Il ne faut pas utiliser les coordonnées canvas mais de la fenêtre !!!!
#
####################

def moveviewxy(event, deltax, deltay, gamedata, classmap, option):
	####################
	# Fonction pour déplacer la vue en:
	# En appyant sur les touches fléchés 
	####################
	mult = 100

	gamedata.log.printinfo("move map arrow")

	################ Déplacement de la vue ################
	# On recup le point central de la fenêtre
	x = int((option.widthWindow)//2)
	y = int((option.heightWindow*0.6)//2)

	event.widget.scan_mark(x, y)

	movex = x + (mult * deltax)
	movey = y + (mult * deltay)

	classmap.mapcanv.scan_dragto(movex, movey, gain = 1)
	gamedata.log.printinfo(f"coords (0,0) : {classmap.mapcanv.coords(classmap.listmap[0].canvastuiles)}")
	#######################################################

def startmoveviewmouse(event):
	####################
	# Fonction pour déplacer la vue en:
	# Maintenant le click droit de la souris
	# Partie 1
	# Utiliser .scan_mark(x, y)
	#
	####################
	event.widget.scan_mark(event.x, event.y)

def moveviewmouse(event):
	####################
	# Fonction pour déplacer la vue en:
	# Maintenant le click droit de la souris
	# Partie 2
	# Utiliser .scan_dragto(x, y)
	# !!!! A cause de l'utilisation de Move est très couteux !!!!
	####################
	event.widget.scan_dragto(event.x, event.y, gain = 1)


def moveviewz(event, gamedata, classmap, option):
	####################
	# Fonction pour zoomer/dézoomer
	# - En utilisant la molette de la souris
	# - Depuis le centre de la window
	# - On prend pour valeur min de la taille d'une tuile 5
	#
	# On zoome quand on multiplie par delta
	# On dezoome quand on divise par delta
	#
	#	--- * 2 = ------ 	== Zoom car on agrandit
	#
	# 	--- / 3 = - 		== DeZoom car on réduit
	####################
	# 1°) On calcul les coord canvas de la souris
	# 2°) On normalise le delta pour prendre en compte les différentes plateformes
	# 3°) On recup la taille d'une tuile
	# 4°) On scale 
	# 5°) On change les texture des tuiles pour la nouvelles tuiles
	#####################

	idorigine = 0
	while event.widget.type(idorigine) != "image":
		idorigine += 1

	gamedata.log.printinfo(f"coord de la tuile 0,0 Canvas: , {classmap.mapcanv.coords(classmap.listmap[0].canvastuiles)}")

	####################\ 1°) \####################

	mousex = int(event.widget.canvasx(event.x))
	mousey = int(event.widget.canvasy(event.y))

	# On recup les coord-canvas de la tuile
	idtuile = event.widget.find_closest(mousex, mousey)

	gamedata.log.printinfo(f"coordonnées window de la souris: , {mousex}, {mousey}")
	############################################################

	####################\ 2°) \####################
	#Pour éviter les différence entre windows et Mac ont normalise delta
	#Doit prendre en compte linux -_-
	gamedata.log.printinfo(f"{event.delta}")


	if (event.delta <= 0) or (event.num == 5):
		delta = -2
	if (event.delta > 0) or (event.num == 4):
		delta = 2
	############################################################


	####################\ 3°) \####################
	# On recup la taille d'une tuile
	x = gamedata.tuilesize
	#print("x, event.delta, delta: ",x, event.delta, delta)
	############################################################

	# Doit trouver les valeurs parfaite max et min
	# Zoom = max = x = 320
	# DeZoom = min = x = 5
	# À l'avenir changer la valeur minimum par une valeur calculer a partir de la taille de la carte

	####################\ 4°) \####################
	#Zoom
	canvasgooriginewindow(classmap)
	if (x<320) and (delta == 2):
		print("Zoom")
		event.widget.scale("tuile", 0, 0, delta, delta)
		x = x*delta
	#Dezoom
	elif(x>5) and (delta == -2):
		print("DeZoom")
		#On rend positive le delta sinon il inverse le sens de la carte
		event.widget.scale("tuile", 0, 0, -1/(delta), -1/(delta))
		x = x*(-1/(delta))
	#On recup les nouvelles coord du pointeur de la souris
	coordcanv = event.widget.coords(idtuile)
	centerviewcanvas(gamedata, classmap, option, coordcanv)
	# On change la taille des tuiles stocker dans les données globaux
	gamedata.newsizetuile(x)
	###################################################################

	####################\ 5°) \#########################################
	# Recalcul des images
	# On Update l'atlas pour prendre en compte la nouvelle taille des textures
	gamedata.resizeatlas(x)
	#Tuile graphique:
	for imgid in event.widget.find_withtag("img"):

		# Si c'est un village on assigne directiement la variable texture
		if "village" in event.widget.gettags(imgid):
			texture = "settlement.png"
		# Si c'est une armée
		elif "army" in event.widget.gettags(imgid):
			# On recup les coordonnées canvas
			coord = classmap.mapcanv.coords(imgid)
			# On transforme en coordonnées Map
			coord = common.coordcanvastomap(gamedata, classmap, option, coord)
			# On cherche l'objet armée
			# On se balade parmi les Seigneurs
			for lord in range(gamedata.Nb_lord):
				army = gamedata.coordtoarmy(lord, coord)
				# Si la fonction n'a pas renvoyé False on a trouvé l'armée
				if army != False:
					texture = army.texture
		else:
			# Sinon On vient recup la texture stocker dans la Classtuile
			texture = classmap.listmap[imgid-1].texture_name

		# On change la texture lié
		event.widget.itemconfigure(imgid, image = gamedata.atlas[texture].image)
	############################################################
	gamedata.log.printinfo(f"taille Atlas: {len(gamedata.atlas)}")
	############################################################

def moveviewzcenter(gamedata, classmap, option, delta):
	####################
	# Version simplifié pour zoom/dezoom au centre de la carte
	#####################

	####################\ 1°) \####################
	# On recup la taille d'une tuile et définit le delta
	x = gamedata.tuilesize
	if delta < 0:
		delta = -2
	else:
		delta = 2
	############################################################

	####################\ 2°) \####################
	# DeZoom
	canvasgooriginewindow(classmap)
	if delta < 0:
		classmap.mapcanv.scale("tuile", 0, 0, -1/(delta), -1/(delta))
		x = x*(-1/(delta))
	else:
		classmap.mapcanv.scale("tuile", 0, 0, (delta), (delta))
		x = x*delta
	print(x)
	# Place au centre de l'écran
	coordcanv = [classmap.mapcanv.canvasx(option.widthWindow//2), classmap.mapcanv.canvasx((option.heightWindow*0.6)//2)]
	centerviewcanvas(gamedata, classmap, option, coordcanv)
	# On change la taille des tuiles stocker dans les données globaux
	gamedata.newsizetuile(x)
	###################################################################

	####################\ 5°) \#########################################
	# Recalcul des images
	# On Update l'atlas pour prendre en compte la nouvelle taille des textures
	gamedata.resizeatlas(x)
	#Tuile graphique:
	for imgid in classmap.mapcanv.find_withtag("img"):
		# Si c'est un village on assigne directiement la variable texture
		if "village" in classmap.mapcanv.gettags(imgid):
			texture = "settlement.png"
		# Si c'est une armée
		elif "army" in classmap.mapcanv.gettags(imgid):
			# On recup les coordonnées canvas
			coord = classmap.mapcanv.coords(imgid)
			# On transforme en coordonnées Map
			coord = common.coordcanvastomap(gamedata, classmap, option, coord)
			# On cherche l'objet armée
			# On se balade parmi les Seigneurs
			for lord in range(gamedata.Nb_lord):
				army = gamedata.coordtoarmy(lord, coord)
				# Si la fonction n'a pas renvoyé False on a trouvé l'armée
				if army != False:
					texture = army.texture



		else:
			# Sinon On vient recup la texture stocker dans la Classtuile
			texture = classmap.listmap[imgid-1].texture_name


		# On change la texture lié
		classmap.mapcanv.itemconfigure(imgid, image = gamedata.atlas[texture].image)
	############################################################
	gamedata.log.printinfo(f"taille Atlas: {len(gamedata.atlas)}")

###########################################################################

def centerviewcanvas(gamedata, classmap, option, coordcanv):
	##################
	# Fonction pour centrer la vue sur les coordonnées canvas donnés
	##################

	# On se place à l'origine
	canvasgooriginewindow(classmap)

	ts = gamedata.tuilesize


	# On calcule les coordonnées Windows nécessaires pour placer au centre de la window les coords Canvas Voulu
	# On se place en coord[0], coord[1]
	# On veut se placer au centre
	# On calcul donc le centre de la window du canvas
	# x = (1200/20)/2 = 30
	# y = ((1200/1.6)/20)//2 = 18
	# On ajoute les coord
	#  movex = coorcanva[0] - tuilesize*30, movey = coorcanva[0] - tuilesize*18

	movex = coordcanv[0] - ((option.widthWindow/ts)//2) * ts
	movey = coordcanv[1] - (((option.heightWindow*0.6)/ts)//2) * ts
	gamedata.log.printinfo(f"déplacement de x,y: , {movex}, {movey}")

	# On indique ou on veut aller
	classmap.mapcanv.scan_mark(0,0)
	# On drag la différence
	classmap.mapcanv.scan_dragto(-int(movex), -int(movey), gain = 1)
	#classmap.mapcanv.move("tuile", -movex, -movey)

######################### Fonction Coord ############################

def canvasgooriginewindow(classmap):
	##################
	# Fonction pour faire déplacer le canvas vers l'origine de la fenêtre
	##################
	# On cherche la différence entre la window et la canvas
	coord = [classmap.mapcanv.canvasx(0), classmap.mapcanv.canvasy(0)]

	# On indique ou vont aller
	classmap.mapcanv.scan_mark(0,0)
	# On drag la différence
	classmap.mapcanv.scan_dragto(int(coord[0]), int(coord[1]), gain = 1)

###########################################################################
