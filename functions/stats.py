
import functions.log as log

#################### Fonction Stats ####################

##########
# Ensemble de Fonction et variable qui vont contenir les Stats du Jeu:
# - Chaque Fin de Tour on enregistre les données suivantes de Chacun des Seigneurs dans un dico:
# --> La Puissance Militaire:
#		--> Le Power, le Nombre d'armée, la Composantes des Armées
# --> La Démographie:
#		--> Le Nombre de Population au Total, le Nombre de VIllage, La Population dans les Villages
# --> L'économie:
#		--> 
# --> Le Score:
#
# --> Le Nb total de Mort
# Pour tout ce qui est indépendant on enregistre dans une case spéciale Nommé "Indépendant"

class ClassDicoStat:


	def __init__(self):
		######
		# Methode pour initialiser le dico des tats
		######
		# On créer le dico
		self.dico_stat = {}

	def init_dico_stat(self, gamedata):
		######
		# Methode pour initialiser le dico des tats
		######
		# On créer les clés
		for lord in gamedata.list_lord:
			self.dico_stat[lord.lordname] = []

	def add_lord_dico(self, lord):
		######
		# Methode pour ajouter un Nouveaux Seigneur au dico
		######
		self.dico_stat[lord.lordname] = []

	def turnend(self, gamedata):
		#####
		# Methode appelé à la fin du tour Pour Stocker les données
		#####
		nb_turn = gamedata.nb_turn-1
		for lord in gamedata.list_lord:
			turn = self.turn_dico(lord, nb_turn)
			self.dico_stat[lord.lordname] += [[nb_turn, turn]]

	def turn_dico(self, lord, nb_turn):
		######
		# Methode pour créer et renvoyer le dico des données du nbturn pour le seigneur donné en paramètre
		######

		turn_dico = {}
		# On ajoute les Données Militaire
		power = lord.power
		nbarmy = len(lord.army)
		turn_dico["Military"] = [power, nbarmy]

		# On ajoute les Données Démographique
		nbPop = lord.total_pop()
		nbVillage = len(lord.fief)

		turn_dico["Demography"] = [nbPop, nbVillage]

		# On ajoute les Données Économique
		nb_res = lord.nb_ressource
		nb_money = lord.nb_money
		salary = lord.total_salaryarmy()
		prod_global = lord.prod_global()

		turn_dico["Economy"] = [nb_res, nb_money, salary, prod_global]

		# On ajoute le Score
		score = lord.score()
		nb_vassal = len(lord.vassal)

		turn_dico["Score"] = [score, nb_vassal]
		# On ajoute Les Morts


		turn_dico["Death"] = []

		return turn_dico

	def printdico(self):
		#####
		# Methode pour afficher le Contenu du dico
		#####
		print(self.dico_stat)

###### Main #######
dico_stat = ClassDicoStat()





