import tkinter


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

class Classvillage(object):

	def __init__(self,x,y):
		self.name = "test"
		self.x = x
		self.y = y

		self.population = []
		self.priest = ""
		self.lord = ""

	#pop: Classhuman	
	def addpopulation(self, pop):
		self.population += [pop]

	#lord: Classlord
	def setlord(self, lord):
		self.lord = lord

	#priest: Classpriest
	def setpriest(self, priest):
		self.priest = priest

	def setnamevillage(self, name):
		self.name = name




class Classlord(object):

	def __init__(self, lordname: str, player: bool):

		self.nb_ressource = 10
		
		self.nb_money = 10

		self.nb_population = 0

		self.global_joy = 0

		self.name = lordname
		self.player = player

		self.vassal = []

		self.fief = []


	def addvassal(self, vassal):
		self.vassal += [vassal]

	def addfief(self, village):
		self.fief += [village]


#Classe générale:
class ClassHuman(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg







