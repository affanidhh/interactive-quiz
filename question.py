import logging
import time
from functools import lru_cache

class Question:
    """
    Classe représentant une question du jeu.

    Attributs:
        enonce (str): L'énoncé de la question.
        options (list): Les options de réponse.
        reponse_correcte (int): L'indice de la réponse correcte.
        difficulte (int): Le niveau de difficulté de la question.
    """

    def __init__(self, enonce, options, reponse_correcte, difficulte):
        """
        Initialise une instance de la classe Question.

        Args:
            enonce (str): L'énoncé de la question.
            options (list): Les options de réponse.
            reponse_correcte (int): L'indice de la réponse correcte.
            difficulte (int): Le niveau de difficulté de la question.

        Raises:
            ValueError: Si les arguments ne sont pas valides.
        """
        if not enonce or not isinstance(enonce, str):
            raise ValueError("L'énoncé de la question doit être une chaîne de caractères non vide.")
        if not options or not isinstance(options, list) or not all(isinstance(option, str) for option in options):
            raise ValueError("Les options doivent être une liste de chaînes de caractères non vides.")
        if not isinstance(reponse_correcte, int) or reponse_correcte < 1 or reponse_correcte > len(options):
            raise ValueError("L'indice de la réponse correcte doit être un entier valide.")
        if not isinstance(difficulte, int) or difficulte < 1 or difficulte > 3:
            raise ValueError("Le niveau de difficulté doit être un entier entre 1 et 3.")

        self.enonce = enonce
        self.options = options
        self.reponse_correcte = reponse_correcte
        self.difficulte = difficulte
        logging.info(f"Question créée: {self.enonce} avec difficulté {self.difficulte}")

    @lru_cache(maxsize=32)
    def poser(self, presentateur, joueur):
        """
        Pose la question à un joueur et gère la réponse.

        Args:
            presentateur (Presentateur): Le présentateur du jeu.
            joueur (Joueur): Le joueur à qui la question est posée.

        Returns:
            bool: Vrai si le joueur a donné la bonne réponse, Faux sinon.

        Raises:
            ValueError: Si la réponse de l'utilisateur est hors limites.
        """
        presentateur.annoncer_tour(joueur.nom)
        print(f"\n{self.enonce}")
        for i, option in enumerate(self.options, 1):
            print(f"{i}. {option}")

        debut = time.time()
        try:
            reponse = int(input("\nVotre réponse (numéro) : ").strip())
            if reponse < 1 or reponse > len(self.options):
                raise ValueError("Réponse hors limites")
            temps = time.time() - debut
        except ValueError:
            logging.error("Réponse hors limites ou erreur de saisie")
            presentateur.annoncer_resultat(False)
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue : {e}")
            presentateur.annoncer_resultat(False)
            return False

        temps_limite = 5 + 2 * (self.difficulte - 1)
        if temps > temps_limite:
            logging.info(f"Temps écoulé : {temps:.1f} secondes")
            print(f"\nTemps écoulé : {temps:.1f} secondes")
            presentateur.annoncer_resultat(False)
            return False

        if reponse == self.reponse_correcte:
            joueur.score += self.difficulte
            logging.info(f"Bonne réponse de {joueur.nom}, score actuel : {joueur.score}")
            presentateur.annoncer_resultat(True)
            return True
        else:
            logging.info(f"Mauvaise réponse de {joueur.nom}, la bonne réponse était : {self.options[self.reponse_correcte - 1]}")
            presentateur.annoncer_resultat(False, self.options[self.reponse_correcte - 1])
            return False