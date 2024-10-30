import sys
import tkinter
from PIL import ImageTk, Image, ImageShow
import random


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
#
#
#
#
#
#
#
#############################################################################

################## Objet qui ne doivent pas être Enregistrer ################
# - les Images
#
#
#
#
#
#
#############################################################################









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
	#	transformer Foret en un Sous-dico afin de prendre en compte plusieurs biomes possible de forêts
	#
	#
	#
	####################
	# !!!! Voir Pour le cout en mémoire de la fonction !!!!
	####################

	#On se place dans le dossier Asset puis dans Terrain
	pf = c_d+"/Asset/terrain/"
	#print(pf)
	#print(len(os.listdir()))
	# On créer le Dico que l'on va renvoyer:
	dico_file = {"mountains": [],"ocean": [],"plains": [],"forest": [],"other": []}

	#On se balade dans le dossier
	for t_folder in os.listdir(pf):
		#LE PUTAIN DE .DS_Store M'EMMERDE RAHHHHHHHHH
		if t_folder != ".DS_Store":
			#Si ne finit pas par .png c'est un dossier
			if t_folder[-4:] != ".png":
				#On se balade dans le sous dossier
				for sub_folder in os.listdir(pf+t_folder):
					print(sub_folder)
					if sub_folder != ".DS_Store":
						#On vérifier que le nom du fichier correspond à l'un des 4 types définies
						if sub_folder[:9] == "mountains":
							print(sub_folder[:9])
							dico_file["mountains"] += [[sub_folder,loadtexturedico(pf+t_folder+"/"+sub_folder)]]
						elif sub_folder[:5] == "ocean":
							print(sub_folder[:5])
							dico_file["ocean"] += [[sub_folder,loadtexturedico(pf+t_folder+"/"+sub_folder)]]
						elif sub_folder[:6] == "plains":
							print(sub_folder[:6])
							dico_file["plains"] += [[sub_folder,loadtexturedico(pf+t_folder+"/"+sub_folder)]]
						elif sub_folder[8:14] == "forest":
							print(sub_folder[8:14])
							dico_file["forest"] += [[sub_folder,loadtexturedico(pf+t_folder+"/"+sub_folder)]]
						#Si il n'est rentrée dans aucun des 4 types il rentre dans other
						else:
							print(sub_folder)
							dico_file["other"] += [[sub_folder,loadtexturedico(pf+t_folder+"/"+sub_folder)]]

			#Sinon c'est un fichier que l'on doit charger
			else:
				print(t_folder)
				dico_file["other"] += [[t_folder,loadtexturedico(pf+t_folder)]]

	#print("Mountains: ",dico_file["mountains"])
	#print("ocean: ",dico_file["ocean"])
	#print("Plains: ",dico_file["plains"])
	#print("Forest: ",dico_file["forest"])
	#print("Other: ",dico_file["other"])
	
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


def loadtexturefromdico(dico_file, filename, type, sizetuile):
	####################
	# Fonction qui va charger une image depuis le dico
	# l'image est resize à la taille d'une tuile
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
		return [dico_file[type][index][0], ImageTk.PhotoImage(img)]

	# Sinon on renvoit une erreur
	else:
		print("erreur fichier non trouvé")



if __name__ == '__main__':


	#### Test Dico ####
	dico_file = assetLoad()
	for key in dico_file.keys():
		print(key,dico_file[key])
		print("\n")
	####################



	#### Test Chargement Image ####
	
	root = tkinter.Tk()
	tp = tkinter.Toplevel(root)
	frame = tkinter.Frame(tp)
	frame.pack()
	canvas = tkinter.Canvas(frame)

	tk_image = randomloadtexturefromdico(dico_file, "ocean", 100)[1]

	canvas.pack()
	canvas.create_image(0, 0, image = tk_image)
	tk_image2 = loadtexturefromdico(dico_file, "plains.png", "plains", 500)[1]
	canvas.create_image(500, 0, image = tk_image2)

	root.mainloop()

	################################



