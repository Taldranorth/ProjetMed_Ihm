import time
import random

import functions.interfacegame as interfacegame
import functions.gameclass as gameclass
import functions.moveview as moveview
import functions.genproc as genproc
import functions.affichage as affichage
import functions.common as common

#########################
# Fichier qui vient contenir les fonctions liées à la gestion de l'ia
#
#
#########################
# - Utiliser Automate fini Déterministe
# - Utiliser un arbre de priorité
#	--> Faire un graphe papier
#	--> Utiliser grammaire
#
#
#########################
# Calcul la Menace Des Autres Seigneurs
# - Puissance * Distance avec territoires
# Si La Menace est Importante est que la Puissance est Égal alors déclare la guerre
#
#
######
# Plusieurs Caractères:
# - Expantioniste, Privilège l'expansion par Construction de Village
#		--> Construit un nouveau Village si il atteint un Objectif de population bas dans son derniers
# - Militariste, Privilège l'expansion par Conquête
#		--> Recrute une armée si il atteint un Objectif de population
#			--> Si il p
# - Économiste, Privilège une aproche plus économiste
#		--> 
#
######
# Construction de Village:
# - Si Expantioniste Construit dés qu'il peut
# - Sinon Construit Si il a le triple des Ressources Nécessaires
#
######
# Vassalisation:
# - Si la possibilité de Vassaliser un Seigneurs atteint 75%, tente de le Vassaliser
#
#
######
# Immigration:
# - Si possède un village qui à moins de Populations que prévu ainsi que 4* les ressource nécessaires pour faire immigrer, fait immigrer
# - 
######
# Armé:
# - Si possède 2*Cout de prod
# - Si possède 2*Entretien
######
# Automate de Base:
# 0°) 
# - Si les caisse sont en dessous d'une certaine Valeur alors il tax, en 1er les Vassaux, ensuite son fief
# 1°)
# - Cherche a atteindre une Population de 20 dans tout ces villages avant d'en construire un Nouveau
# - Construit Une église dés qu'il peut
# 2°)
# - Si il possède les ressources et 2* la Production nécessaire pour un soldat recrute alors un Soldat
# - Cherche a possède une armée composé de 20 soldat + 1 chevalier avant de créer une nouvelle armée
# 3°)
# - Si le Pourcentage de Réussite est de 75% alors tente de Vassaliser un Seigneurs
# - Si le Score de Menace d'une Autre IA est trop importante alors elle lui déclare la guerre
# 4°)
# - Si il est en guerre il gère les armée pour d'abord détruire les troupes adverse et ensuite prendre leur village
######


def mainai(gamedata, classmap, option):
	
	# ON affiche la banderole que l'ia Joue
	banderole_window = interfacegame.banderole(gamedata, classmap, option)

	lord = gamedata.list_lord[gamedata.Nb_toplay]
	player = gamedata.list_lord[gamedata.playerid]

	# L'Ia joue
	# 0°) Tax
	# Si le Seigneur atteint un stock Minimum il tax
	if lord.verifcost(10,10) == False:
		r = False
		m = False
		if lord.nb_ressource < 10:
			r = True
		if lord.nb_money < 10:
			m = True
		i = 0
		while (lord.verifcost(10,10) == False) and (i< len(lord.fief)):
			# le i village paye la tax au seigneurs
			village = lord.fief[i]
			gamedata.log.printinfo(f"{lord.lordname} Éxige une tax aux village {village.name} de Ressource:{r}, d'Écus:{m}")
			gamedata.log.printinfo(f"{lord.lordname} possède dans ses caisses: {lord.nb_ressource} ressource,{lord.nb_money} écus")
			actiontaxVillage(gamedata, classmap, option, lord, village, r, m)
			i += 1
	# 1°) Immigration
	for village in lord.fief:
		if len(village.population) < 20:
			nbpaysan = 0
			nbartisan = 0
			# Si possède 4* les ressources nécessaires pour recruter un Paysan
			if lord.verifcost(4,4) == True:
				nbpaysan += 1
			if lord.verifcost(12,12):
				nbartisan += 1
			actionimmigration(gamedata, classmap, option, lord, village, nbpaysan, nbartisan)

	# 1°) Église
	# Si possède les ressources nécessaires pour construire une Église
	for village in lord.fief:
		if village.priest == 0:
			if lord.verifcost(10,10):
				gamedata.log.printinfo(f"{lord.lordname} Construit une Église dans {village.name}")
				village.buildchurch(gamedata.randomnametype("Nom"))

	# 1°) Construction de Village
	# Si possède un village avec plus de 20 de population
	if canbuildvillage(gamedata, classmap, option, lord) == True:
		gamedata.log.printinfo(f"{lord.lordname} Peut Construire un Village")
		actionbuildvillage(gamedata, classmap, option, lord)


	# 2°) Création d'armée
	if canrecruitarmy(gamedata, classmap, option, lord) == True:
		gamedata.log.printinfo(f"{lord.lordname} Peut Créer une Armée")
		if lord.verifcost(2,2) == True:
			village = lord.fief[0]
			idvillage = common.coordmaptoidtuile(option, [village.x, village.y])
			# Récupère les coord de la 1er cases libres
			coord = interfacegame.searchposition(gamedata, classmap, option, village)
			i = len(lord.army)
			# Créer l'armée
			lord.createarmy(village.name, coord[0], coord[1])
			classmap.listmap[idvillage].setarmyinplace(lord.army[i])
			# Recrute un Soldat
			lord.army[i].recruitsoldier(gamedata.randomnametype("Nom"))
			# Affiche l'armée
			affichage.printarmy(gamedata, classmap, option, lord.army[i])
			lord.sub_money(2)
			lord.sub_ressource(2)
			gamedata.log.printinfo(f"{lord.lordname} A créer l'armée {lord.army[i].name}")

	# 2°) Recrutement Soldat/ Chevalier
	for army in lord.army:
		# Recrutement Soldat
		efficiency = lord.total_efficiency()
		if (lord.verifcost(4,4) == True) and ((efficiency[0] > 2) and (efficiency[1] > 2)):
			army.recruitsoldier(gamedata.randomnametype("Nom"))
			lord.sub_money(2)
			lord.sub_ressource(2)
			efficiency = lord.total_efficiency()
			gamedata.log.printinfo(f"{lord.lordname} A recruter dans l'armée {army.name}, 1 soldat")

		# Recrutement Chevalier
		if army.knight == 0:
			if (lord.verifcost(20, 20) == True) and ((efficiency[0] > 8) and (efficiency[1] > 8)):
				army.recruitknight(gamedata.randomnametype("Surnom"))
				affichage.printupdatearmy(gamedata, classmap, army)

				lord.sub_money(10)
				lord.sub_ressource(10)
				efficiency = lord.total_efficiency()
				gamedata.log.printinfo(f"{lord.lordname} A recruter dans l'armée {army.name}, {army.knight.name}")

	
	list_lord_menace = []

	# 3°) Vassalisation/Menace
	for otherlord in gamedata.list_lord:
		# Si le seigneur selectionner n'est pas le Seigneurs qui joue
		if (otherlord != lord) and (otherlord != player):
			# On calcul la réussite
			succes = interfacegame.vassal_try(gamedata, lord, otherlord)
			gamedata.log.printinfo(f"{lord.lordname} à {succes}% de chance de Vassaliser: {otherlord.lordname}")
			# On calcul la menace
			# On calcul la distance
			distx = otherlord.fief[0].x - lord.fief[0].x 
			disty = otherlord.fief[0].y - lord.fief[0].y
			if distx < 0:
				distx = distx*-1
			if disty < 0:
				disty = disty*-1
			dist = distx + disty
			menace = (otherlord.score()-lord.score())//dist
			# On ajoute la menace du Seigneur dans la liste de menace
			print("menace: ", menace)
			list_lord_menace += [[otherlord.idlord, menace]]
			if succes >= 75:
				gamedata.log.printinfo(f"{lord.lordname} tente de Vassaliser: {otherlord.lordname}")
				interfacegame.vassal_offer(gamedata, classmap, option, lord, otherlord, succes)

	gamedata.log.printinfo(f"{lord.lordname} liste de Menace: {list_lord_menace}")
	# 4°) Guerre
	# Si le Seigneur est en Guerre
	if len(lord.war) > 0:
		nbarmy = 0
		nblord = 0
		# Tant que le Seigneur possède des Armées libre
		# 4°) Attaque de Troupe
		while(nbarmy < len(lord.army)) and (nblord < len(lord.war)):
			gamedata.log.printinfo(f"l'armée {lord.army[nbarmy].name} à t'elle une action de prévu ?: {gamedata.inactionfile(lord.army[nbarmy], "army")}")
			# Si l'armée à déjà une action en cours one ne fait rien
			if gamedata.inactionfile(lord.army[nbarmy], "army") == False:
				if len(lord.war[nblord].army) > 0:
					nbarmy2 = 0
					while (nbarmy2 < len(lord.war[nblord].army)) and (nbarmy < len(lord.army)):
						gamedata.log.printinfo(f"{lord.lordname} déplace {lord.army[nbarmy].name} pour attaquer {lord.war[nblord].army[nbarmy2].name} de {lord.war[nblord].lordname}")
						interfacegame.sequencemovefight(gamedata, classmap, option, lord.army[nbarmy], lord.war[nblord].army[nbarmy2])
						nbarmy2 += 1
						nbarmy += 1
			nblord += 1

		nblord = 0
		# Tant que le Seigneur possède des Armées libre
		# 4°) Attaque de Village
		while(nbarmy < len(lord.army)) and (nblord < len(lord.war)):
			gamedata.log.printinfo(f"l'armée {lord.army[nbarmy].name} à t'elle une action de prévu ?: {gamedata.inactionfile(lord.army[nbarmy], "army")}")
			# Si l'armée à déjà une action en cours one ne fait rien
			if gamedata.inactionfile(lord.army[nbarmy], "army") == False:
				nbvillage = 0
				while ((nbvillage < len(lord.war[nblord].fief)) and (nbarmy < len(lord.army))):
					gamedata.log.printinfo(f"{lord.lordname} déplace {lord.army[nbarmy].name} pour attaquer {lord.war[nblord].fief[nbvillage].name} de {lord.war[nblord].lordname}")
					interfacegame.sequencemovetakevillage(gamedata, classmap, option, lord, lord.army[nbarmy], lord.war[nblord].fief[nbvillage])
					nbvillage += 1
					nbarmy += 1
			nblord += 1




	# Une fois que l'ia à terminé on incrémente Nb_toplay
	gamedata.Nb_toplay += 1
	# Supprime la banderole
	interfacegame.destroybanderole(gamedata, classmap, banderole_window)
	# Et On rend les clés de la Maison,le sémaphore
	gamedata.semaphore = False

def canbuildvillage(gamedata, classmap, option, lord):
	####
	# Fonction qui renvoit True si il trouve un village avec la population >= 20
	####
	for village in lord.fief:
		if len(village.population)>= 20:
			return True

	return False

def canrecruitarmy(gamedata, classmap, option, lord):
	######
	# Fonction qu renvoit True si l'ia possède un nombre d'armée < fief/2 et que ses armée sont remplit
	######
	if len(lord.army) <= (len(lord.fief)//2):
		for army in lord.army:
			if (len(army.unit) != 20) or (army.knight == 0):
				return False
		return True
	return False


def actionbuildvillage(gamedata, classmap, option, lord):
	#####
	# Ne peut construire que Dans un Rayon de 5 case autour de son territoires
	#####
	# On vérifie que le seigneur possède les ressource nécessaire pour construire un village
	if lord.verifcost(15,15) == True:
		gamedata.log.printinfo(f"{lord.lordname} Cherche un Lieu pour construire son nouveaux village aux alentour de {lord.fief[0].name}")
		# On cherche dans un Rayon de 5 cases autour de son village principale les lieux ou il peut construire un village
		i = 0
		# On cherche Une cases autour de la ville principale
		idcases = searchvillage(gamedata, classmap, option, lord.fief[i])
		# Si on a pas trouvé autour de la ville principale
		while ((idcases == 0) and (i < len(lord.fief))):
			gamedata.log.printinfo(f"{lord.lordname} n'a pas trouvé pour {lord.fief[i].name}")
			i += 1
			if (i < len(lord.fief)):
				gamedata.log.printinfo(f"{lord.lordname} Cherche un Lieu pour construire son nouveaux village aux alentour de {lord.fief[i].name}")
				idcases = searchvillage(gamedata, classmap, option, lord.fief[i])
		# Si on a trouvé une cases on construit un village
		if idcases != 0:
			gamedata.log.printinfo(f"{lord.lordname} à trouvé :{idcases}")
			# On construit le village
			classmap.lvillages += [idcases]
			classmap.listmap[idcases].createvillage(gamedata)
			classmap.listmap[idcases].setpossesor(lord.lordname)
			village = classmap.listmap[idcases].village
			# On ajoute à la liste des fief du Seigneurs
			lord.addfief(village)
			# On ajoute la pop dans le village
			genproc.genpopvillage(gamedata, classmap, option, village, 8, 2)
			gamedata.log.printinfo(f"{lord.lordname} à Fonder :{village.name} en pos: {village.x}, {village.y}")
			# On retire les ressources
			lord.sub_ressource(15)
			lord.sub_money(15)
			# On mets à jour la carte
			# On affiche le village
			affichage.printvillageunit(gamedata, classmap, option, [village.x, village.y])
			# On affiche sa bordure
			affichage.bordervillageunit(gamedata, classmap, option, village)


def searchvillage(gamedata, classmap, option, village):
	####
	# Fonction qui renvoit les coord Map du lieux autour du village ciblé ou on peut construire un nouveaux villages
	####
	xvill = village.x
	yvill = village.y

	for x in range(-5, 5):
		for y in range(-5, 5):
			# On vérifie que les coordonnées sont dans la carte
			if ((xvill+x) > 0) and ((xvill+x) < option.mapx):
				if ((yvill+y) > 0) and ((yvill+y) < option.mapy):
					idtuile = common.coordmaptoidtuile(option,[xvill + x, yvill + y])
					if genproc.buildvillagepossible(option, classmap, idtuile) == True:
						return idtuile
	return 0

def actionbuildchurch(gamedata, classmap, option, lord):
	pass

def actiontaxVillage(gamedata, classmap, option, lord, village, ressource:bool, money:bool):
	#####
	# Fonction Pour faire payer au village du Lord leur tax
	#####
	if ressource == True:
		for roturier in village.population:
			# On les faits payer leur taxes
			roturier.pay_tax_ressource(lord)
	if money == True:
		for roturier in village.population:
			# On les faits payer leur taxes
			roturier.pay_tax_money(lord)
	# On update les infos du village
	village.updateinfo()

def actionimmigration(gamedata, classmap, option, lord, village, nbpaysan, nbartisan):
	gamedata.log.printinfo(f"{lord.lordname} Fait venir {nbpaysan} paysan et {nbartisan} artisan")
	for x in range(nbpaysan):
		pop = gameclass.ClassRoturier(gamedata.randomnametype("Nom"), "paysan", False)
		village.addpopulation(pop)
		lord.sub_ressource(1)
		lord.sub_money(1)

	for x in range(nbartisan):
		pop = gameclass.ClassRoturier(gamedata.randomnametype("Nom"), "artisan", False)
		village.addpopulation(pop)
		lord.sub_ressource(4)
		lord.sub_money(4)


def actionwar(gamedata, classmap, option, lord):
	pass

def actionarmymovement(gamedata, classmap, option, lord):
	pass

def actionsubjugation(gamedata, classmap, option, lord):
	pass


