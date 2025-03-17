import requests
import subprocess

# Configuration
GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "affanidhh"
REPO_NAME = "Les-Douze-Coups-de-Midi"
LOCAL_BRANCH = "main"

def get_latest_commit_sha(owner, repo, branch):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits/{branch}"
    response = requests.get(url)
    response.raise_for_status()
    commit_data = response.json()
    return commit_data["sha"]

def get_local_commit_sha(branch):
    result = subprocess.run(["git", "rev-parse", branch], stdout=subprocess.PIPE, check=True)
    return result.stdout.strip().decode()

def main():
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

if __name__ == "__main__":
    main()