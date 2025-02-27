import os
import csv
import json
import time
import requests
import wikipediaapi
from dotenv import load_dotenv

# 🔹 Load API Key
load_dotenv()
RAWG_API_KEY = os.getenv("RAWG_API_KEY")
RAWG_URL = "https://api.rawg.io/api/games"
CSV_FILE = "data/rawg_game_data.csv"

# 🔹 Initialize Wikipedia API
wiki = wikipediaapi.Wikipedia(user_agent="GameRecommender/1.0 (raaz.adarsh@gmail.com)", language="en")

def get_wikipedia_summary(game_name):
    """Fetch the first paragraph of a Wikipedia page for the given game name and ensure it's wrapped in quotes."""
    page = wiki.page(game_name)
    summary = page.summary.split(".")[0] + "." if page.exists() else "No summary available"

    # 🔹 Ensure summary is always wrapped in double quotes
    return f'{summary}'

# 🔹 Fetch Data from RAWG
def fetch_rawg_games():
    page = 1
    max_pages = 10
    all_games = []

    while page <= max_pages:
        print(f"Fetching RAWG games, page {page}...")
        params = {"key": RAWG_API_KEY, "page": page, "page_size": 40}
        response = requests.get(RAWG_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            all_games.extend(parse_game_data(data["results"]))
            time.sleep(1.5)
        else:
            print(f"❌ RAWG Fetch Error: {response.status_code} - {response.text}")
            time.sleep(5)

        page += 1

    save_to_csv(all_games, CSV_FILE)
    print(f"✅ RAWG Data Saved: {CSV_FILE}")

# 🔹 Parse API Data Based on Graph Model
def parse_game_data(games):
    parsed = []
    for game in games:
        description = game.get("description")
        wiki_summary = get_wikipedia_summary(game["name"]) if not description else description  # Use Wikipedia if missing

        parsed.append({
            "id": game.get("id"),
            "name": game.get("name"),
            "released": game.get("released"),
            "genres": ", ".join(g["name"] for g in game.get("genres", [])),
            "platforms": ", ".join(p["platform"]["name"] for p in game.get("platforms", [])),
            "developers": ", ".join(d["name"] for d in game.get("developers", [])) if game.get("developers") else "",
            "publishers": ", ".join(p["name"] for p in game.get("publishers", [])) if game.get("publishers") else "",
            "background_image": game.get("background_image"),
            "rating": game.get("rating"),
            "description": wiki_summary  # 🔹 Updated to include Wikipedia summary if RAWG description is missing
        })
    return parsed

# 🔹 Save to CSV
def save_to_csv(data, filename):
    keys = ["id", "name", "released", "genres", "platforms", "developers", "publishers", "background_image", "rating", "description"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    fetch_rawg_games()
