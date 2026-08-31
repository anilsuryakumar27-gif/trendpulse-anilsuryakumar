import pandas as pd

# --- 1. Load the Data ---

input_file = "data/trends_20260831.json" 

print(f"Loading data from {input_file}...")
df = pd.read_json(input_file)


print(f"Loaded {len(df)} stories from {input_file}")


# --- 2. Clean the Data ---
# a. Duplicates: 
df = df.drop_duplicates(subset=['post_id'])
print(f"After removing duplicates: {len(df)}")

# b. Missing values: 
df = df.dropna(subset=['post_id', 'title', 'score'])
print(f"After removing nulls: {len(df)}")

# c. Whitespace: 
df['title'] = df['title'].str.strip()

# d. Data types: 
df['score'] = df['score'].astype(int)
df['num_comments'] = df['num_comments'].fillna(0).astype(int)

# e. Low quality: 
df = df[df['score'] >= 5]
print(f"After removing low scores: {len(df)}")


# --- 3. Save as CSV 
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)
print(f"\nSaved {len(df)} rows to {output_file}")

# Print category summary
print("\nStories per category:")
category_counts = df['category'].value_counts()
for category, count in category_counts.items():
    print(f"{category}  {count}")
