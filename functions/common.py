
#################################### Fonction Calcul de coord ####################################

def coordcanvastomap(gamedata, classmap, option, coord):
	##################
	# Fonction pour traduire les coordonnées du canvas en coordonnées de la carte √
	##################
	# Le problème est que l'on à forcément un décalage qui se créer pour des valeur importante lors de la division
	# Ex:
	# (389-(20//2))/20 = 18.95 = 18 hors on veut 19
	# Comment calculer efficacement ?
	ts = gamedata.tuilesize

	xmap = ((coord[0])//ts)
	ymap = ((coord[1])//ts)

	return [xmap, ymap]

def coordmaptocanvas(gamedata, classmap, option, coord, decalage:bool):
	##################
	# Fonction pour traduire les coordonnées map en coordonnées du canvas centrer ou non √
	##################

	#gamedata.log.printinfo(f"Pour coord map: {coord[0]}, {coord[1]}")

	ts = gamedata.tuilesize

	if decalage == True:
		# calcul de base
		xcanvas = (coord[0]*ts)+(ts/2)
		ycanvas = (coord[1]*ts)+(ts/2)
	else:
		xcanvas = (coord[0]*ts)
		ycanvas = (coord[1]*ts)		
	#gamedata.log.printinfo(f"coordcanv: {xcanvas}, {ycanvas}")

	return [xcanvas, ycanvas]

def coordmaptoidtuile(option, coord):
	##################
	# Fonction pour traduire les coordonnées map en idtuile √
	##################

	idtuile = coord[0] + (option.mapx*coord[1])
	return idtuile

##########################################################################################

def distance(object1, object2):
	###############
	# Fonction qui retourne la distance entre 2 objets
	###############
	print("pos Objet1:", object1.x, object1.y)
	print("pos Objet2:", object2.x, object2.y)
	distx = object1.x - object2.x
	disty = object1.y - object2.y
	if distx < 0:
		distx = distx*-1
	if disty < 0:
		disty = disty*-1
	dist = distx + disty
	print("distance: ", dist)
	return dist



