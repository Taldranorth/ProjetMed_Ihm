import tkinter
import random


####################
#
# Utiliser un Id pour séparer les instance ?
#
#
# 1 classe Empire:
#			- Total Ressource
#			- Total Or
#			- Total Population
#			- Noble Assujeti
#			- 
#
#
#
# 1 classe générale:
#			- Nom
#			- Age
#			- Ressource
#			- Or
#
# 2 sous-classe noble:
#	Seigneur:
# 			- Territoire attaché
#			- Titre
#
#	Chevalier:
#			- Territoire attaché
#
# 1 sous-classe clergé:
#	Prêtre:
#			- Église attaché
#			- Don
#
#
#
# 1 sous-classe Tier États
#	Paysans:
#			- Village attaché
#			
# Village:
#	--> Seigneur
#	--> Territoire associé
#		--> Quand un villageois travail sur une plaine un Champ apparaît
#
####################




class kingdom(object):
	def __init__(self):
		pass
	pass

class Classvillage:

	def __init__(self,x,y):
		self.name = "test"
		self.x = x
		self.y = y

		self.population = []
		self.priest = 0
		self.lord = 0

		self.money = 0
		self.ressource = 0
		self.global_joy = 100

	#pop: Classhuman	
	def addpopulation(self, pop):
		self.population += [pop]

		# Calcul de la joie global du village
		temp_joy = 0
		for pop in self.population:
			temp_joy += pop.joy
		self.global_joy = temp_joy/len(self.population)

		self.money += pop.money
		self.ressource += pop.ressource
		print("lord: ",self.lord)
		# Une fois mis à jour on mets à jour pour le seigneur du village
		# 'list' object has no attribute 'updateinfo'
		if self.lord != 0:
			self.lord.updateinfo()

	#lord: Classlord
	def setlord(self, lord):
		self.lord = lord

	#priest: Classpriest
	def setpriest(self, priest):
		self.priest = priest

	def setnamevillage(self, name):
		self.name = name




class Classlord:

	def __init__(self, lordname: str, player: bool):

		self.personnal_ressource = 10
		self.personnal_money = 10

		self.nb_ressource = 0
		self.nb_money = 0

		self.nb_population = 0

		self.global_joy = 0

		self.lordname = lordname
		self.player = player

		# liste des vassaux
		# d'autre seigneurs
		self.vassal = []

		# Liste du territoire gérer directement par le seigneur
		self.fief = []


	def addvassal(self, vassal):
		self.vassal += [vassal]

	def addfief(self, village):
		self.fief += [village]

	def updateinfo(self):
		############
		# On update les données du seigneur
		# selon les vassaux
		# Selon les villages directement possédés
		############

		temp_joy = 0
		# On calcul pour les vassaux
		for vassal in self.vassal:
			self.nb_ressource += vassal.nb_ressource
			self.nb_money += nb_money
			temp_joy += vassal.global_joy

		# On calcul pour le fief
		for village in self.fief:
			self.nb_ressource += village.ressource
			self.nb_money += village.money
			temp_joy += village.global_joy

		self.global_joy = temp_joy/(len(self.vassal)+len(self.fief))



		


#Classe générale:
class ClassHuman:

	def __init__(self, name):
		self.name = name
		self.ressource = 0
		self.money = 0
		self.joy = 100







