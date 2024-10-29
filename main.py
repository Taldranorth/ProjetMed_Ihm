import tkinter
import genproc
import random
from time import time

#Doit terminé de faire un Prototype:
# - Ajouter Un moyen de déplacer la vue √
#	--> Doit modifier afin de prendre en compte le non focus sur le widget du canvas
#		--> Doit appliquer le bind des touches à la root
#		--> Doit trouver un moyen de stocker les objets dans une données facilement accesible
#			--> Un dico ?
#			--> Place les bases du stockage de données
#	--> Doit modifier afin d'accèlerer le déplacement avec le maintient de la touche
#	--> Doit modifier afin de pouvoir drag le terrain
# - Ajouter un moyen de Zoomer/Dézoomer



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

	#Init de la fenêtre

	#Création de la fenêtre
	win1 = tkinter.Toplevel(root, height = heightWindow, width= widthWindow)

	#Frame Affichage
	fcanvas = tkinter.Frame(win1)
	fcanvas.pack(expand="True", fill="both")
	createmap(heightWindow, widthWindow, pic, fcanvas, mapx, mapy, 20)

	#Frame Boutton
	fbutton = tkinter.Frame(win1)
	fbutton.pack(expand="True", fill="both")
	#Bouton pour quitter
	Button_exit = tkinter.Button(fbutton,command = exit, text = "Quitter")
	Button_exit.pack(side="bottom")
#########################



######################### Gestion de la Carte #######################################################
def createmap(heightWindow, widthWindow, pic, frame, mapx, mapy, sizetuile):
	#Si heigthWindow/1.5 le boutton quitter disparait
	mapcanv = tkinter.Canvas(frame,height = ((heightWindow)/1.55), width = ((widthWindow)/1.5))
	#Pas d'espacement, taille d'un carré: 15 pour tester
	#SI entre -1 et -0.5 = lac = bleu
	#Si entre -0.5 et 0 = plaine = Jaune
	#SI entre 0 et 0.5 = forêt = Vert
	#Si entre 0.5 et 1 = Montagne = Gris

	#Le Canvas est décomposé en 2 coordonées:
	# - Canvas Coordinate qui sont les objet dans l'espace du Canvas
	# - Window Coordinate qui sont les object dans l'espace de la fenêtre
	#Quand je doit changer la vue je doit changer les Windows coordonnées

	#.canvasx(screenx, gridspacing=None)
	#Translates a window x coordinate screenx to a canvas coordinate. If gridspacing is supplied, the canvas coordinate is rounded to the nearest multiple of that value.

	#.canvasy(screeny, gridspacing=None)
	#Translates a window y coordinate screeny to a canvas coordinate. If gridspacing is supplied, the canvas coordinate is rounded to the nearest multiple of that value.




	#On Créer les Différentes Cases avec le tags tuile pour indiquer et les trouvé plus facilement
	#On ajoute aussi le tags click pour indiquer qu'ils sont clickables
	#On ajoute aussi les tags x et y qui correspond à la casse ou ils est situés
	#2ieme version: ajouter un tag supplémentaire liées aux types
	for x in range(mapx):
		for y in range(mapy):
			mapcanv.create_rectangle((x*sizetuile), (y*sizetuile), (x*sizetuile)+sizetuile, (y*sizetuile)+sizetuile, fill = tuile(pic[x][y]), tags = ["click","tuile",x,y],outline='black')
			#print(tuile(pic[x][y]))

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
	#1er Version qui lier la valeur d'une case à une Couleur,
	#2eme Version doit lier la valeur d'une case à une texture
	#3ieme version doit lier la valeur d'une tuile à une case d'un type de texture qui en compte un ensemble ex: plaine possède plaine1.txt, plaine2.txt, plaine3.txt
	# -> return random.rand(len(objectfolder)) 
	if(nb <= -0.5):
		return "blue"
	elif(nb>-0.5 and nb <=0):
		return "yellow"
	elif(nb>0 and nb <= 0.5):
		return "green"
	else:
		return "grey"

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
	if event.delta <= 0:
		delta = -2
	else:
		delta = 2



	#On prend pour valeur min de la taille d'une tuile 5
	#On vérifier que la taile d'une tuile soit supérieur à 5
	#Pour calculer on utiliser seulement les coord x du premier carré du canvas qui doit être forcement à l'index 1
	print(event.widget.coords(1))
	x = (event.widget.coords(1)[2] - event.widget.coords(1)[0])
	#On multiplie par le delta recup
	print(x, event.delta, delta)

	# Doit trouver les valeurs parfaite max et min
	# Zoom = max = x = 320
	# DeZoom = min = x = 5
	#

	####################
	#Zoom
	if (x<640) and (delta == 2):
		event.widget.scale("tuile", x0, y0, delta, delta)
	#Dezoom
	elif(x>5) and (delta == -2):
		event.widget.scale("tuile", x0, y0, 1/delta, 1/delta)
	####################

def moveviewxy(event, deltax, deltay):
	####################
	# Fonction pour déplacer la vue en:
	# Maintenant le click gauche de la souris
	# En placant le souris sur une extrémité de la caméra
	# En appyant sur les touches fléchés 
	####################
	mult = 50

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
	mainscreen(1200,1200,root,pic, mapx, mapy)


	root.mainloop()