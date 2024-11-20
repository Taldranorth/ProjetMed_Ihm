import time
import random

import functions.interface as interface


#########################
# Fichier qui vient contenir les fonctions liées à la gestion de l'ia
#
#
#########################
# - Utiliser Automate fini Déterministe
# - Utiliser un arbre de priorité
#	--> Faire un graphe papier
#	--> Utiliser grammaire
#
#
#########################

def mainai(gamedata, classmap, option):
	
	# ON affiche la banderole que l'ia Joue
	banderole_window = interface.banderole(gamedata, classmap, option)

	lord = gamedata.list_lord[gamedata.Nb_toplay]

	#L'Ia joue

	# Une fois que l'ia à terminé on incrémente Nb_toplay
	gamedata.Nb_toplay += 1
	# Supprime la banderole
	interface.destroybanderole(gamedata, classmap, banderole_window)
	# Et On rend les clés de la Maison,le sémaphore
	gamedata.semaphore = False

def actionbuildvillage():
	pass

def actionbuildchurch():
	pass

def actiontax():
	pass

def actionimmigration():
	pass


def actionwar():
	pass

def actionarmymovement():
	pass

def actionsubjugation():
	pass