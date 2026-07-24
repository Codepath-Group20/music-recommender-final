"""Run a user-profile-based recommendation demo.

This script accepts simple user taste inputs and prints recommendations using
both the vector cosine similarity path and the legacy baseline rule-based path.
"""

import argparse

from recommender import Song, Recommender, load_songs, recommend_songs


def build_songs(song_dicts):
    return [
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


def compute_dataset_means(songs):
    if not songs:
        return 0.0, 0.0, 0.0, 0.0

    num_songs = len(songs)
    mean_tempo = sum(song.tempo_bpm for song in songs) / num_songs
    mean_valence = sum(song.valence for song in songs) / num_songs
    mean_danceability = sum(song.danceability for song in songs) / num_songs
    mean_acousticness = sum(song.acousticness for song in songs) / num_songs
    return mean_tempo, mean_valence, mean_danceability, mean_acousticness


def build_target_vector(rec, genre, mood, energy):
    song_dicts = load_songs("data/songs.csv")
    songs = build_songs(song_dicts)
    mean_tempo, mean_valence, mean_danceability, mean_acousticness = compute_dataset_means(songs)

    target_song = Song(
        id=0,
        title="target",
        artist="",
        genre=genre,
        mood=mood,
        energy=energy,
        tempo_bpm=mean_tempo,
        valence=mean_valence,
        danceability=mean_danceability,
        acousticness=mean_acousticness,
    )
    return rec.to_vector(target_song)


def print_recommendations(recommendations, header):
    print(f"\n{header}\n")
    for item in recommendations:
        if isinstance(item, tuple):
            song_dict, score, explanation = item
            print(f"{song_dict['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}\n")
        else:
            print(f"{item.title} - {item.artist}")


def parse_args():
    parser = argparse.ArgumentParser(description="Run profile-based recommendations")
    parser.add_argument("--genre", default="pop", help="User favorite genre")
    parser.add_argument("--mood", default="happy", help="User favorite mood")
    parser.add_argument("--energy", type=float, default=0.8, help="Target energy level")
    parser.add_argument(
        "--mode",
        choices=["vector", "baseline", "both"],
        default="both",
        help="Recommendation mode to run",
    )
    parser.add_argument("--top-k", type=int, default=5, help="Number of top recommendations")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    song_dicts = load_songs("data/songs.csv")
    songs = build_songs(song_dicts)
    rec = Recommender(songs)

    print("User profile")
    print("------------")
    print(f"Genre: {args.genre}")
    print(f"Mood: {args.mood}")
    print(f"Target energy: {args.energy}")
    print(f"Mode: {args.mode}")
    print(f"Top K: {args.top_k}\n")

    if args.mode in ("vector", "both"):
        target_vector = build_target_vector(rec, args.genre, args.mood, args.energy)
        recommendations = rec.recommend_by_vector(target_vector, top_k=args.top_k)
        print_recommendations(recommendations, "Top recommendations (vector cosine):")

    if args.mode in ("baseline", "both"):
        baseline = recommend_songs(
            {"genre": args.genre, "mood": args.mood, "energy": args.energy},
            song_dicts,
            k=args.top_k,
        )
        print_recommendations(baseline, "Top recommendations (baseline):")


if __name__ == "__main__":
    main()
