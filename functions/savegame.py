import json
import functions.gameclass as gameclass

"""
A FAIRE:
Ajout de retour utilisateur si jamais aucune sauvegarde n'as été trouvée.

save de :
- taille de la carte et seed
- nombre de seigneurs, noms, couleurs
- ressources, argent, bonheur, nb de tours
- nb de villages de chaque seigneurs, save de la population et eglise ou pas
- population des villages: nb ressources, nb d'argent
- emplacement des villages sur la carte
- vassaux
- liste armée : chevalier, soldat
-

"""


"""
Sauvegarde les données importantes de la partie dans un fichier JSON.
"""
def save_game(gamedata, classmap, filename="savegame.json"):
    data = {}
	
    #Sauvegarde des paramètres globaux
    data["Nb_tour"] = gamedata.Nb_tour

    #Taille de la carte et seed
    if hasattr(classmap, "mapsize_x") and hasattr(classmap, "mapsize_y"):
        data["mapsize"] = {"x": classmap.mapsize_x, "y": classmap.mapsize_y}
    else:
        data["mapsize"] = {"x": 100, "y": 100}  #Taille par défaut

    if hasattr(classmap, "map_seed"):
        data["map_seed"] = classmap.map_seed
    else:
        data["map_seed"] = None  #Aucun seed défini

    #Sauvegarde des seigneurs
    data["list_lord"] = []
    for lord in gamedata.list_lord:
    	data["list_lord"].append({"name": lord.lordname, "color": lord.color, "resources": lord.nb_ressource, "money": lord.nb_money, "player": lord.player})

    # Écriture dans un fichier JSON
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Partie sauvegardée dans le fichier '{filename}'")



"""
Charge les données d'une partie depuis un fichier JSON.
"""
def load_game(gamedata, classmap, filename="savegame.json"):
    with open(filename, "r") as file:
        data = json.load(file)

    #Restauration des paramètres globaux
    gamedata.Nb_tour = data["Nb_tour"]

    #Resto de la taille et du seed de la carte
    if "mapsize" in data:
        classmap.mapsize_x = data["mapsize"].get("x", 100)  #par défaut 100 si absent
        classmap.mapsize_y = data["mapsize"].get("y", 100)
    if "map_seed" in data:
        classmap.map_seed = data["map_seed"]

    #resto des seigneurs
    gamedata.list_lord = []  	#Réinitialiser la liste actuelle pour mettre celle sauvegardé
    for lord_data in data["list_lord"]:
    	new_lord = gameclass.Classlord(lord_data["name"], lord_data["player"], len(gamedata.list_lord))
        new_lord.setcolor(lord_data["color"])
        new_lord.nb_ressource = lord_data["resources"]
        new_lord.nb_money = lord_data["money"]
        gamedata.list_lord.append(new_lord)

    print(f"Partie chargée depuis le fichier '{filename}'.")


