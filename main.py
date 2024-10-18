import tkinter
import genproc
import random
from time import time

#Doit terminé de faire un Prototype:
# - Ajouter Un moyen de déplacer la vue
# - Ajouter un moyen de Zoomer/Dézoomer
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




	#On Créer les Différentes Cases avec le tags Click pour indiquer et les trouvé plus facilement
	#2ieme version: ajouter un tag supplémentaire liées aux types
	for x in range(mapx):
		for y in range(mapy):
			mapcanv.create_rectangle((x*sizetuile), (y*sizetuile), (x*sizetuile)+sizetuile, (y*sizetuile)+sizetuile, fill = tuile(pic[x][y]), tags = "click")
			#print(tuile(pic[x][y]))

	#ON lie les différentes Cases à l'action click
	mapcanv.tag_bind("click", "<Button-1>", coord)
	#On lie Command+molette aux zoom/dézoom


	#On lie Command+Button1 aux déplacement de la vue
	#Voir pour Utiliser Motion
	mapcanv.bind("<Shift-Button-1>", moveviewxy)



	mapcanv.pack(expand ="True",)





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
	#Fonction pour zoomer/dézoomer
	pass


def moveviewxy(event):
	print("moveviewxy")
	# Fonction pour déplacer la vue en:
	# Maintenant le click gauche de la souris
	# En placant le souris sur une extrémité de la caméra
	# En appyant sur les touches fléchés 
	event.widget.canvasx(event.x)
	event.widget.canvasy(event.y)


def coord(event):
	print(event.x,event.y)


###########################################################################


######################### Main #########################
if __name__ == '__main__':
	#Init de la fenêtre
	root = tkinter.Tk()
	#définition de la taille de la carte
	mapx = 50
	mapy = 50
	pic = genproc.genNoiseMap(10, (random.random()*time()), mapx, mapy)
	mainscreen(1200,1200,root,pic, mapx, mapy)


	root.mainloop()