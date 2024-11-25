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
# Calcul la Menace Des Autres Seigneurs
# - Puissance * Distance avec territoires
# Si La Menace est Importante est que la Puissance est Égal alors déclare la guerre
#
#
######
# Plusieurs Caractères:
# - Expantioniste, Privilège l'expansion par Construction de Village
# - Militariste, Privilège l'expansion par Conquête
# - Économiste, Privilège une aproche plus économiste
#
######
# Construction de Village:
# - Si Expantioniste Construit dés qu'il peut
# - Sinon Construit Si il a le triple des Ressources Nécessaires
#
######
# Vassalisation:
# - Si la possibilité de Vassaliser un Seigneurs atteint 75%, tente de le Vassaliser
#
#
######
# Immigration:
# - 
# - 
######
# Armé:
# - Si possède 4*Cout de prode
# - Si possède 4*Entretien
######


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