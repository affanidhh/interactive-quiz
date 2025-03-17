import subprocess
import sys

def install_requirements():
    """Installe les modules requis à partir du fichier requirements.txt."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Installation des modules requis terminée.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation des modules requis : {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()