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
#	--> Quand un village est construit il est automatiquement 
#
#	Conditions pour créer un Village:
#		--> ressource = 10
#		--> money = 4
#
#	Conditions pour créer une Église:
#		--> ressource = 4 
#		--> money = 4
#
####################

class Classlord:
	####################
	# Class Seigneur 
	####################

	def __init__(self, lordname: str, player: bool, id: int):

		self.idlord = 0

		self.personnal_ressource = 10
		self.personnal_money = 10

		self.nb_ressource = 0
		self.nb_money = 0
		self.power = 0

		self.nb_population = 0

		self.global_joy = 0

		self.lordname = lordname
		self.player = player

		# liste des vassaux
		# d'autre seigneurs
		self.vassal = []

		# Liste du territoire gérer directement par le seigneur
		# Object village
		self.fief = []

		# Liste des Armées
		self.army = []

		# Liste des seigneur avec les quelles on est en guerres
		self.war = []

		#Type du seigneur si non joueur, cela vient coder son comportement
		# liste de type: ["expansionniste", "belliciste", "économique"]
		# Pour plus tard
		self.type = 0

	def createarmy(self, village):
		print("On créer une armée dans le village: ", village.name)
		self.army += [Classarmy(village.x, village.y, ("unit_" + village.name))]

	def addvassal(self, vassal):
		self.vassal += [vassal]
		self.updateinfo()

	def addfief(self, village):
		self.fief += [village]
		village.setlord(self)
		self.updateinfo()

	def updateinfo(self):
		############
		# On update les données du seigneur
		# selon les vassaux
		# Selon les villages directement possédés
		# Selon les troupes
		############

		temp_joy = 0
		self.nb_ressource = self.personnal_ressource
		self.nb_money = self.personnal_money
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

		# On calcule les troupes
		for army in self.army:
			power += army.power

	def endofturn(self):
		for village in self.fief:
			village.endofturn()



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

		self.influence = 0

		self.church = 0

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
		#print("lord: ",self.lord)
		# Une fois mis à jour on mets à jour pour le seigneur du village
		# 'list' object has no attribute 'updateinfo'
		if self.lord != 0:
			self.lord.updateinfo()

	def buildchurch(self, name):
		# On définit que le village à une église
		self.church = 1
		# On créer le prêtre associé à l'église
		self.priest = Classpriest(name)


	#lord: Classlord
	def setlord(self, lord):
		self.lord = lord

	#priest: Classpriest
	def setpriest(self, priest):
		self.priest = priest

	def setnamevillage(self, name):
		self.name = name

	def endofturn(self):
		for pop in self.population:
			pop.endofturn()


# Classe qui vient définir une armée
class Classarmy:

	def __init__(self, x, y, name:chr):
		# Nom de la troupe
		self.name = name

		# position actuelle de la troupe
		self.x = x
		self.y = y
		# objet tuile
		self.idCanv = 0


		# Chevalier qui mène la troupe
		self.knight = 0
		# Liste de pop
		self.unit = []

		# Puissance de la troupe
		self.power = 0

		# Déplacement possible de la troupe
		self.movecapacity = 0
		self.moveturn = self.movecapacity

		# Texture de l'armée
		self.texture = 0

	def recruitknight(self, name:chr):
		#######
		# Méthode pour recruter un Chevalier
		#######
		self.knight = ClassKnight(name)


	def recruitsoldier(self, name:chr):
		#######
		# Méthode pour recruter un Soldat
		#######
		self.unit += [ClassSoldier(name)]

	def updatearmy(self):
		#######
		# Méthode pour Update les infos de l'armée
		#######

		# On update la capacité militaire
		self.power = 0
		if self.knight != 0:
			self.power = self.knight.power
		for unit in self.unit:
			self.power += unit.power

		# On update la capicité de mouvement
		self.movecapacity = 0
		# Si soldat et knight
		if (self.knight != 0) and (len(self.unit) != 0):
			self.movecapacity = 7
		# Sinon si seulement knight
		elif self.knight != 0:
			self.movecapacity = 10
		# Sinon si seulement unit
		elif len(self.unit) != 0:
			self.movecapacity = 4
		self.moveturn = self.movecapacity



	def updatemovementcapacity(self):
		#######
		# Méthode pour update la capacité de mouvement
		#######
		pass

	def movearmy(self):
		#######
		# Méthode pour déplacer l'armée
		#######
		pass


class Classpriest:

	def __init__(self, name):
		self.name = name
		self.ressource = 0
		self.money = 0
		self.joy = 50

	def setname(self, name):
		self.name = name



#Classe générale:
class ClassHuman:

	def __init__(self, name):
		self.name = name
		self.ressource = 1
		self.money = 0
		self.joy = 50
		#capacité de production
		self.cp = 2
		self.age = random.randrange(15,30)

	def endofturn(self):
		pass



class ClassKnight:

	def __init__(self, name:chr):
		self.name = name
		self.ressource = 10
		self.money = 10
		self.joy = 50
		self.age = random.randrange(15,30)
		self.power = 10
		self.movecapacity = 10


class ClassSoldier:

	def __init__(self, name:chr):
		self.name = name
		self.ressource = 1
		self.money = 0
		self.joy = 50
		self.age = random.randrange(15,30)
		self.power = 1
		self.movecapacity = 4

