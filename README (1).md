# Jeu de Quiz Interactif

Bienvenue dans notre jeu de quiz interactif ! Ce projet est conçu pour offrir une expérience de quiz amusante et engageante, avec des fonctionnalités telles que des questions dynamiques, des niveaux de difficulté ajustables, et des récompenses pour les joueurs.

## Table des matières
1. [Introduction](#introduction)
2. [Fonctionnalités](#fonctionnalités)
3. [Installation](#installation)
4. [Utilisation](#utilisation)
5. [Structure du Projet](#structure-du-projet)
6. [Documentation](#documentation)
7. [Contribuer](#contribuer)
8. [Licence](#licence)

## Introduction

Ce jeu de quiz interactif est conçu pour tester vos connaissances dans divers domaines tels que la géographie, l'histoire, la science, et plus encore. Les joueurs peuvent répondre à des questions, accumuler des points, et gagner des badges en fonction de leurs performances.

## Fonctionnalités

- **Questions Dynamiques** : Une variété de questions de différents niveaux de difficulté.
- **Niveaux de Difficulté Ajustables** : La difficulté des questions s'ajuste en fonction des performances des joueurs.
- **Récompenses et Badges** : Les joueurs peuvent gagner des badges en fonction de leurs scores et de leurs niveaux de difficulté.
- **Voix Off** : Annonces vocales pour une expérience immersive.

## Installation

### Prérequis

- Python 3.7 ou plus récent
- `pip` pour la gestion des packages Python

### Étapes d'Installation

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/affanidhh/quiz-game.git
    cd quiz-game
    ```

2. Installez les dépendances :
    ```sh
    pip install -r requirements.txt
    ```

3. Exécutez le jeu :
    ```sh
    python jeu.py
    ```

## Utilisation

Lancez le jeu en exécutant le fichier `jeu.py`. Le jeu vous guidera à travers les différentes phases, posera des questions, et annoncera les résultats.

## Structure du Projet

- `jeu.py` : Fichier principal contenant la logique du jeu.
- `requirements.txt` : Liste des dépendances nécessaires pour exécuter le jeu.
- `README.md` : Documentation du projet.

## Documentation

### 1. Erreurs Rencontrées et Corrections

**SyntaxError: invalid syntax. Perhaps you forgot a comma?**

**Message d'erreur:**
```
Traceback (most recent call last):
  File "/Users/affanidhh/Downloads/Test /main.py", line 1, in <module>
    from jeu import Jeu  # Assurez-vous que le nom du fichier où la classe Jeu est définie est 'jeu.py'
  File "/Users/affanidhh/Downloads/Test /jeu.py", line 309
    nouveaux_badges = [nom pour nom, condition in cls.BADGES.items() if condition(joueur)]
                       ^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

**Cause:**
Cette erreur est due à une mauvaise syntaxe dans la compréhension de liste.

**Correction:**
La syntaxe correcte pour la compréhension de liste est :
```python
[nom for nom, condition in cls.BADGES.items() if condition(joueur)]
```

**Erreurs de dépendances manquantes**

**Message d'erreur:**
```
ModuleNotFoundError: No module named 'nom_du_module'
```

**Cause:**
Les modules requis n'étaient pas installés.

**Correction:**
Ajout d'une fonction `verifier_et_installer_modules()` pour vérifier et installer les modules nécessaires à partir du fichier `requirements.txt`.

**Erreurs de syntaxe dans le code Python**

**Message d'erreur:**
```
Erreurs détectées par flake8 :
```

**Cause:**
Erreurs de style ou de syntaxe détectées par flake8.

**Correction:**
Ajout d'une fonction `verifier_code()` pour vérifier les erreurs de syntaxe dans le fichier `jeu.py` avec flake8 et les corriger avant d'exécuter le script.

### 2. Documentation des Fonctions et Modules

#### Fonctions Utilisées

**verifier_et_installer_modules**

```python
def verifier_et_installer_modules():
    """
    Vérifie et installe/mettre à jour les modules nécessaires spécifiés dans le fichier requirements.txt.
    """
```

- **Description :** Vérifie et installe/mettre à jour les modules nécessaires spécifiés dans le fichier `requirements.txt`.
- **Paramètres :** Aucun.
- **Retour :** Aucun.

**verifier_code**

```python
def verifier_code():
    """
    Vérifie les erreurs de syntaxe dans le fichier jeu.py avec flake8.
    """
```

- **Description :** Vérifie les erreurs de syntaxe dans le fichier `jeu.py` avec flake8.
- **Paramètres :** Aucun.
- **Retour :** Aucun.

#### Classes Utilisées

**IVoixOff**

```python
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
```

- **Description :** Interface pour Voix Off.
- **Méthodes :**
  - `annoncer(self, type_message, **kwargs)`: Méthode abstraite pour annoncer un message.

**VoixOff**

```python
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
            ...
        }

    def annoncer(self, type_message, **kwargs):
        """
        Annonce un message aléatoire basé sur le type de message.
        
        :param type_message: Type de message à annoncer.
        :param kwargs: Arguments supplémentaires pour formater le message.
        """
        replique = random.choice(self.repliques[type_message])
        print(f"[Voix off] {replique.format(**kwargs)}")
```

- **Description :** Classe pour gérer les annonces de la Voix Off.
- **Méthodes :**
  - `__init__(self)`: Initialise les répliques.
  - `annoncer(self, type_message, **kwargs)`: Annonce un message aléatoire basé sur le type de message.

**Presentateur**

```python
class Presentateur:
    """
    Classe pour gérer les annonces du présentateur.
    """
    def __init__(self, nom, voix_off: IVoixOff = None):
        self.nom = nom
        self.voix_off = voix_off

    def annoncer_phase(self, nom_phase):
        """
        Annonce le début d'une nouvelle phase.
        
        :param nom_phase: Nom de la phase.
        """
        ...

    def annoncer_tour(self, nom_joueur):
        """
        Annonce le tour d'un joueur.
        
        :param nom_joueur: Nom du joueur.
        """
        ...

    def annoncer_resultat(self, resultat, question=None):
        """
        Annonce le résultat d'une question pour un joueur.
        
        :param resultat: Booléen indiquant si la réponse est correcte.
        :param question: Instance de Question contenant les détails de la question.
        """
        ...

    def annoncer_elimination(self, joueur):
        """
        Annonce l'élimination d'un joueur.
        
        :param joueur: Instance de Joueur à éliminer.
        """
        ...

    def annoncer_duel(self, joueur1, joueur2):
        """
        Annonce le début d'un duel entre deux joueurs.
        
        :param joueur1: Premier joueur.
        :param joueur2: Deuxième joueur.
        """
        ...

    def annoncer_etoile_mysterieuse(self, nom_joueur):
        """
        Annonce le début de l'Étoile Mystérieuse pour un joueur.
        
        :param nom_joueur: Nom du joueur.
        """
        ...
```

- **Description :** Classe pour gérer les annonces du présentateur.
- **Méthodes :**
  - `__init__(self, nom, voix_off: IVoixOff = None)`: Initialise le présentateur avec un nom et une voix off optionnelle.
  - `annoncer_phase(self, nom_phase)`: Annonce le début d'une nouvelle phase.
  - `annoncer_tour(self, nom_joueur)`: Annonce le tour d'un joueur.
  - `annoncer_resultat(self, resultat, question=None)`: Annonce le résultat d'une question pour un joueur.
  - `annoncer_elimination(self, joueur)`: Annonce l'élimination d'un joueur.
  - `annoncer_duel(self, joueur1, joueur2)`: Annonce le début d'un duel entre deux joueurs.
  - `annoncer_etoile_mysterieuse(self, nom_joueur)`: Annonce le début de l'Étoile Mystérieuse pour un joueur.

**Joueur**

```python
class Joueur:
    """
    Classe représentant un joueur.
    """
    def __init__(self, nom):
        self.nom = nom
        self.score = 0
        self.niveau_difficulte = 1  # Échelle de 1 (facile) à 3 (difficile)

    def ajuster_difficulte(self, reussite):
        """
        Ajuste la difficulté en fonction du succès ou de l'échec du joueur.
        
        :param reussite: Booléen indiquant si le joueur a réussi.
        """
        ...

    def __str__(self):
        return f"{self.nom} : {self.score} points"
```

- **Description :** Classe représentant un joueur.
- **Méthodes :**
  - `__init__(self, nom)`: Initialise un joueur avec un nom.
  - `ajuster_difficulte(self, reussite)`: Ajuste la difficulté en fonction du succès ou de l'échec du joueur.
  - `__str__(self)`: Retourne une représentation en chaîne du joueur avec son score.

**Question**

```python
class Question:
    """
    Classe représentant une question de quiz.
    """
    def __init__(self, enonce, options, reponse_correcte, difficulte, theme, explication):
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
        ...

    @staticmethod
    def valider_entree_utilisateur(nb_options):
        """
        Valide l'entrée utilisateur pour s'assurer qu'elle est un numéro valide.
        
        :param nb_options: Nombre d'options disponibles.
        :return: Choix de l'utilisateur.
        """
        ...
```

- **Description :** Classe représentant une question de quiz.
- **Méthodes :**
  - `__init__(self, enonce, options, reponse_correcte, difficulte, theme, explication)`: Initialise une question de quiz.
  - `poser(self, presentateur, joueur)`: Pose une question au joueur et traite sa réponse.
  - `valider_entree_utilisateur(nb_options)`: Valide l'entrée utilisateur pour s'assurer qu'elle est un numéro valide.

**Recompense**

```python
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
        ...
```

- **Description :** Classe pour gérer les récompenses et badges des joueurs.
- **Méthodes :**
  - `verifier_badges(cls, joueur)`: Vérifie et attribue les badges gagnés par le joueur.

**Jeu**

```python
class Jeu:
    """
    Classe principale pour gérer le jeu.
    """
    def __init__(self):
        self.presentateur = Presentateur("Jean-Luc Reichmann", voix_off=VoixOff())
        self.questions = self._charger_questions()
        self.scores = self._charger_scores()

    def _charger_questions(self):
        """
        Charge les questions depuis une source de données.
        """
        ...

    def _charger_scores(self):
        """
        Charge les scores depuis un fichier JSON.
        """
        ...

    def _sauvegarder_scores(self):
        """
        Sauvegarde les scores dans un fichier JSON.
        """
        ...

    def jouer_tour(self, joueur):
        """
        Joue un tour de jeu pour un joueur donné.
        
        :param joueur: Instance de Joueur.
        """
        ...

    def jouer(self):
        """
        Démarre le jeu.
        """
        ...
```

- **Description :** Classe principale pour gérer le jeu.
- **Méthodes :**
  - `__init__(self)`: Initialise le jeu en chargeant les questions et les scores.
  - `_charger_questions(self)`: Charge les questions depuis une source de données.
  - `_charger_scores(self)`: Charge les scores depuis un fichier JSON.
  - `_sauvegarder_scores(self)`: Sauvegarde les scores dans un fichier JSON.
  - `jouer_tour(self, joueur)`: Joue un tour de jeu pour un joueur donné.
  - `jouer(self)`: Démarre le jeu.

### 2.3. Modules Utilisés

#### random

- **Description :** Le module `random` permet de générer des nombres aléatoires.
- **Fonctions Utilisées :**
  - `random.choice(seq)`: Retourne un élément aléatoire de la séquence non-vide `seq`.

#### time

- **Description :** Le module `time` permet de manipuler le temps (ex: obtenir l'heure actuelle, mesurer la durée).
- **Fonctions Utilisées :**
  - `time.time()`: Retourne le temps écoulé en secondes depuis l'époque (le 1er janvier 1970, 00:00:00 UTC).

#### json

- **Description :** Le module `json` permet de manipuler des données en format JSON (JavaScript Object Notation).
- **Fonctions Utilisées :**
  - `json.load(fp)`: Désérialise `fp` (un texte ou un fichier binaire contenant un document JSON) en un objet Python.
  - `json.dump(obj, fp)`: Sérialise `obj` en un flux de texte JSON et l'écrit dans `fp` (un texte ou un fichier binaire).

#### os

- **Description :** Le module `os` permet d'interagir avec le système d'exploitation (ex: vérifier l'existence de fichiers).
- **Fonctions Utilisées :**
  - `os.path.exists(path)`: Retourne `True` si `path` fait référence à un chemin existant.

#### sys

- **Description :** Le module `sys` permet d'interagir avec l'interpréteur Python (ex: sortie du programme).
- **Fonctions Utilisées :**
  - `sys.exit([arg])`: Termine l'exécution du programme en optionnellement passant un argument à l'interpréteur.

#### subprocess

- **Description :** Le module `subprocess` permet de lancer des sous-processus (ex: installer des modules, vérifier le code).
- **Fonctions Utilisées :**
  - `subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False)`: Exécute la commande décrite par `args`. Si la commande retourne un code de sortie différent de zéro, une `CalledProcessError` est levée.

#### abc

- **Description :** Le module `abc` permet de définir des classes et méthodes abstraites.
- **Fonctions Utilisées :**
  - `abc.ABC`: Une classe utilitaire permettant de définir des classes abstraites.
  - `abc.abstractmethod`: Un décorateur indiquant des méthodes abstraites dans les classes abstraites.

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer, veuillez suivre les étapes suivantes :

1. Fork le dépôt.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/NouvelleFeature`).
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`).
4. Poussez votre branche (`git push origin feature/NouvelleFeature`).
5. Ouvrez une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.