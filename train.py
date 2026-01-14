import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "google/byt5-small"
CSV_PATH = "dataset.csv"
MAX_LEN = 196
BATCH_SIZE = 16    
LR = 2e-5
EPOCHS = 5
OUTPUT_DIR = "./hindi_corrector_trainer"

df = pd.read_csv(CSV_PATH)
df = df[["input", "target"]].dropna()
df["input"] = df["input"].astype(str).str.strip()
df["target"] = df["target"].astype(str).str.strip()
df = df[(df["input"] != "") & (df["target"] != "")]

dataset = Dataset.from_pandas(df)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def preprocess(batch):
    inputs = tokenizer(
        batch["input"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LEN,
    )
    targets = tokenizer(
        batch["target"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LEN,
    )
    labels = targets["input_ids"]
    labels = [
        [(tok if tok != tokenizer.pad_token_id else -100) for tok in seq]
        for seq in labels
    ]
    inputs["labels"] = labels
    return inputs

dataset = dataset.map(preprocess, batched=True, remove_columns=list(df.columns))

dataset = dataset.train_test_split(test_size=0.05, seed=42)
train_ds = dataset["train"]
val_ds = dataset["test"]

collator = DataCollatorForSeq2Seq(tokenizer, model=model)

args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    eval_strategy="steps",
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    learning_rate=LR,
    num_train_epochs=EPOCHS,
    logging_steps=100,
    eval_steps=500,
    save_steps=500,
    save_total_limit=2,
    fp16=False,
    bf16=False,
    gradient_accumulation_steps=1,
    max_grad_norm=1.0,
    report_to="none",
    load_best_model_at_end=True,
    save_strategy="steps",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    data_collator=collator,
    tokenizer=tokenizer,
)

trainer.train()

trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"Training finished. Model saved at {OUTPUT_DIR}")