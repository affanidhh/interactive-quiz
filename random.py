import random
import time
import json
import os
import sys
from abc import ABC, abstractmethod

class IVoixOff(ABC):
    """
    Interface pour la voix off du jeu.
    Cette interface définit les méthodes que toute voix off doit implémenter.
    """
    @abstractmethod
    def annoncer(self, type_message, **kwargs):
        pass

class VoixOff(IVoixOff):
    """
    Classe responsable de la gestion des répliques de la voix off.
    Principe SRP : Cette classe a une seule responsabilité.
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
        Annonce un message de la voix off.
        Principe OCP : Ouvert à l'extension (ajout de nouvelles répliques).
        """
        replique = random.choice(self.repliques[type_message])
        print(f"[Voix off] {replique.format(**kwargs)}")

class Presentateur:
    def __init__(self, nom, voix_off: IVoixOff = None):
        self.nom = nom
        self.voix_off = voix_off

    def annoncer_phase(self, nom_phase):
        print(f"\n{self.nom} : --- {nom_phase} ---")
        if self.voix_off:
            self.voix_off.annoncer('phase')

    def annoncer_tour(self, nom_joueur):
        print(f"\n{self.nom} : {nom_joueur}, à vous de jouer !")

    def annoncer_resultat(self, resultat, question=None):
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
        if self.voix_off:
            self.voix_off.annoncer('elimination', joueur=joueur.nom)

    def annoncer_duel(self, joueur1, joueur2):
        if self.voix_off:
            self.voix_off.annoncer('duel', joueur1=joueur1.nom, joueur2=joueur2.nom)

    def annoncer_etoile_mysterieuse(self, nom_joueur):
        if self.voix_off:
            self.voix_off.annoncer('etoile')
        print(f"\n{self.nom} : {nom_joueur}, vous allez maintenant tenter de découvrir l'Étoile Mystérieuse !")
        print(f"{self.nom} : Répondez correctement à au moins 3 questions sur 5 pour remporter l'étoile.")

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.score = 0
        self.niveau_difficulte = 1  # Échelle de 1 (facile) à 3 (difficile)

    def ajuster_difficulte(self, reussite):
        """Ajuste la difficulté selon les performances."""
        if reussite:
            self.niveau_difficulte = min(3, self.niveau_difficulte + 0.5)
        else:
            self.niveau_difficulte = max(1, self.niveau_difficulte - 0.5)

    def __str__(self):
        return f"{self.nom} : {self.score} points"

class Question:
    def __init__(self, enonce, options, reponse_correcte, difficulte, theme, explication):
        self.enonce = enonce
        self.options = options
        self.reponse_correcte = reponse_correcte
        self.difficulte = difficulte  # 1-3
        self.theme = theme
        self.explication = explication

    def poser(self, presentateur, joueur):
        presentateur.annoncer_tour(joueur.nom)
        print(f"\n[{self.theme}] {self.enonce}")
        for i, opt in enumerate(self.options, 1):
            print(f"{i}. {opt}")

        debut = time.time()
        reponse = self.valider_entree_utilisateur(len(self.options))
        temps = time.time() - debut

        temps_limite = 5 if self.difficulte == 1 else 7 if self.difficulte == 2 else 10
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
        """Valide l'entrée utilisateur avec des messages clairs et des réessais."""
        while True:
            try:
                choix = int(input("\nVotre réponse (numéro) : "))
                if 1 <= choix <= nb_options:
                    return choix
                print(f"⚠️ Entrez un numéro entre 1 et {nb_options}.")
            except ValueError:
                print("❌ Entrée invalide. Veuillez entrer un nombre.")

class Recompense:
    BADGES = {
        "Novice": lambda j: j.score >= 10,
        "Expert": lambda j: j.niveau_difficulte >= 2.5,
        "Maître": lambda j: j.score >= 30
    }

    @classmethod
    def verifier_badges(cls, joueur):
        """Attribue des badges selon les performances."""
        nouveaux_badges = [nom for nom, condition in cls.BADGES.items() if condition(joueur)]
        if nouveaux_badges:
            print(f"🎉 {joueur.nom} obtient les badges : {', '.join(nouveaux_badges)} !")

class Jeu:
    def __init__(self):
        self.presentateur = Presentateur("Jean-Luc Reichmann", voix_off=VoixOff())
        self.questions = self._charger_questions()
        self.scores = self._charger_scores()

    def _charger_questions(self):
        questions = [
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
            {"question": "Quel est le plus grand lac d'eau douce du monde?", "options": ["Lac Supérieur", "Lac Victoria", "Lac Baïkal", "Lac Tanganyika"], "correct_option": 1, "difficulty": "moyen", "theme": "Géographie", "explication": "Le plus grand lac d'eau douce du monde est le Lac Supérieur."},
            {"question": "Qui a écrit 'Roméo et Juliette'?", "options": ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"], "correct_option": 1, "difficulty": "moyen", "theme": "Littérature", "explication": "William Shakespeare a écrit 'Roméo et Juliette'."},
            {"question": "Quel est le plus grand désert chaud du monde?", "options": ["Sahara", "Gobi", "Antarctique", "Kalahari"], "correct_option": 1, "difficulty": "difficile", "theme": "Géographie", "explication": "Le plus grand désert chaud du monde est le Sahara."},
            {"question": "Quel est le plus grand pays d'Afrique?", "options": ["Algérie", "Nigeria", "Égypte", "Afrique du Sud"], "correct_option": 1, "difficulty": "moyen", "theme": "Géographie", "explication": "Le plus grand pays d'Afrique est l'Algérie."},
            {"question": "Qui a découvert l'Amérique?", "options": ["Christophe Colomb", "Vasco de Gama", "Marco Polo", "Ferdinand Magellan"], "correct_option": 1, "difficulty": "facile", "theme": "Histoire", "explication": "Christophe Colomb a découvert l'Amérique."},
            {"question": "Quel est le plus grand volcan actif du monde?", "options": ["Mauna Loa", "Krakatoa", "Etna", "Vésuve"], "correct_option": 1, "difficulty": "difficile", "theme": "Géographie", "explication": "Le plus grand volcan actif du monde est le Mauna Loa."},
            {"question": "Qui a écrit 'La Divine Comédie'?", "options": ["Dante Alighieri", "Geoffrey Chaucer", "John Milton", "Homer"], "correct_option": 1, "difficulty": "difficile", "theme": "Littérature", "explication": "Dante Alighieri a écrit 'La Divine Comédie'."}
        ]
        return [Question(q["question"], q["options"], q["correct_option"], self._convertir_difficulte(q["difficulty"]), q["theme"], q["explication"]) for q in questions]

    def _convertir_difficulte(self, difficulte):
        if difficulte == "facile":
            return 1
        elif difficulte == "moyen":
            return 2
        elif difficulte == "difficile":
            return 3
        return 1  # Par défaut

    def _charger_scores(self):
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                return json.load(f)
        return {}

    def _sauvegarder_scores(self):
        with open("scores.json", "w") as f:
            json.dump(self.scores, f)

    def _afficher_scores(self, joueurs):
        print("\n--- Scores ---")
        for joueur in joueurs:
            print(joueur)

    def _eliminer_joueurs(self, joueurs):
        scores = [j.score for j in joueurs]
        if len(set(scores)) == 1:
            print("\nÉgalité ! Personne n'est éliminé.")
            return joueurs
        score_min = min(scores)
        return [j for j in joueurs si j.score > score_min]

    def duel_final(self, joueur1, joueur2):
        self.presentateur.annoncer_duel(joueur1, joueur2)
        questions_duel = [q for q in self.questions si q.difficulte == 3]
        random.shuffle(questions_duel)

        for question in questions_duel:
            self.presentateur.annoncer_tour(joueur1.nom)
            if question.poser(self.presentateur, joueur1):
                print(f"{joueur1.nom} marque {question.difficulte} point(s) !")
            else:
                print(f"{jou