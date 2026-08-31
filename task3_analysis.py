import pandas as pd
import numpy as np

# --- 1. Load and Explore (4 marks) ---
input_file = "data/trends_clean.csv"
df = pd.read_csv(input_file) # Load data/trends_clean.csv into a Pandas DataFrame

# Print the shape of the DataFrame (rows and columns)
print(f"Loaded data: {df.shape}")

# Print the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Print the average score and average num_comments across all stories
avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()
print(f"\nAverage score    : {avg_score:,.0f}")
print(f"Average comments : {avg_comments:,.0f}")


# --- 2. Basic Analysis with NumPy (8 marks) ---
print("\n--- NumPy Stats ---")
# Convert the score column to a NumPy array for calculations
scores_array = df['score'].to_numpy()

# What is the mean, median, and standard deviation of score?
mean_score = np.mean(scores_array)
median_score = np.median(scores_array)
std_score = np.std(scores_array)

# What is the highest score and lowest score?
max_score = np.max(scores_array)
min_score = np.min(scores_array)

print(f"Mean score     : {mean_score:,.0f}")
print(f"Median score   : {median_score:,.0f}")
print(f"Std deviation  : {std_score:,.0f}")
print(f"Max score      : {max_score:,.0f}")
print(f"Min score      : {min_score:,.0f}")

# Which category has the most stories?
top_category = df['category'].value_counts().idxmax()
top_category_count = df['category'].value_counts().max()
print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

# Which story has the most comments? Print its title and comment count.
most_comments_idx = df['num_comments'].idxmax()
top_story_title = df.loc[most_comments_idx, 'title']
top_story_comments = df.loc[most_comments_idx, 'num_comments']
print(f"\nMost commented story: \"{top_story_title}\" - {top_story_comments:,.0f} comments")


# --- 3. Add New Columns (5 marks) ---
# Formula: num_comments / (score + 1)
df['engagement'] = df['num_comments'] / (df['score'] + 1)

# Formula: True if score > average score, else False
df['is_popular'] = df['score'] > avg_score


# --- 4. Save the Result (3 marks) ---
output_file = "data/trends_analysed.csv"

# Save the updated DataFrame to data/trends_analysed.csv
df.to_csv(output_file, index=False)

# Print a confirmation message
print(f"\nSaved to {output_file}")
