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

		self.nb_ressource = 10
		self.nb_money = 10
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

	def createarmy(self, name, x, y):
		# On vérifie qu'il n'y a pas déjà une armée à cette position
		print("On créer une armée dans le village: ", name)
		self.army += [Classarmy(x, y, ("unit " + name))]

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

	def verifcost(self, nb_m, nb_r):
		######
		# Method qui vérifie si il y a suffisament en stock
		# Return True si il y a suffisament
		# Return False Sinon
		######
		if self.nb_money < nb_m:
			return False
		if self.nb_ressource < nb_r:
			return False

		return True

	def sub_ressource(self, nb_r: int):
		#####
		# Methode pour retirer au Seigneurs nb_r Ressource
		#####
		self.nb_ressource -= nb_r

	def sub_money(self, nb_m: int):
		#####
		# Methode pour retirer au Seigneurs nb_m Argent
		#####
		self.nb_money -= nb_m	

	def prod_global(self):
		####
		# Methode qui retourne un tuple qui repèsente la production global de son fief
		####
		prod_money = 0
		prod_ressource = 0
		for village in self.fief:
			prod_money += village.prod_money
			prod_ressource += village.prod_ressource


		return [prod_money, prod_ressource]

	def total_pop(self):
		####
		# Methode qui retourne le nombre total de Pop
		####
		tpop = 0
		for village in self.fief:
			tpop += len(village.population)
		return tpop

	def total_salaryarmy(self):
		r = 0
		m = 0
		for army in self.army:
			salary = army.salarycount()
			r += salary[1]
			m += salary[0]

		return [m, r]


	def tax(self, lord):
		#########
		# Methode Pour payer la taxe envers le Seigneur Régent
		# Doit payer 1/4 des Ressources et Argent
		# Si il ne peut pas payer va levé une tax d'urgence afin de payer au seigneur
		#########

		# On calcul la somme que peut payer le Noble en Ressource et Argent
		tax_money = int(self.nb_money*(1/4))
		tax_ressource = int(self.nb_ressource*(1/4))

		# Si l'une des 2 ressources est null le Noble toit lever une Tax Exceptionnelle pour pouvoir payer Son Seigneur
		if (tax_ressource == 0) and (tax_money == 0):
			for village in self.fief:
				for pop in village.population:
					pop.pay_tax_money(self)
					pop.pay_tax_ressource(self)
			# On recalcul la somme que doit payer le Noble
			tax_money = int(self.nb_money*(1/4))
			tax_ressource = int(self.nb_ressource*(1/4))
		elif (tax_ressource == 0):
			for village in self.fief:
				for pop in village.population:
					pop.pay_tax_ressource(self)
			# On recalcul la somme que doit payer le Noble
			tax_ressource = int(self.nb_ressource*(1/4))
		elif (tax_money == 0):
			for village in self.fief:
				for pop in village.population:
					pop.pay_tax_money(self)
			# On recalcul la somme que doit payer le Noble
			tax_money = int(self.nb_money*(1/4))


		print(f"Moi {self.lordname}: Paye {tax_money} écu à Mon Liege: {lord.lordname}")
		print(f"Moi {self.lordname}: Paye {tax_ressource} ressource à Mon Liege: {lord.lordname}")
		# Le Noble paye la tax
		lord.nb_money += tax_money
		self.nb_money -= tax_money
		lord.nb_ressource += tax_ressource
		self.nb_ressource -= tax_ressource

	def updateinfo(self):
		############
		# On update les données du seigneur
		# selon les vassaux
		# Selon les villages directement possédés
		# Selon les troupes
		############

		temp_joy = 0
		# On calcul pour les vassaux
		for vassal in self.vassal:
			temp_joy += vassal.global_joy

		# On calcul pour le fief
		for village in self.fief:
			temp_joy += village.global_joy

		self.global_joy = temp_joy/(len(self.vassal)+len(self.fief))

		# On calcule les troupes
		for army in self.army:
			self.power += army.power

	def endofturn(self, gamedata):
		#######
		# Méthode fin de tour
		#######

		# On appels la fin de tour pour les armées
		for army in self.army:
			army.endofturn(self)

		# On appels la fin de tour pour les villages
		for village in self.fief:
			village.endofturn(gamedata)

		# On demande au vassaux de payer la tax annuelle
		for vassal in self.vassal:
			print("On tax le vassal: ",vassal.lordname)
			vassal.tax(self)

		# On update les infos du Seigneurs
		self.updateinfo()



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

		self.prod_money = 0
		self.prod_ressource = 0
		self.global_joy = 100

		self.influence = 0

		self.church = 0

		self.border = 2

	def addpopulation(self, pop):
		#####
		# Method Pour ajouter un Roturier à la liste de population du village
		#####
		self.population += [pop]
		# On incrémente le compteur de pop
		if pop.role == "artisan":
			self.nb_artisan += 1
		elif pop.role == "paysan":
			self.nb_paysan += 1

		self.updateinfo()

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

		# On applique la capacité du prêtre à la population du village
		self.translateprietcapacity(self.priest.ability)


	def translateprietcapacity(self, ability):
		####
		# Methode qui pour le Prêtre envoyait Applique un Malus ou un Bonus
		####
		# 2 capacité:
		# - Bonus de Production de Ressource (+2) 	(Bonus_Ressource)
		# - Bonus d'immigration				 		(Bonus_Immigration)
		####
		if ability == "Bonus_Ressoure":
			# On augmente la production de tout les Roturiers
			for pop in self.population:
				pop.addcpbonus(2)

	#lord: Classlord
	def setlord(self, lord):
		self.lord = lord

	#priest: Classpriest
	def setpriest(self, priest):
		self.priest = priest

	def setnamevillage(self, name):
		self.name = name

	def testbirthpop(self, gamedata):
		#######
		# Method Pour Faire une Pop selon le niveau de bonheur 
		#######
		# Fait le tour de la population:
		# 1°) Prend 2 Pop avec un Age entre 15 et 30 et fait une moyenne de leur Bonheur
		# 2°) Lance un chiffre entre 0 et 100, on y ajoute le Bonheur Moyen du couple
		# 3°) Si le chiffre atteint ou dépasse le Seuil(75) alors on créer une nouvelle pop
		# On considère que la population est libertine
		#######

		# On recup la liste des couples possibles
		lcouple = self.couplepossibility()
		# On se balade dans les couples
		for couple in lcouple:
			# On calcule le bonheur
			joy = (self.population[couple[0]].joy+self.population[couple[1]].joy)//2
			# On recup un chiffre aléatoires
			r = random.randrange(0,100)
			# On y ajoute le bonheur
			r += (joy-50)
			# On vérifie que c'est au dessus du Seuil
			if r >= 75:
				# on créer une nouvelle pop
				# Prend le Rang le plus faible des 2 parents
				# Afin d'éviter une sur apparition des Artisan
				if (self.population[couple[0]].role == "paysan") or (self.population[couple[1]].role == "paysan"):
					pop = ClassRoturier(gamedata.randomnametype("Nom"), "paysan", True)
				else:
					pop = ClassRoturier(gamedata.randomnametype("Nom"), "artisan", True)
				gamedata.log.printinfo(f"félicitation, {self.population[couple[0]].name}({self.population[couple[0]].age}) et {self.population[couple[1]].name}({self.population[couple[1]].age}) ont donné naissance à {pop.name}")
				self.addpopulation(pop)
					

	def couplepossibility(self):
		#######
		# Methode qui renvoit une liste des couples unique possible
		#######
		lcouple = []
		# On se balade dans la populations
		i = 0
		lenpop = len(self.population)
		while i < (lenpop -1):
			# On verifie que la pop cible est dans la tranche d'âge nécessaire
			if (self.population[i].age <= 30) and (self.population[i].age >= 15):
				# On cherche pour le 2ième membre du couple
				i2 = i+1
				# tant qu'ont se balade dans la liste
				while((i2 < lenpop) and ((self.population[i2].age > 30) or (self.population[i2].age < 15))):
					i2 += 1
				if i2 < lenpop:
					lcouple += [[i,i2]]
				# On incrémente à i la différence entre i2 et i +1
				i += ((i2-i)+1)
			else:
				i += 1

		return lcouple


	def killpop(self, pop):
		#######
		# Method pour tuer un Roturier
		#######

		# Les Ressources qu'il possédait sont Récupérer par le Seigneur
		# Si le Village est dirigé par une Seigneur
		if self.lord != 0:
			self.lord.nb_money += pop.money
			self.lord.nb_ressource += pop.ressource

		# On le retire des liste du villages
		if pop.role == "artisan":
			self.nb_artisan -= 1
		elif pop.role == "paysan":
			self.nb_paysan -= 1

		i = 0
		for population in self.population:
			if population == pop:
				self.population = self.population[:i] + self.population[i+1:]
			i += 1

		# On détruit l'objet
		del pop

	def updateinfo(self):
		#######
		# Method pour mettre à jour automatiquement les données du village
		#######

		self.prod_money = 0
		self.prod_ressource = 0
		temp_joy = 0
		for pop in self.population:
			temp_joy += pop.joy
			self.prod_money += pop.tax_money()
			self.prod_ressource += pop.tax_ressource()

		# Calcul de la joie global du village
		self.global_joy = temp_joy/len(self.population)


	def endofturn(self, gamedata):
		#######
		# Méthode fin de tour
		#######		
		for pop in self.population:
			pop.endofturn(self.lord)
			if pop.deathiscoming() == True:
				gamedata.log.printinfo(f"{pop.name} Meurt à l'age de {pop.age}")
				self.killpop(pop)

		# On gère les naissances
		self.testbirthpop(gamedata)
		# On update les infos
		self.updateinfo()


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

	def salarycount(self):
		#######
		# Methode pour renvoyer le salaire total de l'armée [Money,Ressource]
		#######

		count_r = 0
		count_m = 0
		lenpop = len(self.unit)

		if self.knight != 0:
			count_r += 4
			count_m += 4
		count_r += lenpop
		count_m += lenpop

		return [count_m, count_r]

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

	def endofturn(self, lord):
		#######
		# Méthode fin de tour
		#######

		# On appel la Methode Fin de tour pour le Chevalier Si on en a un
		if self.knight != 0:
			self.knight.endofturn(lord)

		#On appel la Methode Fin de tour pour les Soldats
		for soldier in self.unit:
			soldier.endofturn(lord)

		# On update l'armée
		self.updatearmy()

class Classpriest:

	def __init__(self, name):
		self.name = name
		self.ressource = 0
		self.money = 0
		self.joy = 50
		self.ability = 0
		self.getability()

	def setname(self, name):
		self.name = name


	def getability(self):
		######
		# Methode qui fournit aux Prêtre une Capacité Aléatoire Passive 
		######
		# r = random.randrange()
		#self.aptitude = 

		pass

	def endofturn(self, lord):
		#######
		# Méthode fin de tour
		#######
		#
		#
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

	def endofturn(self, lord):
		#######
		# Méthode fin de tour
		#######
		# Tax au Seigneur Son Salaire Si possible
		if lord.verifcost(4,4) == True:
			lord.sub_money(4)
			lord.sub_ressource(4)
		# Sinon réduit son bonheur
		else:
			self.joy -= 10


		# Consomme Si possède les ressources
		if self.ressource > 0:
			self.ressource -= 1
		# Sinon achète Si possède l'argent
		elif self.money > 0:
			self.money -= 1
		# Sinon réduit son bonheur
		else:
			self.joy -= 10
			
		self.age += 1


class ClassSoldier:

	def __init__(self, name:chr):
		self.name = name
		self.ressource = 2
		self.money = 2
		self.joy = 50
		self.age = random.randrange(15,30)
		self.power = 1
		self.movecapacity = 4

	def endofturn(self, lord):
		#######
		# Méthode fin de tour
		#######
		# Tax au Seigneur Son Salaire Si possible
		if lord.verifcost(1,1) == True:
			lord.sub_money(1)
			lord.sub_ressource(1)
		# Sinon réduit son bonheur
		else:
			self.joy -= 10


		# Consomme Si possède les ressources
		if self.ressource > 0:
			self.ressource -= 1
		# Sinon achète Si possède l'argent
		elif self.money > 0:
			self.money -= 1
		# Sinon réduit son bonheur
		else:
			self.joy -= 10

		self.age += 1




"""
Classe Roturier pour représenter les paysans ou artisans avec des caractéristiques spécifiques 
et des actions comme la production et le paiement des impôts.
"""
class ClassRoturier:

	def __init__(self, name, role:str, child:bool):
		# On commence par définir les données de base
		self.name = name
		self.ressource = 1
		self.money = 0
		self.joy = 50
		# capacité de production
		self.cp = 2
		self.cpbonus = 0
		self.cpmalus = 0

		if child == True:
			self.age = 0
		else:
			self.age = random.randrange(15,30)
		# On change selon le rôle données
		self.role = role
		if role == "artisan":
			self.cp = 4
			self.money = 5


	def addcpbonus(self, bonus):
		####
		# Method pour ajouter un Bonus de Production
		#####
		self.cpbonus += bonus


	def subcpbonus(self, bonus):
		####
		# Method pour retirer un Bonus de Production
		#####
		self.cpbonus -= bonus

	def addcpmalus(self, malus):
		####
		# Method pour ajouter un malus de Production
		#####
		self.cpmalus += malus

	def subcpmalus(self, malus):
		####
		# Method pour retirer un Malus de Production
		#####
		self.cpmalus -= malus



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
		if self.age > 8:
			print(f"{self.name} un {self.role} à produit: {self.cp} ressource")
			self.ressource += self.cp
		else:
			print(f"{self.name} un {self.role} à produit: {1} ressource")
			self.ressource += 1			

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

	def deathiscoming(self):
		#######
		# Methode qui vérifie si le Roturier Meurt
		#######
		# On tire un Chiffre entre 0 et 100
		# On à un Seuil de 150
		# Le Seuil baisse selon l'age et le Bonheur
		# Ex:
		# Jean à 50an, il a 50 de Bonheur
		# Le Seuil baisse de 50, et augmente de (50-50) = 0
		# Pour que Jean meurt il doit tirer entre 0 et 100
		######
		# Return True Si il meurt
		# Return False Si il Survit
		######

		# Seuil de Base sans les Bonus/Malus
		s = 150
		# On ajoute l'age dans la balance
		s -= self.age
		# On ajoute le Bonheur dans la balance
		s += (self.joy - 50)

		r = random.randrange(100)
		if r >= s:
			return True
		else:
			return False

	def endofturn(self, lord):
		#######
		# Méthode de fin de tour
		# 1°) Le roturier produit sa capacité de production
		# 2°) il paye la taxe du Seigneur local
		# 3°) Si il n'a plus de ressource il en achète 1
		# 4°) Il consomme 1 de ressource
		# 5°) Si il atteint la capacité limite de Ressource il vend sont éxédent
		# 6°) On calcul son bonheur selon ses besoins
		# 7°) On augmente l'age
		# 8°) Il peut Mourir
		#######
		print(f"{self.name} un {self.role} Possède aux début du tour: {self.money} écu et {self.ressource} Ressource")


		# 1°) Produit la CP
		self.produce()

		# On vérifie que le Roturier est en âge de payer la tax
		if self.age > 8:
			# 2°) Si le Roturier possède un Seigneurs il paye la tax
			if lord != 0:
				self.pay_tax(lord)

		# 3°) Achete si il n'a plus de ressource
		self.buy()

		# 4°) Le Roturier se Nourrit
		self.ressource -= 1

		# 5°) Si le roturier possède de l'excedant il le vend contre de l'argent
		self.sell()

		# 6°) On update son humeur selon ses besoins
		# Si il n'a pas put se nourrir, le bonheur baisse
		if (self.ressource < 0)  and (self.joy > 0):
			self.joy -= 10
		# Sinon Si il à put se nourrir et qu'il à de la bouffe en réserve il est optimiste
		elif (self.ressource > 1) and (self.joy < 100):
			self.joy += 5
		# Sinon rien ne change

		# 7°) On Augmente son Age
		self.age += 1

		# 8°) Mort Possible Du Roturier
		# Gérer au niveau du Village


		print(f"{self.name} un {self.role} Possède à la fin du tour: {self.money} écu et {self.ressource} Ressource")
		print(f"{self.name} un {self.role} à {self.age} ans et est {self.joy}% heureux")


