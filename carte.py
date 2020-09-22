# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte."""
from labyrinthe import Labyrinthe
class Carte:
    """Objet de transition entre un fichier et un labyrinthe."""

    def __init__(self, nom, chaine):
        """Constructeur des cartes de jeu"""
        self.nom = nom
        self.labyrinthe = Labyrinthe(chaine)

    def __repr__(self):
        """Représentation d'une carte"""
        return "<Carte {}>".format(self.nom)