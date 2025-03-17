import logging

class Joueur:
    """
    Classe représentant un joueur.

    Attributs:
        nom (str): Le nom du joueur.
        score (int): Le score du joueur.
    """

    def __init__(self, nom):
        """
        Initialise une instance de la classe Joueur.

        Args:
            nom (str): Le nom du joueur.

        Raises:
            ValueError: Si le nom n'est pas une chaîne de caractères non vide.
        """
        if not nom or not isinstance(nom, str):
            raise ValueError("Le nom du joueur doit être une chaîne de caractères non vide.")
        self.nom = nom
        self.score = 0
        logging.info(f"Joueur {nom} créé avec un score initial de {self.score}")

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du joueur.

        Returns:
            str: Représentation du joueur.
        """
        return f"{self.nom} : {self.score} points"