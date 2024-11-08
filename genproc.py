import matplotlib.pyplot as plt
from perlin_noise.perlin_noise import PerlinNoise
import random
from time import time
import sys

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


def genVillage(map):

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





    pass




def listidplaines(Classmap):
    ####################
    # Fonction pour recuperer l'id des plaines
    #   --> Voir pour remplacer cette fonction par une liste dans Classmap qui est incrémenté automatiquement
    #       --> Est t'il judicieux de garder le compte des différents types outre pour la génération des villages ?
    #
    ####################


    lplaines = []
    tmap = len(Classmap.listmap)

    for i in range(tmap):
        if Classmap.listmap[i].type == "plaines":
            lplaines += [i]

    return lplaines




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