
from datetime import datetime


class Classlog:
	####################
	# Classe qui va gérer toute les Erreurs et autre infos
	####################

	def __init__(self):

		self.file = open("user/log.log", "w")
		self.loglevel = 0


	def printerror(self, ch):

		ch = "Erreur: " + ch
		ch = self.formatlog(ch)
		print(f"\033[0;31m{ch}")
		self.file.write(ch+"\n")
		self.file.flush()

	def printinfo(self, ch):

		ch = "Info: " +ch
		ch = self.formatlog(ch)
		print(f"\033[0;37m{ch}")
		self.file.write(ch+"\n")
		self.file.flush()

	def formatlog(self, ch):
		####################
		# Fonction qui formatte le message pour l'écriture
		####################
		ch = "[" + str(datetime.now())[11:19] +"]" + ch
		return ch


###### Main #######
log = Classlog()