import unittest
from joueur import Joueur

class TestJoueur(unittest.TestCase):

    def test_initialisation(self):
        joueur = Joueur("Maître de Midi")
        self.assertEqual(joueur.nom, "Maître de Midi")
        self.assertEqual(joueur.score, 0)

    def test_initialisation_erreur(self):
        with self.assertRaises(ValueError):
            Joueur("")

    def test_str(self):
        joueur = Joueur("Maître de Midi")
        self.assertEqual(str(joueur), "Maître de Midi : 0 points")

if __name__ == '__main__':
    unittest.main()