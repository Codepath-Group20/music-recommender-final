# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch Alpha (Phase 4 Evaluation Edition)**

---

## 2. Intended Use  

This model is an experimental music recommender designed to sort a curated song catalog against specific user behavioral attributes. It acts as a pedagogical simulation for exploring algorithmic design constraints, rather than an engine for live corporate streaming deployments. It assumes that a user's complex acoustic intent can be modeled by breaking tastes down into three straightforward dimensions: a favorite overarching genre category, a preferred immediate emotional mood tag, and a continuous target energy range value between 0.0 and 1.0.

---

## 3. How the Model Works  

The recommender operates via an additive linear scoring hierarchy that scans every track in an active catalog and assigns points based on cross-attribute alignments. In our original baseline setup, a song is evaluated across three primary dimensions:
- **Genre Matching:** Yields a high categorical bonus of `+2.0` points if the text strings match perfectly.
- **Mood Matching:** Yields a categorical bonus of `+1.0` point if the semantic label matches exactly.
- **Energy Distance:** Computes continuous mathematical proximity using absolute error, contributing a continuous fraction up to a max of `+1.0` point:

`Score = 1.0 - abs(target_energy - song_energy)`

In our Phase 4 experimental iteration (`score_song_experimental_weights`), we adjusted the feature hierarchy to study mathematical sensitivity. We reduced the categorical genre weight to `+1.0` point and doubled the continuous energy similarity scale factor to a maximum multiplier of `2.0`. This successfully repositioned continuous track audio features above categorical taxonomies.

---

## 4. Data  

The catalog utilizes a merged framework comprising 17 tracks across 10 metadata columns, tracking attributes such as title, artist, genre, mood, energy, tempo, and acoustic properties. This dataset pairs simulated, code-generated laboratory records (e.g., electronic lofi and indie-pop archetypes designed for verification tests) with real-world iconic tracks (e.g., Marconi Union, Billie Eilish, and Metallica) to enrich variance. Missing values for continuous metrics in the real-world dataset (such as valence or tempo) are automatically populated with safe fallback null representations to ensure that baseline framework parsing does not trigger structural application failures.

---

## 5. Strengths  

The pipeline handles direct, non-contradictory requests exceptionally well. When a user's intent is well-represented in the data (such as searching cleanly for high-energy pop or low-energy lofi), the additive scoring yields highly logical rankings. Furthermore, string normalizations are robust; the application strips and lowercases string variables prior to scoring evaluations, preventing trailing whitespaces or uppercase mismatches from impacting categorical calculations.

---

## 6. Limitations and Bias 

The scoring system exhibits an overwhelming structural bias toward categorical genre matching, which frequently causes it to override an explicit emotional user intent. This is evident where a high-energy "intense" track was recommended to a user seeking "sad" music simply because the track shared a genre label, completely breaking the user's expected emotional context. Furthermore, because categorical matches (Genre +2.0, Mood +1.0) use hard-coded point spikes, they consistently suppress fine-grained mathematical similarities derived from continuous features like the energy distance equation. Lastly, the dataset exhibits representation bias, lacking specific target combinations (such as high-energy sad pop or classical music), forcing the system to fallback on suboptimal mood overrides.

---

## 7. Evaluation  

### [LOG SET A] Original Baseline Stress Test Results

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
 [4] Score: 0.97 | 'Master of Puppets' by Metallica
     (Actuals -> Genre: metal, Mood: intense, Energy: 0.92)
 [5] Score: 0.96 | 'Storm Runner' by Voltline
     (Actuals -> Genre: rock, Mood: intense, Energy: 0.91)
---------------------------------------------------------------------------

🚀 STRESS TESTING: Profile 2: Genre-Defying Pure Vibe ('The Fluid Acoustic')
   Criteria -> Genre: classical, Mood: focused, Target Energy: 0.1
---------------------------------------------------------------------------
 [1] Score: 1.7 | 'Focus Flow' by LoRoom
     (Actuals -> Genre: lofi, Mood: focused, Energy: 0.4)
 [2] Score: 0.98 | 'Weightless' by Marconi Union
     (Actuals -> Genre: ambient, Mood: calm, Energy: 0.12)
 [3] Score: 0.82 | 'Spacewalk Thoughts' by Orbit Bloom
     (Actuals -> Genre: ambient, Mood: chill, Energy: 0.28)
 [4] Score: 0.76 | 'So What' by Miles Davis
     (Actuals -> Genre: jazz, Mood: smooth, Energy: 0.34)
 [5] Score: 0.75 | 'Library Rain' by Paper Lanterns
     (Actuals -> Genre: lofi, Mood: chill, Energy: 0.35)
---------------------------------------------------------------------------

🚀 STRESS TESTING: Profile 3: Un-biasable Middle-Grounder ('The Perfect Gray Area')
   Criteria -> Genre: rock, Mood: energetic, Target Energy: 0.5
---------------------------------------------------------------------------
 [1] Score: 2.59 | 'Storm Runner' by Voltline
     (Actuals -> Genre: rock, Mood: intense, Energy: 0.91)
 [2] Score: 0.98 | 'Bury a Friend' by Billie Eilish
     (Actuals -> Genre: dark pop, Mood: eerie, Energy: 0.48)
 [3] Score: 0.95 | 'Texas Sun' by Leon Bridges & Khruangbin
     (Actuals -> Genre: soul, Mood: chilled, Energy: 0.55)
 [4] Score: 0.92 | 'Midnight Coding' by LoRoom
     (Actuals -> Genre: lofi, Mood: chill, Energy: 0.42)
 [5] Score: 0.9 | 'Focus Flow' by LoRoom
     (Actuals -> Genre: lofi, Mood: focused, Energy: 0.4)
---------------------------------------------------------------------------
```

### [LOG SET B] Phase 4 Experimental Weight Modification Results

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
 [4] Score: 1.94 | 'Master of Puppets' by Metallica
     (Actuals -> Genre: metal, Mood: intense, Energy: 0.92)
 [5] Score: 1.92 | 'Storm Runner' by Voltline
     (Actuals -> Genre: rock, Mood: intense, Energy: 0.91)
---------------------------------------------------------------------------

🚀 EXPERIMENTAL STRESS TESTING: Profile 2: Genre-Defying Pure Vibe ('The Fluid Acoustic')
   Criteria -> Genre: classical, Mood: focused, Target Energy: 0.1
---------------------------------------------------------------------------
 [1] Score: 2.4 | 'Focus Flow' by LoRoom
     (Actuals -> Genre: lofi, Mood: focused, Energy: 0.4)
 [2] Score: 1.96 | 'Weightless' by Marconi Union
     (Actuals -> Genre: ambient, Mood: calm, Energy: 0.12)
 [3] Score: 1.64 | 'Spacewalk Thoughts' by Orbit Bloom
     (Actuals -> Genre: ambient, Mood: chill, Energy: 0.28)
 [4] Score: 1.52 | 'So What' by Miles Davis
     (Actuals -> Genre: jazz, Mood: smooth, Energy: 0.34)
 [5] Score: 1.5 | 'Library Rain' by Paper Lanterns
     (Actuals -> Genre: lofi, Mood: chill, Energy: 0.35)
---------------------------------------------------------------------------

🚀 EXPERIMENTAL STRESS TESTING: Profile 3: Un-biasable Middle-Grounder ('The Perfect Gray Area')
   Criteria -> Genre: rock, Mood: energetic, Target Energy: 0.5
---------------------------------------------------------------------------
 [1] Score: 2.18 | 'Storm Runner' by Voltline
     (Actuals -> Genre: rock, Mood: intense, Energy: 0.91)
 [2] Score: 1.96 | 'Bury a Friend' by Billie Eilish
     (Actuals -> Genre: dark pop, Mood: eerie, Energy: 0.48)
 [3] Score: 1.9 | 'Texas Sun' by Leon Bridges & Khruangbin
     (Actuals -> Genre: soul, Mood: chilled, Energy: 0.55)
 [4] Score: 1.84 | 'Midnight Coding' by LoRoom
     (Actuals -> Genre: lofi, Mood: chill, Energy: 0.42)
 [5] Score: 1.8 | 'Focus Flow' by LoRoom
     (Actuals -> Genre: lofi, Mood: focused, Energy: 0.4)
---------------------------------------------------------------------------
```

### Profile Comparisons and Analysis (Sensitivity Experiment)
* **Impact of Weight Adjustments on Profile 1:** In the original baseline evaluation, the top track (*Gym Hero*, Score: 2.98) completely overshadowed candidates outside its genre due to the massive +2.0 genre spike. Under the experimental weights (Genre halved to 1.0, Energy doubled to a scale factor of 2.0), *Gym Hero* remained at rank 1 with a score of 2.96. However, non-genre tracks with perfect target energy alignments surged in competitiveness. For instance, *Spitfire* by The Prodigy (a non-pop electronic track matching the 0.95 energy target exactly) climbed from a baseline score of 1.00 up to rank 3 with an experimental score of 2.00, demonstrating that the engine is now significantly more responsive to mathematical feature distances.
* **Sensitivity Shifts in Profile 2:** When evaluating the unavailable "classical" genre, the categorical genre incentive drops to 0 across all tracks. In the baseline system, categorical mood alignment dominated completely, pushing *Focus Flow* ahead of *Weightless* by a large margin (1.70 vs. 0.98). Under the experimental system, doubling the value of proximity calculations drastically narrowed this gap. *Weightless* (which sits perfectly at an ultra-low energy score of 0.12) moved to rank 2 with a highly competitive score of 1.96—nearly matching *Focus Flow* at 2.40.
* **Behavior of Profile 3:** Under the original configuration, the midpoint energy target (0.50) penalized extreme-energy songs heavily, yet *Storm Runner* (0.91 energy) dominated entirely because its +2.0 rock genre bonus outplayed its poor energy alignment. In this experiment, cutting the genre bonus in half lowered *Storm Runner's* score from 2.59 down to 2.18. This allowed tracks like *Bury a Friend* (0.48 energy) and *Texas Sun* (0.55 energy) to close the distance significantly, proving that scaling down dominant categorical weights reduces artificial ranking separation.

### Plain Language Summary
When analyzing how the system behaves, it becomes clear that our algorithm treats song features like an unequal hierarchy rather than a balanced mix. For example, when a user asks for "Anxious High-Energy Joy" (Pop, Sad, 0.95 Energy), the song "Gym Hero" shoots straight to the top of the list. To a human, recommending an intense gym-workout song to someone who specifically asked for "sad" music feels completely wrong. 

However, because our code awards a massive 2.0-point bonus just for matching the word "Pop", any pop song gets an unfair head start. The formula values matching the "Pop" label way more than it punishes the fact that the song is completely missing the "Sad" mood. Because "Gym Hero" has the correct genre and matches the fast-paced energy target, its high score completely overpowers and buries actual lower-energy sad tracks. In short, the "Genre" rule acts like a bully in our math equation, forcing workout tracks onto people who just wanted to listen to a melancholy melody.

---

## 8. Future Work  

To advance this engine, the recommendation scoring pipeline should move away from hardcoded additive metrics and shift toward a normalized vector space similarity framework, such as Cosine Similarity. This transition would evaluate songs along an evenly distributed dimensional plane rather than allowing a single dominant string feature to overpower others. Additionally, incorporating secondary real-world metadata attributes—such as *acousticness* or *danceability*—would establish a multi-layered model of sonic profiles. This development would empower the engine to identify fluid acoustic vibes even when users supply completely novel or mismatched genre labels.

---

## 9. Personal Reflection  

Building and stress-testing this recommendation engine revealed that simple sorting algorithms can easily introduce severe structural design biases. I discovered that minor imbalances in how point rewards are weighted can entirely suppress user preferences, transforming an interactive playlist engine into a rigid filter. This experiment has changed how I perceive standard music streaming applications; I now recognize that behind every playlist recommendation lies an intricate math equation balancing organizational categorization defaults against raw mathematical measurements of personal taste.
