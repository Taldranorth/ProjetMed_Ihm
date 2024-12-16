import tkinter

import functions.log as log
import functions.cheat as cheat
import functions.stats as stats
import functions.event as event
import functions.ailord as ailord
import functions.genproc as genproc
import functions.affichage as affichage
import functions.interfacegame as interfacegame
import functions.interfacemenu as interfacemenu

######################### Fonction Jeu #########################

#################### 
# Ensemble de Fonction qui vont régir un tour de jeu
#	Phase d'un Tour de jeu:
#		- Calcul du gain de Ressource et d'Argent
#		- Calcul Mort/Viellisement de la population
#		- Event
#		-- Début du tour du Joueur
#		- action - Réaction
#		- Fin du tour quand le Joueur clique sur la case fin de tour
#		- Les Vassaux du joueur Joue
#################### 
# fin de tour:
#	- CP = capacité de production >=2
#	- Chaque roturier produit CP ressource
#	- Chaque roturier consomme 1 ressource
#	- Si 1 roturier atteint le plafond de ressource qu'il peut posséder la ressource produite est vendu
#	- Si 1 roturier n'a plus de ressource il achète 1 ressource
#	- Chaque roturier voit son âge augmenté de 1
#	- Si 1 roturier voit son âge atteindre 100 il meurt et c'est ressource/money son transférer au Seigneur du village
#	- Le bonheur augmente 
####################
#Tcl/Tk applications are normally event-driven, meaning that after initialization, the interpreter runs an event loop (i.e. Tk.mainloop()) and responds to events.
#Because it is single-threaded, event handlers must respond quickly, otherwise they will block other events from being processed.
#To avoid this, any long-running computations should not run in an event handler, but are either broken into smaller pieces using timers, or run in another thread.
#This is different from many GUI toolkits where the GUI runs in a completely separate thread from all application code including event handlers.
####################

######################### Initiation de la partie #########################

def initgame(mainmenuwin, gamedata, classmap, option, root, NeutralVill):
	######
	# Fonction Pour initialiser la game
	######
	# On génére La NoiseMap
	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, classmap.mapx, classmap.mapy)
	# On lance la création de la fenêtre du Jeu
	interfacemenu.mainscreen(gamedata, classmap, option, root, pic, NeutralVill)

	# Une fois l'initialisation lancé on détruit la fenêtre du menu principale
	mainmenuwin.destroy()

	# On initialise le Dico des Stats
	stats.dico_stat.init_dico_stat(gamedata)
	stats.dico_stat.printdico()

	# On lance la game
	gameloop(gamedata, classmap, option, root)
	cheat.cheat_menu(gamedata, classmap, option, root)
	root.mainloop()

###########################################################################


def gameloop(gamedata, classmap, option, root):
	####################
	#
	#	Le Retour des Sémaphore :)
	#
	#
	####################

	if gamedata.semaphore == False:
		# si on a fait le tour des joueurs
		if gamedata.Nb_toplay == gamedata.Nb_lord:
			endofturn(gamedata, classmap, option, root)

		# Si c'est au joueurs de jouer
		if gamedata.Nb_toplay == gamedata.playerid:
			# On entre dans la loop du tour du joueur
			playerturn(gamedata, classmap, option)
		# Sinon c'est à un Ia de jouer
		else:
			# On entre dans la loop de l'ia
			notplayerturn(gamedata, classmap, option)

	# On vérifie que la partie n'est pas terminé
	if gamedata.is_finished == False:
		# Si elle ne l'est pas on rapelle cette fonction dans 
		root.after(50, lambda: gameloop(gamedata, classmap, option, root))

def endofturn(gamedata, classmap, option, root):
	######
	# Fonction Qui gère la fin de Tour
	#####
	gamedata.semaphore = True
	log.log.printinfo("Il ne reste plus de Seigneur qui doit Jouer, Fin du tour")
	#print("lplaines: ",classmap.lplaines)
	gamedata.Nb_toplay = 0
	# On vérifie que l'on ne soit pas en état de mettre fin aux jeu:
	if victoryordefeat(gamedata, classmap, option) == False:
		# On fait appel à la fonction de fin de tour
		gamedata.endofturn(classmap)
		# On calcul l'event qui va s'appliquer
		event.Eventsystem.randomevent(gamedata, classmap, option)

		# Une fois que tout les objets se sont update ont update l'interface d'entête
		interfacegame.updateinterface(gamedata, classmap)
		# On Update la Carte Si il y a eu une Update
		affichage.bordervillage(gamedata, classmap, option)

		# On update les Stats
		stats.dico_stat.turnend(gamedata)
		# On affiche dans le terminal l'évolution
		stats.dico_stat.printdico()

		# On affiche la banderole qui indique que c'est aux joueur de Jouer
		idwindow = interfacegame.banderole(gamedata, classmap, option)
		root.after(2000, lambda: interfacegame.destroybanderole(gamedata, classmap, idwindow))

		gamedata.endturn = False
		gamedata.semaphore = False
	else:
		endofgame(gamedata, classmap, option)


def playerturn(gamedata, classmap, option):
	######
	# Fonction qui gère le Tour du Joueur
	######
	# Si le joueur à appuyer sur le bouton fin de tour
	if gamedata.endturn == True:
		log.log.printinfo("Player hit end of turn button")
		# On incrémente le joueur qui doit jouer
		gamedata.Nb_toplay += 1
		# On indique au joueurs que c'est à l'ia de Jouer

# Fonction qui gère l'ia des ennemies
def notplayerturn(gamedata, classmap, option):
	######
	# Fonction qui gère le Tour de l'IA
	######
	# On prend les clés de la maison
	gamedata.semaphore = True
	log.log.printinfo(f"tour de: {gamedata.list_lord[gamedata.Nb_toplay].lordname}, {gamedata.Nb_toplay}, Vaincu: {gamedata.list_lord[gamedata.Nb_toplay].isdefeated}")
	# SI l'ia n'est pas vaincu
	if gamedata.list_lord[gamedata.Nb_toplay].isdefeated == False:
		# L'ia Joue
		ailord.mainai(gamedata, classmap, option)
	# Une fois que l'ia à terminé on incrémente Nb_toplay
	gamedata.Nb_toplay += 1
	# Et On rend les clés de la Maison,le sémaphore
	gamedata.semaphore = False

# after(time, function)

def victoryordefeat(gamedata, classmap, option):
	#######
	# Fonction pour vérifier si le Joueur est en Victoire ou défaite
	#######
	# Return un Bool et modifie une variable dans gamedata

	player = gamedata.list_lord[gamedata.playerid]
	# Si le joueur possède le Status defeated Alots Défaite
	if player.isdefeated == True:
		gamedata.victory = "Défaite"
		return True

	# Si le joueur ne Possède plus de village Alors Défaite
	if len(player.fief) == 0:
		gamedata.victory = "Défaite"
		return True
	# Si le joueur est un vassal d'un autre Seigneurs Alors Défaite
	for lord in gamedata.list_lord:
		if lord != player:
			if player in lord.vassal:
				gamedata.victory = "Défaite"
				return True

	# Sinon si le joueur possède un Nombre de Vassaux = Nombre de Seigneur-1
	# Alors Victoire
	if len(player.vassal) == (gamedata.Nb_lord - 1):
		gamedata.victory = "Victoire"
		return True

	# Sinon si le Joueur est le Dernier Seigneur en Vie
	if gamedata.notdefeatedlord() == 1:
		gamedata.victory = "Victoire"
		return True

	return False

def endofgame(gamedata, classmap, option):
	#####
	# Fonction qui gère la fin de partie
	#####
	interfacemenu.eofgamescreen(gamedata, classmap, option)




