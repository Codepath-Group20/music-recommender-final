# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch Alpha (Phase 4 Evaluation Edition)**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  
- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  
- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  
- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  
- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The scoring system exhibits an overwhelming structural bias toward categorical genre matching, which frequently causes it to override an explicit emotional user intent. This is evident where a high-energy "intense" track was recommended to a user seeking "sad" music simply because the track shared a genre label, completely breaking the user's expected emotional context. Furthermore, because categorical matches (Genre +2.0, Mood +1.0) use hard-coded point spikes, they consistently suppress fine-grained mathematical similarities derived from continuous features like the energy distance equation. Lastly, the dataset exhibits representation bias, lacking specific target combinations (such as high-energy sad pop or classical music), forcing the system to fallback on suboptimal mood overrides.

---

## 7. Evaluation  

### Stress Test Results (Terminal Log Output)

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

### Profile Comparisons and Analysis
* **Profile 1 vs. Dataset Reality:** Testing a contradictory request ("High-Energy Sad Pop") revealed that the mathematical bonus for matching "pop" (+2.0) completely overpowered the user's emotional request for "sad" music. The system recommended "Gym Hero" (an intense workout track) as its top choice, completely failing the user's real mood constraint.
* **Profile 2 Overrides:** Testing an unavailable genre ("classical") successfully stripped away the genre bias. This revealed a secondary surprise: categorical "mood" matching completely overrides raw "energy distance." "Focus Flow" beat out "Weightless" because its explicit "focused" tag provided +1.0 point, even though "Weightless" sat almost perfectly on the user's continuous energy target.
* **Profile 3 Midpoint Behavior:** Placing the energy target at exactly `0.5` severely penalized both hyper-high and hyper-low tracks. This forced the system to lean entirely on how well rock music was represented in our dataset, causing the extreme track "Storm Runner" to dominate simply due to its heavy +2.0 genre alignment bonus.

### Plain Language Summary
When analyzing how the system behaves, it becomes clear that our algorithm treats song features like an unequal hierarchy rather than a balanced mix. For example, when a user asks for "Anxious High-Energy Joy" (Pop, Sad, 0.95 Energy), the song "Gym Hero" shoots straight to the top of the list. To a human, recommending an intense gym-workout song to someone who specifically asked for "sad" music feels completely wrong. 

However, because our code awards a massive 2.0-point bonus just for matching the word "Pop", any pop song gets an unfair head start. The formula values matching the "Pop" label way more than it punishes the fact that the song is completely missing the "Sad" mood. Because "Gym Hero" has the correct genre and matches the fast-paced energy target, its high score completely overpowers and buries actual lower-energy sad tracks. In short, the "Genre" rule acts like a bully in our math equation, forcing workout tracks onto people who just wanted to listen to a melancholy melody.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  
- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  
- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps
