import requests
import time
import json
import os
from datetime import datetime

headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": ["software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}
print("Fetching top stories...")
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(url, headers=headers)
top_story_ids = response.json()

collected_stories = []

print("Fetching and categorizing stories. This might take a minute...")

for story_id in top_story_ids:
    !
    if len(collected_stories) >= 100:
        break
        
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    
    try:
        response = requests.get(story_url, headers=headers)
        story_data = response.json()
        
        
        if story_data and "title" in story_data:
            
            title_lower = story_data["title"].lower()
            assigned_category = None
            
            
            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword in title_lower:
                        assigned_category = category
                        break 
                
                if assigned_category:
                    break 
            
            
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
                
                collected_stories.append(story_dict)
                print(f"Collected {len(collected_stories)}/100: [{assigned_category}] {story_dict['title']}")
                
                
                time.sleep(2) 
                
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")

print(f"\nFinished! We collected exactly {len(collected_stories)} stories.")



today_str = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{today_str}.json"


os.makedirs("data", exist_ok=True)

# Save our list of dictionaries into the JSON file
with open(filename, "w") as file:
    json.dump(collected_stories, file, indent=4)

print(f"Data successfully saved to {filename}")


