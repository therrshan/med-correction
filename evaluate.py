import pandas as pd
import sqlite3
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm
import time
import editdistance
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

MODEL_DIR = "./models/colab-v2"
CSV_PATH = "eval.csv"
MAX_LEN = 196
BATCH_SIZE = 8
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DB_FILE = "common_mistakes.db"

def load_common_mistakes():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT wrong, correct FROM mistakes")
    rows = cursor.fetchall()
    conn.close()
    return {wrong: correct for wrong, correct in rows}

def preclean_input(text, common_mistakes):
    words = text.split()
    cleaned = [common_mistakes.get(w, w) for w in words]
    return " ".join(cleaned)

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR).to(DEVICE)
model.eval()

df = pd.read_csv(CSV_PATH)
df = df[["Hindi_raw", "expected_outputs"]].dropna()
df["Hindi_raw"] = df["Hindi_raw"].astype(str).str.strip()
df["expected_outputs"] = df["expected_outputs"].astype(str).str.strip()

common_mistakes = load_common_mistakes()

def generate_batch(inputs, max_len=MAX_LEN):
    enc = tokenizer(
        inputs,
        truncation=True,
        padding=True,
        max_length=max_len,
        return_tensors="pt"
    ).to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            **enc,
            max_length=max_len,
            num_beams=4,
            early_stopping=True
        )
    decoded = [tokenizer.decode(out, skip_special_tokens=True) for out in outputs]
    return decoded

all_predictions = []
start_time = time.time()
for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Evaluating"):
    batch = df["Hindi_raw"].iloc[i:i+BATCH_SIZE].tolist()
    preds = generate_batch(batch)
    all_predictions.extend(preds)

latency = (time.time() - start_time) / len(df)
df["predictions"] = all_predictions
print(f"\nAverage latency: {latency*1000:.2f} ms/sentence")

df['predictions'] = df['predictions'].apply(lambda x: preclean_input(x, common_mistakes))

df["exact_match"] = df["predictions"] == df["expected_outputs"]
exact_match = df["exact_match"].mean()
print(f"Exact match: {exact_match*100:.2f}%")

def cer(ref, hyp):
    return editdistance.eval(ref, hyp) / max(1, len(ref))

df["cer"] = df.apply(lambda row: cer(row["expected_outputs"], row["predictions"]), axis=1)
avg_cer = df["cer"].mean()
print(f"Average CER: {avg_cer*100:.2f}%")

def get_bleu(ref, hyp):
    return sentence_bleu([list(ref)], list(hyp), smoothing_function=SmoothingFunction().method1)

df["bleu"] = df.apply(lambda row: get_bleu(row["expected_outputs"], row["predictions"]), axis=1)
avg_bleu = df["bleu"].mean()
print(f"Average BLEU: {avg_bleu*100:.2f}%")

df.to_csv("eval_results.csv", index=False)
print("\nResults saved to eval_results.csv")

print("\nSample predictions:")
for i in range(min(5, len(df))):
    print(f"\nInput:     {df['Hindi_raw'].iloc[i]}")
    print(f"Expected:  {df['expected_outputs'].iloc[i]}")
    print(f"Predicted: {df['predictions'].iloc[i]}")
    print(f"CER: {df['cer'].iloc[i]:.4f}")