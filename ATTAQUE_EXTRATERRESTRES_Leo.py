from random import choice, randint # Pour choisir un mot de passe aleatoire
                                   # et la position des extra-terrestres
from itertools import product
from math import ceil

def trouver_lettres_communes(mot1, mot2):
    """
    Trouve les lettres communes entre les deux mots
    `mot1` et `mot2`

    Parameters
    ----------
    mot1 : String
           Premier mot a regarder
    mot2 : String
           Deuxieme mot a regarder

    Returns
    -------
    lettres_communes : Set of characters
                       Ensembles des lettres communes
    nb_lettres_communes : int
                         Nombre des lettres communes
    """
    lettres_communes = set(mot1).intersection(mot2)
    nb_lettres_communes = len(lettres_communes)
    return lettres_communes, nb_lettres_communes

def montrer_lettres_communes(mot, lettres):
    """
    Reecrit le mot `mot` en cachant les lettres qui nes sont
    pas dans l'ensemble de lettres `lettres`

    Parameters
    ----------
    mot : String
          Mot a reecrire
    lettres : Set of characters
              Ensemble de lettres a reecrire

    Returns
    -------
    mot_reecrit : String
                  Le mot `mot` dans lequel les lettres qui n'etaient
                  pas presentes dans l'ensemble `lettres` ont ete
                  remplacees par le charactere '_'
    """
    mot_reecrit = ''
    for l in mot:
        if l in lettres:
            mot_reecrit = mot_reecrit + l
        else:
            mot_reecrit = mot_reecrit + '_'
    return mot_reecrit

def placer_extraterrestres(carte, aliens=None,
                           positions=None, possibles=None,
                           reproduction_rate=1.7):
    carte_lignes = [list(s) for s in carte.split('\n') if 2<len(s)]
    dimension_x = len(carte_lignes)-2
    dimension_y = (len(carte_lignes[0])-2)
    if positions is None:
        positions = set()
        possibles = set()
        for i in range(aliens):
            x = randint(0, dimension_x-1)
            y = randint(0, dimension_y-1)
            positions.update([(x, y)])
            x_possibles = [x]
            if x<dimension_x:
                x_possibles.append(x+1)
            if 0<x:
                x_possibles.append(x-1)
            y_possibles = [y, (y-1)%dimension_y, (y+1)%dimension_y]
            possibles.update(set(product(x_possibles,
                                         y_possibles)).difference(positions))
    else:
        nb_to_place = min(int(ceil(len(positions)*reproduction_rate))-len(positions),
                          (dimension_y*dimension_x)-len(positions))
        for i in range(nb_to_place):
            nouvelle_position = choice(list(possibles))
            possibles.remove(nouvelle_position)
            positions.add(nouvelle_position)
            x, y = nouvelle_position
            x_possibles = [x]
            if x<dimension_x-1:
                x_possibles.append(x+1)
            if 0<x:
                x_possibles.append(x-1)
            y_possibles = [y, (y-1)%dimension_y, (y+1)%dimension_y]
            possible_temporaire = set(product(x_possibles,
                                              y_possibles)).difference(positions)
            possibles.update(possible_temporaire)
    for x, y in positions:
        carte_lignes[x+1][y+1] = 'X'
    carte_finale = [''.join(s) for s in carte_lignes]
    couverture = 100*len(positions)/(dimension_x*dimension_y)
    return '\n'.join(carte_finale), positions, possibles, couverture



with open('alien.txt') as f:
    alien_dessin = f.readline()
alien_dessin = alien_dessin.replace(';', '\n')

with open('map.txt') as f:
    carte_terre = f.readline()
carte_terre = carte_terre.replace(';', '\n')

# Lit l'ensemble des mots possibles
with open('liste.mots.filtrees.txt') as f:
    mots = f.readlines()

# Nettoye la liste des mots
mots_nettoyes = []
for m in mots:
    mots_nettoyes.append(m.strip())

aliens = 2 # Nombre d'aliens
(carte_terre,
 position_aliens,
 possibilitees_aliens,
 couverture) = placer_extraterrestres(carte_terre, aliens)

motDePasse = choice(mots_nettoyes) # Choisi un mot au hasard
taille_mot = len(motDePasse) # Calcul la taille du mot de passe
print(alien_dessin)
print()
print("Vite ! Des aliens envahissent la planète.")
print("Voici la carte de la terre, tu peux voir les aliens ou il y a des 'X'")
print(carte_terre)
print("Tu dois activer la plateforme de défense mondiale.")
print("J'espère que tu connais le mot de passe...")
print()
print("--------------------------------------------------")
print("         BIENVENUE DANS LE RÉSAU DE DÉFENSE MONDIALE    ")
print("--------------------------------------------------")
print()
deviner = input("Entre le mot de passe " +
                "sans accent (le mot a {:d} lettres): ".format(taille_mot)).lower()

# Ici on ne garde que autant de lettres que le mot de passe contient
# C'est pour eviter la triche :)
deviner = deviner[:taille_mot]

lettre_trouvees = set() # Ensemble de lettres deja trouvees
while deviner != motDePasse:
    # Trouve les lettres commune entre le vrai mot de passe
    # et le mot de passe propose par le joueur
    lettres_communes, nb_lettres_communes = trouver_lettres_communes(deviner, motDePasse)

    # Met a jour l'ensemble de lettres deja trouvees avec
    # les nouvelles lettres trouvees
    lettre_trouvees.update(lettres_communes)
    print()
    print("MOT DE PASSE INCORRECT.")
    print()
    (carte_terre,
     position_aliens,
     possibilitees_aliens,
     couverture) = placer_extraterrestres(carte_terre,
                                          aliens,
                                          position_aliens,
                                          possibilitees_aliens)
    print(carte_terre)
    print("Les aliens recouvrent {:.2f}% de la surface de le Terre.Réessaie !".format(couverture))
    if couverture > 55:
        break

    # Construit le mot indice
    mot_indice = montrer_lettres_communes(motDePasse, lettre_trouvees)
    s='s' if 1<len(lettre_trouvees) else ''
    print(" Tu as {:d} bonne{s:s} lettre{s:s}".format(len(lettre_trouvees), s=s))
    print("Indice mot de passe : {:s}.".format(mot_indice))
    print()
    deviner = input("Vite ! Entre le mot de passe : ").lower()

    # Ici on ne garde que autant de lettres que le mot de passe contient
    # C'est pour eviter la triche :)
    deviner = deviner[:taille_mot]
if couverture > 55:
    print("Noon ! Les aliens sont plus nombreux que nous. Tout est perdu."+
          " (le mot de passe etait {:s})".format(motDePasse))
else:
    print("Hourra ! Nous avons gagné le combat,le monde est sauvé !")


