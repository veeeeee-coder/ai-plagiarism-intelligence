# data_prep.py
import csv
import os
import hashlib
from collections import Counter
import pandas as pd

rows = []

# Loop through each folder
for category in ['original', 'paraphrased', 'ai_generated']:
    folder_path = f'data/{category}'
    
    # Get all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Create a unique ID for this text
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Add to our list
        rows.append({
            'text': text,
            'label': category,
            'hash': text_hash
        })

# Create a spreadsheet-like file
df = pd.DataFrame(rows)
df.to_csv('data/dataset.csv', index=False)

print(f"✅ Created dataset with {len(rows)} documents")
print(df['label'].value_counts())