import sys
import random
import tkinter

import functions.log as log
import functions.asset as asset
import functions.gameclass as gameclass
import functions.affichage as affichage
import functions.interfacegame as interfacegame

from time import time

######################### On recup le dossier locale dans une variable	#########################
#import os
#c_d = os.getcwd()
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
# - Le Nb de tour
# - Les données du Joueur
# - Les données des Non-Joueurs
# - La Seed
#
#
#
#
#############################################################################

################## Objet qui ne doivent pas être Enregistrer ################
# - les Images
# - Pic, la noise map obtenue à partir de genNoisemap
#
#
#
#
#
#############################################################################

######################### Def de Classes #########################

class ClassGameData:

	####################
	# Classe qui va contenir toute les données de la partie:
	# 	- Nb tour
	#	- Nb lord
	#	- Taille d'une tuile
	#	- liste de lord
	#		--> type de l'objet: class
	# 
	#	- liste des tuiles
	#
	#	- Le seed de la carte
	#
	#	2 état:
	#		- Avant initialisation de la game
	#		- Après initialisation de la game
	#
	#	À l'initialisation de la game on créer une instance de la classe qui va contenir les données suivante:
	#		nb_turn = 0
	#		Nb_lord = 3
	# 
	####################

	def __init__(self):

		# Variable qui vient contenir le nombre de tour passé
		self.nb_turn = 1
		# Variable qui vient contenir le nombre de joueurs
		self.Nb_lord = 0
		# variable qui vient contenir le Seigneur qui doit jouer
		self.Nb_toplay = 0
		self.tuilesize = 20

		#Seed générer au lancement de l'appli
		self.seed = random.random()*time()

		# Variable bool modifier quand ont veut que le joueur termine son tour
		self.endturn = False
		# Variable bool qui vient représenter un sémaphore qui vient bloquer le process quand un ia ou la fin du tour est actuellement lancé
		self.semaphore = False
		# Variable bool pour indiquer que la partie est terminé
		self.is_finished = False
		# Variable qui vient contenir en Fin de jeu si c'est une Victoire ou une défaite
		self.victory = ""

		# Variable qui vient contenir l'id du lord qui représente le seigneur
		self.playerid = 0
		# Liste qui vient contenir les Seigneurs
		self.list_lord = []

		# Label Frame Atlas
		self.lframe = 0

		# Dico contenant les effets des capacité des prêtres
		self.dico_priest_ability = {}

		# Variable qui vient contenir la file des actions
		# liste de Piles
		self.actionlist = []

		self.log = log.log
		# Donnés qui vient contenir l'état du joueur
		#	Utiliser quand on créer une interface spéciale
		#	Ex: - quand on affiche l'interface du village
		#		- quand on affihe l'interface de construction
		#
		#	liste des état:
		#	"build_village", "interface_village", "interface_war"
		#
		#
		self.state = 0

		# Une fois toute les valeur charger on charge les seigneur de base
		# On créer le seigneur qui représente le joueur
		player = gameclass.Classlord("test", True, self.Nb_lord)
		self.list_lord += [player]
		self.Nb_lord += 1

		for x in range(3):
			self.createlord()

	def notdefeatedlord(self):
		#####
		# Methode qui retourne le Nombre de seigneur Non Vaincu
		#####
		i = 0
		for lord in self.list_lord:
			if lord.isdefeated == False:
				i += 1
		return i

	#tuile: Classtuiles
	def addtuile(self, tuile):
		self.list_tuile += [tuile]

	# Methode pour changer la taille de la tuile
	def newsizetuile(self, size: int):
		self.tuilesize = size

	# Methode pour charger les données d'une save
	def loaddata():
		pass

	def changePlayerLord(self, idplayer, player):
		self.list_lord[idplayer] = player

	def createlord(self):
		self.list_lord += [gameclass.Classlord(("lord "+self.randomnametype("Surnom")), False, self.Nb_lord)]
		
		#color = f'#{random.randrange(256**3):06x}'
		#Liste des couleurs disponibles
		colorlist = ['Yellow', 'BlueViolet' , 'DeepPink', 'Darkorange4', "Orange","Blue4", "Cyan", "LightSalmon", "Khaki1", "coral", "Yellow4", "Firebrick4", "Orange4", "Hotpink4", "Brown","magenta", "Salmon4", "SeaGreen"]
		
		#Trouver les couleurs déjà utilisées
		used_colors = []
		for lord in self.list_lord:
			used_colors.append(lord.color)
    		#Trouver une couleur disponible
		available_colors = []
		for color in colorlist:
			if color not in used_colors:
    				available_colors.append(color)
    				
		#Si plus de couleurs disponibles on affiche dans le terminal une erreur
		if len(available_colors) == 0:
        		raise ValueError("Toutes les couleurs disponibles ont été attribuées. Ajoutez plus de couleurs ou retirez des joueurs")

    		#Choisir une couleur au hasard parmi les couleurs disponibles
		color = random.randint(0, len(available_colors)-1)
		color = available_colors[color]
		
    		#Attribuer la couleur au seigneur et incrémentation du nombre de joueurs
		self.list_lord[self.Nb_lord].setcolor(color)
		self.Nb_lord += 1

	def lordnametoid(self, name):
		#####
		# Fonction qui renvoie l'id du seigneur dont le nom a été donné
		#####
		# On se balade dans la liste des Seigneurs
		for lord in self.list_lord:
			# Si on trouve un seigneur qui à le même nom on renvoit son ID
			if lord.lordname == name:
				return lord.idlord
		# Si on ne trouve pas on Renvoit False
		return False


	def deletelord(self, idlord):
		name = self.list_lord[idlord].lordname[5:]
		# On récup l'objet
		lord = self.list_lord[idlord]

		# On reconstruit la liste de Seigneur
		# On ne peut avoir au minimum que 2 seigneurs avec le Joueur en position 0:
		if len(self.list_lord) > 2:
			i = idlord
			# On reconstruit la liste sans le seigneurs
			self.list_lord = self.list_lord[:i] + self.list_lord[i+1:]
			# On change les id des seigneurs qui était après lui
			while i<len(self.list_lord):
				self.list_lord[i].idlord = i
				i += 1
		else:
			self.list_lord = [self.list_lord[0]]

		# On détruit le seigneur
		del lord
		# On réduit le compteur de seigneur
		self.Nb_lord -= 1

		# On libérer le nom utilisé
		asset.dico_name.freename("Surnom",name)

	def coordtoarmy(self, idlord, coord):
		#######
		# Fonction qui pour les coord map données et l'idlord renvoit l'objet army du lord
		# Return l'objet army si il trouve
		# Sinon False
		#######
		for army in self.list_lord[idlord].army:
			if (army.x == coord[0]) and (army.y == coord[1]):
				#self.log.printinfo(f"armée trouvé pour x: {army.x} et y: {army.y}")
				return army
		#self.log.printerror(f"armée non trouvé pour coord x: {coord[0]} et y: {coord[1]}")
		return False

	def changenewstate(self, newstate: chr):
		####################
		# Fonction pour changer state si == 0
		# Renvoit 0 si l'état n'a pas était changer
		# Renvoit 1 si l'état à était changer
		####################
		if self.state != 0:
			self.log.printerror(f"tente d'entrée dans {newstate}, hors déjà dans un état {self.state}")
			return False
		else:
			self.state = newstate
			self.log.printinfo(f"entre dans un état {newstate}")
			return True


	def statenull(self):
		####################
		# Methode pour renvoyer l'état à null
		####################
		self.log.printinfo(f"On quitte l'état {self.state}")
		self.state = 0

	def endofturn(self, classmap):
		################
		# Méthode appeler pour mettre fin au tour
		################

		# On vide la file des actions pour le tour 0:
		self.eotactionfile()

		# On appelle les méthode des instances des sous-classes lord
		for lord in self.list_lord:
			lord.endofturn(self)
		# On appelle les méhodes des instances des sous-classes villages qui n'ont pas de Seigneurs
		for idvillage in classmap.lvillages:
			village = classmap.idtovillage(idvillage)
			if village.lord == 0:
				village.endofturn(self)

		self.nb_turn += 1

	def exit(self):
		################
		# Méthode appeler quand ont veut quitter le jeu
		################
		self.log.file.close()

		######################## Methode Queue des Actions	########################

	def addactionfile(self, action, turn):
		################
		# Méthode appeler quand ont veut ajouter une action qui se produira dans x tour
		# Définit les variables stocker dans action
		# On utilise la fonction eval() qui intérpréte une chaîne de caractère en une expression
		# Action est donc une chaîne de carac qui reprèsente la fonction et les variables que l'on veut utiliser
		# Ex:  eval("moveunit(gamedata, classmap, option, army, coord)")
		# Il faut voir si il garde le contexte des variables
		# Si non simplement utiliser f"{}"
		################

		# Si actuellement la liste des action prévu est inférieur on ajoute turn liste vide
		if len(self.actionlist) < (turn+1):
			#print("taille file inférieur aux tour:", len(self.actionlist), turn)
			for x in range((turn - len(self.actionlist))+1):
				#print("file action :",self.actionlist)
				self.actionlist += [[]]
		# On ajoute l'action dans la turn pile à la dernière place
		self.actionlist[turn] += [action]
		self.log.printinfo(f"file action après ajout: {self.actionlist}")

	def actionfileeval(self, action):
		################
		# Méthode appeler par eotactionfile pour évaluer l'action selon une liste de fonction connue
		################
		try:
			if action[0] == "sequencemoveunit":
				log.log.printinfo(f"Action trouvé: sequencemoveunit")
				affichage.sequencemoveunit(action[1], action[2], action[3], action[4], action[5])
			elif action[0] == "sequencemovefight":
				log.log.printinfo(f"Action trouvé: sequencemovefight")
				interfacegame.sequencemovefight(action[1], action[2], action[3], action[4], action[5])
			elif action[0] == "sequencemovetakevillage":
				log.log.printinfo(f"Action trouvé: sequencemovetakevillage")
				interfacegame.sequencemovetakevillage(action[1], action[2], action[3], action[4], action[5], action[6])
			elif action[0] == "addpriestcapacity":
				log.log.printinfo(f"Action trouvé: addpriestcapacity")
				action[1].addpriestcapacity()
			elif action[0] == "subcpbonus":
				log.log.printinfo(f"Action trouvé: subcpbonus")
				action[1].subcpbonus(action[2])
			elif action[0] == "subcpmalus":
				log.log.printinfo(f"Action trouvé: subcpmalus")
				action[1].subcpmalus(action[2])
		except BaseException as error:
			log.log.printerror(f"{error}")

	def removeactionfile(self, searchobject):
		################
		# Méthode appeler quand ont veut retirer les actions de l'objet dans la file
		################

		i = 0
		while (i< len(self.actionlist)):
			self.removeactionfileturn(searchobject, i)
			i += 1


	def removeactionfileturn(self, searchobject, turn):
		################
		# Méthode appeler quand ont veut retirer les actions de l'objet dans la file ciblé
		################

		# On Se balade dans la liste des actions pour le tour ciblé
		i = 0
		while(i < len(self.actionlist[turn])):
			action = self.actionlist[turn][i]
			# Si l'action correspond à sequencemoveunit ont vérifie si l'armée utilisé correspond à l'objet
			if action[0] == "sequencemoveunit":
				if searchobject == action[4]:
					# Si c'est le cas ont retire l'action de la liste puis on s'éjecte
					self.actionlist[turn] = self.actionlist[turn][:i] + self.actionlist[turn][i+1:]
					return
			elif action[0] == "sequencemovefight":
				if searchobject == action[4]:
					self.actionlist[turn] = self.actionlist[turn][:i] + self.actionlist[turn][i+1:]
					return
			elif action[0] == "sequencemovetakevillage":
				if searchobject == action[5]:
					self.actionlist[turn] = self.actionlist[turn][:i] + self.actionlist[turn][i+1:]
					return
			i += 1

	def inactionfile(self, searchobject, typeobject):
		################
		# Méthode qui renvoit True si l'objet à une Action dans la file d'actions
		################
		if typeobject == "army":
			for i in range(len(self.actionlist)):
				if self.inactionfileturn(searchobject, typeobject, i) == True:
					return True
		return False

	def inactionfileturn(self, searchobject, typeobject, turn):
		################
		# Méthode qui renvoit True si l'objet à une Action dans la file d'actions à la turn pile
		################
		if typeobject == "army":
			pile = self.actionlist[turn]
			for action in pile:
				if action[0] == "sequencemoveunit":
					if searchobject == action[4]:
						return True
				elif action[0] == "sequencemovefight":
					if searchobject == action[4]:
						return True
				elif action[0] == "sequencemovetakevillage":
					if searchobject == action[5]:
						return True

		return False


	def eotactionfile(self):
		################
		# Méthode appeler à la fin du tour
		################
		# - Doit fix le comportement pour que les actions soit accompli si elles peuvent être accompli
		#	--> On éxécute donc autant d'actions que l'on peut 
		#		--> Les actions qui correspondent à des sequences se réapelle elle même et se réajoute eux même dans la file
		#			Si elles ne peuvent s'effectuer entierement


		self.log.printinfo("On éxécute toute les actions qui reste en 0")
		if len(self.actionlist) > 1:
			for action in self.actionlist[0]:
				self.log.printinfo(f"action: {action}")
				self.actionfileeval(action)
		self.log.printinfo("Toute les actions ont été éxécuter, On déplace les piles actions vers la gauche 0<--1, 1<--2")
		# Si la pile est supérieur à 1 il n'y a pas que la pile 0
		if len(self.actionlist) > 1:
			i = 0
			while i < (len(self.actionlist)-1):
				self.actionlist[i] = self.actionlist[i+1]
				i += 1
			self.actionlist[i] = []


		self.log.printinfo("Toute les piles actions ont était déplacer fin de eotactionfile")
		self.log.printinfo(f"file action après fin de tour: {self.actionlist}")

	####################################################################################



class ClassOptions:
	####################
	# Classe qui va contenir toute les options de paramètre:
	#	- Definition de la fenêtre
	#	- Definition de la carte
	#
	#
	# Au lancement du programme il va chercher si le fichier option.ini est bien présent 
	# Si c'est le cas il va charger les options contenu dedans
	# Sinon il va charger les options par défauts
	####################


	def __init__(self):

		#Défintion de la fenêtre
		self.widthWindow = 1200
		self.heightWindow = 1200


		#self.listResolutionWindow = []
		#self.listResolutionWindow += 

		# Octaves utilisés pour la gen de la carte
		self.octaves = 10


	def loadoption(self):
		# f = open("user/Config.ini")
		# 
		#
		#
		#
		# F.close()
		pass


class Classmap:
	####################
	# Classe qui va contenir toute les sous-classes tuiles dans une liste associer à un identificateur
	#		--> Une liste ou un dictionnaire ?
	#		--> l'avantage du dictionnaire et de pouvoir balancer l'identificateur pour en recup la tuile
	####################
	def __init__(self):

		# Variable qui vient contenir le frame du canvas
		self.framecanvas = 0
		# Variable qui vient contenir le canvas de la map
		self.mapcanv = 0
		# Variable qui vient contenir les TK variable de l'entête
		self.tkvar_list = []

		#dico qui vient contenir les Classtuiles 
		self.listmap = {}
		self.nbtuile = 0

		#Liste qui vient contenir les idTuile des:
		#	--> Villages
		#	--> Plaines
		self.lvillages = []
		self.lplaines = []

		# Définition de la carte
		self.mapx = 100
		self.mapy = 100

	def addtuileinlist(self, tuile):
		self.listmap[self.nbtuile] = tuile
		tuile.setidtuile(self.nbtuile)
		self.nbtuile += 1

	def setmapcanv(self, mapcanv):
		self.mapcanv = mapcanv

	def setlframecanvas(self, framecanvas):
		self.framecanvas = framecanvas

	def idtovillage(self, idvillage):
		####################
		# Fonction qui retoure l'objet village selon l'id de la tuile renvoyer
		####################

		return self.listmap[idvillage].village

	def removeidvillage(self, idvillage):
		#######
		# Methode Pour retirer un village selon son id
		#######
		village = self.listmap[idvillage].village
		# On retire le Bind de la tuile
		self.listmap[idvillage].village = 0
		# On supprime son affichage
		affichage.delvillageunit(self.mapcanv, idvillage)

		# On le cherche dans la liste idvillage avant de le retirer
		i = 0
		for village in self.lvillages:
			if village == idvillage:
				self.lvillages = self.lvillages[:i] + self.lvillages[i+1:]
				# Une fois trouvé on le del Puis on s'éjecte
				del village
				return
			i += 1

	def nametoid(self, name):
		####################
		# Méthode pour obtenir l'id d'un village selon son nom
		####################
		for ele in self.lvillages:
			if self.listmap[ele].village.name == name:
				return ele


class Classtuiles:
	####################
	# Classe qui va contenir toute les données liée à une tuile:
	#
	#	- N° de la tuile
	#	- Propriétaire de la tuile:
	#		--> Un seigneur ou personne(nature)
	#		--> Quand la tuile est créer personne ne possède la tuile
	#	- Ressource présente
	#	- Ressource particulière
	#		--> Optionnelle, pour après que le projet soit terminer
	#	- Bonus/Malus
	#	- texture file associé
	#			--> On sépare le texture file du texture
	#				--> texture_name = le nom du fichier
	#				--> texture = le fichier charger est resize
	#			--> Selon le type on associe un background
	####################

	def __init__(self, texture_name, type, x, y, canvasobject):
		# N° de la tuile, définie par classmap
		self.id = 0
		# Position de la tuile
		self.x = x
		self.y = y
		self.type = type
		# Si une armée est présente sur la tuile
		self.armyintuile = 0

		# nom du fichier texture associé
		self.texture_name = texture_name
		self.background = "plains.png"

		# Si c'est un village
		self.village = None

		# Nom du propriétaire de la tuile
		self.possesor = "wild"

		# Objet du canvas associé
		self.canvastuiles = canvasobject

		# Selon le type de la classe on définit:
		#	- le rendement en ressource et argent
		#	- le coût en déplacement pour traverser la tuile

		if type == "plains":

			self.ressourceyield = 0
			self.moneyield = 0
			self.movementcost = 1

		elif type == "forest":

			self.ressourceyield = 0
			self.moneyield = 0
			self.movementcost = 2

		elif type == "mountains":

			self.ressourceyield = 0
			self.moneyield = 0
			self.movementcost = 4

		elif type == "ocean":

			self.ressourceyield = 0
			self.moneyield = 0
			self.movementcost = 10

	def setidtuile(self, idt):
		self.id = idt

	def setpossesor(self, possesor):
		self.possesor = possesor

	def setarmyinplace(self, army):
		self.armyintuile = army

	def removearmyinplace(self):
		self.armyintuile = 0

	def createvillage(self, gamedata):
		# On créer un nouveau village que l'on stocke
		self.village = gameclass.Classvillage(self.x, self.y)
		# On set le nom du village
		self.village.setnamevillage(asset.dico_name.randomnametype("Village"))

###########################################################################

######## Main #########
#option = ClassOptions()
#gamedata = ClassGameData()
#Map = Classmap()



