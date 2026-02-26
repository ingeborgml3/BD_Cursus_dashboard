import warnings
import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

try:
    from sentence_transformers import SentenceTransformer
    SBERT_AVAILABLE = True
except ImportError:
    SBERT_AVAILABLE = False
    print("⚠️  sentence-transformers not installed. Running in TF-IDF only mode.")

warnings.filterwarnings("ignore")
print("✅ Imports complete")

# ── File paths ────────────────────────────────────────────────────────────────
MODULES_PATH   = "BD_Dataset1_Training_Modules_v3.csv"
CUSTOMERS_PATH = "BD_Dataset2_HCP_Profiles_v3 (1).csv"

# ── Settings ──────────────────────────────────────────────────────────────────
USE_SBERT      = SBERT_AVAILABLE
SBERT_MODEL    = "paraphrase-multilingual-MiniLM-L12-v2"
LSA_COMPONENTS = 150
TFIDF_NGRAM    = (1, 2)
W_TFIDF        = 0.35
W_SBERT        = 0.65
BOOST_LANGUAGE      = 0.06
BOOST_DOMAIN        = 0.08
BOOST_OPCO          = 0.05
BOOST_CONTRACT_CERT = 0.03
BOOST_SKILL         = 0.04
BOOST_FORMAT        = 0.03
PENALTY_DURATION    = 0.10
TOP_K          = 5
MMR_LAMBDA     = 0.70
CANDIDATE_POOL = 50

SKILL_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2, "Expert": 3}
SKILL_PHRASES = {
    "Beginner":     "with limited experience",
    "Intermediate": "with moderate clinical experience",
    "Advanced":     "with extensive clinical experience",
    "Expert":       "with expert-level clinical expertise",
}
OBJECTIVE_TO_DOMAIN = {
    "Urology & Critical Care":           ["ttm", "temperature", "icu", "critical",
                                           "réanimation", "hypothermie", "foley",
                                           "urolog", "bodyguar"],
    "Medication Management":             ["alaris", "pyxis", "infusion", "pump",
                                           "medication", "dispensing", "rowa",
                                           "guardrails", "drug", "perfusion",
                                           "médicament", "dispensation", "pharmacie",
                                           "healthsight", "opco", "qualiopi"],
    "Vascular Access & Infusion":        ["picc", "vascular", "catheter", "iv",
                                           "nexiva", "midline", "piccline", "access",
                                           "accès", "vasculaire", "insertion"],
    "Specimen Collection & Diagnostics": ["vacutainer", "specimen", "blood",
                                           "preanalytical", "collection", "microtainer",
                                           "a-line", "preset", "prélèvement",
                                           "préanalytique", "sang"],
}

# ── Load & clean modules ──────────────────────────────────────────────────────
modules_raw = pd.read_csv(MODULES_PATH, encoding="utf-8-sig")
DROP_MODULE_COLS = ["Target_Roles", "Created_By"]
modules_raw.drop(columns=[c for c in DROP_MODULE_COLS if c in modules_raw.columns], inplace=True)
modules_raw["Duration_Hours"] = pd.to_numeric(modules_raw["Duration_Hours"], errors="coerce").fillna(1.0)
modules_raw["Course_Active"]  = modules_raw["Course_Active"].str.strip().str.upper().fillna("YES")
CAT_MODULE_COLS = ["Skill_Level", "Training_Type", "Delivery_Format",
                   "Topic_Domain", "Business_Unit", "Business_Unit_Full",
                   "OPCO_Eligible", "Certification", "Language", "Country"]
for col in CAT_MODULE_COLS:
    if col in modules_raw.columns:
        modules_raw[col] = modules_raw[col].fillna("Unknown").str.strip()
modules_df = modules_raw[modules_raw["Course_Active"] == "YES"].copy().reset_index(drop=True)
print(f"✅ Modules loaded: {len(modules_df)} active modules")

# ── Build module texts ────────────────────────────────────────────────────────
def build_module_text(df):
    return (
        df["Description"].fillna("")   + " " +
        df["Topic_Domain"].fillna("")  + " " +
        df["Topic_Domain"].fillna("")  + " " +
        df["Training_Type"].fillna("") + " " +
        df["Skill_Level"].fillna("")   + " " +
        df["Module_Title"].fillna("")
    ).str.strip()

module_texts = build_module_text(modules_df)

# ── TF-IDF + LSA (fit on modules only) ───────────────────────────────────────
tfidf_vectorizer = TfidfVectorizer(
    ngram_range=TFIDF_NGRAM, min_df=2, max_df=0.95,
    sublinear_tf=True, strip_accents="unicode",
    token_pattern=r"(?u)\b\w\w+\b",
)
M_tfidf_sparse = tfidf_vectorizer.fit_transform(module_texts)
n_comp = min(LSA_COMPONENTS, M_tfidf_sparse.shape[1] - 1)
svd    = TruncatedSVD(n_components=n_comp, random_state=42)
M_tfidf = normalize(svd.fit_transform(M_tfidf_sparse))
print("✅ TF-IDF + LSA ready")

# ── Sentence-BERT ─────────────────────────────────────────────────────────────
if USE_SBERT:
    print(f"Loading SBERT model: {SBERT_MODEL} ...")
    sbert_model = SentenceTransformer(SBERT_MODEL)
    M_sbert = sbert_model.encode(
        module_texts.tolist(), batch_size=64,
        show_progress_bar=True, convert_to_numpy=True,
        normalize_embeddings=True,
    )
    print("✅ SBERT ready")
else:
    print("ℹ️  SBERT unavailable — using TF-IDF for both slots.")
    sbert_model = None
    M_sbert = M_tfidf.copy()


# ── Helper functions ──────────────────────────────────────────────────────────
def infer_domain(objective: str):
    obj_lower = objective.lower()
    for domain, keywords in OBJECTIVE_TO_DOMAIN.items():
        if any(kw in obj_lower for kw in keywords):
            return domain
    return None


def build_customer_sentence(profile: dict) -> str:
    skill   = SKILL_PHRASES.get(profile.get("Skill_Level_Self_Assessed", ""), "with clinical experience")
    opco    = " OPCO-eligible for certified training." if profile.get("OPCO_Eligibility", "").lower() == "yes" else ""
    product = f" Product interest: {profile['Preferred_BD_Product']}." \
              if profile.get("Preferred_BD_Product", "").lower() not in ("", "unknown", "nan", "no preference") else ""
    return (
        f"{profile.get('Customer_Role', 'Professional')} specialised in "
        f"{profile.get('Specialty_Service', 'clinical care')} {skill}, "
        f"objective: {profile.get('Training_Objective', 'professional development')}. "
        f"Based at {profile.get('Establishment_Type', 'hospital')} in "
        f"{profile.get('Country', 'Europe')}, language: {profile.get('Language', 'English')}. "
        f"Prefers {profile.get('Format_Preference', 'E-learning')}, "
        f"available for {profile.get('Available_Time_Hours', 8)} hours."
        f"{opco}{product}"
    )


def mmr_rerank(scores, module_embeds, candidate_idx, top_k=TOP_K, lam=MMR_LAMBDA):
    if len(candidate_idx) <= top_k:
        return candidate_idx.tolist()
    selected  = []
    remaining = list(candidate_idx)
    while len(selected) < top_k and remaining:
        if not selected:
            best = max(remaining, key=lambda i: scores[i])
        else:
            sel_embeds = module_embeds[selected]
            best, best_val = None, -np.inf
            for idx in remaining:
                mmr_val = lam * scores[idx] - (1 - lam) * np.max(np.dot(sel_embeds, module_embeds[idx]))
                if mmr_val > best_val:
                    best, best_val = idx, mmr_val
        selected.append(best)
        remaining.remove(best)
    return selected


# ── Main recommend function (called by the dashboard) ────────────────────────
def recommend(profile: dict, top_k: int = TOP_K) -> pd.DataFrame:
    """
    Takes a profile dict from the dashboard, returns top_k recommended modules
    as a DataFrame with columns: Module_Title, Training_Type, Delivery_Format,
    Duration_Hours, Topic_Domain, Skill_Level, OPCO_Eligible, Description,
    Fusion_Score.
    """
    sentence = build_customer_sentence(profile)

    # Embed the single customer
    C_tfidf = normalize(svd.transform(tfidf_vectorizer.transform([sentence])))
    if USE_SBERT:
        C_sbert = sbert_model.encode([sentence], normalize_embeddings=True, convert_to_numpy=True)
    else:
        C_sbert = C_tfidf.copy()

    # Cosine similarity
    sim_tfidf = np.dot(C_tfidf, M_tfidf.T)[0]
    sim_sbert = np.dot(C_sbert, M_sbert.T)[0]
    scores    = W_TFIDF * sim_tfidf + W_SBERT * sim_sbert

    # Boosts
    mod_skill_num = modules_df["Skill_Level"].map(SKILL_ORDER).fillna(1).values
    cust_skill    = SKILL_ORDER.get(profile.get("Skill_Level_Self_Assessed", ""), 1)
    skill_diff    = mod_skill_num - cust_skill

    inferred_domain = infer_domain(profile.get("Training_Objective", ""))
    if inferred_domain:
        scores += BOOST_DOMAIN * (modules_df["Topic_Domain"].values == inferred_domain).astype(float)

    scores += BOOST_LANGUAGE * (modules_df["Language"].values == profile.get("Language", "")).astype(float)
    scores += BOOST_SKILL    * (((skill_diff >= 0) & (skill_diff <= 1)).astype(float))
    scores += BOOST_FORMAT   * (modules_df["Delivery_Format"].values == profile.get("Format_Preference", "")).astype(float)
    scores -= PENALTY_DURATION * (modules_df["Duration_Hours"].values > float(profile.get("Available_Time_Hours", 8))).astype(float)

    # MMR re-ranking
    candidate_idx = np.argsort(scores)[::-1][:CANDIDATE_POOL]
    top_idx       = mmr_rerank(scores, M_sbert, candidate_idx, top_k=top_k)

    results = modules_df.iloc[top_idx].copy()
    results["Fusion_Score"] = scores[top_idx].round(4)

    return results.reset_index(drop=True)
