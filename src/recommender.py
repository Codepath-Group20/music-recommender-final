from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

VECTOR_FEATURES = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")


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
        self._vector_bounds = self._compute_vector_bounds(songs)

    def _compute_vector_bounds(self, songs: List[Song]) -> Dict[str, Tuple[float, float]]:
        bounds: Dict[str, Tuple[float, float]] = {}
        for feature in VECTOR_FEATURES:
            values = [getattr(song, feature, 0.0) for song in songs if getattr(song, feature, None) is not None]
            if values:
                bounds[feature] = (min(values), max(values))
        return bounds

    def _normalize_feature(self, value: float, feature: str) -> float:
        bounds = self._vector_bounds.get(feature)
        if bounds is None:
            return float(value)
        min_value, max_value = bounds
        if max_value == min_value:
            return 0.0
        return (float(value) - min_value) / (max_value - min_value)

    def to_vector(self, song: Song) -> List[float]:
        """Convert the five numeric audio features into a normalized 5D vector."""
        return [self._normalize_feature(getattr(song, feature, 0.0), feature) for feature in VECTOR_FEATURES]

    def _cosine_similarity(self, left: List[float], right: List[float]) -> float:
        if len(left) != len(right):
            raise ValueError("Vectors must have the same length")

        dot_product = sum(a * b for a, b in zip(left, right))
        left_norm = math.sqrt(sum(a * a for a in left))
        right_norm = math.sqrt(sum(b * b for b in right))
        denominator = max(left_norm * right_norm, 1e-9)
        return dot_product / denominator

    def recommend_by_vector(self, target_vector: List[float], top_k: int = 5) -> List[Song]:
        """Recommend the top K songs by cosine similarity with a target vector."""
        if not self.songs:
            return []

        normalized_target = [float(value) for value in target_vector]
        if len(normalized_target) != len(VECTOR_FEATURES):
            raise ValueError(f"Target vector must contain {len(VECTOR_FEATURES)} values")

        scored_songs: List[Tuple[float, Song]] = []
        for song in self.songs:
            similarity = self._cosine_similarity(normalized_target, self.to_vector(song))
            scored_songs.append((similarity, song))

        scored_songs.sort(key=lambda item: item[0], reverse=True)
        return [song for _, song in scored_songs[:top_k]]

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs: List[Tuple[float, Song]] = []
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

        scored_songs.sort(key=lambda item: item[0], reverse=True)
        return [song for _, song in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return f"{song.title} aligns with the user's taste based on content similarity and audio profile."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, mode="r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                songs.append(
                    {
                        "id": int(row.get("id", 0)),
                        "title": row.get("title", "Unknown"),
                        "artist": row.get("artist", "Unknown"),
                        "genre": str(row.get("genre", "")).strip().lower(),
                        "mood": str(row.get("mood", "")).strip().lower(),
                        "energy": float(row.get("energy", 0.0)),
                        "tempo_bpm": float(row.get("tempo_bpm", 0.0)),
                        "valence": float(row.get("valence", 0.0)),
                        "danceability": float(row.get("danceability", 0.0)),
                        "acousticness": float(row.get("acousticness", 0.0)),
                    }
                )
            except (ValueError, KeyError):
                continue
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    genre_pref = str(user_prefs.get("genre", "")).lower()
    mood_pref = str(user_prefs.get("mood", "")).lower()
    target_energy = float(
        user_prefs.get("energy")
        if user_prefs.get("energy") is not None
        else user_prefs.get("target_energy", 0.0)
    )

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


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, "; ".join(reasons)))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
