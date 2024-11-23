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

	def __init__(self, lordname: str, player: bool, idlord: int):

		self.idlord = idlord

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

	def removevassal(self, vassal):
		# On retire le vassal de la liste des vassaux
		if len(self.vassal)>1:
			i = 0
			while i< len(self.vassal):
				if self.vassal[i] == vassal:
					self.vassal = self.vassal[:i] + self.vassal[i+1:]
					return True
		elif len(self.vassal) == 1:
			if self.vassal[0] == vassal:
				self.vassal = []
				return True

		return False


	def removefief(self, village):
		# On Unbind le seigneur de l'objet village
		village.lord = 0
		# On retire le village de la liste des fief
		if len(self.fief) > 1:
			i = 0
			while i < len(self.fief):
				if self.fief[i] == village:
					self.fief = self.fief[:i] + self.fief[i+1:]
					# On renvoit True pour indiquer que l'éxécution est correcte
					return True
		elif len(self.fief) == 1:
			if self.fief[0] == village:
				self.fief = []
				return True
		return False

	def addwar(self, lord):
		############
		# Fonction appeler pour ajouter un seigneur et ses vassaux à la liste des Seigneurs en Guerre
		############
		# On ajoute les Vassaux
		for vassal in lord.vassal:
			self.war += [vassal]
		# On ajoute le Seigneur lui même
		self.war += [lord]

	def removewar(self, lord):
		############
		# Fonction appeler pour retirer un seigneur et ses vassaux de la liste des Seigneurs en Guerre
		############

		# On retire le lord
		i = 0
		found = False
		print(f"On cherche {lord,lord.lordname} dans la liste war{self.war}")
		while (i < len(self.war)) and (found != True):
			# une fois le seigneur trouver On le supprime de la liste
			if self.war[i] == lord:
				self.war = self.war[:i] + self.war[i+1:]
				print(f"On à trouver, liste war changer: {self.war}")
				found = True

		# On retire les vassaux du lord
		# Récursif
		for vassal in lord.vassal:
			self.removewar(vassal)

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
			self.power += army.power

	def endofturn(self):
		#######
		# Méthode fin de tour
		#######

		# On appels la fin de tour pour les armées
		for army in self.army:
			army.endofturn()

		# On appels la fin de tour pour les villages
		for village in self.fief:
			village.endofturn()



class Classvillage:

	def __init__(self,x,y):
		self.name = "test"
		# Coordonnées Map
		self.x = x
		self.y = y

		self.population = []
		self.priest = 0
		self.lord = 0
		self.nb_artisan = 0
		self.nb_paysan = 0

		self.money = 0
		self.ressource = 0
		self.global_joy = 100

		self.influence = 0

		self.church = 0

		self.border = 2

	#pop: Classhuman	
	def addpopulation(self, pop):
		self.population += [pop]
		# On incrémente le compteur de pop
		if pop.role == "artisan":
			self.nb_artisan += 1
		elif pop.role == "paysan":
			self.nb_paysan += 1

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
		#######
		# Méthode fin de tour
		#######		
		for pop in self.population:
			pop.endofturn(self.lord)


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
		self.updatearmy()


	def recruitsoldier(self, name:chr):
		#######
		# Méthode pour recruter un Soldat
		#######
		self.unit += [ClassSoldier(name)]
		self.updatearmy()

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

	def endofturn(self):
		#######
		# Méthode fin de tour
		#######

		# On appel la Methode Fin de tour pour le Chevalier
		self.knight.endofturn()

		#On appel la Methode Fin de tour pour les Soldats
		for soldier in self.unit:
			soldier.endofturn()

		# On update l'armée
		self.updatearmy()





class Classpriest:

	def __init__(self, name):
		self.name = name
		self.ressource = 0
		self.money = 0
		self.joy = 50
		self.aptitude = 0
		self.getaptitude()

	def setname(self, name):
		self.name = name


	def getaptitude():
		######
		# Methode qui fournit aux Prêtre une Capacité Aléatoire Passive 
		######
		#self.aptitude = 

		pass

	def endofturn(self):
		#######
		# Méthode fin de tour
		#######
		pass




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
		#######
		# Méthode fin de tour
		#######
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

	def endofturn(self):
		#######
		# Méthode fin de tour
		#######
		pass


class ClassSoldier:

	def __init__(self, name:chr):
		self.name = name
		self.ressource = 1
		self.money = 0
		self.joy = 50
		self.age = random.randrange(15,30)
		self.power = 1
		self.movecapacity = 4

	def endofturn(self):
		#######
		# Méthode fin de tour
		#######
		pass


"""
Classe Roturier pour représenter les paysans ou artisans avec des caractéristiques spécifiques 
et des actions comme la production et le paiement des impôts.
"""
class ClassRoturier:
	#starting_money= pécule initial des artisans (modifiable selon les besoins)
	#role = paysans ou artisans

	def __init__(self, name, role:str):
		# On commence par définir les données de base
		self.name = name
		self.ressource = 1
		self.money = 0
		self.joy = 50
		# capacité de production
		self.cp = 2
		self.age = random.randrange(15,30)
		# On change selon le rôle données
		self.role = role
		if role == "artisan":
			self.cp = 4
			self.money = 5

	def pay_tax(self, lord):
		#####
		# Method pour payer la taxe du Seigneur
		#####
		tax = 0

		# Selon le rôle du Roturier l'impôt est différent en Ressource et Argent
		if self.role == "paysans":
			tax = 1/2
		elif self.role == "artisan":
			tax = 1/4

		# Si le roturier peut payer en Argent il paye en argent
		if self.money > (10 * tax):
			m = self.tax_money()
			print(f"{self.name} un {self.role} à payer: {m} écu")
			lord.nb_money += m
			self.money -= m
		else:
			r = self.tax_ressource()
			print(f"{self.name} un {self.role} à payer: {r} Ressource")
			lord.nb_ressource += r
			self.ressource -= r

	def pay_tax_money(self, lord):
		#####
		# Method pour payer Une taxe Argent Spéciale au Seigneur
		#####
		money = self.tax_money()
		lord.nb_money += money
		self.money -= money


	def pay_tax_ressource(self, lord):
		#####
		# Method pour payer Une taxe Ressource Spéciale au Seigneur
		#####
		ressource = self.tax_ressource()	
		lord.nb_ressource += ressource
		self.ressource -= ressource


	def tax_money(self):
		#####
		# Fonction qui renvoit la tax Argent que peut payer le Roturier
		####
		money = 0

		if self.role == "paysan":
			money = int(self.money*(1/2))
		elif self.role == "artisan":
			money = int(self.money*(1/4))
		#print(money)
		return money

	def tax_ressource(self):
		#####
		# Fonction qui renvoit la tax Ressource que peut payer le Roturier
		####
		ressource = 0
		if self.role == "paysan":
			ressource = int(self.ressource*(1/2))
		elif self.role == "artisan":
			ressource = int(self.ressource*(1/4))
		# int() arrondi à l'inférieur hors on veut le supérieur
		# Spécialement quand le Roturier possède 1 de ressource en réserve
		if (ressource == 0) and (self.ressource > 0):
			ressource = 1
		#print(ressource)
		return ressource

	def produce(self):
		####
		# Methode pour produire la capacité de production en ressource
		####
		print(f"{self.name} un {self.role} à produit: {self.cp} ressource")
		self.ressource += self.cp

	def sell(self):
		####
		# Methode pour incrémenter l'argent du montant de ressource qu'il va vendre
		####
		# Si possède un nombre de Ressource > 10
		if self.ressource > 10:
			# On calcule le montant
			i = self.ressource - 10
			# On retire à ressource
			self.ressource -= i
			# On ajoute à argent
			self.money += i
			print(f"{self.name} un {self.role}: gagne {i} argent")

	def buy(self):
		####
		# Methode pour acheter une ressource si il en a plus
		####
		if self.ressource == 0:
			self.money -= 1
			self.ressource += 1

	def death(self):
		####
		# Methode qui tue le Roturier
		####
		pass


	def endofturn(self, lord):
		#######
		# Méthode de fin de tour
		# 1°) Le roturier produit sa capacité de production
		# 2°) il paye la taxe du Seigneur local
		# 3°) Si il n'a plus de ressource il en achète 1
		# 4°) Il consomme 1 de ressource
		# 5°) Si il atteint la capacité limite de Ressource il vend sont éxédent
		# 6°) On calcul son bonheur selon ses besoins
		# 7°)
		#######
		print(f"{self.name} un {self.role} Possède aux début du tour: {self.money} écu et {self.ressource} Ressource")
		# 1°) Produit la CP
		self.produce()

		# 2°) Si le Roturier possède un Seigneurs il paye la tax
		if lord != 0:
			self.pay_tax(lord)

		# 3°) Achete si il n'a plus de ressource
		self.buy()

		# 4°) Le Roturier se Nourrit
		self.ressource -= 1

		# 5°) Si le roturier possède de l'excedant il le vend contre de l'argent
		self.sell()
		print(f"{self.name} un {self.role} Possède à la fin du tour: {self.money} écu et {self.ressource} Ressource")

		# 6°) On update son humeur selon ses besoins

		# 7°) On Augmente son Age
		self.age += 1



