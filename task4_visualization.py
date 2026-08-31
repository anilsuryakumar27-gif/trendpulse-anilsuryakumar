import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Setup (2 marks) ---

os.makedirs("outputs", exist_ok=True)


input_file = "data/trends_analysed.csv"
df = pd.read_csv(input_file)


# --- 2. Chart 1: Top 10 Stories by Score (6 marks)
plt.figure(figsize=(10, 6))


top_10 = df.nlargest(10, 'score')


titles = top_10['title'].apply(lambda x: x[:50] + '...' if len(str(x)) > 50 else x)
scores = top_10['score']


plt.barh(titles, scores, color='skyblue')
plt.xlabel('Score')
plt.title('Top 10 Stories by Score')
plt.gca().invert_yaxis() 
plt.tight_layout()


plt.savefig("outputs/chart1_top_stories.png")
plt.close()


# --- 3. Chart 2: Stories per Category (6 marks)
plt.figure(figsize=(8, 5))


category_counts = df['category'].value_counts()


category_counts.plot(kind='bar', color=['coral', 'mediumseagreen', 'orchid', 'gold', 'cornflowerblue', 'tomato'])
plt.xlabel('Category')
plt.ylabel('Number of Stories')
plt.title('Stories per Category')
plt.xticks(rotation=45)
plt.tight_layout()


plt.savefig("outputs/chart2_categories.png")
plt.close()


# --- 4. Chart 3: Score vs Comments Scatter Plot (6 marks) 
plt.figure(figsize=(8, 5))


popular = df[df['is_popular'] == True]
non_popular = df[df['is_popular'] == False]

plt.scatter(non_popular['score'], non_popular['num_comments'], color='gray', alpha=0.6, label='Non-Popular')
plt.scatter(popular['score'], popular['num_comments'], color='crimson', alpha=0.8, label='Popular')

plt.xlabel('Score')
plt.ylabel('Number of Comments')
plt.title('Score vs Comments')
plt.legend()
plt.tight_layout()


plt.savefig("outputs/chart3_scatter.png")
plt.close()


# --- BONUS: Dashboard (+3 marks)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('TrendPulse Dashboard', fontsize=16)

# Panel 1: Top 10 Stories
axes[0].barh(titles, scores, color='skyblue')
axes[0].set_title('Top 10 Stories')
axes[0].invert_yaxis()

# Panel 2: Categories
category_counts.plot(kind='bar', ax=axes[1], color=['coral', 'mediumseagreen', 'orchid', 'gold', 'cornflowerblue', 'tomato'])
axes[1].set_title('Stories per Category')
axes[1].tick_params(axis='x', rotation=45)

# Panel 3: Scatter Plot
axes[2].scatter(non_popular['score'], non_popular['num_comments'], color='gray', alpha=0.6, label='Non-Popular')
axes[2].scatter(popular['score'], popular['num_comments'], color='crimson', alpha=0.8, label='Popular')
axes[2].set_title('Score vs Comments')
axes[2].legend()

plt.tight_layout()


plt.savefig("outputs/dashboard.png")
plt.close()

print("All charts and dashboard successfully generated and saved in the 'outputs/' folder!")
