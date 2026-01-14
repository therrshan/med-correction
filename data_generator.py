import pandas as pd
from tqdm import tqdm
from noise import create_curriculum_samples, add_noise
from corpus import generate_medical_sentences
import random

def generate_dataset(num_base=6000, variants_per=2, output="dataset.csv"):
    print(f"Generating {num_base} base medical sentences...")
    clean_sentences = generate_medical_sentences(num_base)
    print(f"Got {len(clean_sentences)} unique sentences")
    
    print(f"Adding noise variants...")
    dataset = []
    
    for clean in tqdm(clean_sentences, desc="Corrupting"):
        noisy_variants = create_curriculum_samples(clean, num_variants=variants_per)
        for noisy, target in noisy_variants:
            dataset.append({"input": noisy, "target": target})
    
    print(f"Generated {len(dataset)} noisy samples")
    
    print("Adding no-correction samples...")
    num_no_correction = int(len(clean_sentences) * 0.15)
    no_correction = random.sample(clean_sentences, min(num_no_correction, len(clean_sentences)))
    
    for sentence in no_correction:
        dataset.append({"input": sentence, "target": sentence})
    
    target_size = 10000
    if len(dataset) < target_size:
        print(f"Current: {len(dataset)}, adding more to hit {target_size}...")
        needed = target_size - len(dataset)
        more_sources = random.choices(clean_sentences, k=needed)
        
        for clean in more_sources:
            noisy = add_noise(clean, intensity=0.18, multiplier=2.0)
            if noisy != clean:
                dataset.append({"input": noisy, "target": clean})
    
    random.shuffle(dataset)
    
    df = pd.DataFrame(dataset)
    df.to_csv(output, index=False, encoding='utf-8')
    
    print(f"\nStats:")
    print(f"  Total: {len(df)}")
    print(f"  Unique clean: {len(clean_sentences)}")
    print(f"  Need correction: {len(df[df['input'] != df['target']])}")
    print(f"  Already correct: {len(df[df['input'] == df['target']])}")
    print(f"  Saved to: {output}")
    
    print(f"\nSamples:")
    for i in range(5):
        row = df.iloc[i]
        print(f"\n{i+1}. Input:  {row['input']}")
        print(f"   Target: {row['target']}")
    
    return df

if __name__ == "__main__":
    generate_dataset(num_base=15000, variants_per=2, output="dataset.csv")