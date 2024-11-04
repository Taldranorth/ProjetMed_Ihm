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
#			--> c'est créer par dessus, tout est garder en mémoire
#
#	!!! Doit créer un Atlas des label !!!
#	Quand une texture est adapter dans le bon format on stocker le nom de la texture avec le label associer dans l'atlas
#
#	--> Cela permettrait de garder en mémoire que 4 texture et 4 label plutôt que 100*100 texture et labels 
#	--> Cela permettrait aussi de ne pas avoir à recréer de label et de juste modifier la texture associer

# Atlas Mis en Place !!!!
# Je viens de réduire l'utilisation de la mémoire à seulement 115 Mo
# Maintenant je dois comprendre d'ou vient le lag quand on observe beaucoup de case à la fois

# J'ai terminé de refactoriser l'utilisation du dico

# Objectif:
#	Correctif:
#	- Faire la doc de ce qui a était fait
#	- Réduire le lag lors de l'observation d'un grand groupe de cases
#		--> Utilisation du processeurs importante
#	- Corriger le décalage avec l'écran arrière
#		!!!
#		--> Le problème vient du calcul de la variable newtp dans moveviewz , doit améliorer le calcul
#			--> Après implémenter une version qui n'utilise pas la map carre
#		!!!
#
#	- Refactoriser le Code
#		--> Le Nettoyer
#		--> Retirer les Commentaires Inutiles		
#		--> Prévoir l'ajout de future Tuiles
#	- !!!! Commencer a s'entrainer avec les CLasses !!!!
#		--> Transformer Atlas en classe
#
#	- !!! Voir pour ajouter la taille de la texture resize à l'atlas !!!
#	- Prendre en compte linux dans la fonction moveviewz
#
#	Additif:
#	- Déplacement en mettant la souris sur la bordure extérieur de la carte
#	- Menu Principale
#	- Interface en Jeu
#		--> Entête
#
#	- Affichage En tête
#	- Landforme
#	- Préparer Système de la Boucle Principale
#	- Recup Texture.png des Batiment, Unités, Event, Blason
#		--> Recup Image Event depuis CK 2 ou 3
#	- Sauvegarde des données
#	- Ajouter du Son
#		--> https://stackoverflow.com/questions/28795859/how-can-i-play-a-sound-when-a-tkinter-button-is-pushed
#
#	- Ajouter de l'animation
#		--> https://stackoverflow.com/questions/53418926/button-motion-animation-in-tkinter
#			--> Semble très gourmand
#				--> Trouver une solution plus performante
#
#	- Doit changer la carte pour remplacer l'utilisation des tags par des classes pour la tuile
#		--> Doit changer tout ce qui utiliser les tags
#		--> Vérifier le cout en perf et garder l'ancien système dans un coin au cas ou
#
#
#	- Centrer la fenêtre du Menu principale
#		--> Ajouter un Fond d'écran un peu joli
#			--> Ajouter un Peu d'anim
#
#
#	- Ajouter un systeme de randomisation des texture
#		--> SI la texture tirer n'est pas une texture de base mais une "Incomplète" charger en dessous une texture
#
#
#

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







######################### Menu Principale #########################

def mainmenu(heightWindow, widthWindow, root):
	# Création de la fenêtre
	mainmenuwin = tkinter.Toplevel(root, height = heightWindow, width = widthWindow)

	# Création de la frame
	fmainm = tkinter.Frame(mainmenuwin)
	fmainm.pack(expand="True", fill="both")

	# Mise en Place des Menus

	# Button Play
	Button_mainm_Play = tkinter.Button( fmainm, text = "Jouer")

	# Button Quickplay
	Button_mainm_QuickPlay = tkinter.Button( fmainm, command = lambda: mainscreen(heightWindow, widthWindow,root,pic, option.mapx, option.mapy), text = "Partie Rapide")
	#mainmenuwin.destroy()

	# Button Load
	Button_mainm_load = tkinter.Button(fmainm, text = "Load")

	#Button Options
	Button_mainm_option = tkinter.Button(fmainm, text = "Options")

	#Button Exit
	Button_mainm_exit = tkinter.Button(fmainm, command = exit, text = "Quitter")

	#Pack des Button
	Button_mainm_Play.pack()
	Button_mainm_QuickPlay.pack()
	Button_mainm_load.pack()
	Button_mainm_option.pack()
	Button_mainm_exit.pack()



###########################################################################

######################### Écran de Jeu #########################
def mainscreen(heightWindow, widthWindow, root, pic, mapx, mapy):

	# Création de la fenêtre
	win1 = tkinter.Toplevel(root, height = heightWindow, width= widthWindow)

	interface(win1,heightWindow, widthWindow)

	# Frame Map
	fcanvas = tkinter.Frame(win1)
	fcanvas.pack(expand="True", fill="both")

	createmap(heightWindow, widthWindow, pic, fcanvas, mapx, mapy, 20,dico_file)
####################################################################################################



######################### Gestion de la Carte #######################################################
def createmap(heightWindow, widthWindow, pic, frame, mapx, mapy, sizetuile, dico_file):
	global atlas
	#Si heigthWindow/1.5 le boutton quitter disparait
	mapcanv = tkinter.Canvas(frame,height = ((heightWindow)/1.6), width = widthWindow)
	lframe = tkinter.Frame(frame)
	# On Créer les Différentes Cases avec le tags tuile pour indiquer et les trouvé plus facilement
	# On ajoute aussi le tags click pour indiquer qu'ils sont clickables
	# On ajoute aussi les tags x et y qui correspond à la casse ou ils est situés
	# ONn ajoute aussi le tag pic[x][y] qui correspond à la valeur de la case gen
	# 2ieme version: ajouter un tag supplémentaire liées aux types
	for x in range(mapx):
		for y in range(mapy):

			# On utilise la valeur de la case pour définir la tuile que l'on va créer
			tl = tuile(pic[x][y])

			# Création de la carte avec Rectangle
			#mapcanv.create_rectangle((x*sizetuile), (y*sizetuile), (x*sizetuile)+sizetuile, (y*sizetuile)+sizetuile, fill = tl[0], tags = ["click","tuile",x,y,pic[x][y], tl[1]], outline='black')
			
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

			##### Version Non-Aléatoire Dico Sans Atlas #####
			#tk_img = typetoimgdico(dico_file, tl[1], sizetuile)
			#################################################


			##### Version Non-Aléatoire Dico Avec Atlas #####
			
			if tl[1] == "mountains":
				if data.checkAtlas(atlas, "mountains_inner.png") == False:
					tk_img = data.loadtexturefromdico(dico_file, "mountains_inner.png", tl[1], sizetuile)
					label = tkinter.Label(lframe,image = tk_img[1])
					label.image = tk_img[1]
					atlas = data.addAtlas(atlas, label, tk_img[0])
				else:
					label = atlas["mountains_inner.png"]

			elif tl[1] == "forest":
				if data.checkAtlas(atlas, "conifer_forest_inner.png") == False:
					tk_img = data.loadtexturefromdico(dico_file, "conifer_forest_inner.png", tl[1], sizetuile)
					label = tkinter.Label(lframe,image = tk_img[1])
					label.image = tk_img[1]
					atlas = data.addAtlas(atlas, label, tk_img[0])
				else:
					label = atlas["conifer_forest_inner.png"]

			elif tl[1] == "plains":
				if data.checkAtlas(atlas, "plains.png") == False:
					tk_img = data.loadtexturefromdico(dico_file, "plains.png", tl[1], sizetuile)
					label = tkinter.Label(lframe,image = tk_img[1])
					label.image = tk_img[1]
					atlas = data.addAtlas(atlas, label, tk_img[0])
				else:
					label = atlas["plains.png"]

			elif tl[1] == "ocean":
				if data.checkAtlas(atlas, "ocean_inner.png") == False:
					tk_img = data.loadtexturefromdico(dico_file, "ocean_inner.png", tl[1], sizetuile)
					label = tkinter.Label(lframe,image = tk_img[1])
					label.image = tk_img[1]
					atlas = data.addAtlas(atlas, label, tk_img[0])
				else:
					label = atlas["ocean_inner.png"]
			
			################################

			##### Version Aléatoire Dico #####
			#tk_img = data.randomloadtexturefromdico(dico_file, tl[1], sizetuile)[1]

			################################

			#########Garde en mémoire l'image ######
			#The solution is to make sure to keep a reference to the Tkinter object, for example by attaching it to a widget attribute:
			#label = tkinter.Label(lframe,image = tk_img)
			#label.image = tk_img
			#########################################
			mapcanv.create_image((x*sizetuile), (y*sizetuile), image = label.image, tags = ["img",tl[1],"tuile","click", x, y, pic[x][y]])

	#print("taille atlas: ",len(atlas))
	#On lie Command+molette aux zoom/dézoom
	mapcanv.bind("<MouseWheel>", lambda event, lf=lframe :moveviewz(event, lf))

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

	mapcanv.pack(expand ="True", fill = "y")

####################################################################################################

######################### Fonction Interface ############################

def interface(win,heightWindow, widthWindow):

	####################
	# Fonction qui met en place l'interface en Jeu, voir l'entête
	# HeightWindow et widthWindow sont la taille de la fenêtre de jeu
	# 
	# Actuellement l'interface est défini à l'extérieur
	#
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
	topframe = tkinter.Frame(win, height = heightWindow/28, width= widthWindow, background = "grey")
	# En tête Bas
	bottomFrame = tkinter.Frame(win, height = heightWindow/18, width= widthWindow, background = "grey")

	topframe.pack(expand = "True", side = "top")
	bottomFrame.pack(expand = "True", side = "bottom")


	# Liste de Bouton

	# Button Gauche
	Button_military = tkinter.Button(bottomFrame, text= "Militaire")
	Button_gestion = tkinter.Button(bottomFrame, text= "Gestion")


	# Button Droit

	# Buton pour quitter(A remplacer par un listbutton)
	# Exit, Option, Load, Sauvegarder
	Button_exit = tkinter.Button(bottomFrame, command = exit, text = "Quitter")
	# Button pour acceder à la vue générale
	Button_globalview = tkinter.Button(bottomFrame, text = "Vue Générale")


	# On pack les Button
	Button_gestion.pack(side="left")
	Button_military.pack(side="left")
	Button_exit.pack(side="right")
	Button_globalview.pack(side="right")

#########################################################################



######################### Fonction Secondaire ############################
def tuile(nb):
	####################
	# 1er Version qui lier la valeur d'une case à une Couleur,
	# 2eme Version doit lier la valeur de la case à un type qui sera caractériser par un Tag:
	#	blue, Ocean
	#	yellow, plain
	#	green, forest
	#	grey, mountain
	####################
	if(nb <= -0.25):
		return ("grey", "mountains")
	elif(nb>-0.25 and nb <=0):
		return ("green", "forest")
	elif(nb>0 and nb <= 0.25):
		return ("yellow", "plains")
	else:
		return ("blue", "ocean")



def typetoimg(type, sizetuile):
	####################
	# Fonction qui va renvoyer une image selon le type envoyer en entré
	# l'image est resize à la taille d'une tuile
	####################

	img = ""

	if type == "mountains":
		#print("mountain")
		img = data.loadtexture("/asset/texture/terrain/mountains/mountains_inner.png", sizetuile)
	elif type == "forest":
		#print("forest")
		img = data.loadtexture("/asset/texture/terrain/conifer_forest/conifer_forest_inner.png", sizetuile)
	elif type == "plains":
		#print("plains")
		img = data.loadtexture("/asset/texture/terrain/plains/plains.png", sizetuile)
	elif type == "ocean":
		#print("ocean")
		img = data.loadtexture("/asset/texture/terrain/ocean/ocean_inner.png", sizetuile)
	return img


def typetoimgdico(dico_file, type, sizetuile):
	####################
	# Fonction qui va renvoyer une image selon le type envoyer en entré et le dico
	# l'image est resize à la taille d'une tuile
	####################

	img = ""

	if type == "mountains":
		#print("mountain")
		img = data.loadtexturefromdico(dico_file, "mountains_inner.png", type, sizetuile)[1]
	elif type == "forest":
		#print("forest")
		img = data.loadtexturefromdico(dico_file, "conifer_forest_inner.png", type, sizetuile)[1]
	elif type == "plains":
		#print("plains")
		img = data.loadtexturefromdico(dico_file, "plains.png", type, sizetuile)[1]
	elif type == "ocean":
		#print("ocean")
		img = data.loadtexturefromdico(dico_file, "ocean_inner.png", type, sizetuile)[1]
	return img


def moveviewz(event, lframe):
	global atlas
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


	####################################### Doit Changer ###############################################
	#Pour calculer on utiliser seulement les coord x du premier carré du canvas qui doit être forcement à l'index 1
	print("event.widget.coords(1): ", event.widget.coords(1))
	# Carte avec Rectangle
	# On utilise x1 et x0 pour obtenir la taille actuelle d'1 tuile de la carte
	#x = (event.widget.coords(1)[2] - event.widget.coords(1)[0])
	# Carte avec texture
	#
	x = (event.widget.coords(1)[1] - event.widget.coords(1)[0])
	print("x, event.delta, delta: ",x, event.delta, delta)
	####################################################################################################



	# Doit trouver les valeurs parfaite max et min
	# Zoom = max = x = 320
	# DeZoom = min = x = 5
	# À l'avenir changer la valeur minimum par une valeur calculer a partir de la taille de la carte

	####################
	f = 0
	m = 0
	o = 0
	p = 0
	#Zoom
	if (x<320) and (delta == 2):
		print("Zoom")
		event.widget.scale("tuile", x0, y0, delta, delta)
	#Dezoom
	elif(x>5) and (delta == -2):
		print("DeZoom")
		#On rend positive le delta sinon il inverse le sens de la carte
		event.widget.scale("tuile", x0, y0, 1/(-delta), 1/(-delta))


	#Recalcul des images



	############################# Doit Changer ###############################
	tp = event.widget.coords(1)
	# Carte avec Rectangle
	#newsize = tp[2] - tp[0]
	# Carte Sans Rectangle
	newsize = tp[1] - tp[0]
	print("newsize : ", newsize)
	##########################################################################

	#Tuile graphique:
	for ele in event.widget.find_withtag("img"):

		type = event.widget.gettags(ele)[1]
		# Version Non-random ou on utilise les texture de bases:
		# Quand la classe des tuile sera implémenter utiliser le nom de la texture 
		if type == "forest":
			#Si dans la fonction on n'a pas déjà recalculer la nouvelle image pour le type selectionner
			if f == 0:
				#On recréer l'image
				tk_img = data.loadtexturefromdico(dico_file, "conifer_forest_inner.png", type, int(newsize))
				# On change modifier le label associer à la texture dans l'atlas
				atlas = data.changelabelAtlas(atlas, tk_img[0], tk_img[1])				
				f = 1
			# On recup le label associer à la texture
			label = atlas["conifer_forest_inner.png"]
		elif type == "mountains":
			if m == 0:
				tk_img = data.loadtexturefromdico(dico_file, "mountains_inner.png", type, int(newsize))
				atlas = data.changelabelAtlas(atlas, tk_img[0], tk_img[1])	
				m = 1
			label = atlas["mountains_inner.png"]
		elif type == "ocean":
			if o == 0:
				tk_img = data.loadtexturefromdico(dico_file, "ocean_inner.png", type, int(newsize))
				atlas = data.changelabelAtlas(atlas, tk_img[0], tk_img[1])						
				o = 1
			label = atlas["ocean_inner.png"]
		elif type == "plains":
			if p == 0:
				tk_img = data.loadtexturefromdico(dico_file, "plains.png", type, int(newsize))
				atlas = data.changelabelAtlas(atlas, tk_img[0], tk_img[1])						
				p = 1
			label = atlas["plains.png"]

		event.widget.itemconfigure(ele,image = label.image)
	print("Atlas: ", atlas)


	####################














#################### 
# Ensemble de Fonction pour déplacer la vue en:
# Maintenant le click gauche de la souris √
# En placant le souris sur une extrémité de la caméra
# En appyant sur les touches fléchés √
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


######################### Autre Fonction #########################

def highlightCase(event):
	####################
	# Fonction qui ilumine la case sur laquelle est présente la souris
	####################

	#event.widgetitemconfigure()
	pass


def coord(event):
	print(event.x, event.y)
	print(event.widget.gettags("current"))


###########################################################################






######################### Def de Classes #########################


class Classtuiles:
	####################
	# Classe qui va contenir toute les données liée à une tuile:
	#
	#	- N° de la tuile
	#	- Propriétaire de la tuile:
	#		--> Un seigneur ou personne(nature)
	#		--> Quand la tuile est créer personne ne possède la tuile
	#	- Ressource présente
	#	- Ressource particulière
	#		--> Optionnelle, pour après que le projet soit terminer
	#	- Bonus/Malus
	#	- texture file associé
	#			--> On sépare le texture file du texture
	#				--> texture_name = le nom du fichier
	#				--> texture = le fichier charger est resize
	####################

	def __init__(self, texture_name, x, y):
		# N° de la tuile
		self.x = x
		self.y = y
		# nom du fichier texture associé
		self.texture_name = texture_name
		# nom du propriétaire de la tuile
		self.possesor = "wild"






class ClassOptions:
	####################
	# Classe qui va contenir toute les options de paramètre:
	#	- Definition de la fenêtre
	#	- Definition de la carte
	#
	#
	# Au lancement du programme il va chercher si le fichier option.ini est bien présent 
	# Si c'est le cas il va charger les options contenu dedans
	# Sinon il va charger les options par défauts
	####################


	def __init__(self):

		#Défintion de la fenêtre
		self.heightWindow = 1200
		self.widthWindow = 1200
		# Définition de la carte
		self.mapx = 100
		self.mapy = 100


	def loadoption():
		# f = open(Config.ini)
		#
		#
		#
		pass




###########################################################################

######################### Main #########################
if __name__ == '__main__':
	#Init de la fenêtre
	root = tkinter.Tk()
	#On créer l'atlas
	atlas = data.createAtlas()

	#Chargement des Options:
	option = ClassOptions()

	pic = genproc.genNoiseMap(10, (random.random()*time()), option.mapx, option.mapy)
	#Chargement en mémoires des images du dico:
	dico_file = data.assetLoad()
	

	# Menu principale
	mainmenu(option.heightWindow, option.widthWindow, root)
	# Si on veut tester rapidement la boucle de jeu sans passer par le menu principale
	#mainscreen(option.heightWindow, option.widthWindow, root, pic, option.mapx, option.mapy)


	root.mainloop()