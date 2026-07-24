🎵 Music Recommender Simulation

Project Summary

In this project, I have designed and implemented a simplified, content-based music recommendation engine written in Python.

My simulation parses a catalog of tracks, constructs a distinct user taste profile, evaluates each individual song using a weighted scoring algorithm, and returns the top-ranked recommendation list. By balancing discrete categorical matches with continuous numeric differences, the engine simulates how modern streaming platforms map user preferences to a massive library of songs.

How The System Works

Our recommendation system evaluates songs by checking how closely their attributes align with a user's target profile.

Core Architecture

Song Attributes:
Each song object in our catalog contains categorical tags (genre, mood) and continuous features scored from $0.0$ to $1.0$ (energy, danceability, acousticness).

User Profile:
The user profile defines explicit preferences: a favorite genre, a desired mood, and a specific target energy level.

The Scoring Loop:
The recommender evaluates every song in the CSV, aggregates points based on categorical exact-matches and numerical distance math, sorts the library in descending order, and returns the top $K$ tracks.

Algorithm Recipe

Our recommendation engine uses a hybrid scoring system combining categorical matching and numerical distance tracking:

Genre Match ($+2.0$ pts): Direct bonus if the song matches the user's primary favorite genre.

Mood Match ($+1.0$ pt): Direct bonus if the song matches the user's current vibe.

Energy Similarity (Up to $+1.0$ pt): Calculated using absolute error subtraction: $1.0 - |E_{\text{song}} - E_{\text{target}}|$. A perfect match yields $1.0$ point, while opposing extremes yield $0.0$ points.

Potential Biases & Limitations

Genre Dominance: Because a genre match provides twice the weight of a mood match, the system may heavily over-prioritize genre boundaries, potentially filtering out an incredibly relevant, high-energy Electronic track for a user who selected Rock.

Cold Start / Fixed Limits: The system entirely relies on explicit user inputs and cannot currently infer shifts in mood based on skipped tracks or listening time.

Overview of Real-World Systems

Modern music platforms rely on two primary recommendation frameworks:

Collaborative Filtering: Analyzes user behavior patterns (likes, shares, skips) to group similar users together and recommend music based on collective listening habits.

Content-Based Filtering: Analyzes the intrinsic qualities of individual tracks (such as tempo, genre, and acousticness) to recommend music with matching mathematical and categorical profiles.

Our Simulation Approach

This simulation prioritizes a Content-Based Filtering approach using a weighted-score scoring rule. Instead of blindly favoring high-energy or high-valence tracks, the algorithm calculates the absolute distance between a song's continuous attributes ($F_{\text{song}}$) and a user's specified ideal preferences ($P_{\text{user}}$).

The individual feature alignment is calculated using the formula:

$$\text{Feature Score} = 1.0 - |F_{\text{song}} - P_{\text{user}}|$$

The system then aggregates these continuous feature scores along with categorical bonuses (like exact genre and mood matches) using customizable user-profile weights to compute an overall compatibility score for each track. Finally, a ranking rule sorts the full catalog to generate a clean, top-$N$ list of personalized suggestions.

Data Structures

Song Object Attributes

id (int): Unique identifier for the track.

title (string): Title of the song.

artist (string): Performing artist.

genre (string): Categorical genre (e.g., Pop, Synthwave, Rock).

mood (string): Categorical vibe indicator (e.g., Happy, Chill, Intense).

energy (float): Numerical value from $0.0$ to $1.0$ representing intensity.

tempo_bpm (int): Beats per minute.

valence (float): Numerical value from $0.0$ to $1.0$ describing musical positivity.

danceability (float): Numerical value from $0.0$ to $1.0$ representing rhythmic stability.

acousticness (float): Numerical value from $0.0$ to $1.0$ tracking acoustic vs electronic presence.

UserProfile Object Attributes

user_id (int/string): Unique identification for the user.

preferred_genres (list of strings): Target categories for hard matching or bonuses.

preferred_moods (list of strings): Target moods for contextual affinity.

target_features (dict): Ideal baseline float values for continuous metrics (energy, valence, danceability, acousticness).

feature_weights (dict): Importance scaling metrics assigned to individual features, ensuring heavily weighted preferences exert a greater influence over final song calculation scores.

Getting Started

Setup

Create a virtual environment (optional but recommended):

python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows


Install dependencies:

pip install -r requirements.txt


Run the app:

python -m src.main


Running Tests

Run the starter tests with:

pytest


You can add more tests in tests/test_recommender.py.

Sample Recommendation Output

Below is a live trace of our recommender generating a ranked recommendation list for a user searching for Happy Pop:

Loaded songs: 17
==================================================
RECOMMENDATIONS FOR: Genre=Pop | Mood=Happy
==================================================
1. "Blinding Lights" by The Weeknd
   📊 Final Score: 3.92
   💡 Reasons: genre match (Pop) (+2.0), mood match (Happy) (+1.0), energy similarity (+0.92)
--------------------------------------------------
2. "Midnight City" by M83
   📊 Final Score: 1.93
   💡 Reasons: mood match (Dreamy) (+0.0), energy similarity (+0.93)
--------------------------------------------------
3. "Texas Sun" by Leon Bridges & Khruangbin
   📊 Final Score: 0.70
   💡 Reasons: energy similarity (+0.70)
--------------------------------------------------


Experiments You Tried

Use this section to document the experiments you ran. For example:

What happened when you changed the weight on genre from $2.0$ to $0.5$?

What happened when you added tempo or valence to the score?

How did your system behave for different types of users?

Limitations and Risks

Summarize some limitations of your recommender:

It only works on a tiny catalog.

It does not understand lyrics or language semantic meaning.

It might over-favor one genre or mood based on high starting weights.

You will go deeper on this in your model card.

Reflection

Read and complete model_card.md:

Model Card

Write 1 to 2 paragraphs here about what you learned:

How recommenders turn raw features and categorical tokens into accurate predictions.

Where systemic bias, data feedback loops, or unfairness could show up in simple or complex systems like this.
