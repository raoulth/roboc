# -*-coding:Utf-8 -*

def regles_du_jeu():
    """Affiche les règles de Roboc"""
    separateur = "+" + "-".center(50, "-") + "+"
    print(separateur)
    print("|" + "Bienvenue dans Roboc !".center(50) + "|")
    # print(ligne)
    print(separateur)
    print("""Aide Jeu du Roboc : Labyrinthe formé d'obstacles !

Légende (4 symboles) :
X : le robot
| : des murs. -> Le robot ne peut pas les traverser.
. (point) : porte pouvant être traversée.
O : point de sortie du labyrinthe, pour gagner le jeu.

Contrôles du robot:
 Q : Sauvegarder et Quitter la partie en cours
 N : Se déplacer vers le haut
 E : Se déplacer vers la droite
 S : Se déplacer vers le bas
 O : Se déplacer vers la gauche

"Direction + nombre" permet d'avancer nombre de fois :
(Par exemple E3 = Avancer de trois cases vers l'est)
Si "nombre" est trop grand, le robot avancera autant que
possible. Mais ne visez pas une case hors du labyrinthe.""")
    print(separateur)
    print("|" + "Amusez-vous bien !".center(50) + "|")
    print(separateur)