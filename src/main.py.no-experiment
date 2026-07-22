"""
Phase 4: Recommender System Evaluation & Stress Testing
Entry point for evaluating adversarial user profiles against the scoring logic.
"""

import csv
import os


def load_songs_dataset(csv_path: str) -> list:
    """Loads songs from songs.csv into a list of dictionaries with proper type casting."""
    songs = []
    if not os.path.exists(csv_path):
        print(f"Warning: '{csv_path}' not found. Creating a mockup dataset for demonstration...")
        return get_mock_dataset()

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                songs.append({
                    "title": row.get("title", "Unknown Title"),
                    "artist": row.get("artist", "Unknown Artist"),
                    "genre": row.get("genre", "").strip().lower(),
                    "mood": row.get("mood", "").strip().lower(),
                    "energy": float(row.get("energy", 0.0))
                })
            except (ValueError, TypeError):
                continue
    return songs


def score_song(song: dict, profile: dict) -> float:
    """
    Implements the pipeline math explicitly:
    - Genre Match: +2.0 points
    - Mood Match: +1.0 point
    - Energy Distance Similarity: 1.0 - abs(target_energy - song_energy)
    """
    # 1. Genre Check
    genre_score = 2.0 if song["genre"] == profile["genre"].lower() else 0.0
    
    # 2. Mood Check
    mood_score = 1.0 if song["mood"] == profile["mood"].lower() else 0.0
    
    # 3. Energy Calculation
    energy_distance = abs(profile["target_energy"] - song["energy"])
    energy_similarity = 1.0 - energy_distance
    
    # Total Score Summation
    total_score = genre_score + mood_score + energy_similarity
    return total_score


def get_top_recommendations(songs: list, profile: dict, k: int = 5) -> list:
    """Scores all songs, sorts them descending, and returns the top K recommendations."""
    scored_songs = []
    for song in songs:
        score = score_score = score_song(song, profile)
        # Store metadata and computed components for easy terminal logging
        scored_songs.append({
            "title": song["title"],
            "artist": song["artist"],
            "genre": song["genre"],
            "mood": song["mood"],
            "energy": song["energy"],
            "total_score": round(score, 3)
        })
    
    # Sort descending by total score
    scored_songs.sort(key=lambda x: x["total_score"], reverse=True)
    return scored_songs[:k]


def get_mock_dataset() -> list:
    """Fallback sample dataset representing a realistic songs.csv for testing."""
    return [
        {"title": "Melancholy Symphony", "artist": "Luna", "genre": "pop", "mood": "sad", "energy": 0.21},
        {"title": "Neon Heartbreak", "artist": "The Midnight", "genre": "pop", "mood": "sad", "energy": 0.88},
        {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "pop", "mood": "happy", "energy": 0.92},
        {"title": "Chill Coffee", "artist": "Lofi Beats", "genre": "lofi", "mood": "focused", "energy": 0.12},
        {"title": "Heavy Metal Thunder", "artist": "Iron Core", "genre": "rock", "mood": "energetic", "energy": 0.95},
        {"title": "Soft Velvet Strings", "artist": "Classic Ensemble", "genre": "classical", "mood": "focused", "energy": 0.15},
        {"title": "Alternative Horizon", "artist": "Grit", "genre": "rock", "mood": "energetic", "energy": 0.52},
    ]


if __name__ == "__main__":
    # Path setup (looks for songs.csv in data/ or root folder)
    csv_filename = "songs.csv"
    songs_data = load_songs_dataset(csv_filename)
    
    # Define the 3 Adversarial Test Profiles
    adversarial_profiles = {
        "Profile 1: Paradoxical Request ('Anxious High-Energy Joy')": {
            "genre": "pop",
            "mood": "sad",
            "target_energy": 0.95
        },
        "Profile 2: Genre-Defying Pure Vibe ('The Fluid Acoustic')": {
            "genre": "classical", 
            "mood": "focused",
            "target_energy": 0.10
        },
        "Profile 3: Un-biasable Middle-Grounder ('The Perfect Gray Area')": {
            "genre": "rock",
            "mood": "energetic",
            "target_energy": 0.50
        }
    }
    
    print("==========================================================")
    print("      RECOMMENDER SYSTEM SYSTEM EVALUATION REPORT         ")
    print("==========================================================\n")
    print(f"Loaded {len(songs_data)} tracks to evaluate.")
    
    # Execute the evaluation loop
    for profile_name, preferences in adversarial_profiles.items():
        print(f"\n🚀 STRESS TESTING: {profile_name}")
        print(f"   Criteria -> Genre: {preferences['genre']}, Mood: {preferences['mood']}, Target Energy: {preferences['target_energy']}")
        print("-" * 75)
        
        top_5 = get_top_recommendations(songs_data, preferences, k=5)
        
        # Formatted output ready for your terminal review and markdown fence copying
        for rank, song in enumerate(top_5, 1):
            print(f" [{rank}] Score: {song['total_score']} | '{song['title']}' by {song['artist']}")
            print(f"     (Actuals -> Genre: {song['genre']}, Mood: {song['mood']}, Energy: {song['energy']})")
        print("-" * 75)
