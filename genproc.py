import sys
import random
import matplotlib.pyplot as plt

import gameClass

from time import time
from perlin_noise.perlin_noise import PerlinNoise
#########################
#
#
#
#
#
#
#
#
#
#########################

random.seed()

"""
#Version De base
#Pour s'assurer on génére un chiffre entre 0 et 1 que l'on multiplie par l'horloge interne
noise = PerlinNoise(octaves=10, seed=(random.random()*time()))
xpix, ypix = 100, 100
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]


#print(pic)

plt.imshow(pic, cmap='gray')
plt.show()
"""




def genNoiseMap(octaves, seed, mapx, mapy):
    #On génére le bruit
    noise = PerlinNoise(octaves, seed)
    xpix, ypix = mapx, mapy
    pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    #print(len(pic))
    #print(pic)
    return pic




######################### Fonction Gen Détail #########################
#
# Comment Gérer cela ? À qu'elle étape ?
#       - En utilisant la Noise map ?
#       - Après avoir utiliser la map du Canvas ?
#
#
#


def genVillage(classmap, gamedata, options):

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
    #print(Classmap.listmap)

    nb_neutral_village = 10

    # On en gen 10 
    # Valeur Test
    for x in range(len(gamedata.list_lord) + nb_neutral_village):
        # On choisit une plaines aléatoire
        # On vient selectionner un id aléatoire présent dans lplaines
        r = classmap.lplaines[random.randrange(len(classmap.lplaines))]
        print("r: ",r)
        # On verifie que la tuile est une plaines avec aucun village à proximiter
        while buildvillagepossible(options, classmap, r) == False:
            r = classmap.lplaines[random.randrange(len(classmap.lplaines))]
        # On créer le village
        classmap.listmap[r].createvillage()
        # On ajoute son id dans la liste
        classmap.lvillages += [r]
        # Si il y a un seigneur non neutre qui n'a pas encore de village on lui assigne un seigneur
        if x < len(gamedata.list_lord):
            # On assigne la variable qui contient le Seigneurla classe dans village
            classmap.listmap[r].village.setlord(gamedata.list_lord[x])
            # On ajoute la variable du  village dans la liste des fief du Seigneur
            gamedata.list_lord[x].addfief(classmap.listmap[r].village)
            # On change le Propriétaire de la tuile du village
            classmap.listmap[r].setpossesor(gamedata.list_lord[x].lordname)


    print("lvillage: ",classmap.lvillages)


def listidplaines(Classmap):
    ####################
    # Fonction pour recuperer l'id des plaines
    #   --> Voir pour remplacer cette fonction par une liste dans Classmap qui est incrémenté automatiquement
    #       --> Est t'il judicieux de garder le compte des différents types outre pour la génération des villages ?
    #
    ####################


    lplaines = []
    tmap = len(Classmap.listmap)

    for idtuile in range(tmap):
        #print(Classmap.listmap[idtuile].type)
        if Classmap.listmap[idtuile].type == "plains":
            #Classmap.mapcanv.create_rectangle(Classmap.listmap[idtuile].x*20, Classmap.listmap[idtuile].y*20, (Classmap.listmap[idtuile].x*20)+20, (Classmap.listmap[idtuile].y*20)+20)
            lplaines += [idtuile]

    return lplaines

def buildvillagepossible(options, Classmap, idtuile):
    ####################
    # Fonction pour vérifier qu'il n'y a pas de villages déjà construit dans les zones voisines
    # Utiliser lplaines pour réduire le temps de calcul
    # 2°) Conditions:
    #   --> Si le type de la case verif n'est pas une plaines on passe à la suite
    #   --> Sinon on verif qu'un village n'est pas déjà présent
    #
    #   Calcul de l'id selon la position: x+(Xmax*y)
    #   Calcul de la position selon l'id: x = id%Xmax, y = id//Xmax
    #
    #   Returne False Si il y a un village dans la zone
    #
    #
    ####################
    #On recup la taille max de X
    xmax = options.mapx
    #On calcule les coords X,Y de l'idtuile
    xidtuile = idtuile%xmax
    yidtuile = idtuile//xmax

    # On Vérifier que la tuile sélectionner n'est pas en bord de map
    if (xidtuile == 0) or (yidtuile == 0):
        return False
    elif (xidtuile == (options.mapx-1)) or (yidtuile == (options.mapy-1)):
        return False


    for x in range(-5,5):
        for y in range(-5,5):
            idtemp = (xidtuile+x)+(xmax*(yidtuile+y))
            #print("idtemp: ", idtemp)
            #On verifie qu'il n'y a pas de villages dans un rayon de 2 cases
            if idtemp in Classmap.lvillages:
                return False
    return True



def genpopvillage(option, classmap, gamedata, idvillage, nbpop):
    ####################
    # Fonction pour remplir un village de villageois
    ####################
    for x in range(nbpop):
        # On créer le villageois
        pop = gameClass.ClassHuman(gamedata.randomnametype("Nom"))
        # On l'ajoute
        classmap.listmap[idvillage].village.addpopulation(pop)
        



#######################################################################







if __name__ == '__main__':
    pic = genNoiseMap(10, (random.random()*time()), 250, 250)
    plt.imshow(pic, cmap='gray')
    plt.show()








"""
#Version avec Plusieurs Octaves
noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

xpix, ypix = 100, 100
pic = []
for i in range(xpix):
    row = []
    for j in range(ypix):
        noise_val = noise1([i/xpix, j/ypix])
        noise_val += 0.5 * noise2([i/xpix, j/ypix])
        noise_val += 0.25 * noise3([i/xpix, j/ypix])
        noise_val += 0.125 * noise4([i/xpix, j/ypix])

        row.append(noise_val)
    pic.append(row)

plt.imshow(pic, cmap='gray')
plt.show()
"""