import os
import subprocess
import sys
import requests

# Configuration
REQUIRED_MODULES = ['psutil', 'pyttsx3', 'sqlite3']
GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "affanidhh"
REPO_NAME = "Les-Douze-Coups-de-Midi"
LOCAL_BRANCH = "main"

def install_missing_modules():
    for module in REQUIRED_MODULES:
        try:
            __import__(module)
            print(f"Module {module} est déjà installé.")
        except ImportError:
            print(f"Module {module} non trouvé. Installation...")
            subprocess.run([sys.executable, "-m", "pip", "install", module], check=True)

def get_latest_commit_sha(owner, repo, branch):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits/{branch}"
    response = requests.get(url)
    response.raise_for_status()
    commit_data = response.json()
    return commit_data["sha"]

def get_local_commit_sha(branch):
    result = subprocess.run(["git", "rev-parse", branch], stdout=subprocess.PIPE, check=True)
    return result.stdout.strip().decode()

def check_for_updates():
    try:
        remote_sha = get_latest_commit_sha(REPO_OWNER, REPO_NAME, LOCAL_BRANCH)
        local_sha = get_local_commit_sha(LOCAL_BRANCH)
        
        if remote_sha == local_sha:
            print("Le code est à jour.")
        else:
            print("Le code n'est pas à jour.")
            print(f"SHA distant : {remote_sha}")
            print(f"SHA local : {local_sha}")
            print("Veuillez mettre à jour votre dépôt local en synchronisant avec le dépôt distant.")
    except Exception as e:
        print(f"Erreur lors de la vérification des mises à jour : {e}")

def check_syntax_errors():
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    for py_file in py_files:
        print(f"Vérification de la syntaxe dans {py_file}...")
        result = subprocess.run([sys.executable, "-m", "py_compile", py_file], stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Erreurs de syntaxe trouvées dans {py_file} :\n{result.stderr.decode()}")
        else:
            print(f"Pas d'erreurs de syntaxe dans {py_file}.")

def run_unit_tests():
    print("Exécution des tests unitaires...")
    result = subprocess.run([sys.executable, "-m", "unittest", "discover"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
    if result.returncode != 0:
        print(f"Erreurs dans les tests unitaires :\n{result.stderr.decode()}")
    else:
        print("Tous les tests unitaires passent avec succès.")

def main():
    install_missing_modules()
    check_for_updates()
    check_syntax_errors()
    run_unit_tests()

if __name__ == "__main__":
    main()