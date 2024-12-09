import os
import sys
import random
import tkinter

import functions.log as log

from PIL import ImageTk, Image, ImageShow

c_d = os.getcwd()

#########
# - Fichier Qui vient contenir les Dico et Fonctions liéers à la gestion des Assets:
#	-- Atlas qui vient contenir les textures préparés pour être utilisé
#	-- Dico_file qui vient contenir tout les fichiers texture chargés en mémoire
#	-- Dico_name qui vient contenir les noms chargé en mémoires
#########


########################\ 	Class Atlas 	\########################

class ClassAtlas:

	def __init__(self):
		self.dico = {}
		self.lframe = 0

	# Methode pour definir le labelframe
	def setlframe(self, lframe):
		self.lframe = lframe

	# Methode Atlas
	def addAtlas(self, label, filename):
		####################
		# Methode pour ajouter une nouvelle entré à l'Atlas
		####################		
		self.dico[filename] = label

	def checkAtlas(self, filename):
		####################
		# Methode pour voir si une texture est présente dans l'atlas
		####################
		if filename in self.dico.keys():
			return True
		else:
			return False

	def changelabelAtlas(self, filename, img):
		####################
		# Methode pour changer la texture associer à un label
		####################
		self.dico[filename].configure(image = img)
		self.dico[filename].image = img

	def loadtextureatlas(self, dico_file, tuilesize, texture_name, type):
		######
		# Methode pour charger dans l'atlas la texture viser
		######

		# Si la texture n'est pas déjà présent dans l'atlas on la prépare est place
		if self.checkAtlas(texture_name) == False:
			# On prépare la texture à la taille voulu
			tk_img = loadtexturefromdico(dico_file, texture_name, type, tuilesize)
			# On créer le label associer
			label = tkinter.Label(self.lframe, image = tk_img[1])
			label.image = tk_img[1]
			# On stocke le label dans l'atlas
			self.addAtlas(label, tk_img[0])

	def loadtextureatlassize(self, dico_file, texture_name, type, size):
		######
		# Methode pour charger dans l'atlas la texture viser avec une taille spécifique
		######
		# Si la texture n'est pas déjà présent dans l'atlas on la prépare est place
		if self.checkAtlas(texture_name) == False:
			# On prépare la texture à la taille voulu
			tk_img = loadtexturefromdico(dico_file, texture_name, type, int(size))
			print(tk_img)
			# On créer le label associer
			label = tkinter.Label(self.lframe, image = tk_img[1])
			label.image = tk_img[1]
			# On stocke le label dans l'atlas
			self.addAtlas(label, tk_img[0])


	def resizeatlas(self, dico_file, tuilesize):
		######
		# Methode pour resize toute les textures de l'atlas à la valeur indiqué
		######

		# Pour le tuple stocker dans l'atlas
		for key_atlas in self.dico.keys():
			# on cherche le type du fichier de l'atlas
			type = self.searchtexturetypeindico(dico_file, key_atlas)

			ts = tuilesize
			if type in ["soldier", "knight"]:
				ts = tuilesize/2

			# on recalcul l'image depuis son fichier source mais avec la nouvelle résolution
			tk_img = loadtexturefromdico(dico_file, key_atlas, type, int(ts))
			# On change le label associer à l'image
			self.changelabelAtlas(tk_img[0], tk_img[1])


	def searchtexturetypeindico(self, dico_file, texture_name):
		######
		# Fonction qui renvoit le type de la texture
		######	

		for key_type in dico_file.keys():
			# on cherche dans les tuples du type
			for entry in dico_file[key_type]:
				if texture_name in entry:
					return key_type

################################################################################################

######################## Fonction Dico_file ########################


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
	####################
	# Si on concidère que le cout en mémoire est trop important on peu remplacer le fichier ouvert par le chemin du fichier
	# Ex: Oceans: ["Ocean.png", "/Asset/terrain/Ocean/Ocean.png"]
	####################

	#On se place dans le dossier Asset puis dans texture
	pf = c_d+"/asset/texture"
	#print(pf)
	#print(len(os.listdir()))
	# On créer le Dico que l'on va renvoyer:
	dico_file = {"mountains": [],"ocean": [],"plains": [],"forest": [],"interface":[],"build":[],"event":[],"unit":[], "knight":[], "soldier":[] ,"other": []}


	dico_file = exploresubfolder(dico_file, pf)
	
	return dico_file


def exploresubfolder(dico_file, filepath):

	####################
	# Fonction appeler pour explorer les sous-dossier et remplir le dico avec les fichier .png trouver
	####################

	for file in os.listdir(filepath):
		#log.log.printinfo(f"Fichier chargés: {file}")
		# Si ce n'est pas un fichier .png c'est un sous dossier que l'on explore dans un sous appel de la même fonction
		if (file[-4:] != ".png") and (file != ".DS_Store" ):
			dico_file = exploresubfolder(dico_file, filepath+"/"+file)
		# Sinon c'est un fichier que l'on teste
		else:
			if file != ".DS_Store":
				#print(filepath+"/"+file)
				#On vérifier que le nom du fichier correspond à l'un des 4 types définies
				if file[:9] == "mountains":
					#print(sub_folder[:9])
					dico_file["mountains"] += [[file, filepath+"/"+file]]
				elif file[:5] == "ocean":
					#print(sub_folder[:5])
					dico_file["ocean"] += [[file, filepath+"/"+file]]
				elif file[:6] == "plains":
					#print(sub_folder[:6])
					dico_file["plains"] += [[file, filepath+"/"+file]]
				elif file[8:14] == "forest":
					#print(sub_folder[8:14])
					dico_file["forest"] += [[file, filepath+"/"+file]]
				# Si présent dans le dossier build
				elif filepath[-5:] == "build":
					dico_file["build"] += [[file, filepath+"/"+file]]
				# Si présent dans le dossier event
				elif filepath[-5:] == "event":
					dico_file["event"] += [[file, filepath+"/"+file]]
				# Si présent dans le dossier interface
				elif filepath[-9:] == "interface":
					dico_file["interface"] += [[file, filepath+"/"+file]]
				# Si présent dans le dossier unit
				elif filepath[-4:] == "unit":
					dico_file["unit"] += [[file, filepath+"/"+file]]
				# Si présent dans le dossier knight
				elif filepath[-6:] == "knight":
					dico_file["knight"] += [[file, filepath+"/"+file]]
				# Si présent dans le dossier soldier
				elif filepath[-7:] == "soldier":
					dico_file["soldier"] += [[file, filepath+"/"+file]]
				#Si il n'est rentrée dans aucun des 4 types il rentre dans other
				else:
					#print(sub_folder)
					dico_file["other"] += [[file, filepath+"/"+file]]
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
		img = loadtexturedico(dico_file[type][r][1])
		img = img.resize((sizetuile,sizetuile), Image.BOX)
		l = [dico_file[type][r][0], ImageTk.PhotoImage(img)]
		img.close()
		return l
	else:
		log.log.printinfo("erreur type non présent dans les clé du dico")
		log.log.printinfo(f"{dico_file.keys()}")

def randomtexturefromdico(dico_file, type):
	####################
	# Fonction qui va renvoyer le nom d'une texture Aléatoire depuis le dico du type désirer
	####################
	if type in dico_file.keys():
		r = random.randrange(len(dico_file[type]))
		texture_name = dico_file[type][r][0]
		return texture_name
	else:
		log.log.printinfo("erreur type non présent dans les clé du dico")
		log.log.printinfo(f"{dico_file.keys()}")


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
	try:

		# On cherche l'image dans le dico
		index = -1
		for ele in range(len(dico_file[type])):
			if dico_file[type][ele][0] == filename:
				index = ele

			# Si on l'a trouvé on continue
			if index != -1:
				img = loadtexturedico(dico_file[type][index][1])
				img = img.resize((sizetuile,sizetuile), Image.BOX)
				l = [filename, ImageTk.PhotoImage(img)]
				img.close()
				return l
	except:
		log.log.printerror(f"erreur fichier {filename} non trouvé dans registre {type}")

################################################################################################

######################## Class Dico_Name ########################

class ClassDicoName:

	def __init__(self):
		self.dico = self.loadnamedico(os.getcwd()+"/asset/name.txt")

	def loadnamedico(self, filepath):
		####################
		# Fonction qui va renvoyer un dico ayant la liste de nom séparé en 3 partie:
		#	Nom
		#	Surnom
		#	NomVillage
		# + une variable int initialisé à 0 qui permet de compter le nombre de fois que le nom est utilisé
		####################

		# On créer le dico
		dico_name = {"Nom":[], "Surnom":[], "Village":[]}
		# On ouvre le fichier name.txt
		f = open(filepath, "r")
		#print(f.read())

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
					dico_name[var] += [[line[:-1], 0]]
				else:
					dico_name[var] += [[line, 0]]
			line = f.readline()

		# On ferme le fichier
		f.close()
		return dico_name

	def randomnametype(self, type):
		####
		# Methode qui renvoit un Nom aléatoire du type voulu
		####
		try:
			r = random.randrange(len(self.dico[type]))
			# Si c'est un Surnom ou NomVillage déjà utilisé on regen
			if (self.dico[type][r][1] == 1) and (type != "Nom"):
				r = random.randrange(len(self.dico[type]))
			# On met à 1 le compteur pour indiquer que le nom est utiliser
			self.dico[type][r][1] = 1
			name = self.dico[type][r][0]
			return name
		except:
			self.log.printerror("type :"+type+"non présent dans le dico")

	def freename(self, type, name):
		#####
		# Methode pour libérer un nom utilisé
		#####
		i = 0
		while self.dico[type][i][0] != name:
			i += 1
		log.log.printinfo(f"index du Nom trouvé i:{i}")
		log.log.printinfo(f"On libére {name}")
		self.dico[type][i][1] = 0


#################################################################

########## Main #########
# Dico des noms
dico_name = ClassDicoName()
log.log.printinfo(f"Dico des Noms chargés")

# Dico des Assets
dico_file = assetLoad()
log.log.printinfo(f"Dico des Assets chargés")

# Atlas des Textures
atlas = ClassAtlas()
log.log.printinfo(f"Atlas Créer")




