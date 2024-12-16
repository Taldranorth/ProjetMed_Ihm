
import os
import json

import functions.log as log
import functions.cheat as cheat
import functions.common as common
import functions.genproc as genproc
import functions.moveview as moveview
import functions.gameclass as gameclass
import functions.interfacemenu as intermenu


"""
Sauvegarde les données importantes de la partie dans un fichier JSON
"""
def save_game(gamedata, classmap, option,filename="savegame.json"):
	data = {}
    
    #Sauvegarde des paramètres globaux
	data["Nb_tour"] = gamedata.Nb_tour
    #Taille de la carte et seed
	data["map_seed"] = gamedata.seed
	if hasattr(classmap, "mapsize_x") and hasattr(classmap, "mapsize_y"):
		data["mapsize"] = {"x": classmap.mapsize_x, "y": classmap.mapsize_y}
	else:
		data["mapsize"] = {"x": 100, "y": 100}  # Taille par défaut
	
    # Sauvegarde des tuiles
	data["tiles"] = []
	for tile_id, tile in classmap.listmap.items():
		data["tiles"].append({
			"id": tile_id,
			"x": tile.x,
			"y": tile.y,
			"type": tile.type,
			"texture_name": tile.texture_name,
			"has_village": isinstance(tile.village, gameclass.Classvillage)
            })
	
    #Save des seigneurs
	data["list_lord"] = []
	for lord in gamedata.list_lord:
		lord_data = {
			"name": lord.lordname,
			"color": lord.color,
			"resources": lord.nb_ressource,
			"money": lord.nb_money,
			"joy": lord.global_joy,
			"player": lord.player,
			"vassals": [vassal.lordname for vassal in lord.vassal],  # Noms des vassaux
			"villages": [],
			"armies": [],
		}

        #Sauvegarde des villages du seigneur
		for village in lord.fief:
			village_data = {"name": village.name,
				"location": {"x": village.x, "y": village.y},  #Emplacement sauvegardé
				#"tuile": common.coordmaptoidtuile(option, [village.x, village.y]),   #Calcul des coordonnées de la tuile du village
				"population": [{
						"name": pop.name,
						"role": pop.role,
						"money": pop.money,
						"resources": pop.ressource,
						"age": pop.age,
						"joy": pop.joy,
				}for pop in village.population],
				"nb_artisan": village.nb_artisan,
				"nb_paysan": village.nb_paysan,
				"prod_money": village.prod_money,
				"prod_ressource": village.prod_ressource,
				"global_joy": village.global_joy,
				"has_church": village.church,
			}
			lord_data["villages"].append(village_data)
			print(f"Village {village.name} enregistré à la tuile ID {common.coordmaptoidtuile(option, [village.x, village.y])} avec coordonnées ({village.x}, {village.y})")
		
		#Sauvegarde des armées du seigneur
		for army in lord.army:
			army_data = {
				"name": army.name,
				"location": {"x": army.x, "y": army.y},
				"knight": {"name": army.knight.name, "power": army.knight.power, "joy": army.knight.joy} if army.knight else None,
				"soldiers": [{
						"name": soldier.name,
						"power": soldier.power,
						"joy": soldier.joy,
				}for soldier in army.unit],
			}
			lord_data["armies"].append(army_data)
		data["list_lord"].append(lord_data)

	#Sauvegarde des villages sans seigneurs
	data["independent_villages"] = []
	for tile_id,tile in classmap.listmap.items():
		if isinstance(tile.village, gameclass.Classvillage) and not tile.village.lord:
			village = tile.village
			village_data = {"name": village.name,
				"location": {"x": village.x, "y": village.y},  
				#"tuile": common.coordmaptoidtuile(option, [village.x, village.y]),   #Calcul des coordonnées de la tuile du village
				"population": [{
						"name": pop.name,
						"role": pop.role,
						"money": pop.money,
						"resources": pop.ressource,
						"age": pop.age,
						"joy": pop.joy,
				}for pop in village.population],
				"nb_artisan": village.nb_artisan,
				"nb_paysan": village.nb_paysan,
				"prod_money": village.prod_money,
				"prod_ressource": village.prod_ressource,
				"global_joy": village.global_joy,
				"has_church": village.church,
			}
			data["independent_villages"].append(village_data)
			print(f"Village SANS SEIGNEUR {village.name} enregistré à la tuile ID {common.coordmaptoidtuile(option, [village.x, village.y])} avec coordonnées ({village.x}, {village.y})")

	#Écriture dans un fichier JSON
	with open(filename, "w") as file:
		json.dump(data, file, indent=4)
	print(f"Partie sauvegardée dans le fichier '{filename}'.")



"""
Charge les données d'une partie depuis un fichier JSON
"""
def load_game(gamedata, classmap, option, filename="savegame.json"):
	with open(filename, "r") as file:
		data = json.load(file)
    
    #Restauration des paramètres globaux
	gamedata.Nb_tour = data["Nb_tour"]
    #Resto de la taille et du seed de la carte
	if "map_seed" in data:
		gamedata.seed = data["map_seed"]
	if "mapsize" in data:
		classmap.mapsize_x = data["mapsize"].get("x", 100)  #Par défaut 100 
		classmap.mapsize_y = data["mapsize"].get("y", 100)
    #Utiliser la fonction genNoiseMap pour générer la carte avec la seed sauvegardée
	print(f"Carte générée avec la seed: {gamedata.seed}")
	
	#Regen de la carte à partir de la seed sauvegardé
	global pic
	pic = genproc.genNoiseMap(option.octaves, gamedata.seed, classmap.mapsize_x, classmap.mapsize_y)
   
    
    # Réinitialiser la liste des tuiles dans la carte
	classmap.listmap = {}
    # Recréer les tuiles de la carte
	for tile_data in data["tiles"]:
		from functions.data import Classtuiles
		tile_id = tile_data["id"]
		classmap.listmap[tile_id] = Classtuiles(texture_name=tile_data["texture_name"], type=tile_data["type"], x=tile_data["x"], y=tile_data["y"], canvasobject=None) 
	
	#Réinitialiser la liste des villages
	classmap.lvillages = []
	print("Listevillages avant réajustement: ",classmap.lvillages)
	
	
    #Restauration des seigneurs
	gamedata.list_lord = []  	#Réinitialiser la liste actuelle
	for lord_data in data["list_lord"]:
		new_lord = gameclass.Classlord(lord_data["name"], lord_data["player"], len(gamedata.list_lord))
		new_lord.setcolor(lord_data["color"])
		new_lord.nb_ressource = lord_data["resources"]
		new_lord.nb_money = lord_data["money"]
		new_lord.global_joy = lord_data["joy"]

        #Restauration des villages du seigneur
		new_lord.fief = []
		for village_data in lord_data["villages"]:
			new_village = gameclass.Classvillage(x = village_data["location"]["x"], y= village_data["location"]["y"]) 
			new_village.setnamevillage(village_data["name"])
			new_village.nb_artisan = village_data["nb_artisan"]
			new_village.nb_paysan = village_data["nb_paysan"]
			new_village.prod_money = village_data["prod_money"]
			new_village.prod_ressource = village_data["prod_ressource"]
			new_village.global_joy = village_data["global_joy"]
			new_village.church = village_data["has_church"]

            #Restauration de la population du village
			for pop_data in village_data["population"]:
				new_pop = gameclass.ClassRoturier(name = pop_data["name"], role = pop_data["role"], child=False)
				new_pop.money = pop_data["money"]
				new_pop.ressource = pop_data["resources"]
				new_pop.age = pop_data["age"]
				new_pop.joy = pop_data["joy"]
				new_village.addpopulation(new_pop)
			
			#Associer le bon village à la bonne tuile
			tile_id = common.coordmaptoidtuile(option, [new_village.x, new_village.y])
			print("numero tuile",tile_id)
			
			if tile_id in classmap.listmap:
				classmap.listmap[tile_id].village = new_village
				if tile_id not in classmap.lvillages:
					classmap.lvillages.append(tile_id)
				print(f"Village {new_village.name} assigné à la tuile ID {tile_id} avec coordonnées ({new_village.x}, {new_village.y})")
			else:
				print(f"Erreur : Tuile ID {tile_id} introuvable pour le village {new_village.name}")
			print("listvillage: ",classmap.lvillages)
			#print("listmap: ",classmap.listmap)
			print("\n\n")

		    #Associe le village au seigneur
			new_village.setlord(new_lord)
			new_lord.fief.append(new_village)
		
		gamedata.list_lord.append(new_lord)
		
	#Restauration des villages sans seigneurs
	if "independent_villages" in data:
		for village_data in data["independent_villages"]:
			new_village = gameclass.Classvillage(x = village_data["location"]["x"], y= village_data["location"]["y"]) 
			new_village.setnamevillage(village_data["name"])
			new_village.nb_artisan = village_data["nb_artisan"]
			new_village.nb_paysan = village_data["nb_paysan"]
			new_village.prod_money = village_data["prod_money"]
			new_village.prod_ressource = village_data["prod_ressource"]
			new_village.global_joy = village_data["global_joy"]
			new_village.church = village_data["has_church"]

		    #Restauration de la population du village
			for pop_data in village_data["population"]:
				new_pop = gameclass.ClassRoturier(name = pop_data["name"], role = pop_data["role"], child=False)
				new_pop.money = pop_data["money"]
				new_pop.ressource = pop_data["resources"]
				new_pop.age = pop_data["age"]
				new_pop.joy = pop_data["joy"]
				new_village.addpopulation(new_pop)
			
			#Associer le bon village à la bonne tuile
			tile_id = common.coordmaptoidtuile(option, [new_village.x, new_village.y])
			print("numero tuile",tile_id)
			
			if tile_id in classmap.listmap:
				classmap.listmap[tile_id].village = new_village
				if tile_id not in classmap.lvillages:
					classmap.lvillages.append(tile_id)
				print(f"Village {new_village.name} assigné à la tuile ID {tile_id} avec coordonnées ({new_village.x}, {new_village.y})")
			else:
				print(f"Erreur : Tuile ID {tile_id} introuvable pour le village {new_village.name}")
			print("listvillage apès chargement: ",classmap.lvillages)
			print("classmap aprs char:",classmap.listmap)
	print(f"Partie chargée depuis le fichier '{filename}'.")



"""
Permet de vérifier dans le terminal que les seigneurs sont toujours les mêmes 
et ont le bon nombre de villages et d'armées
On pourrait rajouter d'autres précisions (notamment pour le retour user)
"""
def update_game_interface(gamedata, classmap):
    for lord in gamedata.list_lord:
        print(f"Seigneur {lord.lordname} avec {len(lord.fief)} villages et {len(lord.army)} armées.")


"""
Affiche l'écran principal du jeu après le chargement de la partie.
Copie de initgame dans interfacemenu.py
"""
def show_game_screen(gamedata, classmap, option, root):
    intermenu.mainscreen(gamedata, classmap, option, root, pic, upload_save = True)

    intermenu.mainmenuwin.destroy()
    intermenu.gameloop(gamedata, classmap, option, root)
    cheat.cheat_menu(gamedata, classmap, option, root)
    root.mainloop()



"""
Charge les données depuis un fichier JSON et démarre la partie.
"""
def load_game_and_start(gamedata, classmap, option, root, mainmenuwin, filename="savegame.json"):
    #Charge les données sauvegardées
	load_game(gamedata, classmap, option, filename)

	#Vérifie que le chargement des villages n'as pa été écrasé par autre chose
	for tile_id in classmap.lvillages:
		village = classmap.listmap[tile_id].village
		if isinstance(village, gameclass.Classvillage):
			print(f"Village valide après chargement : {village.name} sur la tuile {tile_id}")
		else:
			print(f"ERREUR : Village sur la tuile {tile_id} est invalide après chargement.")

	show_game_screen(gamedata, classmap, option, root)
	mainmenuwin.destroy()
	print("Partie chargée et prête à jouer !")






