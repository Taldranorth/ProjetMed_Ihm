
import functions.log as log

def fight(gamedata, classmap, army1, army2):
	##################
	# Fonction pour gérer le combat entre 2 armée
	##################
	# Prend en entrée l'objet armée1 et l'objet armée2
	# - Renvoit True Si Armée1 gagne le combat
	# - Renvoit False Si Armée2 gagne le Combat
	# Selon certaines Conditions Armée 1 gagne le Combat
	# SI army1.power > army2.power
	#
	if army1.power > army2.power:
		return True
	else:
		return False

def TakeVillage(gamedata, classmap, option, lord, army, village, subjugate):
	##################
	# Fonction pour gérer la prise de Village par le Seigneur
	##################
	# Subjugate vient définir 2 comportement:
	# Si C'est le Seul Village Du Seigneur Ennemie:
	#	- Soit ajoute au domaine personelle de l'attaquant 	(subjugate == False)
	#	- Soit Vassaliser le Seigneur Ennemie				(subjufate == True)
	# Si ce n'est pas le Seul Village du Seigneur Ennemie:
	#	- Ajoute au domaine personelle de l'attaquant
	# Si le Seigneur Ennemie possède des Vassaux ils sont soit libérer soit ajouté a c'est vassaux
	#	- On prend comme cas de figure standars la prise de contrôle immédiate des Vassaux

	log.log.printinfo(f"Prise de {village.name} par {lord.lordname}")

	# Si le village n'est pas indépendant
	if village.lord != 0:
		Ennemielord = village.lord

		# Si le Seigneur Ennemies possède Encore plus d'1 Village
		if len(Ennemielord.fief) > 1:
			log.log.printinfo(f"Le Seigneur {Ennemielord.lordname} possède plus de 1 village")
			# On debind le Village du Seigneur Ennemie
			Ennemielord.removefief(village)
			# ON Prend le contrôle du village
			lord.addfief(village)
		# Sinon On Vassalise le Seigneur ou on le détruit et récupère le village
		else:
			log.log.printinfo(f"C'est le dernier village de: {Ennemielord.lordname}")
			# on retire le seigneur et c'est vassaux de la liste War
			lord.removewar(Ennemielord)
			# On retire le joueur de la liste war du Seigneurs Ennemie et de c'est vassaux
			Ennemielord.removewar(lord)
			# On transfert le controle des Vassaux du Seigneurs Ennemie aux joueur
			for vassallord in Ennemielord.vassal:
				# On retire le vassal de la liste du seigneurs Ennemie
				Ennemielord.removevassal(vassallord)
				# On l'ajoute à la liste du Joueur
				lord.addvassal(vassal)
				log.log.printinfo(f"{vassal.lordname} subjuger")
			log.log.printinfo(f"{lord.lordname} à pris le contrôle de tout les Vassaux Ennemie")
			# On Vassalise le Seigneur
			if subjugate == True:
				# On Vassalise le Seigneurs Ennemie
				lord.addvassal(Ennemielord)
				log.log.printinfo(f"{Ennemielord.lordname} subjuger")
			# On détruit le Seigneur
			else:
				# On transfert le contrôle du Village du Seigneur Ennemies
				Ennemielord.removefief(village)
				lord.addfief(village)
				log.log.printinfo(f"{Ennemielord.lordname} ANÉANTIE")
				# ON LE DELETE NIARK NIARK NIARK NIARK
				Ennemielord.defeated()
	else:
		lord.addfief(village)

	# On update l'affichage du territoire
	bordervillageunit(gamedata, classmap, option, village)
	# On update l'affichage de l'entête
	updateinterface(gamedata, classmap)