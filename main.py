import tkinter
import genproc
import random
import data
from time import time

#Doit terminé de faire un Prototype:
# - Ajouter Un moyen de déplacer la vue √
#	--> Doit modifier afin de prendre en compte le non focus sur le widget du canvas
#		--> Doit appliquer le bind des touches à la root
#		--> Doit trouver un moyen de stocker les objets dans une données facilement accesible
#			--> Un dico ?
#			--> Place les bases du stockage de données
#	--> Doit modifier afin d'accèlerer le déplacement avec le maintient de la touche
#	--> Doit modifier afin de pouvoir drag le terrain √
# - Ajouter un moyen de save la carte gen
# - Pas assez d'eau gen, doit trouver un moyen d'améliorer cela √
#	--> Inverser le sens de gen et est réduit la condition pour les extreme
#		Avant: NB <=-0.5 == Blue; -0.5 < NB <= 0 == Yellow; 0<NB <= 0.5 == Green; 0.5< NB == Grey
#		Maintenant: NB <=-0.25 == Grey; -0.25< NB <= 0 == Green; 0< NB <= 0.25 == Yellow; 0.25< NB == Blue
# - Ajouter un moyen de Zoomer/Dézoomer √


# !!! Attention pour une grande carte cela ram !!!
# C'est l'affichage de plein de case qui cause la ram, voir si c'est le cache ou l'affichage

# Fait un teste avec le Moniteur d'activité lancer à coté
# L'utilisation de la ram est plutôt équilibrer, entre 130-160mo
# Quand on déplace la vue sur une zone de la carte remplie le proc est utiliser à 70%

# Trop d'appel à la fonction ? X
# J'ai tester avec une valeur incrémenter à chaque fois que la fonction motion est appelé, l'appel à la fonction est relativement léger
# pour une carte de 250*250 on y fait appel que 16* pour aller d'un bout à l'autre de la map


# Le Garbage Collector emmerde √
# ils suppriment l'image obtenue à la sortie de loadtexture()
# https://github.com/ythy/blog/issues/302

# mapcanv.create_image((x*sizetuile), (y*sizetuile), image = tk_img, tags = "img")
# Créer un décalage avec l'affichage arrière

# Doit adapter le zoom/dezoom aux texture √
# 	--> tester la sélection des tuiles textures
#	--> tester le resize des tuiles textures
#
# Problème:
#	--> Trop de mémoire pris
#	--> Doit refactorer pour utiliser le dico √
#	--> Doit garder les anciennes fonctions afin de pouvoir les réutiliser pour charger une texture particulière √
#	--> Ne connais pas le fonctionnement exacte du label
#		--> Quand je créer une nouveau label du nom de label sachant qu'un label existe déjà, l'ancien label est t'il supprimer ou garder en mémoire ?

# J'ai terminé de refactoriser




#########################
#
#
#
#
#
#
#
#
#
#########################





#########################
def mainscreen(heightWindow, widthWindow, root, pic, mapx, mapy):

	#Création de la fenêtre
	win1 = tkinter.Toplevel(root, height = heightWindow, width= widthWindow)

	#Frame Affichage
	fcanvas = tkinter.Frame(win1)
	fcanvas.pack(expand="True", fill="both")
	createmap(heightWindow, widthWindow, pic, fcanvas, mapx, mapy, 20,dico_file)

	#Frame Boutton
	fbutton = tkinter.Frame(win1)
	fbutton.pack(expand="True", fill="both")
	#Bouton pour quitter
	Button_exit = tkinter.Button(fbutton,command = exit, text = "Quitter")
	Button_exit.pack(side="bottom")
#########################



######################### Gestion de la Carte #######################################################
def createmap(heightWindow, widthWindow, pic, frame, mapx, mapy, sizetuile, dico_file):

	#Si heigthWindow/1.5 le boutton quitter disparait
	mapcanv = tkinter.Canvas(frame,height = ((heightWindow)/1.55), width = ((widthWindow)/1.5))

	# On Créer les Différentes Cases avec le tags tuile pour indiquer et les trouvé plus facilement
	# On ajoute aussi le tags click pour indiquer qu'ils sont clickables
	# On ajoute aussi les tags x et y qui correspond à la casse ou ils est situés
	# ONn ajoute aussi le tag pic[x][y] qui correspond à la valeur de la case gen
	# 2ieme version: ajouter un tag supplémentaire liées aux types
	for x in range(mapx):
		for y in range(mapy):


			# On utilise la valeur de la case pour définir la tuile que l'on va créer
			tl = tuile(pic[x][y])
			mapcanv.create_rectangle((x*sizetuile), (y*sizetuile), (x*sizetuile)+sizetuile, (y*sizetuile)+sizetuile, fill = tl[0], tags = ["click","tuile",x,y,pic[x][y], tl[1]], outline='black')
			


			##### Version Non-Aléatoire  #####
			#tk_img = typetoimg(tl[1], sizetuile)
			"""
			if tl[1] == "mountains":
				tk_img = data.loadtexture("/asset/terrain/mountains/mountains_inner.png", sizetuile)
			elif tl[1] == "forest":
				tk_img = data.loadtexture("/asset/terrain/conifer_forest/conifer_forest_inner.png", sizetuile)
			elif tl[1] == "plains":
				tk_img = data.loadtexture("/asset/terrain/plains/plains.png", sizetuile)
			elif tl[1] == "ocean":
				tk_img = data.loadtexture("/asset/terrain/ocean/ocean_inner.png", sizetuile)
			"""
			################################

			##### Version Non-Aléatoire Dico #####
			if tl[1] == "mountains":
				tk_img = data.loadtexturefromdico(dico_file, "mountains_inner.png", tl[1], sizetuile)[1]
			elif tl[1] == "forest":
				tk_img = data.loadtexturefromdico(dico_file, "conifer_forest_inner.png", tl[1], sizetuile)[1]
			elif tl[1] == "plains":
				tk_img = data.loadtexturefromdico(dico_file, "plains.png", tl[1], sizetuile)[1]
			elif tl[1] == "ocean":
				tk_img = data.loadtexturefromdico(dico_file, "ocean_inner.png", tl[1], sizetuile)[1]


			################################


			##### Version Aléatoire Dico #####
			#tk_img = data.randomloadtexturefromdico(dico_file, tl[1], sizetuile)[1]

			################################

			################################
			#The solution is to make sure to keep a reference to the Tkinter object, for example by attaching it to a widget attribute:
			label = tkinter.Label(image = tk_img)
			label.image = tk_img
			################################
			#label.pack()
			print((x*sizetuile), (y*sizetuile), tk_img)
			#mapcanv.create_image((x*sizetuile), (y*sizetuile), image = tk_img)
			mapcanv.create_image((x*sizetuile), (y*sizetuile), image = tk_img, tags = ["img",tl[1]])

	#On lie Command+molette aux zoom/dézoom
	mapcanv.bind("<MouseWheel>", moveviewz)

	#On focus sur le widget sinon il ne prendra pas en compte les entrées des touches fléchés
	mapcanv.focus_set()

	#On lie les touches fléchés aux déplacement de la vue
	mapcanv.bind('<KeyPress-Left>', lambda event, x=1,y=0: moveviewxy(event,x,y))
	mapcanv.bind("<KeyPress-Right>", lambda event, x=-1,y=0: moveviewxy(event,x,y))
	mapcanv.bind("<KeyPress-Up>", lambda event, x=0,y=1: moveviewxy(event,x,y))
	mapcanv.bind("<KeyPress-Down>", lambda event, x=0,y=-1: moveviewxy(event,x,y))

	#On lie le déplacement de la vue au maintient du bouton droit de la souris + motion
	mapcanv.bind('<Shift-ButtonPress-1>', startmoveviewmouse)
	mapcanv.bind('<Shift-B1-Motion>', moveviewmouse)


	#ON lie les différentes Cases à l'action click
	mapcanv.tag_bind("click", "<Button-1>", coord)

	mapcanv.pack(expand ="True")

####################################################################################################


######################### Fonction Secondaire ############################
def tuile(nb):
	####################
	# 1er Version qui lier la valeur d'une case à une Couleur,
	# 2eme Version doit lier la valeur de la case à un type qui sera caractériser par un Tag:
	#	blue, Ocean
	#	yellow, plain
	#	green, forest
	#	grey, mountain
	#
	# 3eme Version doit lier la valeur d'une case à une texture
	# 4ieme version doit lier la valeur d'une tuile à une case d'un type de texture qui en compte un ensemble ex: plaine possède plaine1.txt, plaine2.txt, plaine3.txt
	#	-> return random.rand(len(objectfolder)) 
	####################
	if(nb <= -0.25):
		#data.loadtexture("/asset/terrain/mountains_inner.png",20)
		return ("grey", "mountains")
	elif(nb>-0.25 and nb <=0):
		#data.loadtexture("/asset/terrain/conifer_forest_inner.png",20)
		return ("green", "forest")
	elif(nb>0 and nb <= 0.25):
		#data.loadtexture("/asset/terrain/plains.png",20)
		return ("yellow", "plains")
	else:
		#data.loadtexture("/asset/terrain/ocean/ocean_inner.png",20)
		return ("blue", "ocean")



def typetoimg(type, sizetuile):
	####################
	# Fonction qui va renvoyer une image selon le type envoyer en entréer
	# l'image est resize à la taille d'une tuile
	####################

	img = ""
	print(type)

	if type == "mountains":
		#print("mountain")
		img = data.loadtexture("/asset/terrain/mountains/mountains_inner.png", sizetuile)
	elif type == "forest":
		#print("forest")
		img = data.loadtexture("/asset/terrain/conifer_forest/conifer_forest_inner.png", sizetuile)
	elif type == "plains":
		#print("plains")
		img = data.loadtexture("/asset/terrain/plains/plains.png", sizetuile)
	elif type == "ocean":
		#print("ocean")
		img = data.loadtexture("/asset/terrain/ocean/ocean_inner.png", sizetuile)
	return img

def moveviewz(event):
	####################
	# Fonction pour zoomer/dézoomer
	# En utilisant la molette de la souris
	#
	# Doit utiliser .scale(tagOrId, xOffset, yOffset, xScale, yScale)
	# xScale, yScale = 1 == No Scaling
	#
	# On zoome quand on multiplie par delta
	# On dezoome quand on divise par delta
	#
	#	--- * 2 = ------ 	== Zoom car on agrandit
	#
	# 	--- / 3 = - 		== DeZoom car on réduit
	####################

	#Comprendre le fonctionnement de cela
	x0 = event.widget.canvasx(event.x)
	y0 = event.widget.canvasy(event.y)

	#Pour éviter les différence entre windows et Mac ont normalise delta
	#Doit prendre en compte linux -_-
	if event.delta <= 0:
		delta = -2
	else:
		delta = 2
	#On prend pour valeur min de la taille d'une tuile 5
	#On vérifier que la taile d'une tuile soit supérieur à 5
	#Pour calculer on utiliser seulement les coord x du premier carré du canvas qui doit être forcement à l'index 1
	#print(event.widget.coords(1))
	x = (event.widget.coords(1)[2] - event.widget.coords(1)[0])
	#print(x, event.delta, delta)

	# Doit trouver les valeurs parfaite max et min
	# Zoom = max = x = 320
	# DeZoom = min = x = 5
	# À l'avenir changer la valeur minimum par une valeur calculer a partir de la taille de la carte

	####################
	#Zoom
	if (x<320) and (delta == 2):
		event.widget.scale("tuile", x0, y0, delta, delta)
		event.widget.scale("img", x0, y0, delta, delta)
		tp = event.widget.coords(1)
		newsize = tp[2] - tp[0]
		print(x0,y0, delta, newsize)
		#Tuile graphique:
		for ele in event.widget.find_withtag("img"):
			print(ele, event.widget.gettags(ele))
			#On créer une nouvelle version de l'image qui va remplacer l'ancienne
			img = typetoimg(event.widget.gettags(ele)[1], int(newsize))
			#Garde en mémoire l'image
			label = tkinter.Label(image = img)
			label.image = img
			event.widget.itemconfigure(ele,image = img)


	#Dezoom
	elif(x>5) and (delta == -2):
		#On rend positive le delta sinon il inverse le sens de la carte
		event.widget.scale("tuile", x0, y0, 1/(-delta), 1/(-delta))
		event.widget.scale("img", x0, y0, 1/(-delta), 1/(-delta))
		tp = event.widget.coords(1)
		newsize = tp[2] - tp[0]
		print(x0,y0, 1/(-delta), newsize)
		# Tuile graphique
		for ele in event.widget.find_withtag("img"):
			print(ele, event.widget.gettags(ele))
			#On créer une nouvelle version de l'image qui va remplacer l'ancienne
			img = typetoimg(event.widget.gettags(ele)[1], int(newsize))
			#Garde en mémoire l'image
			label = tkinter.Label(image = img)
			label.image = img
			event.widget.itemconfigure(ele,image = img)
	####################










#################### 
# Ensemble de Fonction pour déplacer la vue en:
# Maintenant le click gauche de la souris
# En placant le souris sur une extrémité de la caméra
# En appyant sur les touches fléchés 
####################

def moveviewxy(event, deltax, deltay):
	####################
	# Fonction pour déplacer la vue en:
	# Maintenant le click gauche de la souris
	# En placant le souris sur une extrémité de la caméra
	# En appyant sur les touches fléchés 
	####################
	mult = 100

	print("move map arrow")

	################ Déplacement de la vue ################

	event.widget.move("tuile", mult*deltax, mult*deltay)

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


def coord(event):
	print(event.widget.gettags("current"))


###########################################################################


######################### Main #########################
if __name__ == '__main__':
	#Init de la fenêtre
	root = tkinter.Tk()
	#définition de la taille de la carte
	mapx = 100
	mapy = 100
	pic = genproc.genNoiseMap(10, (random.random()*time()), mapx, mapy)
	#Chargement en mémoires des images du dico:
	dico_file = data.assetLoad()
	
	mainscreen(1200,1200,root,pic, mapx, mapy)


	root.mainloop()