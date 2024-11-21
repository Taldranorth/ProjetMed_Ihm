#########################
# Fichier qui vient contenir les Régles liées à la gestion des ressources par les Populations
# - Gestion des Ressources
# - Gestion Du marché
#########################

###### Def Termes ######
# - Une pop est un Roturer
# - Un roturier est une pop qui est soit:
#		--> Un paysan, un Roturier:
#			--> Qui ne dispose pas D'argent de départ
#			--> Une valeur de Production Minimum (= 2)
#			--> Demande le minium pour faire Immiger
#		--> Un artisans, un Roturier:
#			--> Qui dispose d'une Bourse de 4 pièce au départ
#			--> A une valeur de Production de 4
#			--> Demande bien plus de ressource pour faire Immigrer
# - Un Noble est un Lord qui règne sur des Roturiers
#	--> Il peut soummetre à un Impot c'est sujets
#	--> Il peut être Taxer par son Seigneur
#	--> Il Tax les paysans de la moitier de leur Ressources
#	--> Il tax les Artisant du quart de leur Ressources
#	--> Il verse une part de la tax au Prêtre
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