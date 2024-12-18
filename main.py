import os
import sys
import random
import tkinter

import functions.log as log
import functions.data as data
import functions.asset as asset
import functions.cheat as cheat
import functions.ailord as ailord
import functions.genproc as genproc
import functions.moveview as moveview
import functions.gameclass as gameclass
import functions.affichage as affichage
import functions.interfacegame as interfacegame
import functions.interfacemenu as interfacemenu


from time import time

# Objectif:
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
####################################################################

##################\ Doit Faire: \#######################
# Main:
# - Déplacement en mettant la souris sur la bordure extérieur de la carte
# - Améliorer le Zoom/Dezoom
#
# Interface:
# - Améliorer l'interface
# - Suprimer le carrer du village ou l'église a était construite
# - Léger décalage sur la droite lorsqu'on centre la vue
#
# Moveview: 
#	- Implémenter une limite sur le déplacement de la vue pour ne pas aller plus loin que nécessaires
#		--> Implémenter pour Déplacement avec Souris
#
# Interface:
# - Recalculer toute les positions d'interfaces
#		--> Rentre dans la partie résolution dynamique
# - améliorer interface
# - Ajouter la prise de village et le combat d'armée à l'interface de déplacement d'armée
#	--> Si souris sur armée ennemie alors affiche icône Combat
#	--> Si souris sur village Ennemies alors affiche icône Pillage
#########################################################

# -> Refactoriser le code pour réduire la réutilisation de même code pour a la place utilisr une fonction commune liée a l'objet utiliser
# -> Refactorisation tout les calculs de Coordonnées pour utiliser les fonctions Commune

# -> Fix la possetion de multiple armé
#	-->Faire poper aux alentour de la ville la nouvelle armée si la case de la ville est déjà occupé par une armée
# -> Rework Interface avec Grid
#	--> Interface_Army

#####
# - La trajectoire Actuelle d'une armée doit s'afficher quand on clique dessus

# - Fix différence click droit Mac/Linux
# - Besoin d'un Retour utilisateur Quand Action Impossible
#####

####

# - Mettre en place un level Log Erreur
# - LVL 0: On affiche seulement les critique dans la Console
# - LVL 1: On affiche les critiques et les important dans la Console
# - LVL 2: On affiche tout dans la Console
# - Ajouter Couleur au Log

# - Implémenter les Différents type de Comportement pour l'IA

# - Gérer les armées ennemies quand le Seigneur n'est plus là
#	--> On les Supprimer ou ont les ajoute à la liste des Armées Bandit ?

# - Changer les Interfaces Pour qu'elle n'utilise plus la texture de "base"

# - Pour l'instant Les Seigneurs IA ne peuvent vassaliser le Joueur

# - Définir comment annuler une action ajouter dans la file d'action
#	--> Si c'est une armée on cherche dans la file toute les actions qui ont pour paramètre l'objet Armée

# - AJouter affichage Victoire ou défaite aux combat d'armée
#	--> Utilisé système de Notification
# - Remplir le Menu Cheat

# - Pousser la Gestion de la Menace

# -> Ajouter Bouton Pour annuler Si on déplace une armée mais que l'on veut annuler son déplacement au tour prochain
#	--> Annuler retire l'action en cour dans la pile 1 ou 0

# - Réaction au Bonheur
# --> Si le Bonheur d'un vassaux est trop bas alors il tente une révolte
# --> Si le Bonheur d'une armée est trop basse alors elle se révolte
# --> Ajouter Rebellion Vassaux Contre Seigneur

# - Refactoriser Classmap
# --> Changer le lien entre les objets villages et les tuiles
# --> Changer lvillage pour un Dico qui contient pour l'id l'objet Village
# - Refactoriser la Création de Village
# - Changer Frame de l'atlas pour le lier à la root ?

# - Changer Fonctionnement Event mercenary_army Pour pouvoir afficher le prix de l'armée de mercenaire et sa troupe

# - Voir comment gérer de manière efficace le Text Tooltip pour que ce soit dynamique
#	--> Liste qui contient des chaines de caractère avec des appels de variable ?
#		--> Non c'est toujours le même problème, actuellement c'est les valeurs qui sont stocké et non l'adresse mémoire qui est accéder
#			--> Il faut envoyé une variable dynamique et non statique
#				--> Putain python fait chier

# - Mettre en Place Fonctions ListBox qui disparait
#####

#### Fait:
"""
Implémenter:
 - Améliorer Zoom/Dezoom
 	--> Limité à 1 zoom par action
 - Améliorer Geule de l'Interface
 	--> Utiliser Texture
 - Implémenter Structure Animation
 - Implémenter Structure Notification
 - Ajouter ToolTipe aux Graphes
 - Implémenter Bezier
 - Améliorer Retour Utilisateur Fin de Tour
 - Ajouter Notification début de tour Croissance des Villages
 - Implémenter Garde fous lors d'ailord main
 - Implémenter Interface Save/Load
 - Affichage du Pathfinding en cours des armées


Refactoriser:
 - Améliorer Selection de Village Pour la Construction d'église
 	--> 1 clique pour zoom, 2 clique pour sélectionner
 - Interface de Création de Seigneur
 - Refactoriser le Calcul et l'affichage des Graphes en utilisant Bezier

Fix:
 - Différence Mac/Linux
 - Tooltipe Canvas qui peuvent rester après la destruction de leur objets
 - SnowBale de la vassalisation de l'ennemie
"""
####

#### Objectif Restant ####
# - Refactorisation Option/classmap et Gamedata pour être défini dans data et accéder à partir d'un appel du fichier
# - Implémenter Résolution Dynamique
# - Implémenter Réactions Armées et Vassaux
# - Implémenter Comportement de l'IA
# - Terminé Graphe Stat
# - Implémenter ToolTip sur Graphe Stat
# - Trouvé un Moyen de Centré les fenêtre d'interfaces
# - Implémenter Image Event
# - Implémenter Menu Options
# - Implémente Gestion de la population par case
# - Optimiser et Refactoriser
# - Graphe Stats par Bezier
######


######
# -> Ajouter Bouton Pour annuler Si on déplace une armée mais que l'on veut annuler son déplacement au tour prochain
# -> Rework Interface avec Grid
#	--> Interface_Army
######## Fonctionnalité Principale à Implémenter
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
# - Implémenter à la révolte des villages la révoltes de l'armée locale si le bonheur est mauvais
# - Implémenter la création de Bandit
# - Changer interface entête pour afficher icône boufe et money
# - Implémenter une interface plus pousser d'attaque de village
# - Implémenter une interface plus pousser d'attaque d'armée
# - Refactoriser le Code
########

#### Landforme ####
# --> Utiliser Octaves Pour générer groupe de Terrain
# --> Repasser un coup de Noise map dans le groupe de Terrain qui vient définir les tuiles

# Pour régler le problème de la taille d'écran
#https://pypi.org/project/screeninfo/

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
	
