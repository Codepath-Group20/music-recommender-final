"""
Phase 4: Recommender System Evaluation & Step 3 Data Experiment
Invokes the new experimental scoring method to test weight sensitivity.
"""

import sys
import os

# Ensure the pipeline can safely locate modules inside src/
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from recommender import load_songs, score_song_experimental_weights


def get_top_recommendations(songs: list, profile: dict, k: int = 5) -> list:
    """Scores all songs using the new experimental tracking formula and sorts them."""
    scored_songs = []
    for song in songs:
        score, _ = score_song_experimental_weights(profile, song)
        scored_songs.append({
            "title": song["title"],
            "artist": song["artist"],
            "genre": song["genre"],
            "mood": song["mood"],
            "energy": song["energy"],
            "total_score": round(score, 3)
        })
    
    scored_songs.sort(key=lambda x: x["total_score"], reverse=True)
    return scored_songs[:k]


if __name__ == "__main__":
    # Robust path discovery matching your ls -R layout
    csv_filename = "songs.csv"
    if not os.path.exists(csv_filename) and os.path.exists("data/songs.csv"):
        csv_filename = "data/songs.csv"
        
    songs_data = load_songs(csv_filename)
    
    # Define the 3 Adversarial Test Profiles
    adversarial_profiles = {
        "Profile 1: Paradoxical Request ('Anxious High-Energy Joy')": {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.95
        },
        "Profile 2: Genre-Defying Pure Vibe ('The Fluid Acoustic')": {
            "genre": "classical", 
            "mood": "focused",
            "energy": 0.10
        },
        "Profile 3: Un-biasable Middle-Grounder ('The Perfect Gray Area')": {
            "genre": "rock",
            "mood": "energetic",
            "energy": 0.50
        }
    }
    
    print("==========================================================")
    print("   RECOMMENDER SYSTEM SYSTEM EXPERIMENTAL REPORT (STEP 3)  ")
    print("==========================================================")
    print(f"Loaded {len(songs_data)} tracks from: '{csv_filename}'")
    print("Using scoring function: 'score_song_experimental_weights'\n")
    
    for profile_name, preferences in adversarial_profiles.items():
        print(f"\n🚀 EXPERIMENTAL STRESS TESTING: {profile_name}")
        print(f"   Criteria -> Genre: {preferences['genre']}, Mood: {preferences['mood']}, Target Energy: {preferences['energy']}")
        print("-" * 75)
        
        top_5 = get_top_recommendations(songs_data, preferences, k=5)
        
        for rank, song in enumerate(top_5, 1):
            print(f" [{rank}] Score: {song['total_score']} | '{song['title']}' by {song['artist']}")
            print(f"     (Actuals -> Genre: {song['genre']}, Mood: {song['mood']}, Energy: {song['energy']})")
        print("-" * 75)
