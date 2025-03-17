from jeu import Jeu  # Assurez-vous que le nom du fichier où la classe Jeu est définie est 'jeu.py'

if __name__ == "__main__":
    try:
        jeu = Jeu()
        
        if input("Mode entraînement ? (o/n) : ").lower() == 'o':
            print("Le mode entraînement est activé. Les scores ne seront pas sauvegardés.")
            jeu.jouer()
        else:
            jeu.jouer()
    except KeyboardInterrupt:
        print("\n\nLe jeu a été interrompu. À bientôt !")
        sys.exit(0)