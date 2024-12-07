import os
import sys
import random
import tkinter

import functions.log as log
import functions.data as data
import functions.cheat as cheat
import functions.ailord as ailord
import functions.genproc as genproc
import functions.moveview as moveview
import functions.gameclass as gameclass
import functions.affichage as affichage
import functions.interfacegame as interfacegame
import functions.interfacemenu as interfacemenu


from time import time

#Doit terminé de faire un Prototype:
# - Ajouter Un moyen de déplacer la vue √
#	--> Doit modifier afin de prendre en compte le non focus sur le widget du canvas
#		--> Doit appliquer le bind des touches à la root
#		--> Doit trouver un moyen de stocker les objets dans une données facilement accesible
#			--> Un dico ?
#			--> Place les bases du stockage de données
#	--> Doit modifier afin d'accèlerer le déplacement avec le maintient de la touche

# !!! Attention pour une grande carte cela ram !!!
# C'est l'affichage de plein de case qui cause la ram, voir si c'est le cache ou l'affichage

# Fait un teste avec le Moniteur d'activité lancer à coté
# L'utilisation de la ram est plutôt équilibrer, entre 130-160mo
# Quand on déplace la vue sur une zone de la carte remplie le proc est utiliser à 70%

# Trop d'appel à la fonction ? X
# J'ai tester avec une valeur incrémenter à chaque fois que la fonction motion est appelé, l'appel à la fonction est relativement léger
# pour une carte de 250*250 on y fait appel que 16* pour aller d'un bout à l'autre de la map

# The canvas has known performance problems when you create lots of canvas items, even if you delete the canvas items.
# Canvas item ids are not recycled, so the list of item ids that the canvas must maintain grows without bounds and makes the canvas slower on each iteration.
#	--> Définir des marges d'id pour les différents objets du canvas
#

# Objectif:
#	Correctif:
#	- Faire la doc de ce qui a était fait
#	- Réduire le lag lors de l'observation d'un grand groupe de cases
#		--> Utilisation du processeurs importante
#			--> Problème uniquement présent sur mac
#
#	- Refactoriser le Code
#		--> Le Nettoyer
#		--> Retirer les Commentaires Inutiles
#
#	Additif:
#	- Ajouter du Son
#		--> https://stackoverflow.com/questions/28795859/how-can-i-play-a-sound-when-a-tkinter-button-is-pushed
#
#	- Ajouter de l'animation
#		--> https://stackoverflow.com/questions/53418926/button-motion-animation-in-tkinter
#			--> Semble très gourmand
#				--> Trouver une solution plus performante
#
#	- Changer tout les EXIT pour ajouter une fenêtre de confirmation
#		--> Rappel de la dernière sauvegarde si >1 minute
#
#	Partie Graphique:
#	- Changer la police d'écriture
#		--> font = "Police"
# !!!!!!
# Faire des fonctions de recherche optimiser
#		--> Cela devrait permettre de réduire l'utilisation de la mémoire
# !!!!!!


######################### Normes #########################
# https://peps.python.org/pep-0008/#package-and-module-names
#	Nom de Variable:
#
#
#	Nom de Class:
#	- CapWords convention
#
#	Method Names and Instance Variables	
#	- lowercase with words separated by underscores as necessary to improve readability
#	- Use one leading underscore only for non-public methods and instance variables
#	Ex: Pour une Class nomer Outer -> self.outer_instance
#
#########################################################

##################\ Doit Faire: \#######################
# Main:
# - Déplacement en mettant la souris sur la bordure extérieur de la carte
# - Améliorer le Zoom/Dezoom
#
# Interface:
# - Améliorer l'interface
# - Suprimmer le carrer du village ou l'église a était construite
# - Léger décalage sur la droite lorsqu'on centre la vue
#

# Data:
#
#
# Moveview: 
#	- Implémenter une limite sur le déplacement de la vue pour ne pas aller plus loin que nécessaires
#
# Interface:
# - Recalculer toute les positions d'interfaces
#		--> Rentre dans la partie résolution dynamique
# - améliorer interface
# - Ajouter la prise de village et le combat d'armée à l'interface de déplacement d'armée
#	--> Si souris sur armée ennemie alors affiche icône Combat
#	--> Si souris sur village Ennemies alors affiche icône Pillage


# - Ajouter Gestion des couleurs à PlayMenu

# - Implémenter Tout les Event prévu x
# - Implémenter Event Positif 3/4
# - Implémenter Event Neutre 1/2

# - Implémenter Tout les Event prévu
# - Implémenter l'affichage de l'event pour le Joueur
#########################################################


# Il y a 2 décalage possible:
#	- c'elle causer par moveviewxy
#		--> décalage de l'affichage sur le canvas
#			--> Réglable par l'utilisation des coord du point d'origine de la map_canvas
#	- c'elle causer par moveviewmouse
#		--> décalage du canvas sur la fenêtre
#			--> Je ne sais pas, je ne vois pas comment la régler

# Décider d'adapter moveviewxy pour utiliser scan_dragto
#	--> Plus performant car liés à l'afichage des coord et non le changement des coord de tout les objets du canvas comme move()

# -> Fix Build Church
#	--> Aucun retour quand on construit une église

# -> Revoir la destruction de village
# -> Refactoriser le code pour réduire la réutilisation de même code pour a la place utilisr une fonction commune liée a l'objet utiliser
#	--> Voir la récupération de village selon la position x,y via Classmap
# -> Refactorisation tout les calculs de Coordonnées pour utiliser les fonctions Commune
# -> Peut être utiliser Bezier pour l'affichage du Pathfinding

# -> Fix la possetion de multiple armé
#	-->Faire poper aux alentour de la ville la nouvelle armée si la case de la ville est déjà occupé par une armée
# -> Rework Interface avec Grid
#	--> Interface_Army

#####

# - La trajectoire d'une armée doit s'afficher quand on clique dessus

# - Fix différence click droit Mac/Linux
# - Besoin d'un Retour utilisateur Quand Action Impossible
#####

####
# - Retravailler Interface Village
# - Retravailler Menu Jouer
#	--> Doit permettre de Définir les Villages Indépendants
#	--> Doit Afficher sur la minimap les villages de départs

# - Graphe de Fin de Partie
# 	--> Comment stocker les données des  différentes étapes ?
#		--> Une liste qui contient en 0 le tour 0 avec les données des différents Seigneur ?
#	--> Quoi stocker qui soit suffisament pertinent ?
#		--> Ne pas stocker des données qui soit calculable

# - Mettre en place un level Log Erreur
# - LVL 0: On affiche seulement les critique dans la Console
# - LVL 1: On affiche les critiques et les important dans la Console
# - LVL 2: On affiche tout dans la Console

# - Au niveau Économique séparé la valeur des Ressource et des Écus

# - Rendre aléatoire le placement des villages par l'Ia
#	--> Pré-Remplir une liste de coord entre [0-5] ou il va tirer aléatoirement ?

# - Implémenter les Différents type de Comportement pour l'IA

# - Ajouter une Condition qui vérifie qu'une armée ne soit pas déjà présente sur la case

# - Gérer les armées ennemies quand le Seigneur n'est plus là
#	--> On les Supprimer ou ont les ajoute à la liste des Armées Bandit ?

# - Changer les Interfaces Pour qu'elle n'utilise plus la texture de "base"

# - Pour l'instant Les Seigneurs IA ne peuvent vassaliser le Joueur

# --> Ajouter la gestion de la couleur aux menu Play

# - Définir comment annuler une action ajouter dans la file d'action
#	--> Si c'est une armée on cherche dans la file toute les actions qui ont pour paramètre l'objet Armée

# - Bloquer la vue Pour le Déplacement avec la Souris



# - Retravailler Menu Déplacement Unité
# - AJouter affichage Victoire ou défaite aux combat d'armée
# - Remplir le Menu Cheat

# - Améliorer Interface Village Stat
#	--> Empécher de quitter l'interface Village quand on est dedans
#	--> Ajouter ScrollBar

# - Améliorer Création de Seigneur en ajoutant une Scrollbar

# - Ajouter texture Pseudo-Aléatoire

# - Ajouter Rebellion Vassaux Contre Seigneur

# - Pousser la Gestion de la Menace

# -> Ajouter Bouton Pour annuler Si on déplace une armée mais que l'on veut annuler son déplacement au tour prochain
#	--> Annuler retire l'action en cour dans la pile 1 ou 0

# - Vérifier Pour l'initialisation de la map la différence entre X et Y

#https://www.aimosta.com/Blogt/blogt-16.html

# - Réaction au Bonheur
# --> Si le Bonheur d'un vassaux est trop bas alors il tente une révolte


# - Déplacer les différentes fonctions dans common
# - Déplacer les différentes fonctions dans warfunctions
# - Réorganiser interfacemenu
# - Réorganiser le Projet en Transformant des Fonctions en Methode
# - Changer Fonctionnement Dico_file pour qu'il soit séparer de Gamedata
# - Changer Fonctionnement Dico_name pour qu'il soit séparer de Gamedata
# - Refactoriser Fonction qui change la Bordure d'un Unique Village pour utiliser PrintvillageBorderunit
# - Refactoriser Classmap
# --> Changer le lien entre les objets villages et les tuiles
# --> Changer lvillage pour un Dico qui contient pour l'id l'objet Village
# - Refactoriser la Création de Village
#####

#### Objectif Week-End:
# - Réaction Bonheur Vassaux
# - Event
# - Fix, Optimisation et Refactorisation
# - Pop-Up --> Event.Enter, Event.Leave
# - Graphe Stats
####



######## Fonctionnalité Principale à Implémenter
# - Implémenter Event
# - Implémenter Résolutions Dynamique
# - Implémenter les Réactions
# - Implémenter les Différents Comportement de l'IA
# - Refactoriser le Code
########

######## Fonctionnalité Majeur Secondaire
# - Implémenter Sauvegarde et Chargement de Données
# - Implémenter Options
# - Implémenter marché
# - Implémenter Landforme
# - Gestion de la population par case
# - Pousser le Calcul de la Menace
# - Pousser le Combat entre les Armées
# - Refactoriser le Code
########

######## Fonctionnalité Mineur Secondaire
# - Faire petite animations qui montre le gain et la perte de Ressource
# - Système de Pop-up d'événement en début de tour En bas à droite Comme Armée qui termine son déplacement ou village qui termine de se construire voir Civ
# - Affiné la prise de Village pour prendre en compte le PIllage de ressource et la mort de Villageois
# - Affiné le Combat entre 2 armée pour prendre en compte la Capture du Chevalier Ennemie et la mort des Soldats
# - Implémenter Système de Tooltip (affichage d'info-Bulle)
# - Implémenter à la révolte des villages la révoltes de l'armée locale si le bonheur est mauvais
# - Implémenter la création de Bandit
# - Changer interface entête pour afficher icône boufe et money
# - Implémenter une interface plus pousser d'attaque de village
# - Implémenter une interface plus pousser d'attaque d'armée
# - Améliorer le réaffichage d'une bordure
# - Refactoriser le Code
########

#### Landforme ####
# --> Utiliser Octaves Pour générer groupe de Terrain
# --> Repasser un coup de Noise map dans le groupe de Terrain qui vient définir les tuiles


######################### Main #########################
if __name__ == '__main__':

	#Init de la fenêtre
	root = tkinter.Tk()
	log.log.printinfo(f"Hauteur de l'écran:  {root.winfo_screenheight()}")
	log.log.printinfo(f"Largeur de l'écran: {root.winfo_screenwidth()}")

	# Chargement des Options:
	option_instance = data.ClassOptions()
	# Initialisation de GameData
	gamedata_instance = data.ClassGameData()
	log.log.printinfo("Initialisation log terminé")

	# Initialisation de la Carte
	map_instance = data.Classmap()

	# Menu principale
	interfacemenu.mainmenu(gamedata_instance, map_instance, option_instance, root)
	log.log.printinfo("Initialisation de l'application terminé")

	root.mainloop()
