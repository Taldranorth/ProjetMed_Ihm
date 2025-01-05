# ProjetMed_Ihm
BOURDON Kilian | CHAUDET Fearghal

Capacité du Programme:
 - Pop-up
 - Message Temporaire
 - Retour utilisateur Gain/Perte de Ressource/Écus
 - délimitation information importante dans l'entête haut et action entête bas

 - système d'event un peu poussé
 - Pathfinding Basique
 - Automate Limité à une répétition des mêmes actions dans le même odres et avec les mêmes conditions
 - Sauvegarde/Chargement de la Partie
 - Menu de Debug
 - Gestion des Paramètre D'application
 - Système d'écriture des logs
 - Résumé de fin de partie limité
 - Voir fichier /docs/aipop.md pour la définition de la population

Graphe des classes:

 assets.py
 - ClassAtlas
 - ClassDicoName

 data.py
 - ClassGameData
 - ClassOptions
 - Classmap

 event.py
 - ClassEvent

 gameclass.py
 - Classlord
  --> Classarmy
 		--> ClassKnight
 		--> ClassSoldier
 - Classvillage
 	--> Classpriest
 	--> ClassRoturier


 log.py
 - classlog

 stats.py
 - ClassDicoStat


Problème:
 - winfo_screenheight() ne renvoit pas la résolution correcte -> obligé de multiplier par 1.4
 - Même Si on permet à l'utilisateur de sélectionner une résolution elle n'est modifier qu'après avoir relancer l'application
 - Il manque le système du marché afin de compenser la surproduction de ressource par l'achat/vente (voir Marché dans le Jeu Stellaris)
 - Les stats collecté durant la partie ne sont pas sauvegardé
 - le zoom n'est pas correcte et fait facilement perdre l'utilisateur
 - il manque l'indicatif de la dernière sauvegarde lorsque l'on veut quitter la partie
 - Quitter la partie = quitter l'application
 - dans le menu de sauvegarde/chargement le temps de jeu n'est pas indiqué pour chaque sauvegarde, cela pourrait permettre d'aider l'utilisateur à mieux les différencier
 - Début d'un système de notification affin d'afficher des infos bulles clicable à gauche de l'écran
 - Diconame doit être refactoriser pour utiliser l'architecture .json
 - Arrrrghhh faut refactoriser 

Résultat Playtest Extérieur:
 - Construire Village:
 	--> sortir automatiquement quand Construction Impossible
 	--> Ajouter retour Utilisateur Impossibilité directe en affichant les cases en rouge
 - Info générale, ajouter plus d'espace entre les catégories
 - Ajouter Scrollbar à la Vue détaillée 
 - Ajouter Tooltip, Event Armée Mercenaire
 - Ajouter information sur le système de tax plus poussé
 - Incompréhension Pathfinding

Architecture du Projet:
 - asset
 	--> texture
 	--> name.txt
 - docs
 	--> aipop.md
 	--> Regle.md
 - functions
 - perlin_noise
 - user
 	--> save
 	--> config.ini
 	--> log.log
 - .gitignore
 - main.py
 - README.md


Crédit:
Perlin Noise library:
[https://github.com/salaxieb/perlin_noise](https://github.com/salaxieb/perlin_noise)

World Map Tiles Set:
[https://opengameart.org/content/world-map-tiles]