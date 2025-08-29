
# 🎮 LUDOPEDIA – Your Gaming Encyclopedia

Ludopedia is a video game encyclopedia powered by graph databases and AI. It enables analysts and gamers to explore relationships between the most popular streamed video games in an intuitive and interactive way.

# 📌 Project Overview

Problem Statement: Discover and visualize relationships between the top streamed video games.

Solution: A Neo4j-powered application that integrates data from Twitch, IGDB, and AI-generated insights to provide rich visualizations, natural language querying, and analytical summaries.

Goals:

Show users the underlying data model they interact with.

Enable natural language queries that translate into Cypher.

Visualize relationships between games, companies, genres, and influencers.

# 🏗️ Architecture

The system is built around Neo4j with automated pipelines using Apache Airflow.

Data Sources

Twitch API
 – Top games & streams

IGDB API
 – Game details, genres, developers, etc.

AI (ChatGPT) – Company summaries

Airflow DAGs

DAG 1: Fetch top 20 video games + associated streams (Twitch).

DAG 2: Fetch related games + streams (IGDB + Twitch).

DAG 3: Add relationships (release year, game type, similar games, genres, developers).

DAG 4: Generate AI summaries for companies.

DAG 5: Calculate average view counts per game.

All DAGs merge data directly into Neo4j as nodes and relationships.

# 📊 Features

Graph Visualization: Explore the Neo4j model of games, genres, and companies.

Natural Language → Cypher: Query the graph with plain English.

Interactive Queries: Editable Cypher queries for power users.

Rich Output: Each query returns a graph, a table, and an AI summary.

# 🚧 Challenges

Missing company URLs in IGDB → fallback to GPT summaries.

Ensuring AI-generated Cypher queries were valid → tuned with Neo4j schema context.

Data quality → handled nulls and missing fields.


# Language
    Python3

# Install Dependencies
    pip install -r requirements.txt

# Set ENV
    Set the Twitch and RAWG API credentials in the .env file

# Configuration
    Current config is to load 5000 games from IGDB and 10 Pages from RAWG.IO  (10 * 40 = 400 game data). Tweak it as per requirement
# Run the application
    python3 src/main.py

# Output
    Find the dataset in data/ folder; latest_game_data.csv and rawg_game_data.csv
