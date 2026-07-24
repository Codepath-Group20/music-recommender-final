# 🎧 Music Recommender System (Vector Engine & Hybrid Pipeline)

## Project Summary
This project features a content-based music recommendation engine written in Python. It includes both a legacy **rule-based point accumulator** and an upgraded **5D vector cosine similarity engine**. 

By comparing additive string matching against continuous multi-dimensional vector space calculations, this project explores how sorting algorithms handle structural bias and acoustic feature alignment.

---

## Architecture & Scoring Engines

### 1. Vector Cosine Similarity Engine (New)
Converts 5 numerical audio features into a normalized 5D feature vector v to evaluate track similarity via **Cosine Similarity**:

    v = [ energy, tempo_bpm (normalized), valence, danceability, acousticness ]

* **Tempo Normalization:** Min-max scaled across the dataset to bound `tempo_bpm` between 0.0 and 1.0.
* **Zero Division Guard:** Includes an epsilon threshold (`1e-9`) for numerical stability.
* **Synthetic Target Vector:** Anchored by the user's requested `energy` setting and auto-filled using dataset averages for remaining audio attributes.

### 2. Baseline Pipeline (`score_song`)
Our original rule-based algorithm operates via an additive point accumulator:
* **Genre Match (`+2.0` points):** Direct bonus if the song category matches the favorite genre.
* **Mood Match (`+1.0` point):** Secondary bonus if the semantic mood label matches.
* **Energy Proximity (Up to `+1.0` point):** Calculated using absolute difference: `1.0 - abs(target_energy - song_energy)`.

---

## Quickstart & CLI Usage

Run the main CLI script using the virtual environment:

```bash
./.venv/bin/python src/main.py [OPTIONS]
```

### Supported CLI Flags

* `--mode [vector|baseline|both]`: Choose recommendation engine mode (default: `vector`).
* `--top-k N`: Number of recommendations to return (default: `5`).

### CLI Examples

**Compare Vector vs. Legacy Baseline side-by-side:**
```bash
./.venv/bin/python src/main.py --mode both --top-k 5
```

**Run Vector Mode only:**
```bash
./.venv/bin/python src/main.py --mode vector
```

### Sample Output

```text
Top recommendations (vector cosine):
1. Gym Hero - Max Pulse
2. Sunrise City - Neon Echo

Top recommendations (baseline):
1. Gym Hero - Score: 2.98
   (genre match: pop [+2.0], mood match: happy [+1.0], energy similarity [+0.98])
```

---

## Running Automated Tests

Run the test suite via `pytest`:

```bash
./.venv/bin/pytest -q
```

---

## Key Takeaways & Analytical Insights

* **The Genre "Bully" Effect:** In the rule-based baseline, hardcoded string matches (`+2.0` points) easily overrode continuous acoustic attributes.
* **Vector Balance:** Moving to 5D vector space allows multi-dimensional sonic features (`danceability`, `valence`, `acousticness`) to weigh in fairly without single-metadata locks.
