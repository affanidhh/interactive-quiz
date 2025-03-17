import unittest
from presentateur import Presentateur

class TestPresentateur(unittest.TestCase):

    def test_initialisation(self):
        presentateur = Presentateur("Jean-Luc Reichmann")
        self.assertEqual(presentateur.nom, "Jean-Luc Reichmann")

    def test_initialisation_erreur(self):
        with self.assertRaises(ValueError):
            Presentateur("")

    def test_annoncer_phase(self):
        presentateur = Presentateur("Jean-Luc Reichmann")
        with self.assertRaises(ValueError):
            presentateur.annoncer_phase("")

    def test_annoncer_tour(self):
        presentateur = Presentateur("Jean-Luc Reichmann")
        with self.assertRaises(ValueError):
            presentateur.annoncer_tour("")