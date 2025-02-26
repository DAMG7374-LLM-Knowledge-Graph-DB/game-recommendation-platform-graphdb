from fetch_igdb import fetch_igdb_games
from fetch_rawg import fetch_rawg_games

if __name__ == "__main__":
    print("🚀 Starting IGDB Fetch...")
    fetch_igdb_games()

    print("🚀 Starting RAWG Fetch...")
    fetch_rawg_games()

    print("✅ Data Collection Complete!")
