import sqlite3

def create_database(db_name):
    """Crée une base de données SQLite avec une table pour les questions."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            context TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Base de données {db_name} créée avec succès.")

def add_question(db_name, question, context):
    """Ajoute une question avec son contexte à la base de données."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions (question, context)
        VALUES (?, ?)
    ''', (question, context))
    conn.commit()
    conn.close()
    print("Question ajoutée avec succès.")

def main():
    db_name = 'questions.db'
    create_database(db_name)
    
    # Liste étendue de questions à ajouter
    questions = [
        {"question": "Quelle est la capitale de la France?", "context": "Cette question concerne la géographie de l'Europe."},
        {"question": "Qui a écrit 'Les Misérables'?", "context": "Cette question concerne la littérature française."},
        {"question": "Quelle est la formule chimique de l'eau?", "context": "Cette question concerne la chimie de base."},
        {"question": "Quel est le plus grand désert du monde?", "context": "Cette question concerne les géographies extrêmes."},
        {"question": "Qui est le fondateur de Microsoft?", "context": "Cette question concerne l'histoire de l'informatique."},
        {"question": "Quelle est la distance entre la Terre et la Lune?", "context": "Cette question concerne l'astronomie."},
        {"question": "Quel est le symbole chimique de l'or?", "context": "Cette question concerne la chimie des éléments."},
        {"question": "Qui a peint la Joconde?", "context": "Cette question concerne l'histoire de l'art."},
        {"question": "Quelle est la capitale de l'Italie?", "context": "Cette question concerne la géographie de l'Europe."},
        {"question": "En quelle année a eu lieu la Révolution française?", "context": "Cette question concerne l'histoire de France."},
        {"question": "Quelle est la plus grande planète du système solaire?", "context": "Cette question concerne l'astronomie."},
        {"question": "Quel est le plus haut sommet du monde?", "context": "Cette question concerne la géographie."},
        {"question": "Qui a découvert la pénicilline?", "context": "Cette question concerne l'histoire de la médecine."},
        {"question": "Quelle est la langue officielle du Brésil?", "context": "Cette question concerne les langues du monde."},
        {"question": "Quel est le plus long fleuve du monde?", "context": "Cette question concerne la géographie."}
    ]

    for q in questions:
        add_question(db_name, q["question"], q["context"])

if __name__ == "__main__":
    main()