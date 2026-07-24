"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import (
    load_songs,
    recommend_songs,
    Song,
    Recommender,
)


def main() -> None:
    # Load raw song dicts from CSV and convert to Song dataclass instances
    song_dicts = load_songs("data/songs.csv")
    songs = [
        Song(
            id=s.get("id", 0),
            title=s.get("title", "Unknown"),
            artist=s.get("artist", "Unknown"),
            genre=s.get("genre", ""),
            mood=s.get("mood", ""),
            energy=s.get("energy", 0.0),
            tempo_bpm=s.get("tempo_bpm", 0.0),
            valence=s.get("valence", 0.0),
            danceability=s.get("danceability", 0.0),
            acousticness=s.get("acousticness", 0.0),
        )
        for s in song_dicts
    ]

    rec = Recommender(songs)

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # Build a user target vector by creating a synthetic Song using the
    # dataset means for numeric features and the user's target energy.
    if songs:
        mean_tempo = sum(s.tempo_bpm for s in songs) / len(songs)
        mean_valence = sum(s.valence for s in songs) / len(songs)
        mean_dance = sum(s.danceability for s in songs) / len(songs)
        mean_acoustic = sum(s.acousticness for s in songs) / len(songs)
    else:
        mean_tempo = mean_valence = mean_dance = mean_acoustic = 0.0

    target_song = Song(
        id=0,
        title="target",
        artist="",
        genre=user_prefs["genre"],
        mood=user_prefs["mood"],
        energy=user_prefs["energy"],
        tempo_bpm=mean_tempo,
        valence=mean_valence,
        danceability=mean_dance,
        acousticness=mean_acoustic,
    )

    target_vector = rec.to_vector(target_song)

    import argparse

    parser = argparse.ArgumentParser(description="Run music recommender CLI")
    parser.add_argument(
        "--mode",
        choices=["vector", "baseline", "both"],
        default="vector",
        help="Recommendation mode: 'vector' for cosine similarity, 'baseline' for rule-based, 'both' to show both",
    )
    parser.add_argument("--top-k", type=int, default=5, help="Number of top recommendations to return")
    args = parser.parse_args()

    if args.mode == "vector":
        recommendations = rec.recommend_by_vector(target_vector, top_k=args.top_k)

        print("\nTop recommendations (vector cosine):\n")
        for song in recommendations:
            print(f"{song.title} - {song.artist}")

    elif args.mode == "baseline":
        baseline = recommend_songs(user_prefs, song_dicts, k=args.top_k)

        print("\nTop recommendations (baseline):\n")
        for song_dict, score, explanation in baseline:
            print(f"{song_dict['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}\n")

    else:  # both
        recommendations = rec.recommend_by_vector(target_vector, top_k=args.top_k)

        print("\nTop recommendations (vector cosine):\n")
        for song in recommendations:
            print(f"{song.title} - {song.artist}")

        baseline = recommend_songs(user_prefs, song_dicts, k=args.top_k)

        print("\nTop recommendations (baseline):\n")
        for song_dict, score, explanation in baseline:
            print(f"{song_dict['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}\n")


if __name__ == "__main__":
    main()
