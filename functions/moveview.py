import functions.data as data

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
	if event.delta <= 0:
		delta = -2
	else:
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
	# SI on veut recup depuis le centre de l'écran
	coordcanv = [event.widget.canvasx(option.widthWindow//2), event.widget.canvasx((option.heightWindow*0.6)//2)]
	centerviewcanvas(gamedata, option, event.widget, coordcanv)
	# On change la taille des tuiles stocker dans les données globaux
	gamedata.newsizetuile(x)
	############################################################

	####################\ 5°) \####################
	#Recalcul des images
	newsize = x
	print("newsize : ", newsize)

	###############################\ !!! À modifier !!! \#############################
	# Trouver un moyen de se débaraser des 4 variables
	# Ne plus utiliser le type de la texture

	###################################################################################
	f = 0
	m = 0
	o = 0
	p = 0
	v = 0
	#Tuile graphique:
	for ele in event.widget.find_withtag("img"):

		type = event.widget.gettags(ele)[1]
		# Version Non-random ou on utilise les texture de bases:
		# Quand la classe des tuile sera implémenter utiliser le nom de la texture
		# Utiliser #gamedata.loadtextureatlas(texture_name, type)
		if type == "forest":
			#Si dans la fonction on n'a pas déjà recalculer la nouvelle image pour le type selectionner
			if f == 0:
				#On recréer l'image
				tk_img = data.loadtexturefromdico(gamedata.dico_file, "conifer_forest_inner.png", type, int(newsize))
				# On change le label associer à la texture dans l'atlas
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])				
				f = 1
			# On recup le label associer à la texture
			label = gamedata.atlas["conifer_forest_inner.png"]
		elif type == "mountains":
			if m == 0:
				tk_img = data.loadtexturefromdico(gamedata.dico_file, "mountains_inner.png", type, int(newsize))
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])	
				m = 1
			label = gamedata.atlas["mountains_inner.png"]
		elif type == "ocean":
			if o == 0:
				tk_img = data.loadtexturefromdico(gamedata.dico_file, "ocean_inner.png", type, int(newsize))
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])						
				o = 1
			label = gamedata.atlas["ocean_inner.png"]
		elif type == "plains":
			if p == 0:
				tk_img = data.loadtexturefromdico(gamedata.dico_file, "plains.png", type, int(newsize))
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])						
				p = 1
			label = gamedata.atlas["plains.png"]
		elif type == "build":
			if v == 0:
				tk_img = data.loadtexturefromdico(gamedata.dico_file, "settlement.png", type, int(newsize))
				gamedata.changelabelAtlas(tk_img[0], tk_img[1])
				v = 1
			label = gamedata.atlas["settlement.png"]

		event.widget.itemconfigure(ele,image = label.image)
	############################################################
	gamedata.log.printinfo(f"taille Atlas: , {len(gamedata.atlas)}")
	############################################################

###########################################################################

def centerviewcanvas(gamedata, option, mapcanv, coordcanv):
	##################
	# Fonction pour centrer la vue sur les coordonnées canvas donnés
	##################
	# Si on appelle la fonction en envoyant seulement l'origine du canvas cela centre la vue sur l'origine
	##################

	# On recup le décalage entre le haut-gauche de la window(pas screen) et le canvas
	movex = mapcanv.canvasx(0)
	movey = mapcanv.canvasy(0)
	gamedata.log.printinfo(f"déplacement de x,y: , {movex}, {movey}")
	# On déplace de movex et movey Pour avoir Wind(0,0) = Canv(0,0)
	mapcanv.move("tuile", +movex, +movey)


	# On calcule les coordonnées Windows nécessaires pour placer au centre de la window les coords Canvas Voulu
	# On se place en coord[0], coord[1]
	# On veut se placer au centre
	# On calcul donc le centre de la window du canvas
	# x = (1200/20)/2 = 30
	# y = ((1200/1.6)/20)//2 = 18
	# On ajoute les coord
	#  movex = coorcanva[0] - tuilesize*30, movey = coorcanva[0] - tuilesize*18

	movex = coordcanv[0] - ((option.widthWindow/gamedata.tuilesize)//2) * gamedata.tuilesize
	movey = coordcanv[1] - (((option.heightWindow*0.6)/gamedata.tuilesize)//2) * gamedata.tuilesize
	gamedata.log.printinfo(f"déplacement de x,y: , {movex}, {movey}")
	mapcanv.move("tuile", -movex, -movey)

######################### Fonction Coord ############################

def canvasgooriginewindow(classmap):
	##################
	# Fonction pour faire déplacer le canvas vers l'origine de la fenêtre
	##################
	# On cherche la différence entre la window et la canvas
	coord = [classmap.mapcanv.canvasx(0), classmap.mapcanv.canvasy(0)]

	# On indique ou vont aller
	classmap.mapcanv.scan_mark(0,0)
	# On drague la différence
	classmap.mapcanv.scan_dragto(int(coord[0]), int(coord[1]), gain = 1)

###########################################################################

#################################### Fonction Calcul de coord ####################################


def coordcanvastomap(option, tuilesize, coord, mapcanv):
	##################
	# Fonction pour traduire les coordonnées du canvas en coordonnées de la carte
	##################
	xorigine = mapcanv.canvasx(0)
	yorigine = mapcanv.canvasy(0)
	gamedata.log.printinfo(f"xorigine: , {xorigine}")
	gamedata.log.printinfo(f"yorigine: , {yorigine}")
	gamedata.log.printinfo(f"coord: , {coord}")

	xmap = (((coord[0] + xorigine) - tuilesize/2)%tuilesize)
	ymap = (((coord[1] + yorigine) - tuilesize/2)%tuilesize)


	return [xmap, ymap]

def coordmaptocanvas(gamedata, classmap, option, coord):
	##################
	# Fonction pour traduire les coordonnées map en coordonnées du canvas √
	##################

	gamedata.log.printinfo(f"Pour coord map: , {coord[0]}, {coord[1]}")

	ts = gamedata.tuilesize

	# calcul de base
	xcanvas = (coord[0]*ts)+(ts/2)
	ycanvas = (coord[1]*ts)+(ts/2)
	gamedata.log.printinfo(f"On a coordcanv sans décalage origine: , {xcanvas}, {ycanvas}")
	# On prend en compte le point d'origine du canvas qui peut être actuellement déplacer à une valeur != 0
	gamedata.log.printinfo(f"Point d'origine, {classmap.mapcanv.canvasx(0)}, {classmap.mapcanv.canvasy(0)}")
	xcanvas = xcanvas - classmap.mapcanv.canvasx(0)
	ycanvas = ycanvas - classmap.mapcanv.canvasy(0)
	gamedata.log.printinfo(f"On a coordcanv avec décalage origine: , {xcanvas}, {ycanvas}")

	return [xcanvas, ycanvas]

##########################################################################################
