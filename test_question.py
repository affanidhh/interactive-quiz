import unittest
from unittest.mock import patch
from question import Question
from presentateur import Presentateur
from joueur import Joueur

class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.presentateur = Presentateur("Jean-Luc Reichmann")
        self.joueur = Joueur("Maître de Midi")

    def test_initialisation(self):
        question = Question("Quelle est la capitale de la France?", ["Paris", "Londres", "Berlin", "Madrid"], 1, 1)
        self.assertEqual(question.enonce, "Quelle est la capitale de la France?")
        self.assertEqual(question.options, ["Paris", "Londres", "Berlin", "Madrid"])
        self.assertEqual(question.reponse_correcte, 1)
        self.assertEqual(question.difficulte, 1)

    def test_initialisation_erreur(self):
        with self.assertRaises(ValueError):
            Question("", ["Paris", "Londres", "Berlin", "Madrid"], 1, 1)
        with self.assertRaises(ValueError):
            Question("Quelle est la capitale de la France?", [], 1, 1)
        with self.assertRaises(ValueError):
            Question("Quelle est la capitale de la France?", ["Paris", "Londres", "Berlin", "Madrid"], 5, 1)
        with self.assertRaises(ValueError):
            Question("Quelle est la capitale de la France?", ["Paris", "Londres", "Berlin", "Madrid"], 1, 0)

    def test_poser_bonne_reponse(self):
        question = Question("Quelle est la capitale de la France?", ["Paris", "Londres", "Berlin", "Madrid"], 1, 1)
        with patch('builtins.input', return_value="1"):
            self.assertTrue(question.poser(self.presentateur, self.joueur))
            self.assertEqual(self.joueur.score, 1)

    def test_poser_mauvaise_reponse(self):
        question = Question("Quelle est la capitale de la France?", ["Paris", "Londres", "Berlin", "Madrid"], 1, 1)
        with patch('builtins.input', return_value="2"):
            self.assertFalse(question.poser(self.presentateur, self.joueur))
            self.assertEqual(self.joueur.score, 0)

if __name__ == '__main__':
    unittest.main()