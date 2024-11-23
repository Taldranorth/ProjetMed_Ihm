#########################
# Fichier qui vient contenir les Régles liées à la gestion des ressources par les Populations
# - Définition des Différentes Population
# - Définition de la Gestion des Ressources
# - Définition de la Gestion Du marché
#########################

###### Def Termes ######
# - Une pop est un Roturer
# - Un roturier est une pop qui est soit:
#		--> Un paysan, un Roturier:
#			--> Qui ne dispose pas D'argent de départ
#			--> Une valeur de Production Minimum (= 2)
#			--> Demande le minium pour faire Immiger (1R, 1M)
#		--> Un artisans, un Roturier:
#			--> Qui dispose d'une Bourse de 4 pièce au départ
#			--> A une valeur de Production de 4 minimum
#			--> Demande bien plus de ressource pour faire Immigrer
#		--> Si un Roturier Peut payer un Impôt en Argent alors il payera en Argent, Sinon en Ressource
# - Un Noble est un Seigneur qui règne uniquement sur des Roturiers
#	--> Il peut soummetre à un Impot c'est sujets
#	--> Il peut être Taxer par son Seigneur
#	--> Il Tax les paysans de la moitier de leur Ressources
#	--> Il tax les Artisant du quart de leur Ressources
#	--> Il verse une part de la tax au Prêtre
#	--> Il ne peut possèder de Vassaux
#
# - Un Seigneur est Un noble qui règne sur des Roturiers et d'autres Nobles(c'est vassaux)
#	--> Il n'a pas de Supérieurs est donc ne peut être soumis à une tax
#	--> Il peut taxer Un village Composé de Roturiers
#	--> Il peut taxer un Nobles à hauteur de 1/4 de c'est ressources et Argent
#
# - Un Prêtre est une entité relier à une église
#	--> Il ne produit ni Ressource ni Argent
#	--> Il n'est pas soumis aux tax
#	--> 
#
# - Un Chevalier est un 
#
#
#
# - Un Soldat est un 
#
#
#
# - CP = capacité de production >=2
#########################

###### fin de tour: ######
#	- CP = capacité de production >=2
#	- Chaque roturier produit CP ressource
#	- Chaque roturier consomme 1 ressource
#	- Si 1 roturier atteint le plafond de ressource qu'il peut posséder la ressource produite est vendu
#	- Si 1 roturier n'a plus de ressource il achète 1 ressource
#	- Chaque roturier voit son âge augmenté de 1
#	- Si 1 roturier voit son âge atteindre 100 il meurt et c'est ressource/money son transférer au Seigneur du village
#	- Le bonheur augmente 
#########################

#
# - Si une pop atteint le plafond de Ressource son excédant est vendu contre de l'argent
# - Si une pop n'a plus de ressource il achète une ressource avec de l'argent
# 
# 
#
#