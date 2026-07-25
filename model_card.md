# Model Card & System Reflections

## 1. System Limitations & Biases
* **Metadata Dependency:** The engine relies on accurate audio feature scoring (`energy`, `valence`, `danceability`, `acousticness`, `tempo_bpm`). If dataset entries contain inaccurate audio feature measurements, the vector space representation will misalign recommendations.
* **Dataset Scale Limitations:** With a small catalog, edge-case requests (such as high-energy acoustic classical tracks) may yield suboptimal similarity scores due to sparse representation in vector space.
* **Synthetic Target Bias:** Filling unspecified target dimensions with dataset averages assumes average preference for non-specified traits, which may slightly pull recommendations toward typical dataset trends.

## 2. Misuse Potential & Prevention
* **System Misuse:** Recommendation systems can be manipulated through "playlist stuffing" or attribute manipulation to artificially inflate a track's proximity to popular user target vectors.
* **Prevention Strategies:** Implement strict vector validation guardrails, feature scaling caps, and multi-factor similarity bounds to prevent single-attribute manipulation.

## 3. Reliability Testing & Surprises
* **Key Surprise:** During initial testing, unnormalized `tempo_bpm` values (ranging from 60 to 180) completely dominated the cosine similarity calculation, rendering features bounded between $0.0$ and $1.0$ (like `energy`) negligible.
* **Resolution:** Implementing min-max bound computation (`_compute_vector_bounds`) directly in the recommender engine restored balanced feature weighting across all 5 dimensions.

## 4. AI Collaboration Reflection
* **Helpful AI Suggestion:** The AI suggested adding an epsilon guard (`1e-9`) inside the cosine similarity function to prevent potential zero-division crashes when handling zero-magnitude vectors.
* **Flawed AI Suggestion:** During early CLI refactoring, the AI attempted to overwrite the primary user interface with heavy agentic execution loops that consumed high credit quotas and altered legacy test signatures.
* **Human Intervention:** Reverted the breaking signature changes, preserved the core `Recommender.recommend_by_vector` interface, and added standard CLI flags (`--mode`, `--top-k`) to ensure backward compatibility and reliable testing.
