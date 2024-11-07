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

class village(object):

	def __init__(self):
		pass

	pass




class lord(object):

	def __init__(self, lordname: str):

		self.nb_ressource = 10
		#self.nb_ressource = tkinter.IntVar()
		#self.nb_ressource.set(10)

		self.nb_money = 10
		#self.nb_money = tkinter.IntVar()
		#self.nb_money.set(10)

		self.nb_population = 0
		#self.nb_population = tkinter.IntVar()
		#self.nb_population.set(10)

		self.global_joy = 0
		#self.global_joy = tkinter.IntVar()
		#self.global_joy.set(10)

		self.name = lordname


#Classe générale:
class Humain(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg







