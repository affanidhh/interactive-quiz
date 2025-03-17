import sqlite3
import pyttsx3
import random

def speak(text):
    """Utilise pyttsx3 pour lire un texte à haute voix."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_random_question(db_name, asked_questions):
    """Récupère une question aléatoire qui n'a pas encore été posée."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT id, question, context FROM questions')
    all_questions = cursor.fetchall()
    conn.close()

    remaining_questions = [q for q in all_questions if q[0] not in asked_questions]
    if not remaining_questions:
        return None
    return random.choice(remaining_questions)

def ask_question(question, context):
    """Pose une question et vérifie la réponse."""
    speak(context)
    speak(question)
    answer = input("Votre réponse: ")
    return answer

def main():
    db_name = 'questions.db'
    asked_questions = set()

    while True:
        question_data = get_random_question(db_name, asked_questions)
        if not question_data:
            print("Toutes les questions ont été posées.")
            break

        q_id, question, context = question_data
        answer = ask_question(question, context)
        asked_questions.add(q_id)
        speak("Merci pour votre réponse.")
        print("Merci pour votre réponse.")

if __name__ == "__main__":
    main()