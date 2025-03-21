import sys
import random

import functions.log as log
import functions.asset as asset
import functions.common as common
import functions.gameclass as gameclass


from time import time
import matplotlib.pyplot as plt
import perlin_noise.perlin_noise as Perlin_noise

#########################
# Fichier qui vient contenir les fonctions liées à la génération procédurale et la mise en place aléatoire
#########################

random.seed()

def genNoiseMap(octaves, seed, mapx, mapy):
    #On génére le bruit
    noise = Perlin_noise.PerlinNoise(octaves, seed)
    xpix, ypix = mapx, mapy
    pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    #print(len(pic))
    #print(pic)
    return pic

def genVillage(gamedata, classmap, options, NeutralVill):

    ####################
    # Fonction pour Gen les villages
    # Condition pour Gen un Village:
    #
    #       - Pas de village dans un rayon de 4 cases
    #           --> Indiquer dans le sujet 2 cases de chaque cotés 
    #       - 1 village par Dirigeant
    #       - 3-4 village Indépendant
    #       - Seulement sur des Plaines
    ####################


    # On recup la liste des Plaines
    classmap.lplaines = listidplaines(classmap)

    # On en gen 10 
    # Valeur Test
    for x in range(len(gamedata.list_lord) +NeutralVill):
        # On choisit une plaines aléatoire
        # On vient selectionner un id aléatoire présent dans lplaines
        r = classmap.lplaines[random.randrange(len(classmap.lplaines))]
        print("r: ",r)
        # On verifie que la tuile est une plaines avec aucun village à proximiter
        while buildvillagepossible(options, classmap, r) == False:
            r = classmap.lplaines[random.randrange(len(classmap.lplaines))]
        # On créer le village
        classmap.listmap[r].createvillage(gamedata)
        # On ajoute son id dans la liste
        classmap.lvillages += [r]
        # Si il y a un seigneur non neutre qui n'a pas encore de village on lui assigne un village
        if x < len(gamedata.list_lord):
            # On ajoute l'instance du village dans la liste des fief du Seigneur
            gamedata.list_lord[x].addfief(classmap.listmap[r].village)
            # On change le Propriétaire de la tuile du village
            classmap.listmap[r].setpossesor(gamedata.list_lord[x].lordname)

    print("lvillage: ",classmap.lvillages)


def listidplaines(Classmap):
    ####################
    # Fonction pour recuperer l'id des plaines
    #   --> Voir pour remplacer cette fonction par une liste dans Classmap qui est incrémenté automatiquement
    #       --> Est t'il judicieux de garder le compte des différents types outre pour la génération des villages ?
    ####################

    lplaines = []
    tmap = len(Classmap.listmap)

    for idtuile in range(tmap):
        if Classmap.listmap[idtuile].type == "plains":
            lplaines += [idtuile]

    return lplaines

def buildvillagepossible(options, classmap, idtuile):
    ####################
    # Fonction pour vérifier qu'il n'y a pas de villages déjà construit dans les zones voisines
    # Utiliser lplaines pour réduire le temps de calcul
    # 2°) Conditions:
    #   --> Si le type de la case verif n'est pas une plaines on passe à la suite
    #   --> Sinon on verif qu'un village n'est pas déjà présent
    #
    #   Calcul de l'id selon la position de la carte: x+(Xmax*y)
    #   Calcul de la position selon l'id de la tuile sur la carte: x = id%Xmax, y = id//Xmax
    #
    #   Returne False Si il y a un village dans la zone
    ####################
    #On recup la taille max de X
    xmax = classmap.mapx
    #On calcule les coords X,Y de l'idtuile
    coord = common.idtuiletocoordmap(classmap, idtuile)
    xidtuile = coord[0]
    yidtuile = coord[1]

    # On Vérifier que la tuile sélectionner n'est pas en bord de map
    if (xidtuile == 0) or (yidtuile == 0):
        return False
    elif (xidtuile == (classmap.mapx-1)) or (yidtuile == (classmap.mapy-1)):
        return False
    elif(xidtuile == 1) or (yidtuile == 1):
        return False
    elif (xidtuile == (classmap.mapx-2)) or (yidtuile == (classmap.mapy-2)):
        return False
    # On vérifie que c'est une plaines
    if classmap.listmap[idtuile].type != "plains":
        return False

    for x in range(-5,5):
        for y in range(-5,5):
            idtemp = (xidtuile+x)+(xmax*(yidtuile+y))
            #print("idtemp: ", idtemp)
            #On verifie qu'il n'y a pas de villages dans un rayon de 2 cases
            if idtemp in classmap.lvillages:
                return False

    return True

def genpopidvillage(gamedata, classmap, option, idvillage, nbpaysan, nbartisan):
    ####################
    # Fonction pour ajouter de la pop dans un Village à partir de son ID
    ####################
    village = classmap.listmap[idvillage].village
    genpopvillage(gamedata, classmap, option, village, nbpaysan, nbartisan)
        
def genpopvillage(gamedata, classmap, option, village, nbpaysan, nbartisan):
    ####################
    # Fonction pour ajouter de la pop dans un Village à partir de l'objet
    ####################

    # On ajoute les paysans
	for x in range(nbpaysan):
        # On créer le paysan
		pop = gameclass.ClassRoturier(asset.dico_name.randomnametype("Nom"), "paysan", False)
        # On l'ajoute
		village.addpopulation(pop)

    # On ajoute les Artisans
	for x in range(nbartisan):
        # On créer l'artisan
		pop = gameclass.ClassRoturier(asset.dico_name.randomnametype("Nom"), "artisan", False)
        # On l'ajoute
		village.addpopulation(pop)

