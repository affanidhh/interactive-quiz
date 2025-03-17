import subprocess
import sys
import pkg_resources

def install_module(module_name):
    """Installe un module Python en utilisant pip."""
    try:
        print(f"Installation du module {module_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"Module {module_name} installé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation du module {module_name}: {e}")
        sys.exit(1)

def check_and_install_modules(modules):
    """Vérifie et installe les modules requis."""
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    for module in modules:
        if module.lower() not in installed_packages:
            print(f"Module {module} n'est pas installé. Installation en cours...")
            install_module(module)
        else:
            print(f"Module {module} est déjà installé.")

if __name__ == "__main__":
    # Liste des modules requis
    required_modules = [
        "psutil",
        "pyttsx3",
        # Ajoutez d'autres modules requis ici
    ]

    print("Vérification et installation des modules requis...")
    check_and_install_modules(required_modules)
    print("Tous les modules requis sont installés.")