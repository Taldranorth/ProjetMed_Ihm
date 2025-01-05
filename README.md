# ProjetMed_Ihm
BOURDON Kilian | CHAUDET Fearghal

- accompagnez vos sources d'un fichier de nom README (à l'exclusion de tout autre) précisant ce qui a été fait et non fait, la description du graphe de vos classes, ainsi que les points de votre prototype qui mettent en avant les qualités d'une bonne IHM (listés ci-dessous),

- barème indicatif : programmation (4), paradigmes objet (2), qualités ergonomiques (cohérence, concision, structuration des activités, flexibilité, retour d’informations, gestion des erreurs : 10), fonctionnement général et qualités propres (4),

Capacité du Programme:
 - Pop-up Souris
 - Message Temporaire
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

Résultat Playtest Extérieur:
 - Construire Village:
 	--> sortir automatiquement quand Construction Impossible
 	--> Ajouter retour Utilisateur Impossibilité directe en affichant les cases en rouge
 - Info générale, ajouter plus d'espace entre les catégories
 - Ajouter Scrollbar à la Vue détaillée 
 - Ajouter Tooltip, Event Armée Mercenaire
 - Ajouter information sur le système de tax plus poussé
 - Incompréhension Pathfinding


Crédit:
Perlin Noise library:

[https://github.com/salaxieb/perlin_noise](https://github.com/salaxieb/perlin_noise)

World Map Tiles Set:
[https://opengameart.org/content/world-map-tiles]