import tkinter

import functions.log as log
import functions.data as data
import functions.asset as asset
import functions.common as common
import functions.moveview as moveview
import functions.interfacemenu as interfacemenu
import functions.interfacegame as interfacegame

#########################
# Fichier qui vient contenir les fonctions liées à l'affichage
#########################

def printvillage(gamedata, classmap, option, frame):
	##################
	# Fonction pour afficher les villages ainsi que leur noms à la création
	##################

	ts = gamedata.tuilesize
	for ele in classmap.lvillages:
		asset.atlas.loadtextureatlas(asset.dico_file, ts, "settlement.png", "build")
		#On recup la position en x et y 
		posx = classmap.listmap[ele].x
		posy = classmap.listmap[ele].y
		idtuile = posx + (classmap.mapx*posy)
		# On affiche le village
		classmap.mapcanv.create_image((posx*ts)+(ts/2), (posy*ts)+(ts/2), tags = ["village","build","tuile","img", idtuile], image = asset.atlas.dico["settlement.png"].image)

		# On affiche en dessous le nom du village
		classmap.mapcanv.create_text((posx*ts)+(ts/2), (posy*ts), text = classmap.listmap[ele].village.name,tags = ["label","village","tuile", idtuile], activefill = "Black")


	# On ajoute lie au tag village la fonction pour ouvrir l'interface des villages
	classmap.mapcanv.tag_bind("village","<Button-1>", lambda event, opt = option, gd = gamedata, cm = classmap: interfacegame.villageinterface(event, gd, cm, opt))


def printvillageunit(gamedata, classmap, option, coordmap):
	##################
	# Fonction pour afficher un unique village avec les coord_map envoyer
	##################	

	posx = coordmap[0]
	posy = coordmap[1]
	idtuile = posx + (classmap.mapx*posy)

	ts = gamedata.tuilesize
	# On vérifie que la texture est en mémoire
	asset.atlas.loadtextureatlas(asset.dico_file, ts, "settlement.png", "build")

	# On affiche le village
	classmap.mapcanv.create_image((posx*ts)+(ts/2), (posy*ts)+(ts/2), tags = ["village","build","tuile","img", idtuile], image = asset.atlas.dico["settlement.png"].image)

	# On affiche en dessous le nom du village
	classmap.mapcanv.create_text((posx*ts)+(ts/2), (posy*ts), text = classmap.listmap[idtuile].village.name,tags = ["label","village","tuile", idtuile], activefill = "Black")

	# On ajoute lie au village la fonction pour ouvrir l'interface
	classmap.mapcanv.tag_bind("village","<Button-1>", lambda event, opt = option, gd = gamedata, cm = classmap: interfacegame.villageinterface(event, gd, cm, opt))

def delvillageunit(mapcanv, idvillage):
	########
	# Fonction pour supprimer l'affichage d'un village
	########
	# On récup une liste de tout les objets du canvas qui ont le tag village, cela prend en compte les village et leur tags
	# On à 2 objet à détruire
	lcanvvillage = mapcanv.find_withtag("village")
	#print(lcanvvillage)
	#print(idvillage)
	i = 0
	for objet in lcanvvillage:
		if i == 2:
			return
		ltag = mapcanv.gettags(objet)
		print(ltag)
		# Si on à trouvé l'image village
		# Si Objet Village
		if len(ltag) > 4:
			if ((int(ltag[4]) == idvillage)):
				log.log.printinfo(f"Objet Village trouvé pour {idvillage}")
				mapcanv.delete(objet)
				i += 1
		# Si Objet Label
		else:
			# Si on à trouvé le label village
			if (int(ltag[3]) == idvillage):
				log.log.printinfo(f"Objet Label trouvé pour {idvillage}")
				mapcanv.delete(objet)
				i += 1

def bordervillage(gamedata, classmap, option):
	##################
	# Fonction pour afficher les bordures des villages
	##################
	# 1er Version affiche un Carrer Tkinter avec:
	# - En Blanc le Neutre
	# - En Rouge l'ennemie
	# - En Vert l'allier
	# - En Bleu Le Territoire du Joueur


	classmap.mapcanv.delete("border")
	player = gamedata.list_lord[gamedata.playerid]

	# On se balade dans la liste des villages
	for idvillage in classmap.lvillages:
		# On Vérifier à qui appartient le village est décide de la couleur à afficher en Conséquence
		village = classmap.listmap[idvillage].village
		lordname = 0
		if village.lord != 0:
			lordname = village.lord.lordname
			if village.lord == player:
				color = "blue"
			elif village.lord in player.vassal:
				color = "green"
			elif village.lord in player.war:
				color = "red"
			else:
				color = village.lord.color
		else:
			color = "white"
		# On calcule la Bordure
		border = village.border
		# On s'assure de ne pas donner des coordonnées hors de la map
		# Pour X
		if village.x-border < 0 :
			posx = 0
		else:
			posx = village.x - border

		if (village.x + border) >= classmap.mapx:
			posx2 = classmap.mapx-1
		else:
			posx2 = village.x + border + 1 

		# Pour Y
		if village.y-border < 0 :
			posy = 0
		else:
			posy = village.y - border

		if (village.y + border) >= classmap.mapy:
			posy2 = classmap.mapy-1
		else:
			posy2 = village.y + border + 1 



		# On convertit les Coordonnées Map en Coordonnées Canvas
		coord0 = common.coordmaptocanvas(gamedata, classmap, option, [posx, posy], False)
		coord1 = common.coordmaptocanvas(gamedata, classmap, option, [posx2, posy2], False)
		classmap.mapcanv.create_rectangle( coord0[0], coord0[1], coord1[0], coord1[1], tags = ["tuile", "border", village.name], outline = color)

def bordervillageunit(gamedata, classmap, option, village):
	##################
	# Fonction pour afficher les bordures d'un unique village
	##################	

	player = gamedata.list_lord[gamedata.playerid]

	# On calcule la couleur
	if village.lord != 0:
		if village.lord == player:
			color = "blue"
		elif village.lord in player.vassal:
			color = "green"
		elif village.lord in player.war:
			color = "red"
		else:
			color = village.lord.color
	else:
		color = "white"

	# On calcule les coordonnées de la Bordure

	# On calcule la Bordure
	border = village.border
	# On s'assure de ne pas donner des coordonnées hors de la map
	# Pour X
	if village.x-border < 0 :
		posx = 0
	else:
		posx = village.x - border

	if (village.x + border) >= classmap.mapx:
		posx2 = classmap.mapx-1
	else:
		posx2 = village.x + border + 1 

	# Pour Y
	if village.y-border < 0 :
		posy = 0
	else:
		posy = village.y - border

	if (village.y + border) >= classmap.mapy:
		posy2 = classmap.mapy-1
	else:
		posy2 = village.y + border + 1 

	# On convertit les Coordonnées Map en Coordonnées Canvas
	coord0 = common.coordmaptocanvas(gamedata, classmap, option, [posx, posy], False)
	coord1 = common.coordmaptocanvas(gamedata, classmap, option, [posx2, posy2], False)
	# Si le village possède déjà une Bordure on Supprime l'ancienne
	delborder(classmap, village)
	# MonkeyPatch
	classmap.mapcanv.create_rectangle( coord0[0], coord0[1], coord1[0], coord1[1], tags = ["tuile", "border", village.name], outline = color)

def delborder(classmap, village):
	##################
	# Fonction pour détruire la bordure d'un unique village
	##################
	lb = classmap.mapcanv.find_withtag("border")
	for ele in lb:
		if classmap.mapcanv.gettags(ele)[2] == village.name:
			log.log.printinfo(f"Bordure Trouvé Pour le village{village.name} On supprime l'ancienne")
			classmap.mapcanv.delete(ele)
			return

def printarmy(gamedata, classmap, option, army, lord):
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
	texture_name = asset.randomtexturefromdico(asset.dico_file, unit)
	# On assigne dans l'armée la texture
	army.texture = texture_name
	# On charge dans l'atlas la texture préparer avec une taille qui correspond à la moitier d'une tuile
	asset.atlas.loadtextureatlassize(asset.dico_file, texture_name, unit, ts/2)
	# On créer à l'emplacement voulu
	army.idCanv = classmap.mapcanv.create_image((posx*ts)+(ts/2), (posy*ts)+(ts/2), tags = ["army","tuile","img", army.name], image = asset.atlas.dico[texture_name].image)
	# On créer la Bordure
	classmap.mapcanv.create_rectangle((posx*ts)+(ts//4), (posy*ts)+(ts//4), (posx*ts)+ts-(ts//4), (posy*ts)+ts-(ts//4), tags = ["borderArmy", "tuile",army.name], outline = lord.color, width = 2)

	# On bind l'interface
	classmap.mapcanv.tag_bind("army", "<Button-1>", lambda event: interfacegame.armyinterface(event, gamedata, classmap, option))
	# On bind le Tootipe
	interfacemenu.tooltipcanvas(classmap.mapcanv, army.idCanv,f"{army.name}\nPuissance:{army.power}", [])

def printupdatearmy(gamedata, classmap, army):
	##################
	# Fonction pour Update l'affichage d'une armée
	##################
	ts = gamedata.tuilesize

	if army.knight != 0:
		unit = "knight"
	else:
		unit = "soldier"
	# On recup la texture
	texture_name = data.randomtexturefromdico(gamedata.dico_file, unit)
	# On la stocke dans la class
	army.texture = texture_name
	# On la charge dans l'atlas
	asset.atlas.loadtextureatlassize(asset.dico_file, texture_name, unit, ts/2)
	# On recup le Canvas Id de l'armée
	armyId = army.idCanv
	# On update l'image
	classmap.mapcanv.itemconfigure(armyId, image = asset.atlas.dico[texture_name].image)

def sequencemoveunit(gamedata, classmap, option, army, coordObjectif):
	##################
	# Fonction pour entamer une séquence de déplacement d'unité vers les CoordMapViser
	##################

	# On calcul les cases par lequel l'armée doit passer
	# Liste dans laquelle on va enregistrer les déplacement nécessaires
	# Algo de Bresenham
	log.log.printinfo("On calcul les déplacement nécessaire")
	log.log.printinfo(f"coord0, coord1: {army.x, army.y}, {coordObjectif}")
	# Brensenham
	#lmovement = brensenham([army.x, army.y], coordObjectif)
	# Pathfinding
	lmovement = pathfinding(gamedata, classmap, option, [army.x, army.y], coordObjectif, 45)
	log.log.printinfo(f"lmovement: {lmovement}")

	idtuile0 = common.coordmaptoidtuile(classmap, [army.x, army.y])
	# Une fois la liste rempli ont éxécute autant que l'on peut
	i = 0
	idtuile = lmovement[i][0]+(classmap.mapx*lmovement[i][1])
	while (army.moveturn - classmap.listmap[idtuile].movementcost >=0) and (i < len(lmovement)):
		idtuile = lmovement[i][0]+(classmap.mapx*lmovement[i][1])
		moveunit(gamedata, classmap, option, army, lmovement[i])
		i += 1
	classmap.listmap[idtuile0].removearmyinplace()
	classmap.listmap[idtuile].setarmyinplace(army)

	# Si la liste n'est pas vide on ajoute dans la file des actions la Sequence de movement 
	if i != len(lmovement):
		log.log.printinfo(f"Il reste des mouvement à effectuer mais il y n'a plus de PM")
		log.log.printinfo(f"On ajoute dans la file des actions")
		gamedata.addactionfile(["sequencemoveunit", gamedata, classmap, option, army, coordObjectif], 1)

def moveunit(gamedata, classmap, option, army, coord):
	##################
	# Fonction pour déplacer une unité à l'emplacement indiqué
	##################

	# On calcul l'id de la tuile
	idtuile = common.coordmaptoidtuile(classmap, coord)

	ts = gamedata.tuilesize

	# On calcul les nouvelles coord
	x = coord[0] - army.x
	y = coord[1] - army.y
	coord = common.coordmaptocanvas(gamedata, classmap, option, [x, y], True)
	# On récupère la bordure
	border = getborderarmy(classmap.mapcanv, army.name)
	log.log.printinfo(f"Unité déplacement vers coord Canvas : {coord}")
	log.log.printinfo(f"On déplace l'armée {army.name} avec l'id Canvas: {army.idCanv} de: {x}x,{y}y ")
	# On déplace l'objet Armé
	classmap.mapcanv.move(army.idCanv, coord[0]- (ts/2), coord[1]-(ts/2))
	print(border)
	# On déplace sa Bordure
	classmap.mapcanv.move(border, coord[0]- (ts/2), coord[1]-(ts/2))

	# On change les coord stocker dans l'armée
	army.x += x
	army.y += y

	# On réduit la capacité de mouvement du tour
	army.moveturn -= classmap.listmap[idtuile].movementcost

def getborderarmy(canvas, armyname):
	#####
	# FOnction pour récupérer la Bordure d'une armée
	####
	# On récupère la liste des Objet
	lobject = canvas.find_withtag("borderArmy")
	# On se balade dedans
	for ele in lobject:
		# on récupère la liste des tags
		ltag = canvas.gettags(ele)
		if ltag[2] == armyname:
			return ele
	return 0

def brensenham(coord0, coord1):
	##################
	# Fonction pour calculer déplacement cases par cases
	# On utilise Brensenham
	# On ne veut pas de diagonal !!!
	##################

	lcase = []

	x = 0
	y = 0
	x2 = coord1[0] - coord0[0]
	y2 = coord1[1] - coord0[1]
	# On calcul la distance à parcourir
	dx = x2
	dy = y2

	e = 0

	# On teste dans quel octant se trouve l'arrivé
	# Si dans l'octant haut droite √
	if (dx>=0) and (dy>=0):
		if dy > dx:
			e = dy
			dy = dy*2
			dx = dx*2
			while(y != y2):
				# déplacement [1, 1]
				e -= dx
				y += 1
				lcase += [[coord0[0] + x, coord0[1] + y]]
				if e < 0:
					x += 1
					e += dy
					lcase += [[coord0[0] + x, coord0[1] + y]]
		else:
			e = dx
			dx = dx*2
			dy = dy*2
			while(x != x2):
				# déplacement [1, 1]
				e -= dy
				x +=1
				lcase += [[coord0[0] + x, coord0[1] + y]]
				if e < 0:
					y += 1
					e += dx
					lcase += [[coord0[0] + x, coord0[1] + y]]
	# Si dans l'octant bas droite √
	elif (dx >=0) and (dy <0):
		if -dy > dx:
			e = dy
			dx = dx*2
			dy = dy*2
			while(y != y2):
				# déplacement [1, -1]
				e += dx
				y -= 1
				lcase += [[coord0[0] + x, coord0[1] + y]]
				if e > 0:
					x += 1
					e += dy
					lcase += [[coord0[0] + x, coord0[1] + y]]
		else:
			e = dx
			dx = dx*2
			dy = dy*2
			while(x != x2):
				# déplacement [1, -1]
				e += dy
				x += 1
				lcase += [[coord0[0] + x, coord0[1] + y]]
				if e <0:
					y -= 1
					e += dx
					lcase += [[coord0[0] + x, coord0[1] + y]]

	# Si dans l'octant haut gauche √
	elif (dx <0) and (dy >= 0):
		if dy > (-dx):
			e = dy
			dx = dx*2
			dy = dy*2
			while(y != y2):
				# déplacement [-1, 1]
				e += dx
				y += 1
				lcase += [[coord0[0] + x, coord0[1] + y]]
				if e < 0:
					x -= 1
					e += dy
					lcase += [[coord0[0] + x, coord0[1] + y]]
		else:
			e = dx
			dx = dx*2
			dy = dy*2
			while(x != x2):
				# déplacement [-1, 1]
				e += dy
				x -= 1
				lcase += [[coord0[0] + x, coord0[1] + y]]
				if e >= 0:
					y += 1
					e += dx 
					lcase += [[coord0[0] + x, coord0[1] + y]]
	# Sinon dans l'octant bas gauche √
	else:
		if -dy > (-dx):
			e = dy
			dx = dx*2
			dy = dy*2
			while(y != y2):
				# déplacement [-1, -1]
				e -= dx
				y -= 1
				lcase += [[coord0[0] + x, coord0[1] + y]]
				if e >= 0:
					x -= 1
					e += dy
					lcase += [[coord0[0] + x, coord0[1] + y]]
		else:
			e = dx
			dx = dx*2
			dy = dy*2
			while(x != x2):
				# déplacement [-1, -1]
				e -= dy
				x -= 1
				lcase += [[coord0[0] + x, coord0[1] + y]]
				if e >= 0:
					y -= 1
					e += dx
					lcase += [[coord0[0] + x, coord0[1] + y]]


	lcase += [[coord1[0], coord1[1]]]
	return lcase


def pathfinding(gamedata, classmap, option, coord0, coord1, degr):
	##################
	# Fonction pour calculer déplacement d'une unité valable, retourne l'itinéraire la plus efficace
	# Utilise des Coordonnées Map
	# On utilise Brensenham
	# Que pour 3 snapshot (3 itinéraires)
	##################
	# 1°) On prend un le point C centre de la droite D Qui va de C0 à C1
	# 2°) On calcul le point C1, soit C avec une rotation de pi/6 (30°)
	#		On Calcul le point C2, soit C avec une rotaion de -pi/6 (30°)
	#
	# Après avoir calculer la formule matricielle suivante:
	# C1 = T0->c0.R30°.Tc0->0.C
	# On obtient l'équation suivante:
	# C1x = ((dx/2 - C0x) * cos(pi/6)) + ((dy/2 - C0y) * (-sin(pi/6))) + C0x
	# C1y = ((dx/2 - C0x) * sin(pi/6)) + ((dy/2 - C0y) * (cos(pi/6))) + C0y
	# On convertit cos(pi/6) = √3/2 +-= 0.86 et sin(pi/6) = 1/2 = 0.5
	# C1x = ((dx//2 - C0x) * 0.86) + ((dy//2 - C0y) * -1/2) + C0x
	# C1y = ((dx//2 - C0x) * 1/2)  + ((dy//2 - C0y) * 0.86) + C0y
	# Pour obtenir la rotation de C2 qui négatif on change le signe de sin √
	##################
	# Pour l'instant on ne prend en compte que 2 degr
	# Pour degré = 30°:
	# cos(30°) = √3/2 +-= 0.86
	# sin(3°) = 1/2 = 0.5

	# Pour degré = 45°:
	# cos(45°) = √2/2 +-= 0.707
	# sin(45°) = √2/2 +-= 0.707

	if degr == 30:
		cosdegr = 0.86
		sindegr = 1/2
	elif degr == 45:
		cosdegr = 0.707
		sindegr = 0.707
	else:
		log.log.printerror("degrer non valide (30 ou 45)")
		return

	# On calcul la distance en C0 et C1
	dx = coord1[0] - coord0[0]
	dy = coord1[1] - coord0[1]
	log.log.printinfo(f"dx, dy: ,{dx}, {dy}")

	# Point Central 
	C = [coord0[0] + dx//2, coord0[1] + dy//2]


	# Point Central haut
	C1 = [0,0]
	# C1x:
	C1[0] = int(((C[0] - coord0[0])*cosdegr) + ((C[1] - coord0[1])*(-sindegr)) + coord0[0])
	# C1y:
	C1[1] = int(((C[0] - coord0[0])*(sindegr)) + ((C[1] - coord0[1])* cosdegr) + coord0[1])
	# Point Central bas 
	C2 = [0,0]
	# C2x:
	C2[0] = int(((C[0] - coord0[0])*cosdegr) + ((C[1] - coord0[1])*(sindegr)) + coord0[0])
	# C2y:
	C2[1] = int(((C[0] - coord0[0])*(-sindegr)) + ((C[1] - coord0[1])*cosdegr) + coord0[1])

	#log.log.printinfo(f"coord0: ,{coord0}")
	#log.log.printinfo(f"coord1: ,{coord1}")

	#log.log.printinfo(f"C: ,{C}")
	#log.log.printinfo(f"C1: ,{C1}")
	#log.log.printinfo(f"C2: ,{C2}")

	# On calcul les 3 itinéraires
	iti1 = brensenham(coord0, C)
	iti2 = brensenham(coord0, C1)
	iti3 = brensenham(coord0, C2)

	iti1 += brensenham(C, coord1)
	iti2 += brensenham(C1, coord1)
	iti3 += brensenham(C2, coord1)

	lsnapshot = [iti1, iti2, iti3]
	#log.log.printinfo(f"liste des itinéraires: {lsnapshot}")
	lcostiti = []

	# On vérifie qu'un itinéraires ne passe pas par une cases interdites

	# compare le cout en déplacement de chaque itinéraires
	#log.log.printinfo(f"Calcul Cout itinéraire")
	for itinéraire in lsnapshot:
		cost = costsequ(gamedata, classmap, option, itinéraire)
		if cost != False:
			lcostiti += [cost]


	i = 0
	small = 0
	# On Ressort l'itinéraires avec le cout le plus faibles
	while i < len(lcostiti):
		if lcostiti[i] < lcostiti[small]:
			small = i
		i += 1

	log.log.printinfo(f"itinéraires le moins couteux avec {lcostiti[small]}PM : {lsnapshot[small]}")

	return lsnapshot[small]

def costsequ(gamedata, classmap, option, itinéraire):
	######
	# Fonction qui retourne le cout en mouvement d'un itinéraire
	# Retoune un False si l'itinéraire est invalide
	######
	cost = 0
	for cases in itinéraire:
		# Si la position x ou y de la cases est supérieur ou inférieur à la longueur de la carte alors invalide
		if (cases[0] >= classmap.mapx) or (cases[1] >= classmap.mapy):
			return False
		elif(cases[0] < 0) or (cases[1] < 0):
			return False
		else:
			# Sinon on calcule le cout de la case
			idtuile = common.coordmaptoidtuile(classmap, cases)
			cost += classmap.listmap[idtuile].movementcost

	return cost

def armymoveoneturn(gamedata, classmap, option, itinéraire, army):
	#####
	# Fonction qui retourne True si l'armée peut faire le trajet en 1 tour
	#####
	cost = 0
	for cases in itinéraire:
		idtuile = common.coordmaptoidtuile(classmap, cases)
		cost += classmap.listmap[idtuile].movementcost
		if cost > army.moveturn:
			return False
	return True


def bezier():
	#####
	# Fonction qui gère l'affichage de la courbe de Bézier
	#####
	pass


