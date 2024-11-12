import sys
import tkinter
import random

import gameClass

from time import time
from PIL import ImageTk, Image, ImageShow


######################### On recup le dossier locale dans une variable	#########################
import os
c_d = os.getcwd()
#################################################################################################



######################### Description du fichier	#########################
# Fonctions dédier a l’ouverture et la sauvegarde de fichier
#
# On utilise la bibliothèque PIL intégrer de bases à python car tkinter ne gère pas les .png
#
#
#
#  
# Pour Importer depuis un sous-dossier:  
# «import subdir.mymodule
# subdir.mymodule.say_hello()»
#
#
#############################################################################

######################### Objet qui doivent être Enregistrer ################
# - Le Nb de tour
# - Les données du Joueur
# - Les données des Non-Joueurs
# - La Seed
#
#
#
#
#############################################################################

################## Objet qui ne doivent pas être Enregistrer ################
# - les Images
# - Pic, la noise map obtenue à partir de genNoisemap
#
#
#
#
#
#############################################################################






###########################################################################

######################### Def de Classes #########################


####################
#
#
#
#
#
####################
class ClassGameData:

	####################
	# Classe qui va contenir toute les données de la partie:
	# 	- Nb tour
	#	- Nb lord
	#	- Taille d'une tuile
	#	- liste de lord
	#		--> type de l'objet: class
	# 
	#	- liste des tuiles
	#
	#	- Le seed de la carte
	#
	#	2 état:
	#		- Avant initialisation de la game
	#		- Après initialisation de la game
	#
	#	À l'initialisation de la game on créer une instance de la classe qui va contenir les données suivante:
	#		Nb_tour = 0
	#		Nb_lord = 3
	#		
	#
	# 
	####################

	def __init__(self):

		# Variable qui vient contenir le nombre de tour passé
		self.Nb_tour = 1
		# Variable qui vient contenir le nombre de joueurs
		self.Nb_lord = 1
		self.tuilesize = 20

		#Seed générer au lancement de l'appli
		self.seed = random.random()*time()

		# Variable bool modifier quand ont veut que le joueur termine son tour
		self.endturn = False

		# Variable qui vient contenir l'id du lord qui représente le seigneur
		self.playerid = 0
		player = gameClass.Classlord("test", True)
		self.list_lord = [player]

		# Dico des Assets
		self.dico_file = assetLoad()
		# Dico des noms
		self.dico_name = loadnamedico(os.getcwd()+"/Asset/name.txt")
		# Atlas
		self.atlas = {}
		# Label Frame Atlas
		self.lframe = 0



	#tuile: Classtuiles
	def addtuile(self, tuile):
		self.list_tuile += [tuile]

	# Fonction pour changer la taille de la tuile
	def newsizetuile(self, size: int):
		self.tuilesize = size

	# Fonction pour charger les données d'une save
	def loaddata():
		pass

	# Fonction pour define le labelframe
	def setlframe(self, lframe):
		self.lframe = lframe

	# Fontion Atlas
	def addAtlas(self, label, filename):
		####################
		# Fonction pour ajouter une nouvelle entréer à l'Atlas
		####################		
		self.atlas[filename] = label

	def checkAtlas(self, filename):
		####################
		# Fonction pour voir si une texture est présente dans l'atlas
		####################
		if filename in self.atlas.keys():
			return True
		else:
			return False

	def changelabelAtlas(self, filename, img):
		####################
		# Fonction pour changer la texture associer à un label
		####################
		self.atlas[filename].configure(image = img)
		self.atlas[filename].image = img

	def changePlayerLord(self, idplayer, player):
		self.list_lord[idplayer] = player


	def randomnametype(self, type):
		if type not in ["Nom", "Surnom", "Village"]:
			print("Type non présent dans Nom, Surnom, Village")

		return self.dico_name[type][random.randrange(len(self.dico_name[type]))]



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

		# Octaves utilisés pour la gen de la carte
		self.octaves = 10


	def loadoption(self):
		# f = open("user/Config.ini")
		# 
		#
		#
		#
		# F.close()
		pass

###########################################################################



def assetLoad():

	####################
	# Fonction qui renvoit le dico qui contient l'ensemble des Images préparer pour être charger en mémoire:
	#
	# On différencie les dossier des fichier par l'extension:
	#	dossier = folder
	#	fichier = file.png
	#
	#	4 clé principale: ocean, mountains, forest, plains
	#	Tout les autres fichier qui ne rentre pas dans other
	#
	# Pour un Dossier qui contient 10 fichier texture: Ocean.png, Ocean_2.png, Ocean_3.png, mountains_1.png, mountains_2.png, forest_1.png, forest_2.png, forest_3.png, plains_1.png, plains_2.png
	# la fonction nous renvois le dico suivant:
	# dicotexture{ 
	#	Oceans: [Ocean.png,l'objet ouvert], Ocean_2.png, Ocean_3.png
	#	Mountains: mountains_1.png, mountains_2.png
	#	Forest: forest_1.png, forest_2.png, forest_3.png
	#	Plains: plains_1.png, plains_2.png
	#	}
	#
	# Doit voir comment utiliser tkinter pour charger les fichier images
	#
	# Amélioration possible:
	#	- transformer Foret en un Sous-dico afin de prendre en compte plusieurs biomes possible de forêts
	#
	# V2:
	#	- Catégorie Supplémentaire:
	#		- Unit
	#		- Build
	#		- Event_Image
	#		- Sound
	#
	####################
	# !!!! Voir Pour le cout en mémoire de la fonction !!!!
	####################
	# Si on concidère que le cout en mémoire est trop important on peu remplacer le fichier ouvert par le chemin du fichier
	# Ex: Oceans: ["Ocean.png", "/Asset/terrain/Ocean/Ocean.png"]
	#
	#
	####################
	#
	# À modifier pour prendre en compte des Sous-Dossiers
	#
	#
	####################

	#On se place dans le dossier Asset puis dans texture
	pf = c_d+"/Asset/texture"
	#print(pf)
	#print(len(os.listdir()))
	# On créer le Dico que l'on va renvoyer:
	dico_file = {"mountains": [],"ocean": [],"plains": [],"forest": [],"build":[],"event":[],"unit":[] ,"other": []}


	dico_file = exploresubfolder(dico_file, pf)
	
	return dico_file





def exploresubfolder(dico_file, filepath):

	####################
	# Fonction appeler pour explorer les sous-dossier et remplir le dico avec les fichier .png trouver
	####################

	for file in os.listdir(filepath):
		# Si ce n'est pas un fichier .png c'est un sous dossier qye l'on explore dans un sous appel de la même fonction
		if (file[-4:] != ".png") and (file != ".DS_Store" ):
			dico_file = exploresubfolder(dico_file, filepath+"/"+file)
		# Sinon c'est un fichier que l'on teste
		else:
			if file != ".DS_Store":
				#print(filepath, filepath[-5:], file)
				#On vérifier que le nom du fichier correspond à l'un des 4 types définies
				if file[:9] == "mountains":
					#print(sub_folder[:9])
					dico_file["mountains"] += [[file,loadtexturedico(filepath+"/"+file)]]
				elif file[:5] == "ocean":
					#print(sub_folder[:5])
					dico_file["ocean"] += [[file,loadtexturedico(filepath+"/"+file)]]
				elif file[:6] == "plains":
					#print(sub_folder[:6])
					dico_file["plains"] += [[file,loadtexturedico(filepath+"/"+file)]]
				elif file[8:14] == "forest":
					#print(sub_folder[8:14])
					dico_file["forest"] += [[file,loadtexturedico(filepath+"/"+file)]]
				# Si présent dans le dossier build
				elif filepath[-5:] == "build":
					dico_file["build"] += [[file, loadtexturedico(filepath+"/"+file)]]
				# Si présent dans le dossier event
				elif filepath[-5:] == "event":
					dico_file["event"] += [[file, loadtexturedico(filepath+"/"+file)]]
				# Si présent dans le dossier unit
				elif filepath[-4:] == "unit":
					dico_file["unit"] += [[file, loadtexturedico(filepath+"/"+file)]]
				#Si il n'est rentrée dans aucun des 4 types il rentre dans other
				else:
					#print(sub_folder)
					dico_file["other"] += [[file,loadtexturedico(filepath+"/"+file)]]
	return dico_file



def loadtexturedico(filepath):
	####################
	# Fonction appeler pour constuire le dico
	####################

	img = Image.open(filepath)
	return img




def loadtexture(filepath, sizetuile):

	####################
	# Fonction appeler quand ont veut charger une image non présente dans le dico
	####################
	# On recup le chemin absolue du fichier
	fp = c_d + filepath
	#print(fp)
	# On charge l'image
	img = Image.open(fp)
	# On resize l'image 
	# https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters
	img = img.resize((sizetuile,sizetuile), Image.BOX)
	#On adapte l'image pour le format de Tkinter
	return ImageTk.PhotoImage(img)


def randomloadtexturefromdico(dico_file, type, sizetuile):
	####################
	# Fonction qui va charger une image Aléatoire depuis le dico
	# l'image est resize à la taille d'une tuile
	####################
	if type in dico_file.keys():
		r = random.randrange(len(dico_file[type]))
		img = dico_file[type][r][1]
		img = img.resize((sizetuile,sizetuile), Image.BOX)
		return [dico_file[type][r][0], ImageTk.PhotoImage(img)]
	else:
		print("erreur type non présent dans les clé du dico")
		print(dico_file.keys())

def randomtexturefromdico(dico_file, type):
	####################
	# Fonction qui va renvoyer le nom d'une texture Aléatoire depuis le dico du type désirer
	####################
	if type in dico_file.keys():
		r = random.randrange(len(dico_file[type]))
		texture_name = dico_file[type][r][0]
		return texture_name
	else:
		print("erreur type non présent dans les clé du dico")
		print(dico_file.keys())


def loadtexturefromdico(dico_file, filename, type, sizetuile):
	####################
	# Fonction qui va charger une image depuis le dico
	# l'image est resize à la taille d'une tuile
	####################
	# dico_file 	--> Le dico ou on va chercher le fichier
	# filename 		--> le nom du fichier
	# type 			--> le type du fichier
	# sizetuile 	--> la taille voulu
	####################

	# On cherche l'image dans le dico
	index = -1
	for ele in range(len(dico_file[type])):
		if dico_file[type][ele][0] == filename:
			index = ele

	# Si on l'a trouvé on continue
	if index != -1:
		img = dico_file[type][index][1]
		img = img.resize((sizetuile,sizetuile), Image.BOX)
		return [filename, ImageTk.PhotoImage(img)]

	# Sinon on renvoit une erreur
	else:
		print("erreur fichier non trouvé")


def loadnamedico(filepath):
	####################
	# Fonction qui va revnoyer un dico ayant la liste de nom séparé en 3 partie:
	#	Nom
	#	Surnom
	#	NomVillage
	####################

	# On créer le dico
	dico_name = {"Nom":[], "Surnom":[], "Village":[]}
	# On ouvre le fichier name.txt
	f = open(filepath, "r")
	#print(f.read())

	#
	var = ""

	# On se balade dans le fichier
	line = f.readline()
	while(line != ""):
		if line[:4] == "Nom:":
			var = "Nom"
		elif line[:7] == "Surnom:":
			var = "Surnom"
		elif line[:8] == "Village:":
			var = "Village"
		else:
			# on evite de prendre en compte les saut à la ligne
			if line[-1:] == "\n":
				dico_name[var] += [line[:-2]]
			else:
				dico_name[var] += [line]
		line = f.readline()


	# On ferme le fichier
	f.close()
	#print(dico_name)
	# On renvoi le dico
	return dico_name

###############################################################################


if __name__ == '__main__':


	atlas = createAtlas()
	#### Test Dico ####
	dico_file = assetLoad()
	#for key in dico_file.keys():
	#	print(key,dico_file[key])
	#	print("\n")
	####################
	#print(dico_file["build"])
	#print(dico_file["ocean"])



	#### Test Chargement Image ####
	
	root = tkinter.Tk()
	tp = tkinter.Toplevel(root)
	frame = tkinter.Frame(tp)
	frame.pack(expand = "True", fill = "both")
	canvas = tkinter.Canvas(frame)

	tk_image = randomloadtexturefromdico(dico_file, "forest", 200)
	label = tkinter.Label(image = tk_image[1])
	label.image = tk_image[1]
	atlas = addAtlas(atlas,label,tk_image[0])


	canvas.pack(expand = "True", fill = "both")
	tk_image2 = loadtexturefromdico(dico_file, "plains.png", "plains", 200)[1]
	canvas.create_image(0, 0, image = tk_image2)
	canvas.create_image(0, 0, image = atlas[tk_image[0]].image)

	canvas.create_image(200, 0, image = tk_image2)
	canvas.create_image(200, 0, image = atlas[tk_image[0]].image)

	canvas.create_image(400, 0, image = tk_image2)
	canvas.create_image(400, 0, image = atlas[tk_image[0]].image)


	canvas.create_image(600, 0, image = tk_image2)
	canvas.create_image(800, 0, image = atlas[tk_image[0]].image)

	root.mainloop()

	################################



