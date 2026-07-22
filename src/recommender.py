from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = []
        for song in self.songs:
            score, _ = score_song(
                {
                    "genre": user.favorite_genre,
                    "mood": user.favorite_mood,
                    "energy": user.target_energy,
                },
                {
                    "genre": song.genre,
                    "mood": song.mood,
                    "energy": song.energy,
                },
            )
            scored_songs.append((score, song))

        scored_songs.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored_songs[:k]]

def load_songs(filepath: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.
    Required by recommend_songs() and src/main.py
    """
    songs = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                songs.append({
                    "id": int(row["id"]) if "id" in row else 0,
                    "title": row.get("title", "Unknown"),
                    "artist": row.get("artist", "Unknown"),
                    "genre": row.get("genre", "").strip().lower(),
                    "mood": row.get("mood", "").strip().lower(),
                    "energy": float(row.get("energy", 0.0)),
                })
            except (ValueError, KeyError):
                continue
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    ORIGINAL SCORING CONFIGURATION (Phase 3 Rule Logic)
    Kept active to prevent breaking existing unit tests.
    """
    score = 0.0
    reasons: List[str] = []

    genre_pref = str(user_prefs.get("genre", "")).lower()
    mood_pref = str(user_prefs.get("mood", "")).lower()
    target_energy = float(user_prefs.get("energy") if user_prefs.get("energy") is not None else user_prefs.get("target_energy", 0.0))

    song_genre = str(song.get("genre", "")).lower()
    song_mood = str(song.get("mood", "")).lower()
    song_energy = float(song.get("energy", 0.0))

    if song_genre == genre_pref:
        score += 2.0
        reasons.append(f"genre match ({song_genre}) (+2.0)")

    if song_mood == mood_pref:
        score += 1.0
        reasons.append(f"mood match ({song_mood}) (+1.0)")

    energy_similarity = 1.0 - abs(song_energy - target_energy)
    score += energy_similarity
    reasons.append(f"energy similarity (+{energy_similarity:.2f})")

    return score, reasons

def score_song_experimental_weights(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    EXPERIMENTAL SCORING CONFIGURATION (Phase 4, Step 3 Data Experiment):
    - Genre Match Importance: Cut in half (1.0 Point down from 2.0)
    - Mood Match Importance: Maintained (1.0 Point)
    - Energy Similarity Importance: Doubled (Multiplier of 2.0 applied to the distance similarity)
    """
    score = 0.0
    reasons: List[str] = []

    genre_pref = str(user_prefs.get("genre", "")).lower()
    mood_pref = str(user_prefs.get("mood", "")).lower()
    target_energy = float(user_prefs.get("energy") if user_prefs.get("energy") is not None else user_prefs.get("target_energy", 0.0))

    song_genre = str(song.get("genre", "")).lower()
    song_mood = str(song.get("mood", "")).lower()
    song_energy = float(song.get("energy", 0.0))

    # 1. Genre Check (Experimental: Halved importance to 1.0)
    if song_genre == genre_pref:
        score += 1.0
        reasons.append(f"genre match ({song_genre}) (+1.0)")

    # 2. Mood Check (Maintained at 1.0)
    if song_mood == mood_pref:
        score += 1.0
        reasons.append(f"mood match ({song_mood}) (+1.0)")

    # 3. Energy Calculation (Experimental: Doubled importance multiplier to 2.0)
    energy_distance = abs(song_energy - target_energy)
    raw_similarity = 1.0 - energy_distance
    energy_similarity = 2.0 * raw_similarity
    
    score += energy_similarity
    reasons.append(f"energy similarity (+{energy_similarity:.2f})")

    return score, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation loop.
    Required by src/main.py
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, "; ".join(reasons)))
        
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
