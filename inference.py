import sqlite3
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_DIR = "./hindi_corrector_trainer"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_LEN = 196
DB_FILE = "feedback.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS common_mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wrong TEXT UNIQUE,
            correct TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_common_mistakes():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT wrong, correct FROM common_mistakes")
    rows = cursor.fetchall()
    conn.close()
    return {wrong: correct for wrong, correct in rows}

def update_common_mistakes(wrong, correct):
    if wrong.strip() == correct.strip():
        return
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO common_mistakes (wrong, correct)
        VALUES (?, ?)
        ON CONFLICT(wrong) DO UPDATE SET correct=excluded.correct
    """, (wrong.strip(), correct.strip()))
    conn.commit()
    conn.close()

def preclean_input(text, common_mistakes):
    words = text.split()
    cleaned = [common_mistakes.get(w, w) for w in words]
    return " ".join(cleaned)

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR).to(DEVICE)
model.eval()

def predict(texts, common_mistakes):
    cleaned = [preclean_input(t, common_mistakes) for t in texts]
    enc = tokenizer(
        cleaned,
        truncation=True,
        padding=True,
        max_length=MAX_LEN,
        return_tensors="pt"
    ).to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            **enc,
            max_length=MAX_LEN,
            num_beams=4,
            early_stopping=True
        )

    predictions = [tokenizer.decode(o, skip_special_tokens=True) for o in outputs]
    return predictions

init_db()
common_mistakes_dict = load_common_mistakes()

if __name__ == "__main__":
    while True:
        user_input = input("\nEnter Hindi sentence (or 'quit' to exit): ").strip()
        if user_input.lower() == "quit":
            break

        pred = predict([user_input], common_mistakes_dict)[0]
        print(f"Model prediction: {pred}")

        while True:
            wrong_word = input("Which word is incorrect? (or press enter if all correct): ").strip()
            if not wrong_word:
                break
            correct_word = input(f"Correct form of '{wrong_word}': ").strip()
            if correct_word:
                update_common_mistakes(wrong_word, correct_word)
                print(f"Learned '{wrong_word}' -> '{correct_word}'")
                common_mistakes_dict = load_common_mistakes()
            else:
                print("Skipped. No correction provided.")