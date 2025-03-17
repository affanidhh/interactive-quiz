import logging

class Presentateur:
    """
    Classe représentant le présentateur du jeu.

    Attributs:
        nom (str): Le nom du présentateur.
    """

    def __init__(self, nom):
        """
        Initialise une instance de la classe Presentateur.

        Args:
            nom (str): Le nom du présentateur.

        Raises:
            ValueError: Si le nom n'est pas une chaîne de caractères non vide.
        """
        if not nom or not isinstance(nom, str):
            raise ValueError("Le nom du présentateur doit être une chaîne de caractères non vide.")
        self.nom = nom

    def annoncer_phase(self, nom_phase):
        """
        Annonce le début d'une phase du jeu.

        Args:
            nom_phase (str): Le nom de la phase à annoncer.

        Raises:
            ValueError: Si le nom de la phase n'est pas une chaîne de caractères non vide.
        """
        if not nom_phase or not isinstance(nom_phase, str):
            raise ValueError("Le nom de la phase doit être une chaîne de caractères non vide.")
        logging.info(f"Annoncer phase: {nom_phase}")
        print(f"\n{self.nom} : --- {nom_phase} ---")

    def annoncer_tour(self, nom_joueur):
        """
        Annonce le tour d'un joueur.

        Args:
            nom_joueur (str): Le nom du joueur dont c'est le tour.

        Raises:
            ValueError: Si le nom du joueur n'est pas une chaîne de caractères non vide.
        """
        if not nom_joueur or not isinstance(nom_joueur, str):
            raise ValueError("Le nom du joueur doit être une chaîne de caractères non vide.")
        logging.info(f"Annoncer tour de: {nom_joueur}")
        print(f"\n{self.nom} : {nom_joueur}, à vous de jouer !")

    def annoncer_resultat(self, resultat, reponse_correcte=None):
        """
        Annonce le résultat d'une question.

        Args:
            resultat (bool): Vrai si le joueur a donné la bonne réponse, Faux sinon.
            reponse_correcte (str, optional): La bonne réponse si le joueur s'est trompé. Par défaut None.

        Raises:
            ValueError: Si le résultat n'est pas un booléen.
        """
        if not isinstance(resultat, bool):
            raise ValueError("Le résultat doit être un booléen.")
        if resultat:
            logging.info("Bonne réponse")
            print(f"{self.nom} : Bonne réponse !")
        else:
            if reponse_correcte:
                logging.info(f"Mauvaise réponse. La bonne réponse était: {reponse_correcte}")
                print(f"{self.nom} : Mauvaise réponse. La bonne réponse était : {reponse_correcte}.")
            else:
                logging.info("Temps écoulé")
                print(f"{self.nom} : Temps écoulé !")

    def annoncer_duel(self, joueur1, joueur2):
        """
        Annonce le début d'un duel entre deux joueurs.

        Args:
            joueur1 (Joueur): Le premier joueur.
            joueur2 (Joueur): Le deuxième joueur.

        Raises:
            ValueError: Si les deux joueurs ne sont pas fournis.
        """
        if not joueur1 or not joueur2:
            raise ValueError("Les deux joueurs doivent être fournis pour le duel.")
        logging.info(f"Duel entre {joueur1.nom} et {joueur2.nom}")
        print(f"\n{self.nom} : Duel final entre {joueur1.nom} et {joueur2.nom} !")

    def annoncer_etoile_mysterieuse(self, nom_joueur):
        """
        Annonce la tentative de découverte de l'Étoile Mystérieuse par un joueur.

        Args:
            nom_joueur (str): Le nom du joueur.

        Raises:
            ValueError: Si le nom du joueur n'est pas une chaîne de caractères non vide.
        """
        if not nom_joueur or not isinstance(nom_joueur, str):
            raise ValueError("Le nom du joueur doit être une chaîne de caractères non vide.")
        logging.info(f"{nom_joueur} tente de découvrir l'Étoile Mystérieuse")
        print(f"\n{self.nom} : {nom_joueur}, vous allez tenter de découvrir l'Étoile Mystérieuse !")