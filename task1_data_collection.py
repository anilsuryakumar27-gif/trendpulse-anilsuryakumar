import requests
import time
import json
import os
from datetime import datetime

# Required header to identify our script
headers = {"User-Agent": "TrendPulse/1.0"}

# Dictionary of categories and their lowercase keywords
categories = {
    "technology": ["software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}
# Fetch the top story IDs
print("Fetching top stories...")
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(url, headers=headers)
top_story_ids = response.json()

# Create an empty list to save the stories we actually want to keep
collected_stories = []

print("Fetching and categorizing stories. This might take a minute...")

# We loop through ALL IDs now, not just the first 15
for story_id in top_story_ids:
    
    # Check if we have reached our goal of 100 stories. If yes, stop the loop!
    if len(collected_stories) >= 100:
        break
        
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    
    try:
        response = requests.get(story_url, headers=headers)
        story_data = response.json()
        
        # Make sure the story has a title before we try to read it
        if story_data and "title" in story_data:
            # Convert title to lowercase so it's easier to match our keywords
            title_lower = story_data["title"].lower()
            assigned_category = None
            
            # Loop through our dictionary of categories to find a match
            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword in title_lower:
                        assigned_category = category
                        break # Stop checking keywords once we find a match
                
                if assigned_category:
                    break # Stop checking categories once we found one
            
            # If the story matched a category, save the 7 required fields!
            if assigned_category:
                story_dict = {
                    "post_id": story_data.get("id"),
                    "title": story_data.get("title"),
                    "category": assigned_category,
                    "score": story_data.get("score", 0),
                    "num_comments": story_data.get("descendants", 0), 
                    "author": story_data.get("by", "Unknown"),
                    "url": story_data.get("url", "")
                }
                # Add this dictionary to our master list
                collected_stories.append(story_dict)
                print(f"Collected {len(collected_stories)}/100: [{assigned_category}] {story_dict['title']}")
                
                # Wait 2 seconds as instructed by your project guidelines
                time.sleep(2) 
                
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")

print(f"\nFinished! We collected exactly {len(collected_stories)} stories.")


# Format today's date as YYYYMMDD
today_str = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{today_str}.json"

# Create the 'data' folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save our list of dictionaries into the JSON file
with open(filename, "w") as file:
    json.dump(collected_stories, file, indent=4)

print(f"Data successfully saved to {filename}")


