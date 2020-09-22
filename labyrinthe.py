# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:
    """Classe représentant un labyrinthe."""
    # Symboles utilisés, variables de classe :
    robot = "X"
    porte = "."
    sortie = "O"
    mur = "|"
    vide = " "
    
    def __init__(self, obstacles):
        """Création du labyrinthe à partir de la chaine d'"obstacles" contenus dans une carte"""
        self.contenu = obstacles
        self.grille = {} # le dictionnaire des obstacles (items) : (portes, murs, sortie, vide)
        # - en clé : leurs coordonnées (x,y) # - en valeur : le symbole
        self.lignes_obstacles = obstacles.split("\n")
        
        numli = 0 # avec numli += 1, car self.lignes_obstacles.index(li) renvoie juste le premier indice correspondant au contenu de la ligne li, or deux lignes différentes peuvent avoir le même contenu
        for li in self.lignes_obstacles:
            numli += 1
            for col in range(len(li)):
                coord = (numli, col + 1)
                if li[col] == Labyrinthe.robot:
                    self.robot_pos = coord # Coordonnées (x,y) du robot
                # on met coordonées et symboles dans la grille, sans tenir compte du robot
                if li[col] == Labyrinthe.porte:
                    self.grille[coord] = Labyrinthe.porte
                elif li[col] == Labyrinthe.sortie:
                    self.grille[coord] = Labyrinthe.sortie
                    self.sortie_pos = coord
                elif li[col] == Labyrinthe.mur:
                    self.grille[coord] = Labyrinthe.mur
                else: # le vide ou même pour le robot
                    self.grille[coord] = Labyrinthe.vide
        
    def __repr__(self):
        """Représentation d'un Labyrinthe, en mettant le robot à sa position"""
        res = ""
        numli = 0
        for li in self.lignes_obstacles:
            numli += 1
            for col in range(len(li)):
                coord = (numli, col + 1)
                if coord == self.robot_pos:
                    res += Labyrinthe.robot
                else:
                    res += str(self.grille[coord])
            res += "\n"
        return res