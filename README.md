# C.U.R.S.U.S.
### Curriculum Unified Recommendation System for Upskilling & Scaling

> AI-powered training recommendation dashboard built for BD Healthcare (Hecton and Dickinson) as part of the M2 MDAI Capstone Project at Grenoble Ecole de Management (March 2026).

---

## Overview

CURSUS is a personalised training pathway recommendation system designed to solve a core operational problem at BD Healthcare: over 600 hours per year spent manually matching Healthcare Professionals (HCPs) to relevant training content.

Given a user profile (role, specialty, language, skill level, available time, and training format preferences), CURSUS generates a personalised 5-module learning pathway in under 5 seconds — handling cold-start profiles, respecting language and skill-level constraints, surfacing Qualiopi-eligible content, and ensuring recommendation diversity through MMR re-ranking.

---

## How It Works

CURSUS runs a 5-stage AI pipeline:

| Step | Name | Description |
|------|------|-------------|
| 01 | Feature Engineering | Profile sentence + module text built and converted to natural language |
| 02 | Dual Embedding | TF-IDF + LSA (35%) fused with Sentence-BERT multilingual (65%), projected to shared vector space |
| 03 | Cosine Similarity | 1,000 x 1,000 pairwise similarity matrix computed simultaneously for all module-HCP pairs |
| 04 | Score Fusion + Boosting | `score = 0.35×TF-IDF + 0.65×SBERT + domain(+4%) + language(+6%) + OPCO(+5%) + skill(+4%)` |
| 05 | MMR Re-ranking | Maximal Marginal Relevance selects Top 5 that are both relevant and diverse |

---

## Tech Stack

- **AI / ML:** scikit-learn (TF-IDF + LSA), Sentence-Transformers (paraphrase-multilingual-MiniLM-L12-v2), NumPy
- **Frontend / Dashboard:** Streamlit
- **Language:** Python 3.13
- **Dataset:** 887 real BD Learning Academy (BDLA) modules + 113 synthetic records (1,000 total), built to BD's own data schema.
-              Dataset available on request.

---

## Key Features

- Cold-start profile handling (no prior training history required)
- Language filtering (French-first for France pilot scope)
- Skill-level constraints (Beginner / Intermediate / Advanced / Expert)
- OPCO / Qualiopi certification boost for revenue-critical courses
- MMR re-ranking to avoid recommending 5 near-identical modules
- Live Streamlit dashboard with profile builder and curriculum output

---

## Project Structure
```
cursus/
├── model.py                  # Core AI pipeline (TF-IDF + SBERT + MMR)
├── cursus_dashboard_v5.py    # Streamlit dashboard
├── data/
│   └── modules_1000.csv      # Full dataset (887 real + 113 synthetic)
├── requirements.txt
└── README.md
```

---

## Live Demo

The dashboard is deployed on Streamlit Cloud:
*[https://bdcursusdashboard-rr7fccqtgodftxvc6mc62m.streamlit.app/]*

---

## Dataset Note

The modelling base expands BD's real French catalogue (64 modules) to a 1,000-module dataset combining the full global BDLA catalogue (887 modules) with 113 synthetic records generated strictly to BD's own data conventions. Synthetic data was a necessary response to structural data quality issues in the raw export (568/648 broken prerequisite cross-references, 47 invalid BU tags, 9% missing Duration_Hours, absent Last_Modified_Date field) and is clearly labelled throughout.

---
## Acknowledgements

Built in collaboration with BD Healthcare (France). Special thanks to our client contact for the openness and quality of engagement throughout the project.
