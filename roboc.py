# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.
Exécutez-le avec Python pour lancer le jeu.
"""
import os
import re
import time
from sys import exit
from carte import *
from regles import *

# On charge les cartes existantes et on crée un dict des sauvegardes éventuelles
cartes_existantes = []
sauvegardes = {}
ATTENTE = 0.1 # temps de pause (en secondes) entre deux mouvements du robot

# on parcourt les noms de fichier du dossier 'cartes'
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier) # joint pour obtenir "cartes\nom_carte.txt"
        nom_carte = nom_fichier[:-4].lower() # enlève le ".txt" du nom du fichier pour avoir celui de la carte
        with open(chemin, "r") as fichier: # ouverture en lecture d'un fichier de carte
            contenu = fichier.read()
            # création d'un objet Carte et insertion dans les 'cartes_existantes'
            nouvelle_carte = Carte(nom_carte, contenu)
            cartes_existantes.append(nouvelle_carte)
# on parcourt les noms de fichier du dossier 'saves' aussi pour la position du robot sauvegardée           
for nom_fichier in os.listdir("saves"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("saves", nom_fichier) # joint pour obtenir "saves\nom_carte.txt"
        nom_carte = nom_fichier[:-4].lower() # il reste 'nom_carte' seul
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
            xy = contenu.split(",")
            position = (int(xy[0]), int(xy[1]))
            for carte in cartes_existantes:
                if carte.nom == nom_carte:
                    if carte.labyrinthe.grille[position] in (Labyrinthe.porte, Labyrinthe.mur, Labyrinthe.vide):
                        try:
                            sauvegardes[nom_carte] = position 
                        except ValueError:
                            pass
# On affiche la présentation et les règles du jeu
regles_du_jeu()
# On affiche les cartes existantes
print("\nLabyrinthes existants :")
for i, carte in enumerate(cartes_existantes):
    if carte.nom in sauvegardes.keys(): # si la sauvegarde avait été trouvée en haut
        print("  {} - {} (partie en cours)".format(i+1, carte.nom)) # afficher (partie en cours en plus)
    else:
        print("  {} - {}".format(i+1, carte.nom))

num_choisi = 0 # le numero de labyrinthe
while not (1 <= num_choisi <= len(cartes_existantes)):
    num_choisi = int(input("\nEntrez un numéro de labyrinthe pour commencer à jouer : "))

# l'objet Carte correspondant au numéro choisi et son labyrinthe associé
carte_choisie = cartes_existantes[num_choisi-1]
lab_choisi = cartes_existantes[num_choisi-1].labyrinthe

continuer_partie = "0" # continuer ou non la partie sauvegardée trouvée
if carte_choisie.nom in sauvegardes:
    while continuer_partie.upper() not in ("C", "N"):
        continuer_partie = input("\tC = Continuer la partie\n\tN = Nouvelle partie\nVous choisissez : ")

if continuer_partie.upper() == "C": # si Continuer a été choisi
    lab_choisi.robot_pos = sauvegardes[carte_choisie.nom]

os.system("cls") # on efface l'écran
print("\n", lab_choisi, sep = "") # avant d'afficher le labyrinthe
print("Ligne {}, Colonne {}\n".format(lab_choisi.robot_pos[0], lab_choisi.robot_pos[1])) # La position du robot

while lab_choisi.robot_pos != lab_choisi.sortie_pos:
    saisie = "" # la saisie clavier du joueur
    reg_ex = r"^([nseoNSEO][0-9]*)|[qQ]$" # regex de vérification
    while re.search(reg_ex, saisie) is None:
        saisie = input("> ")

    if saisie.upper() == "Q":
        print("Quitter ?")
        quitter = input("Mettez Q pour confirmer ou C pour Continuer : ")
        if quitter.upper() == "Q":
            print("Votre partie a été sauvegardée")
            exit() # on quitte
    else:
        if len(saisie) == 1:
            saisie += "1" # pour avoir le bon format pour 'saisie' (2 caractères minimum)
        nbfois = int(saisie[1:]) # on récupère la partie nombre de la 'saisie'

        if saisie[0].upper() == "N":
            coord_visee = (lab_choisi.robot_pos[0] - nbfois, lab_choisi.robot_pos[1])
        elif saisie[0].upper() == "S":
            coord_visee = (lab_choisi.robot_pos[0] + nbfois, lab_choisi.robot_pos[1])
        elif saisie[0].upper() == "E":
            coord_visee = (lab_choisi.robot_pos[0], lab_choisi.robot_pos[1] + nbfois)
        elif saisie[0].upper() == "O":
            coord_visee = (lab_choisi.robot_pos[0], lab_choisi.robot_pos[1] - nbfois)

        if coord_visee not in lab_choisi.grille:
            print("C'est hors du labyrinthe !")
        else: # faire les sommes suivantes pour avoir des entiers pour 'range'
            somme_visee, somme_pos = sum(coord_visee), sum(lab_choisi.robot_pos)
            for i in range(min(somme_visee, somme_pos), max(somme_visee, somme_pos)):
                # le robot bouge progressivement
                if saisie[0].upper() == "N":
                    next_coord = (lab_choisi.robot_pos[0] - 1, lab_choisi.robot_pos[1])
                elif saisie[0].upper() == "S":
                    next_coord = (lab_choisi.robot_pos[0] + 1, lab_choisi.robot_pos[1])
                elif saisie[0].upper() == "E":
                    next_coord = (lab_choisi.robot_pos[0], lab_choisi.robot_pos[1] + 1)
                elif saisie[0].upper() == "O":
                    next_coord = (lab_choisi.robot_pos[0], lab_choisi.robot_pos[1] - 1)
                
                # si la prochaine coordonnée dans son mouvement est parmi :
                if lab_choisi.grille[next_coord] in (Labyrinthe.vide, Labyrinthe.porte, Labyrinthe.sortie):
                    lab_choisi.robot_pos = next_coord # le robot se déplace
                    # On enregistre ces coordonnées dans le fichier de sauvegarde
                    chemin = "saves/" + carte_choisie.nom + ".txt"
                    with open(chemin, "w") as fichier:
                        fichier.write(str(lab_choisi.robot_pos[0]) + "," + str(lab_choisi.robot_pos[1]))    
                    time.sleep(ATTENTE) # pause entre deux mouvements
                    os.system("cls") # on efface l'écran
                    print("\n", lab_choisi, sep = "") # avant d'afficher le labyrinthe et la position du robot
                    print("Ligne {}, Colonne {}\n".format(lab_choisi.robot_pos[0], lab_choisi.robot_pos[1]))
                     
if lab_choisi.robot_pos == lab_choisi.sortie_pos: # Quand le robot a atteint la sortie
    print("Félicitations ! Vous avez gagné !")
os.system("pause")