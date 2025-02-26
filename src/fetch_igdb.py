import os
import csv
import json
import time
import requests
from dotenv import load_dotenv
from igdb.wrapper import IGDBWrapper

# 🔹 Load environment variables from .env file
load_dotenv()

# 🔹 Get credentials from .env
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

# 🔹 File to store OAuth token
OAUTH_FILE = "oauth_token.json"
AUTH_URL = "https://id.twitch.tv/oauth2/token"

# 🔹 Function to Get OAuth Token (Checks Cache First)
def get_twitch_oauth_token():
    # Check if a saved token exists
    if os.path.exists(OAUTH_FILE):
        with open(OAUTH_FILE, "r") as f:
            data = json.load(f)
            if time.time() < data["expires_at"]:
                print(f"🔄 Using Cached OAuth Token: {data['access_token']}")
                return data["access_token"]  # Reuse existing token

    # If no valid token, request a new one
    print("🔑 Requesting New OAuth Token...")
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(AUTH_URL, params=params)

    if response.status_code == 200:
        auth_data = response.json()
        auth_data["expires_at"] = time.time() + auth_data["expires_in"] - 60  # Buffer before expiry

        # Save token to file
        with open(OAUTH_FILE, "w") as f:
            json.dump(auth_data, f)

        print(f"✅ New OAuth Token Retrieved: {auth_data['access_token']}")
        return auth_data["access_token"]
    else:
        raise Exception(f"❌ Failed to obtain access token: {response.text}")

# 🔹 Get a fresh or cached OAuth token
ACCESS_TOKEN = get_twitch_oauth_token()

# 🔹 Initialize IGDB API Wrapper
wrapper = IGDBWrapper(CLIENT_ID, ACCESS_TOKEN)

# 🔹 Define API Query
QUERY_TEMPLATE = """
fields id, name, genres.name, platforms.name, first_release_date, rating, summary,
       cover.url, involved_companies.company.name, game_modes.name, franchise.name,
       player_perspectives.name, themes.name, storyline, total_rating;
where first_release_date != null;
sort first_release_date desc;
limit 500;
offset {offset};
"""


# 🔹 CSV Output File
CSV_FILE = "data/latest_game_data.csv"
CSV_HEADERS = [
    "id", "name", "genres", "platforms", "first_release_date", "rating", "summary",
    "cover_url", "developers", "game_modes", "franchise", "player_perspectives",
    "themes", "storyline", "total_rating"
]


# 🔹 Function to Fetch Data
def fetch_igdb_games():
    offset = 0
    max_games = 5000  # Change this if you need more
    batch_size = 500  # IGDB allows up to 500 per request
    all_games = []

    while offset < max_games:
        print(f"🔄 Fetching games {offset} - {offset + batch_size}...")

        try:
            response = wrapper.api_request("games", QUERY_TEMPLATE.format(offset=offset))
            games = response.decode("utf-8")  # Convert bytes to string
            games = json.loads(games)  # Convert string to JSON
            all_games.extend(games)

            # Save Partial Data
            save_to_csv(all_games)

            # Respect Rate Limit (Wait 1.5 sec)
            time.sleep(1.5)

        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            time.sleep(5)  # Wait before retrying

        offset += batch_size

    print(f"✅ Total Games Fetched: {len(all_games)}")
    return all_games

# 🔹 Function to Save Data to CSV
def save_to_csv(game_data):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writeheader()

        for game in game_data:
            writer.writerow({
                "id": game.get("id"),
                "name": game.get("name"),
                "genres": ", ".join(g["name"] for g in game.get("genres", [])),
                "platforms": ", ".join(p["name"] for p in game.get("platforms", [])),
                "first_release_date": game.get("first_release_date"),
                "rating": game.get("rating"),
                "summary": game.get("summary"),
                "cover_url": game.get("cover", {}).get("url"),
                "developers": ", ".join(c["company"]["name"] for c in game.get("involved_companies", [])),
                "game_modes": ", ".join(m["name"] for m in game.get("game_modes", [])),
                "franchise": game.get("franchise", {}).get("name"),
                "player_perspectives": ", ".join(p["name"] for p in game.get("player_perspectives", [])),
                "themes": ", ".join(t["name"] for t in game.get("themes", [])),
                "storyline": game.get("storyline"),
                "total_rating": game.get("total_rating")
            })


    print(f"📄 Data saved to {CSV_FILE}")

if __name__ == "__main__":
# 🔹 Run Data Fetching
    fetch_igdb_games()
