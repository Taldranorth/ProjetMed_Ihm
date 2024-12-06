import random


######################### Description du fichier	#########################
# 
# Liste de tout les event avec leur fonction associer
#
# Postive:
#	Récolte Abondante:
#		--> Production de Ressource Doublées pour les paysan
#
#	Subvention du Clergé:
#		--> Une construction d'église est gratuites
#
#	Immigration:
#		--> Récupère un Nombre aléatoires de paysan et/ou Artisan
#
#	Armée Volontaires:
#		--> Récupère un Nombre aléatoires de Soldat

# Neutre:
#	armé de Mercenaire:
#		--> Une armée indépendante apparait
#
#	Un nouveau Village:
#		--> Un nouveau Village indépendant apparait
#
#

#	Négatif:
#	La Peste Mon Seigneur!: 
#		--> Une partie de la Population Meurt
#
#
#	Un Incendies Mon Seigneur !:
#		--> Un Village est rayer de la carte
#
#	Des Pillars Mon Seigneur!:
#		--> Vol de Ressource et d'argent dans un Village
#
#	La Famine:
#		--> Mets la production de Ressource à 0
#
#	Nouvelle Foi: 
#		--> Bloque la capacité du Prêtre et baisse le Bonheur dans le Village
#			--> Peut évoluer en un nouvelle event qui peut faire séparer une partie des Villages
#
#	Famine:
#		--> Si niveau de ressource dans un village bas
#			--> Réduit le Rendement du village
#
#	Attaque de Mildiou:
#		--> réduit la Production de Ressource des Paysan
#
#
#
#################### Réaction #########################
#
#	Séparation du VIllage:
#		--> Quand le Bonheur est bas, 
#	
#
#
#
#
# 
#############################################################################

##################
# - À chaque début de tour chaque joueur va tirer un chiffre aléatoire
# - Selon le Chiffre tirer 
#
#
##################

class Classevent:

	def __init__(self):
		# Contient la liste des evenement
		self.listevent = ["nothing", "plague", "famine"]

	def randomevent(self):
		r = random.randrange()
		pass

	def event_plague(self):
		pass

	def event_famine(self):
		pass






