
import tkinter

import functions.moveview as moveview
import functions.interfacemenu as interfacemenu


#############\ Fonction Système Notification \################

class ClassNotifSystem:


	def __init__(self):
		pos = []
		nb_message = 0

	def setposition(self, coord):
		#####
		# Méthode pour changer la position de la colonne des Notifications
		#####
		pos = coord

	def createmessg(self):
		#####
		# Methode pour gérer la création du Message avec sa pop-up
		#####
		pass

	def deletemessg(self):
		#####
		# Methode pour détruire le Message
		#####
		pass

	def showmessg(self):
		#####
		# Methode Pour afficher le Message quand on clique sur la pop-up
		#####
		pass



####### MAIN ########
notifsystem = ClassNotifSystem()