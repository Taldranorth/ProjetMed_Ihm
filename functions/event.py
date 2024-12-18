
import random
import tkinter

import functions.log as log
import functions.stats as stats
import functions.common as common
import functions.genproc as genproc
import functions.affichage as affichage
import functions.interfacegame as interfacegame
import functions.interfacemenu as interfacemenu

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
#	Armé de Mercenaire:
#		--> Une armée indépendante apparait
#
#	Un Nouveau Village:
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
		self.listneutralevent = ["new_village", "mercenary_army", "nothing"]
		self.listnegatifevent = ["plague", "famine", "mildiou", "newfaith", "fire", "bandit"]

	def randomevent(self, gamedata, classmap, option):

		# Pour Chaque Seigneur
		for lord in gamedata.list_lord:
			if lord.isdefeated == False:
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
		
		# Si joueur on affiche l'event
		if lord.idlord == gamedata.playerid:
			eventscreen(gamedata, classmap, option, event)
		else:
			if event == "abundant_harvest":
				self.abundant_harvest(gamedata, lord)
			elif event == "clergy_donation":
				self.clergy_donation(lord)
			elif event == "free_immigration":
				self.free_immigration(gamedata, classmap, option, lord)
			elif event == "free_army":
				self.free_army(gamedata, classmap, option, lord)


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
		return [village.name]

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
		return [village.name, free_paysan, free_artisan]

	def free_army(self, gamedata, classmap, option, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Armée Volontaire
		######
		# - Une Armée Volontaire et une armée qui spawn gratuitement dans la Capitale du Seigneur
		# - Elle ne Peut être composé que de 4-8 soldat
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Une Armée Volontaire")
		# On tire le nombre de Soldat
		nbsoldat = random.randrange(4,8)
		# On créer l'armée
		interfacegame.createarmy(gamedata, classmap, option, lord, nbsoldat, 0)
		# On change le nom
		lord.army[len(lord.army)-1].setname(classmap.mapcanv, "Armée Volontaire")
		return [lord.fief[0].name, nbsoldat]



	#### Neutre #####
	def neutral_event(self, gamedata, classmap, option, lord):
		r = random.randrange(len(self.listneutralevent))
		event = self.listneutralevent[r]
		

		# Si joueur on affiche l'event
		if lord.idlord == gamedata.playerid:
			eventscreen(gamedata, classmap, option, event)
		else:
			if event == "new_village":
				self.new_village(gamedata, classmap, option, lord)
			elif event == "mercenary_army":
				self.mercenary_army(gamedata, classmap, option, lord, True)

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

		return [village.name, village.x, village.y]

	def mercenary_army(self, gamedata, classmap, option, lord, accept: bool):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Armée de Mercenaire
		######
		# - Fait Apparaitre une Armée Si le Seigneur accepte de payer en écus la demande
		# - le prix de la demande est calculer sur le nombre de soldat qui oscille entre 5-10 + le Chevalier
		# - Si joueur alors la fonction est appelé avec la variable accept qui correspond à son choix
		######
		log.log.printinfo(f"{lord.lordname}, Événement: une Troupe de Mercenaire")

		nbsoldat = random.randrange(5,10)
		knight = random.randrange(0,1)

		# On calul le prix
		price = (nbsoldat*2) + (4 * knight)
		# On vérifie que le Seigneur possède les ressource
		if lord.verifcost(0,price) == True:
			# On vérifie que le Seigneur ciblé soit le Joueur
			if lord.idlord == gamedata.playerid:
				if accept == True:
					interfacegame.createarmy(gamedata, classmap, option, lord, nbsoldat, knight)
					lord.army[len(lord.army)-1].setname(classmap.mapcanv, "Armée de Mercenaire")
			else:
				# Si le prix est inférieur au quart de se que possède le seigneurs IA alors il accepte
				if (price < int(lord.nb_money*1/4)):
					interfacegame.createarmy(gamedata, classmap, option, lord, nbsoldat, knight)
					lord.army[len(lord.army)-1].setname(classmap.mapcanv, "Armée de Mercenaire")
			

	##### Négatif ######
	def negatif_event(self, gamedata, classmap, option, lord):

		r = random.randrange(len(self.listnegatifevent))
		event = self.listnegatifevent[r]

		# Si joueur on affiche l'event
		if lord.idlord == gamedata.playerid:
			eventscreen(gamedata, classmap, option, event)
		else:
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
		return [village.name, i]

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
		return [village.name]

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
		return [village.name]


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
		return [village.name]

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
		name = village.name
		x = village.x
		y = village.y
		log.log.printinfo(f"{village.name} ciblé")
		# On rase le Village
		# détruit toute la Population
		for pop in village.population:
			# On incrémente le compteur de Mort
			stats.dico_stat.adddeath(lord, 1)
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
		idvillage = common.coordmaptoidtuile(classmap, [village.x, village.y])
		# On le delete
		classmap.removeidvillage(idvillage)
		return [name, x, y]


	def bandit(self, lord):
		######
		# Method Appeler pour appliquer au Seigneur lord l'event Bandit
		######
		# - L'event consiste en un Vol de Ressource et d'argent dans un Village Aléatorie du Seigneur lord
		# - Entre 0-25% Ressource de Chaque Roturier sont retirer
		# - Entre 0-25% Écus de Chaque Roturier sont retirer
		######
		log.log.printinfo(f"{lord.lordname}, Événement: Des Pillard")
		# On sélectionne un Village aléatoire du Seigneurs
		r = random.randrange(len(lord.fief))
		village = lord.fief[r]
		log.log.printinfo(f"{village.name} ciblé")

		# Les Pillars Pille entre 0-25% des Ressources et/ou 0-25% des Écus du Village
		ressourcetaken = random.randrange(0, 25)
		moneytaken = random.randrange(0, 25)
		log.log.printinfo(f"{ressourcetaken}% Ressource et {moneytaken}% Écus sont retiré à chaque Roturier")
		# Pour chaque Roturier du Village
		for pop in village.population:
			# On retire le % de Ressource
			pop.ressource -= int(pop.ressource*(ressourcetaken/100))
			# On retire le % d'Écus
			pop.money -= int(pop.money*(moneytaken/100))
		return [village.name, ressourcetaken, moneytaken]

def eventscreen(gamedata, classmap, option, event):
	######
	# Fonction qui gère l'affichage de la fenêtre d'event pour le joueur
	######
	# On vérifie que l'event soit utile
	if event != "nothing":
		player = gamedata.list_lord[gamedata.playerid]


		# On céer l'interface
		window_interface_event = tkinter.Frame(classmap.framecanvas)
		window_interface_event.place(x = option.widthWindow*0.25, y = option.heightWindow*0.25)

		# On créer la frame
		frame_interface_event = tkinter.Frame(window_interface_event)
		frame_interface_event.grid()

		# On applique l'event
		############### Positif ###############
		if event == "abundant_harvest":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Evénement: Récolte Abondante").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.abundant_harvest(gamedata, player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Mon Seigneur,\n les récoltes ont été abondante dans le village {stat[0]}").grid(row = 1, column = 1)		

			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
			interfacemenu.tooltip(But, "Production doublé pour 1 tour", [])
		elif event == "clergy_donation":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Evénement: Subvention du Clergé").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			Eventsystem.clergy_donation(player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Quelle Joie Mon Seigneur,\nLe Clergé a décidé de vous subventionner une Église gratuitement !").grid(row = 1, column = 1)
			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
		elif event == "free_immigration":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Evénement: Immigration").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.free_immigration(gamedata, classmap, option, player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Mon Seigneur,\nUn grand nombre de Plébéiens ont décidé de s'installer par eux-mêmes à {stat[0]}").grid(row = 1, column = 1)		
			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
			interfacemenu.tooltip(But, f"{stat[1]} paysan, {stat[2]} artisan rejoignent {stat[0]}", [])
		elif event == "free_army":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Evénement: Armée Volontaires").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.free_army(gamedata, classmap, option, player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Mon Seigneur,\nDans un Élan National une armée de Volontaires c'est formé gratuitement\nElle a rejoint notre Capitale {stat[0]} et compte {stat[1]} loyaux Soldats").grid(row = 1, column = 1)
			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
		############### Neutre ###############
		elif event == "new_village":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Evénement: Un Nouveau Village Indépendant").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.new_village(gamedata, classmap, option, player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Mon Seigneur,\nUn Groupe de piètre Plébéiens à décidé de fondé par eux-mêmes un nouveau village nommé {stat[0]}").grid(row = 1, column = 1)
			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
			interfacemenu.tooltip(But, f"{stat[0]} fondé en {stat[1]}, {stat[2]}", [])
		elif event == "mercenary_army":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Evénement: Armé de Mercenaire").grid(row = 0, column = 1)

			# On mets en place l'image

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = "Mon Seigneur,\nDes mercenaires proposent leur Service !").grid(row = 1, column = 1)

			# On mets en place les Bouttons
			tkinter.Button(frame_interface_event, command = lambda:  b_mercenary_army(gamedata, classmap, option, True, window_interface_event), text = "Oui").grid(row = 3, column = 1)
			tkinter.Button(frame_interface_event, command = lambda:  b_mercenary_army(gamedata, classmap, option, False, window_interface_event), text = "Non").grid(row = 4, column = 1)
		############### Négatif ###############
		elif event == "plague":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Événement: Peste").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.plague(player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Ho Quelle Tragédie Mon Seigneur,\nNotre village de {stat[0]} à était frappé par une Épidémie !\n").grid(row = 1, column = 1)
			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
			interfacemenu.tooltip(But, f"{stat[0]} perd {stat[1]} roturier", [])
		elif event == "famine":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Evénement: Famine").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.famine(gamedata, player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Ho Quelle Drame Mon Seigneur,\nNotre village de {stat[0]} se voit actuellement frappé par une Famine !").grid(row = 1, column = 1)

			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
			interfacemenu.tooltip(But, "Production coupé pour 1 tour", [])
		elif event == "mildiou":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Événement: mildiou").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.mildiou(gamedata, player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Quelle Coup du Sort Mon Seigneur,\nNotre village de {stat[0]} à vue une parti de ces champs être attaqué par le Mildiou !").grid(row = 1, column = 1)

			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
			interfacemenu.tooltip(But, "Production réduite pour 1 tour", [])
		elif event == "newfaith":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Événement: Nouvelle Foi").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.newfaith(gamedata, player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Quelle Trahison Mon Seigneur,\n Ces pouileux de {stat[0]} osent remettre en question notre foi divine\n pour se tourner vers un culte local!\n").grid(row = 1, column = 1)

			# On applique l'event
			Eventsystem.newfaith(gamedata, player)

			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
			interfacemenu.tooltip(But, "Capacité du Prêtre annulée pour 1 tour\nLe Bonheur Baisse", [])
		elif event == "fire":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Événement: Un Incendie").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.fire(classmap, option, player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Ho Quel désespoir Mon Seigneur,\n, Notre Village de {stat[0]} est parti en fumé dans un Incendie Ravageur").grid(row = 1, column = 1)

			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)
			interfacemenu.tooltip(But, f"{stat[0]} détruit en {stat[1]},{stat[2]}", [])
		elif event == "bandit":
			# On mets en place le titre
			tkinter.Label(frame_interface_event, text = f"Événement: Des Pillard").grid(row = 0, column = 1)

			# On mets en place l'image

			# On applique l'event
			stat = Eventsystem.bandit(player)

			# On mets en place le texte
			tkinter.Label(frame_interface_event, text = f"Ho Maleur Mon Seigneur,\nDes Bandit on attaqué notre village de {stat[0]}\n Ils ont pillé pour {stat[1]}% de Ressource et {stat[2]}% d'écu").grid(row = 1, column = 1)

			# On mets en place le boutton ok
			But = tkinter.Button(frame_interface_event, command = lambda: b_exit(window_interface_event), text = "ok")
			But.grid(row = 2, column = 1)



def b_mercenary_army(gamedata, classmap, option, accept, wie):
	#####
	# Fonction pour gèrer le Choix du Joueur vis à vis de l'armée de Mecenaire
	#####
	player = gamedata.list_lord[gamedata.playerid]
	if accept == True:
		Eventsystem.mercenary_army(gamedata, classmap, option, player, True)

	b_exit(wie)



def b_exit(wie):
	#####
	# Fonction pour détruire l'interface
	#####
	wie.destroy()


######## Main ########
Eventsystem = ClassEvent()


