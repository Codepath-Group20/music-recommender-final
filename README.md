# 🎧 Music Recommender Simulation

## Project Summary
This project features a simplified, content-based music recommendation engine written in Python. The simulation parses a multi-layered catalog of tracks, constructs a user taste profile, evaluates each individual song using a weighted scoring algorithm, and returns top-ranked recommendation lists. By examining the interplay between discrete categorical matching and continuous numerical feature distance calculations, this system serves as an exploration of how basic sorting rules can introduce structural behavior and algorithmic biases.

---

## How The System Works

### Core Architecture
* **Song Attributes:** Each track in our catalog contains categorical tags (`genre`, `mood`) and continuous features scored from `0.0` to `1.0` (`energy`, `danceability`, `acousticness`).
* **User Profile:** Defines explicit preferences: a favorite genre, a desired mood target, and a specific target energy level.
* **The Scoring Loop:** The engine sweeps the entire active song database, evaluates each track against user parameters, aggregates scores, and returns the top $K$ tracks sorted in descending order.

### Algorithm Recipes

#### Baseline Pipeline (`score_song`)
Our original rule-based algorithm operates via an additive point-accumulator system:
1. **Genre Match (`+2.0` points):** Direct bonus if the song category matches the user's favorite genre string exactly.
2. **Mood Match (`+1.0` point):** Secondary bonus if the semantic mood label matches exactly.
3. **Energy Proximity (Up to `+1.0` point):** A continuous fraction calculated using absolute mathematical distance:

`Score = 1.0 - abs(target_energy - song_energy)`

#### Phase 4 Experimental Pipeline (`score_song_experimental_weights`)
To evaluate structural bias, an experimental configuration was added to shift the balance of power:
1. **Genre Match (`+1.0` point):** The categorical weight was cut in half to prevent genre from completely overpowering user mood.
2. **Mood Match (`+1.0` point):** Maintained constant to serve as a baseline.
3. **Energy Proximity (Up to `+2.0` points):** The continuous similarity fraction was scaled up by a multiplier of `2.0` to prioritize exact acoustic alignment over metadata labels:

`Score = 2.0 * (1.0 - abs(target_energy - song_energy))`

---

## Experiments and Evaluation Logs

### 1. Baseline System Stress Test Logs
Tested against adversarial profiles to expose edge cases where hardcoded point spikes create unexpected overrides:

```text
🚀 STRESS TESTING: Profile 1: Paradoxical Request ('Anxious High-Energy Joy')
   Criteria -> Genre: pop, Mood: sad, Target Energy: 0.95
---------------------------------------------------------------------------
 [1] Score: 2.98 | 'Gym Hero' by Max Pulse
     (Actuals -> Genre: pop, Mood: intense, Energy: 0.93)
 [2] Score: 2.87 | 'Sunrise City' by Neon Echo
     (Actuals -> Genre: pop, Mood: happy, Energy: 0.82)
 [3] Score: 1.0 | 'Spitfire' by The Prodigy
     (Actuals -> Genre: electronic, Mood: aggressive, Energy: 0.95)
---------------------------------------------------------------------------

🚀 STRESS TESTING: Profile 2: Genre-Defying Pure Vibe ('The Fluid Acoustic')
   Criteria -> Genre: classical, Mood: focused, Target Energy: 0.1
---------------------------------------------------------------------------
 [1] Score: 1.7 | 'Focus Flow' by LoRoom
     (Actuals -> Genre: lofi, Mood: focused, Energy: 0.4)
 [2] Score: 0.98 | 'Weightless' by Marconi Union
     (Actuals -> Genre: ambient, Mood: calm, Energy: 0.12)
---------------------------------------------------------------------------
```

### 2. Phase 4 Data Sensitivity Experiment Logs
Executing the identical adversarial profile battery using the adjusted `score_song_experimental_weights` logic:

```text
🚀 EXPERIMENTAL STRESS TESTING: Profile 1: Paradoxical Request ('Anxious High-Energy Joy')
   Criteria -> Genre: pop, Mood: sad, Target Energy: 0.95
---------------------------------------------------------------------------
 [1] Score: 2.96 | 'Gym Hero' by Max Pulse
     (Actuals -> Genre: pop, Mood: intense, Energy: 0.93)
 [2] Score: 2.74 | 'Sunrise City' by Neon Echo
     (Actuals -> Genre: pop, Mood: happy, Energy: 0.82)
 [3] Score: 2.0 | 'Spitfire' by The Prodigy
     (Actuals -> Genre: electronic, Mood: aggressive, Energy: 0.95)
---------------------------------------------------------------------------

🚀 EXPERIMENTAL STRESS TESTING: Profile 2: Genre-Defying Pure Vibe ('The Fluid Acoustic')
   Criteria -> Genre: classical, Mood: focused, Target Energy: 0.1
---------------------------------------------------------------------------
 [1] Score: 2.4 | 'Focus Flow' by LoRoom
     (Actuals -> Genre: lofi, Mood: focused, Energy: 0.4)
 [2] Score: 1.96 | 'Weightless' by Marconi Union
     (Actuals -> Genre: ambient, Mood: calm, Energy: 0.12)
---------------------------------------------------------------------------
```

### Key Analytical Takeaways
* **The Genre "Bully" Effect:** In the baseline, matching the "pop" label provided an insurmountable `+2.0` point advantage. This forced the system to recommend a high-intensity workout song (*Gym Hero*) to a user explicitly requesting a "sad" emotional context.
* **Sensitivity Shift:** Lowering the genre weight and doubling the energy multiplier allowed continuous characteristics to break through. Non-genre songs that precisely satisfied acoustic requirements (such as *Spitfire* at `0.95` energy and *Weightless* at `0.12` energy) saw their scores double, rendering recommendations significantly more reflective of actual listening textures.

---

## Limitations and Risks
* **Metadata Dependency:** The engine relies on binary string checking. If a track lacks an exact text match for a genre or mood, its score drops heavily regardless of its sonic qualities.
* **Dataset Representation Gaps:** With a small catalog of 17 songs, complex user profiles (like high-energy sad pop or classical) lack target options, forcing suboptimal compromises.
* **Linear Scaling Bias:** Fixed additive scores create structural hierarchies where a single arbitrarily high weight can overpower all other features combined.

---

## Engineering Process Reflection

### Core Learning Moments
Building and stress-testing this recommendation system highlighted that simple sorting algorithms can easily introduce severe structural biases. I discovered that minor imbalances in how point rewards are weighted can entirely suppress user preferences, transforming an interactive playlist engine into a rigid filter. This experiment has changed how I perceive standard music streaming applications; I now recognize that behind every playlist recommendation lies an intricate math equation balancing organizational categorization defaults against raw mathematical measurements of personal taste.

### AI Integration Insights
Using AI tools throughout this process accelerated the transition from architectural design to test implementation. It proved highly effective for generating diverse mock datasets and expanding pipeline logic. However, human intervention was critical to identify where hardcoded weights were overpowering continuous math logic. Reviewing code execution results step-by-step made it clear that algorithms strictly follow mathematical point structures rather than subjective human intent.

### Next Steps for Expansion
To advance this engine, the recommendation scoring pipeline should move away from hardcoded additive metrics and shift toward a normalized vector space similarity framework, such as Cosine Similarity. This transition would evaluate songs along an evenly distributed dimensional plane rather than allowing a single dominant string feature to overpower others. Additionally, incorporating secondary real-world metadata attributes—such as *acousticness* or *danceability*—would establish a multi-layered model of sonic profiles. This development would empower the engine to identify fluid acoustic vibes even when users supply completely novel or mismatched genre labels.
