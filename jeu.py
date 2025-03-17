import random
import time
import json
import os
import sys
import subprocess
from abc import ABC, abstractmethod

def verifier_et_installer_modules():
    """
    Vérifie et installe/mettre à jour les modules nécessaires spécifiés dans le fichier requirements.txt.
    """
    try:
        import pip
    except ImportError:
        print("pip n'est pas installé. Veuillez installer pip et réessayer.")
        sys.exit(1)
    
    with open('requirements.txt', 'r') as f:
        modules = f.read().splitlines()
    
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Le module {module} n'est pas installé. Installation en cours...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        else:
            print(f"Le module {module} est installé. Vérification des mises à jour...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", module])

verifier_et_installer_modules()

def verifier_code():
    """
    Vérifie les erreurs de syntaxe dans le fichier jeu.py avec flake8.
    """
    try:
        result = subprocess.run([sys.executable, "-m", "flake8", "jeu.py"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Erreurs détectées par flake8 :")
            print(result.stdout)
            sys.exit(1)
    except Exception as e:
        print(f"Erreur lors de l'exécution de flake8 : {e}")
        sys.exit(1)

verifier_code()

class IVoixOff(ABC):
    """
    Interface pour Voix Off.
    """
    @abstractmethod
    def annoncer(self, type_message, **kwargs):
        """
        Méthode pour annoncer un message.
        
        :param type_message: Type de message à annoncer.
        :param kwargs: Arguments supplémentaires pour formater le message.
        """
        pass

class VoixOff(IVoixOff):
    """
    Classe pour gérer les annonces de la Voix Off.
    """
    def __init__(self):
        self.repliques = {
            'debut': [
                "Accrochez vos ceintures, on commence l'aventure !",
                "Attention les amis, le stylo est chaud et le jeu aussi !"
            ],
            'correct': [
                "Bonne réponse ! Même mon neveu de 5 ans aurait trouvé ça... enfin presque !",
                "Exact ! Vous êtes chaud comme un soleil d'août aujourd'hui ! 🔥"
            ],
            'incorrect': [
                "Oh la la... C'était {reponse} ! On va dire que c'était un piège !",
                "Non non non ! La réponse était {reponse}. Mais chut, je ne dirai rien à personne ! 🤫"
            ],
            'temps': [
                "Temps écoulé ! Plus lent qu'un escargot enrhumé ! 🐌",
                "Allez, on se réveille ! Le temps, c'est de l'argent ! 💰"
            ],
            'phase': [
                "Phase suivante ! Préparez les glaçons, ça va chauffer ! ❄️",
                "Attention aux oreilles, on passe à la vitesse supérieure ! 🚀"
            ],
            'etoile': [
                "L'Étoile Mystérieuse ! Le moment que tout le monde attend... surtout mon dentiste ! 😬",
                "C'est l'heure de vérité... Et de transpiration ! 💦"
            ],
            'elimination': [
                "C'est la fin du chemin pour {joueur}. On se revoit à la prochaine !",
                "{joueur}, vous êtes éliminé. Mais gardez le sourire ! 😊"
            ],
            'duel': [
                "C'est l'heure du duel final ! Qui sera le Maître de Midi ?",
                "Attention, ça va chauffer entre {joueur1} et {joueur2} ! 🔥"
            ]
        }

    def annoncer(self, type_message, **kwargs):
        """
        Annonce un message aléatoire basé sur le type de message.
        
        :param type_message: Type de message à annoncer.
        :param kwargs: Arguments supplémentaires pour formater le message.
        """
        replique = random.choice(self.repliques[type_message])
        print(f"[Voix off] {replique.format(**kwargs)}")

class Presentateur:
    """
    Classe pour gérer les annonces du présentateur.
    """
    def __init__(self, nom, voix_off: IVoixOff = None):
        """
        Initialise le présentateur avec un nom et une voix off optionnelle.
        
        :param nom: Nom du présentateur.
        :param voix_off: Instance de IVoixOff pour les annonces vocales.
        """
        self.nom = nom
        self.voix_off = voix_off

    def annoncer_phase(self, nom_phase):
        """
        Annonce le début d'une nouvelle phase.
        
        :param nom_phase: Nom de la phase.
        """
        print(f"\n{self.nom} : --- {nom_phase} ---")
        if self.voix_off:
            self.voix_off.annoncer('phase')

    def annoncer_tour(self, nom_joueur):
        """
        Annonce le tour d'un joueur.
        
        :param nom_joueur: Nom du joueur.
        """
        print(f"\n{self.nom} : {nom_joueur}, à vous de jouer !")

    def annoncer_resultat(self, resultat, question=None):
        """
        Annonce le résultat d'une question pour un joueur.
        
        :param resultat: Booléen indiquant si la réponse est correcte.
        :param question: Instance de Question contenant les détails de la question.
        """
        if self.voix_off:
            if resultat:
                self.voix_off.annoncer('correct')
            else:
                if question:
                    reponse = question.options[question.reponse_correcte - 1]
                    self.voix_off.annoncer('incorrect', reponse=reponse)
                else:
                    self.voix_off.annoncer('temps')

    def annoncer_elimination(self, joueur):
        """
        Annonce l'élimination d'un joueur.
        
        :param joueur: Instance de Joueur à éliminer.
        """
        if self.voix_off:
            self.voix_off.annoncer('elimination', joueur=joueur.nom)

    def annoncer_duel(self, joueur1, joueur2):
        """
        Annonce le début d'un duel entre deux joueurs.
        
        :param joueur1: Premier joueur.
        :param joueur2: Deuxième joueur.
        """
        if self.voix_off:
            self.voix_off.annoncer('duel', joueur1=joueur1.nom, joueur2=joueur2.nom)

    def annoncer_etoile_mysterieuse(self, nom_joueur):
        """
        Annonce le début de l'Étoile Mystérieuse pour un joueur.
        
        :param nom_joueur: Nom du joueur.
        """
        if self.voix_off:
            self.voix_off.annoncer('etoile')
        print(f"\n{self.nom} : {nom_joueur}, vous allez maintenant tenter de découvrir l'Étoile Mystérieuse !")
        print(f"{self.nom} : Répondez correctement à au moins 3 questions sur 5 pour remporter l'étoile.")

class Joueur:
    """
    Classe représentant un joueur.
    """
    def __init__(self, nom):
        """
        Initialise un joueur avec un nom.
        
        :param nom: Nom du joueur.
        """
        self.nom = nom
        self.score = 0
        self.niveau_difficulte = 1  # Échelle de 1 (facile) à 3 (difficile)

    def ajuster_difficulte(self, reussite):
        """
        Ajuste la difficulté en fonction du succès ou de l'échec du joueur.
        
        :param reussite: Booléen indiquant si le joueur a réussi.
        """
        if reussite:
            self.niveau_difficulte = min(3, self.niveau_difficulte + 0.5)
        else:
            self.niveau_difficulte = max(1, self.niveau_difficulte - 0.5)

    def __str__(self):
        return f"{self.nom} : {self.score} points"

class Question:
    """
    Classe représentant une question de quiz.
    """
    def __init__(self, enonce, options, reponse_correcte, difficulte, theme, explication):
        """
        Initialise une question de quiz.
        
        :param enonce: Énoncé de la question.
        :param options: Liste des options de réponse.
        :param reponse_correcte: Index de la réponse correcte.
        :param difficulte: Difficulté de la question (1-3).
        :param theme: Thème de la question.
        :param explication: Explication de la réponse correcte.
        """
        self.enonce = enonce
        self.options = options
        self.reponse_correcte = reponse_correcte
        self.difficulte = difficulte  # 1-3
        self.theme = theme
        self.explication = explication

    def poser(self, presentateur, joueur):
        """
        Pose une question au joueur et traite sa réponse.
        
        :param presentateur: Instance de Presentateur pour annoncer la question.
        :param joueur: Instance de Joueur à qui la question est posée.
        """
        presentateur.annoncer_tour(joueur.nom)
        print(f"\n[{self.theme}] {self.enonce}")
        for i, opt in enumerate(self.options, 1):
            print(f"{i}. {opt}")

        debut = time.time()
        reponse = self.valider_entree_utilisateur(len(self.options))
        temps = time.time() - debut

        temps_limite = 5 si self.difficulte == 1 sinon 7 si self.difficulte == 2 sinon 10
        if temps > temps_limite:
            print(f"\nTemps écoulé : {temps:.1f}s")
            presentateur.annoncer_resultat(False)
            return False

        if reponse == self.reponse_correcte:
            joueur.score += self.difficulte
            joueur.ajuster_difficulte(True)
            presentateur.annoncer_resultat(True)
            return True
        else:
            joueur.ajuster_difficulte(False)
            presentateur.annoncer_resultat(False, self)
            return False

    @staticmethod
    def valider_entree_utilisateur(nb_options):
        """
        Valide l'entrée utilisateur pour s'assurer qu'elle est un numéro valide.
        
        :param nb_options: Nombre d'options disponibles.
        :return: Choix de l'utilisateur.
        """
        while True:
            try:
                choix = int(input("\nVotre réponse (numéro) : "))
                if 1 <= choix <= nb_options:
                    return choix
                print(f"⚠️ Entrez un numéro entre 1 et {nb_options}.")
            except ValueError:
                print("❌ Entrée invalide. Veuillez entrer un nombre.")

class Recompense:
    """
    Classe pour gérer les récompenses et badges des joueurs.
    """
    BADGES = {
        "Novice": lambda j: j.score >= 10,
        "Expert": lambda j: j.niveau_difficulte >= 2.5,
        "Maître": lambda j: j.score >= 30
    }

    @classmethod
    def verifier_badges(cls, joueur):
        """
        Vérifie et attribue les badges gagnés par le joueur.
        
        :param joueur: Instance de Joueur à vérifier.
        """
        nouveaux_badges = [nom pour nom, condition in cls.BADGES.items() if condition(joueur)]
        if nouveaux_badges:
            print(f"🎉 {joueur.nom} obtient les badges : {', '.join(nouveaux_badges)} !")

class Jeu:
    """
    Classe principale pour gérer le jeu.
    """
    def __init__(self):
        """
        Initialise le jeu en chargeant les questions et les scores.
        """
        self.presentateur = Presentateur("Jean-Luc Reichmann", voix_off=VoixOff())
        self.questions = self._charger_questions()
        self.scores = self._charger_scores()

     def _charger_questions(self):
        """
        Charge les questions depuis une source de données.
        """
        questions = [
            {"question": "Quel est le plus grand lac d'eau douce du monde?", "options": ["Lac Supérieur", "Lac Victoria", "Lac Baïkal", "Lac Tanganyika"], "correct_option": 1, "difficulty": "moyen", "theme": "Géographie", "explication": "Le plus grand lac d'eau douce du monde est le Lac Supérieur."},
            {"question": "Quelle est la capitale de la France?", "options": ["Paris", "Londres", "Berlin", "Madrid"], "correct_option": 1, "difficulty": "facile", "theme": "Géographie", "explication": "La capitale de la France est Paris."},
            {"question": "Quel est le plus grand océan?", "options": ["Atlantique", "Pacifique", "Indien", "Arctique"], "correct_option": 2, "difficulty": "facile", "theme": "Géographie", "explication": "Le plus grand océan est le Pacifique."},
            {"question": "Quel est le plus long fleuve du monde?", "options": ["Nil", "Amazone", "Yangtsé", "Mississippi"], "correct_option": 2, "difficulty": "moyen", "theme": "Géographie", "explication": "Le plus long fleuve du monde est l'Amazone."},
            {"question": "Qui a écrit 'Les Misérables'?", "options": ["Victor Hugo", "Émile Zola", "Gustave Flaubert", "Marcel Proust"], "correct_option": 1, "difficulty": "moyen", "theme": "Littérature", "explication": "Victor Hugo a écrit 'Les Misérables'."},
            {"question": "Quelle est la planète la plus proche du soleil?", "options": ["Mercure", "Vénus", "Terre", "Mars"], "correct_option": 1, "difficulty": "facile", "theme": "Science", "explication": "La planète la plus proche du soleil est Mercure."},
            {"question": "En quelle année a eu lieu la Révolution française?", "options": ["1789", "1776", "1804", "1815"], "correct_option": 1, "difficulty": "moyen", "theme": "Histoire", "explication": "La Révolution française a eu lieu en 1789."},
            {"question": "Quel est le symbole chimique de l'or?", "options": ["Au", "Ag", "Fe", "O"], "correct_option": 1, "difficulty": "facile", "theme": "Science", "explication": "L'or a pour symbole chimique Au."},
            {"question": "Qui a peint la Joconde?", "options": ["Léonard de Vinci", "Michel-Ange", "Raphaël", "Donatello"], "correct_option": 1, "difficulty": "facile", "theme": "Art", "explication": "La Joconde a été peinte par Léonard de Vinci."},
            {"question": "Quel est le plus grand désert du monde?", "options": ["Sahara", "Gobi", "Antarctique", "Kalahari"], "correct_option": 3, "difficulty": "difficile", "theme": "Géographie", "explication": "Le plus grand désert du monde est l'Antarctique."},
            {"question": "Quel est le plus haut sommet du monde?", "options": ["Everest", "K2", "Kangchenjunga", "Lhotse"], "correct_option": 1, "difficulty": "moyen", "theme": "Géographie", "explication": "Le plus haut sommet du monde est l'Everest."},
            {"question": "Qui a découvert la pénicilline?", "options": ["Alexander Fleming", "Marie Curie", "Louis Pasteur", "Isaac Newton"], "correct_option": 1, "difficulty": "moyen", "theme": "Science", "explication": "Alexander Fleming a découvert la pénicilline."},
            {"question": "Quel est le plus grand mammifère marin?", "options": ["Baleine bleue", "Orque", "Dauphin", "Requin blanc"], "correct_option": 1, "difficulty": "facile", "theme": "Science", "explication": "Le plus grand mammifère marin est la baleine bleue."},
            {"question": "Quel est le plus petit pays du monde?", "options": ["Vatican", "Monaco", "Nauru", "San Marin"], "correct_option": 1, "difficulty": "facile", "theme": "Géographie", "explication": "Le plus petit pays du monde est le Vatican."},
            {"question": "Qui a écrit 'Le Petit Prince'?", "options": ["Antoine de Saint-Exupéry", "Jules Verne", "Albert Camus", "Jean-Paul Sartre"], "correct_option": 1, "difficulty": "moyen", "theme": "Littérature", "explication": "Antoine de Saint-Exupéry a écrit 'Le Petit Prince'."},
            {"question": "Quelle est la capitale de l'Australie?", "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "correct_option": 3, "difficulty": "moyen", "theme": "Géographie", "explication": "La capitale de l'Australie est Canberra."},
            {"question": "Quel est le plus grand continent?", "options": ["Asie", "Afrique", "Amérique du Nord", "Europe"], "correct_option": 1, "difficulty": "facile", "theme": "Géographie", "explication": "Le plus grand continent est l'Asie."},
            {"question": "Qui a inventé l'ampoule électrique?", "options": ["Thomas Edison", "Nikola Tesla", "Alexander Graham Bell", "Benjamin Franklin"], "correct_option": 1, "difficulty": "moyen", "theme": "Science", "explication": "Thomas Edison a inventé l'ampoule électrique."},
            {"question": "Quel est le plus grand pays du monde par superficie?", "options": ["Russie", "Canada", "Chine", "États-Unis"], "correct_option": 1, "difficulty": "facile", "theme": "Géographie", "explication": "Le plus grand pays du monde par superficie est la Russie."},
            {"question": "Quel est le plus grand volcan actif du monde?", "options": ["Mauna Loa", "Krakatoa", "Etna", "Vésuve"], "correct_option": 1, "difficulty": "difficile", "theme": "Géographie", "explication": "Le plus grand volcan actif du monde est le Mauna Loa."},
            {"question": "Qui a écrit 'La Divine Comédie'?", "options": ["Dante Alighieri", "Geoffrey Chaucer", "John Milton", "Homer"], "correct_option": 1, "difficulty": "difficile", "theme": "Littérature", "explication": "Dante Alighieri a écrit 'La Divine Comédie'."}
        ]
        return [Question(q["question"], q["options"], q["correct_option"], self._convertir_difficulte(q["difficulty"]), q["theme"], q["explication"]) for q in questions]

    def _convertir_difficulte(self, difficulte):
        """
        Convertit la difficulté de chaîne de caractères à un entier.
        """
        if difficulte == "facile":
            return 1
        elif difficulte == "moyen":
            return 2
        elif difficulte == "difficile":
            return 3
        return 1  # Par défaut

    def _charger_scores(self):
        """
        Charge les scores depuis un fichier JSON.
        """
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                return json.load(f)
        return {}

    def _sauvegarder_scores(self):
        """
        Sauvegarde les scores dans un fichier JSON.
        """
        with open("scores.json", "w") as f:
            json.dump(self.scores, f)

    def jouer_tour(self, joueur):
        """
        Joue un tour de jeu pour un joueur donné.
        """
        question = random.choice(self.questions)
        reussite = question.poser(self.presentateur, joueur)
        Recompense.verifier_badges(joueur)
        return reussite

    def jouer(self):
        """
        Démarre le jeu.
        """
        self.presentateur.annoncer_phase("Début du jeu")
        joueurs = [Joueur("Alice"), Joueur("Bob"), Joueur("Charlie")]
        
        for tour in range(5):
            for joueur in joueurs:
                self.jouer_tour(joueur)
        
        self.presentateur.annoncer_phase("Fin du jeu")
        self._sauvegarder_scores()

        print("\nScores finaux :")
        for joueur in joueurs:
            print(joueur)

if __name__ == "__main__":
    jeu = Jeu()
    jeu.jouer()