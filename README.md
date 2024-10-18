# ProjetMed_Ihm
 
Architecture:

Project Folder 

	—> Main.py

	—> GenProc.py

	—> MathOpti.py

	—> Affichage.py

	Création de la carte

	Affichage de la carte

	Zoom/dézoom de la carte

	déplacement de la carte

	—> Event.py

	—> Class.py

	Fichier contenant toute les définitions de Classe

	—> Data.py

	Fonctions dédier a l’ouverture et la sauvegarde de fichier

	—> Config.txt

	—> Save Folder

	—> Asset Folder

	—> Tuiles Folder

	—> Images_Event Folder

	—> Interface Folder

Cahier des Charges:  
  
Tour de Jeu:

Conditions de Victoires


- À conquis tout les Seigneur Ennemies

#Quand placer la condition ? à la fin d’un tour ? ou après la conquête d’un seigneur ?


Conditions de Défaites:


- Perte de tout c’est villages

#Quand la condition ? à la fin d’un tour ou après la perte d’un village


Actions Possibiles du Joueurs:


- Militaire:
		- Recruter des Soldats
		- Déclarer la Guerre
		- Tenter de Rallier un Noble
- Civil:
		- Créer Village
		- Constuire Église
		- Immigrer Villageois
		- Impôts

Effets/retour au Joueur:


	- Les boutons doivent s’enfoncer quand on clique dessus
	- Un retour sonore doit être envoyés
		- retour léger afin de ne pas énervé l’utilisateur  
  


Fichier Config:

Si non Présent doit être créer

	—> Résolution Configurer par l’utilisateur

	—> Valeur de Base = résolution de l’écran

Menu:

Menu Principale:
	-→ Nouvelles Partie
	-→ Charger

	—> Options

	—> Quitter

Nouvelle Partie:


	- Taille Carte
	- Nom du Joueur
	- Nb de Seigneur Ennemies
	- Nb de village de départ
		- doit bloquer si la carte n’est pas suffisante
	- Seed
		- Visuel de la carte
		- Quand une nouvelle Seed est gen le visuel est changer
