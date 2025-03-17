import subprocess
import sys

def main():
    # Vérification et installation des modules requis
    try:
        subprocess.check_call([sys.executable, "check_and_install_modules.py"])
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation des modules requis: {e}")
        sys.exit(1)

    # Exécution des tests unitaires
    try:
        subprocess.check_call([sys.executable, "-m", "unittest", "discover"])
        print("Tests unitaires exécutés avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution des tests unitaires: {e}")
        sys.exit(1)

    # Lancement du jeu
    try:
        subprocess.check_call([sys.executable, "jeu.py"])
        print("Jeu lancé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du lancement du jeu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()