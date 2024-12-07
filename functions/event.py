

import random
import functions.log as log
import functions.common as common
import functions.genproc as genproc
import functions.affichage as affichage

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
#	Attaque de Mildiou:
#		--> réduit la Production de Ressource des Paysan
#
#############################################################################

##################
# - À chaque début de tour chaque joueur va tirer un chiffre aléatoire Entre 0 et 100
# Les Probabilité sont les Suivantes:
# - 15% de Chance de Tirer Un Effet Positive
# - 15% de Chance de Tirer Un Effet Négatif
# - 15% de Chance de Tirer Un Effet Neutre
# - Sinon aucun Event ne se déroule
#
##################

class ClassEvent:

	def __init__(self):
		# Contient la liste des evenement
		self.listpositifevent = ["abundant_harvest", "clergy_donation", "free_immigration", "free_army"]
		self.listneutralevent = ["new_village", "mercenary_army", "Nothing"]
		self.listnegatifevent = ["plague", "famine", "mildiou", "newfaith", "fire", "bandit"]

	def randomevent(self, gamedata, classmap, option):

		# Pour Chaque Seigneur
		for lord in gamedata.list_lord:	
			# On tire un Chiffre aléatoire
			r = random.randrange(100)
			log.log.printinfo(f"{lord.lordname}: {r} à était tiré:")
			# Si entre 0-15 Alors Effet Positif
			if (r <= 15):
				log.log.printinfo(f"Un Événement Positive à donc était tiré:")
				self.positif_event(gamedata, classmap, option, lord)
			# Si entre 16-30 Alors Effet Négatif
			elif ((r > 15) and (r <= 30)):
				log.log.printinfo(f"Un Événement Negative à donc était tiré:")
				self.negatif_event(gamedata, classmap, option, lord)
			# Si entre 31-45 Alors Effet Neutre
			elif ((r>30) and (r<=45)):
				log.log.printinfo(f"Un Événement Neutre à donc était tiré:")
				self.neutral_event(gamedata, classmap, option, lord)
			# Sinon Rien
			else:
				log.log.printinfo(f"Rien à était tiré:")


	##### Positive #####
	def positif_event(self, gamedata, classmap, option, lord):
		r = random.randrange(len(self.listpositifevent))
		event = self.listpositifevent[r]
		
		if event == "abundant_harvest":
			self.abundant_harvest(gamedata, lord)
		elif event == "clergy_donation":
			self.clergy_donation(lord)
		elif event == "free_immigration":
			self.free_immigration(gamedata, classmap, option, lord)
		elif event == "free_army":
			self.free_army(lord)



	def abundant_harvest(self, gamedata, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Récolte Abondante
		######
		# tout les paysans du Village ciblé voit leur production de Ressource Doublé
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Récolte Abondante")
		# On sélectionne un Village aléatoire du Seigneurs
		r = random.randrange(len(lord.fief))
		village = lord.fief[r]
		log.log.printinfo(f"{village.name} ciblé")
		
		# On augmente la production de ressource des paysans
		for pop in village.population:
			if pop.role == "paysan":
				# On ajoute le bonus
				pop.addcpbonus(pop.cp)
				# On retire le bonus après 1 tour
				gamedata.addactionfile(["subcpbonus", pop, pop.cp], 1)

	def clergy_donation(self, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Subvention du Clergé
		######
		# - On incrémente simplement le compteur d'église gratuite du seigneur
		#####
		log.log.printinfo(f"{lord.lordname}, Événement: Une Subvention du Clergé")
		lord.freechurch += 1

	def free_immigration(self, gamedata, classmap, option, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Immigrés
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Des Immigrés")
		# On sélectionne un Village aléatoire du Seigneurs
		r = random.randrange(len(lord.fief))
		village = lord.fief[r]
		log.log.printinfo(f"{village.name} ciblé")

		free_paysan = random.randrange(2,10)
		free_artisan = random.randrange(0,3)
		log.log.printinfo(f"{free_paysan} paysan et {free_artisan} artisan arrive dans le village {village.name}")
		genproc.genpopvillage(gamedata, classmap, option, village, free_paysan, free_artisan)

	def free_army(self, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Armée Volontaire
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Une Armée Volontaire")
		pass



	#### Neutre #####
	def neutral_event(self, gamedata, classmap, option, lord):
		r = random.randrange(len(self.listneutralevent))
		event = self.listneutralevent[r]
		
		if event == "new_village":
			self.new_village(gamedata, classmap, option, lord)
		elif event == "mercenary_army":
			self.mercenary_army(gamedata, lord)


	def new_village(self, gamedata ,classmap, option, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Nouveau Village
		######
		log.log.printinfo(f"{lord.lordname}, Événement: un nouveau village Indépendant")

		# On récupère un emplacement aléatoire de la liste des plaines
		r = classmap.lplaines[random.randrange(len(classmap.lplaines))]
		# On vérifie que l'emplacement est correcte
		while genproc.buildvillagepossible(option, classmap, r) == False:
			r = classmap.lplaines[random.randrange(len(classmap.lplaines))]

		# Une fois que l'on à un emplacement correcte On construit le village
		classmap.listmap[r].createvillage(gamedata)
		classmap.lvillages += [r]
		village = classmap.listmap[r].village
		log.log.printinfo(f"Le village {village.name} à était créer à la position {village.x}, {village.y}")
		# On le rempli de Roturier
		genproc.genpopvillage(gamedata, classmap, option, village, 8, 2)
		# On affiche le village
		affichage.printvillageunit(gamedata, classmap, option, [village.x, village.y])
		# On affiche sa Bordure
		affichage.bordervillageunit(gamedata, classmap, option, village)

	def mercenary_army(self, gamedata, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Armée de Mercenaire
		######
		log.log.printinfo(f"{lord.lordname}, Événement: une Troupe de Mercenaire")
		# On vérifie que le Seigneur ciblé soit le Joueur
		if lord.idlord == gamedata.playerid:
			pass
		pass

	##### Négatif ######
	def negatif_event(self, gamedata, classmap, option, lord):

		r = random.randrange(len(self.listnegatifevent))
		event = self.listnegatifevent[r]

		if event == "plague":
			self.plague(lord)
		elif event == "famine":
			self.famine(gamedata, lord)
		elif event == "mildiou":
			self.mildiou(gamedata, lord)
		elif event == "newfaith":
			self.newfaith(gamedata, lord)
		elif event == "fire":
			self.fire(classmap, option, lord)
		elif event == "bandit":
			self.bandit(lord)

	def plague(self, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Peste
		######
		# - On tue une partie de la pop du Village Sélectionner
		# - On sélectionne comment la pop?
		# --> On se balade simplement dans le village
		# - Sous qu'elle critère la pop meurt ?
		# - On tire un dés aléatoires, le chiffre doit faire 
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Peste")
		# On sélectionne un Village aléatoire du Seigneurs
		r = random.randrange(len(lord.fief))
		village = lord.fief[r]
		log.log.printinfo(f"{village.name} ciblé")
		i = 0
		for pop in village.population:

			death = self.plagueunit(pop)
			# Si le Roturier ne survit pas
			if death == False:
				log.log.printinfo(f"{pop.name}, {pop.role}, age = {pop.age} Ne survit pas à la peste")
				village.killpop(pop)
				i += 1
		log.log.printinfo(f"La peste à fait un total de {i} victime dans le village {village.name}")

	def plagueunit(self, pop):
		#####
		# Methode qui renvoit True si la pop envoyait ne survit pas à la Peste
		#####
		# Si enfant alors meurt
		if pop.age < 8:
			return True
		# Si Vieux(>45) alors meurt
		if pop.age > 45:
			return True
		# Si Bonheur Bas alors meurt
		if pop.joy <=40:
			return True

		return False

	def famine(self, gamedata, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event famine
		######
		# - On réduit à 0 la production de tout les Roturiers du Village Sélectionner
		#
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Famine")
		# On sélectionne un Village aléatoire du Seigneurs
		r = random.randrange(len(lord.fief))
		village = lord.fief[r]
		log.log.printinfo(f"{village.name} ciblé")

		for pop in village.population:
			# On applique un Malus de Production Équivalent à la Production + Bonus de Production
			malus = pop.cp + pop.cpbonus
			pop.addcpmalus(malus)
			# Après 1 tour on retire le Malus
			gamedata.addactionfile(["subcpmalus", pop, malus], 1)

	def mildiou(self, gamedata, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Mildiou
		######
		# - On applique un Malus de Production au Paysan de 2
		######
		log.log.printinfo(f"{lord.lordname}, Événement: mildiou")
		# On sélectionne un Village aléatoire du Seigneurs
		r = random.randrange(len(lord.fief))
		village = lord.fief[r]
		log.log.printinfo(f"{village.name} ciblé")

		for pop in village.population:
			# On applique le Malus
			pop.addcpmalus(2)
			# Après 1 tour on retire le Malus
			gamedata.addactionfile(["subcpmalus", pop, 2], 1)


	def newfaith(self, gamedata, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Nouvelle Foi
		######
		# - Retire Pour 1 tour les effets du prêtre dans un village aléatoire du Seigneurs
		# - Baisse de 5 le Bonheur des Roturiers du Village
		# - Réapplique après 1 tour les effets de prêtre
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Nouvelle Foi")
		# On sélectionne un Village aléatoire du Seigneurs
		r = random.randrange(len(lord.fief))
		village = lord.fief[r]
		log.log.printinfo(f"{village.name} ciblé")

		# On baisse le bonheur générale
		for pop in village.population:
			pop.changejoy(-5)

		if village.priest != 0:
			# on retire temporairement l'effet du Prêtre
			village.subpriestcapacity()
			# On ajoute dans la file la réaplication de l'effet du Prêtre après 1 tour
			gamedata.addactionfile(["addpriestcapacity", village], 1)


	def fire(self, classmap, option, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Fire
		######
		# - L'event consiste en un Incendies qui rayé un Village Aléatoire du Seigneur Lord
		# - Toute la pop du village est détruite
		# - Le seigneur n'hérite d'aucune des ressources
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Un Incendie")
		# On sélectionne un Village aléatoire du Seigneurs
		r = random.randrange(len(lord.fief))
		village = lord.fief[r]
		log.log.printinfo(f"{village.name} ciblé")
		# On rase le Village
		# détruit toute la Population
		for pop in village.population:
			# On retire la pop du village
			if pop.role == "artisan":
				village.nb_artisan -= 1
			elif pop.role == "paysan":
				village.nb_paysan -= 1
			# On vérifie que se ne soit pas le dernier
			if len(village.population):
				village.population = village.population[1:]
			else:
				village.population = []
			del pop

		# Si il y a Un prêtre on le delete
		if village.priest != 0:
			priest = village.priest
			village.priest = 0
			del priest

		# On retire le Village du fief du Seigneurs
		lord.removefief(village)
		# On calcul l'id du village
		idvillage = common.coordmaptoidtuile(option, [village.x, village.y])
		# On le delete
		classmap.removeidvillage(village)


	def bandit(self, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Bandit
		######
		# - L'event consiste en un Vol de Ressource et d'argent dans un Village Aléatorie du Seigneur lord
		# - Entre 0-25% Ressource de Chaque Roturier sont retirer
		# - Entre 0-25% Écus de Chaque Roturier sont retirer
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Des Pilliards")
		# On sélectionne un Village aléatoire du Seigneurs
		r = random.randrange(len(lord.fief))
		village = lord.fief[r]
		log.log.printinfo(f"{village.name} ciblé")

		# Les Pillars Pille entre 0-25% des Ressources et/ou 0-25% des Écus du Village
		ressourcetaken = random.randrange(0, 25)
		moneytaken = random.randrange(0, 25)
		log.log.printinfo(f"{ressourcetaken/100}% Ressource et {moneytaken/100}% Écus sont retiré à chaque Roturier")
		# Pour chaque Roturier du Village
		for pop in village.population:
			# On retire le % de Ressource
			pop.ressource -= int(pop.ressource*(ressourcetaken/100))
			# On retire le % d'Écus
			pop.money -= int(pop.money*(moneytaken/100))


######## Main ########
Eventsystem = ClassEvent()


