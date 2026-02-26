"""
CURSUS - BD Training Dashboard (v4)
Changes vs v3:
  - New BD logo
  - Skill level: horizontal checkboxes (same style as format checkboxes)
Run: streamlit run cursus_dashboard_v4.py
"""
import streamlit as st
import pandas as pd
from model import recommend

st.set_page_config(
    page_title="CURSUS – BD Training",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BD_LOGO_B64 = "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"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --navy:    #1B3F6E;
    --orange:  #E8521A;
    --blue:    #2E5FAC;
    --pale:    #EEF3FA;
    --white:   #FFFFFF;
    --bg:      #F0F2F5;
    --border:  #D4DCE8;
    --text:    #1A2B3C;
    --muted:   #6B7C93;
    --radius:  12px;
    --shadow:  0 2px 16px rgba(27,63,110,0.10);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1100px !important; }

/* ── NAVBAR ── */
.navbar {
    background: var(--navy);
    padding: 0 36px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 32px;
}
.navbar-left { display: flex; align-items: center; gap: 14px; }
.navbar-logo { height: 28px; }
.navbar-divider { width: 1px; height: 28px; background: rgba(255,255,255,0.3); }
.navbar-brand { color: var(--white); font-size: 18px; font-weight: 700; letter-spacing: 3px; }
.navbar-right { display: flex; gap: 28px; }
.nav-link { color: rgba(255,255,255,0.6); font-size: 14px; font-weight: 500; text-decoration: none; padding-bottom: 2px; }
.nav-link.active { color: var(--white); border-bottom: 2px solid var(--white); }

/* ── HERO BANNERS ── */
.hero-orange {
    background: linear-gradient(130deg, var(--orange) 0%, #C0401A 100%);
    border-radius: var(--radius);
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-blue {
    background: linear-gradient(130deg, var(--blue) 0%, var(--navy) 100%);
    border-radius: var(--radius);
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-orange::after, .hero-blue::after {
    content: '';
    position: absolute;
    right: -60px; top: -60px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.hero-eyebrow {
    color: rgba(255,255,255,0.75);
    font-size: 11px; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    margin-bottom: 8px;
}
.hero-title { color: var(--white); font-size: 28px; font-weight: 700; margin-bottom: 8px; }
.hero-subtitle { color: rgba(255,255,255,0.80); font-size: 15px; line-height: 1.5; max-width: 600px; }

/* ── PROFILE TAGS ── */
.profile-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
.profile-tag {
    background: rgba(255,255,255,0.15); color: var(--white);
    border-radius: 20px; padding: 5px 14px;
    font-size: 13px; font-weight: 500;
}

/* ── STATS ── */
.stats-row { display: flex; gap: 12px; margin-top: 20px; }
.stat-box { background: rgba(255,255,255,0.12); border-radius: 10px; padding: 14px 24px; text-align: center; min-width: 90px; }
.stat-num { color: var(--white); font-size: 26px; font-weight: 700; line-height: 1; }
.stat-lbl { color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 4px; }

/* ── SECTION CARD ── */
.section-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 20px 28px;
    margin-bottom: 20px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
}
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 16px; padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.section-icon {
    width: 30px; height: 30px; background: var(--pale);
    border-radius: 7px; display: flex; align-items: center;
    justify-content: center; font-size: 15px; flex-shrink: 0;
}
.section-title { font-size: 15px; font-weight: 700; color: var(--text); }

/* ── ALL BUTTONS default (skill + submit + back) ── */
.stButton > button {
    background: var(--white) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    width: 100% !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover { border-color: var(--orange) !important; color: var(--orange) !important; }

/* Submit / back — navy override */
.submit-btn > div > button, .submit-btn button,
.back-btn > div > button,   .back-btn button {
    background: var(--navy) !important;
    border-color: var(--navy) !important;
    color: var(--white) !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}
.submit-btn > div > button:hover, .back-btn > div > button:hover {
    background: var(--blue) !important; border-color: var(--blue) !important;
}

/* ── STREAMLIT WIDGET OVERRIDES ── */
.stSelectbox > div > div {
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    background: var(--white) !important;
}
.stTextArea > div > div > textarea {
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
}

/* Checkbox styling — make them look consistent */
.stCheckbox { margin-bottom: 4px !important; }
.stCheckbox label {
    font-size: 14px !important;
    font-weight: 400 !important;
    letter-spacing: 0px !important;
    text-transform: none !important;
    color: var(--text) !important;
}
.stCheckbox > label > div[data-testid="stMarkdownContainer"] p {
    font-size: 14px !important;
}

label {
    font-size: 11px !important; font-weight: 600 !important;
    letter-spacing: 0.5px !important; text-transform: uppercase !important;
    color: var(--muted) !important;
}
div[data-testid="stForm"] { border: none !important; padding: 0 !important; }

/* ── MODULE CARDS ── */
.type-group-header {
    display: flex; align-items: center; gap: 12px;
    padding: 16px 0 12px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 14px;
}
.type-icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
.type-label { font-size: 16px; font-weight: 700; color: var(--text); }
.type-count { background: var(--pale); color: var(--navy); border-radius: 12px; padding: 2px 10px; font-size: 12px; font-weight: 700; }

.module-card {
    background: var(--white); border-radius: var(--radius);
    padding: 20px 22px; margin-bottom: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 6px rgba(27,63,110,0.06);
}
.module-type-badge {
    display: inline-block; padding: 3px 10px; border-radius: 4px;
    font-size: 10px; font-weight: 700; letter-spacing: 0.5px;
    text-transform: uppercase; margin-bottom: 8px;
}
.badge-qualiopi { background:#FFF3CD; color:#7A5C00; }
.badge-bdla     { background:#CCE5FF; color:#003A7A; }
.badge-product  { background:#D4EDDA; color:#155724; }
.badge-premium  { background:#F8D7DA; color:#721C24; }
.badge-external { background:#E2D9F3; color:#432874; }

.module-title { font-size: 15px; font-weight: 700; color: var(--text); margin-bottom: 6px; }
.module-desc  { font-size: 13px; color: var(--muted); margin-bottom: 12px; line-height: 1.5; }
.meta-pill {
    display: inline-flex; align-items: center; gap: 4px;
    background: var(--pale); border-radius: 12px;
    padding: 3px 10px; font-size: 12px; color: var(--navy);
    margin-right: 4px;
}
.match-badge {
    background: var(--navy); color: var(--white);
    border-radius: 14px; padding: 3px 10px;
    font-size: 11px; font-weight: 700; float: right;
}
.enroll-btn-html {
    display: block; background: var(--navy);
    color: var(--white) !important; text-align: center;
    padding: 10px; border-radius: 8px;
    font-size: 13px; font-weight: 600;
    text-decoration: none; margin-top: 8px;
}
.results-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.results-label { font-size: 14px; color: var(--muted); }
.results-label strong { color: var(--text); }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        return pd.read_csv("C:\\Users\\ingeb\\OneDrive\\Documenten\\Grenoble Ecole de Management\\MDAI\\Capstone Project\\BD_Dataset2_HCP_Profiles_v3_dashboard (1).csv")
    except FileNotFoundError:
        return pd.DataFrame({
            "Customer_Role": ["Nurse","Physician","Pharmacist","ICU Specialist","Nurse Practitioner","System Manager"],
            "Specialty_Service": ["Oncologie","Cardiology","Pharmacie Hospitalière","Pediatrics","Gastroenterology","Operating Theatre"],
            "Establishment_Type": ["CHU","Private Hospital","Academic Medical Center","CH","Centro de Salud","Community Trust"],
            "Country": ["France","Germany","United Kingdom","Italy","Spain","United Kingdom"],
            "Language": ["Français (fr)","Deutsch (de)","English (United Kingdom)","Italiano (it)","Español (es)","English (United Kingdom)"],
            "Years_Experience": [5,12,8,20,3,8],
            "Skill_Level_Self_Assessed": ["Beginner","Advanced","Intermediate","Expert","Beginner","Advanced"],
            "Format_Preference": ["E-learning","Blended","Webinar","Masterclass","Webinar","Blended"],
            "Available_Time_Hours": [4,8,16,2,24,40],
            "Preferred_BD_Product": ["BD PICCline","BD Alaris™","BD Rowa™","BD Insyte™","BD A-Line™","BD Bair Hugger™"],
        })

df = load_data()

MODULES = [
    {"id":"M001","title":"Safe IV Access – Fundamentals",
     "type":"Product Training","format":"E-learning","duration_h":2,
     "skill_level":["Beginner","Intermediate"],
     "target_roles":["Nurse","ICU Specialist","Nurse Practitioner"],
     "products":["BD PICCline","BD Nexiva™","BD Insyte™"],
     "description":"Core principles of peripheral venous catheter insertion and maintenance protocols.","opco":True},
    {"id":"M002","title":"PICC Line Advanced Insertion Techniques",
     "type":"Premium Programs","format":"Masterclass","duration_h":4,
     "skill_level":["Advanced","Expert"],
     "target_roles":["Nurse","Nurse Practitioner","Physician"],
     "products":["BD PICCline","BD Midline"],
     "description":"KOL-led on-site masterclass covering ultrasound-guided PICC insertion.","opco":True},
    {"id":"M003","title":"Medication Safety & Infusion Management",
     "type":"Qualiopi-Certified","format":"Blended","duration_h":8,
     "skill_level":["Intermediate","Advanced"],
     "target_roles":["Pharmacist","Clinical Pharmacist","Pharmacy Manager"],
     "products":["BD Alaris™","BD BodyGuard T"],
     "description":"Qualiopi-certified programme on safe medication management and infusion pump use.","opco":True},
    {"id":"M004","title":"Hospital Dispensing Automation – Getting Started",
     "type":"BD Learning Academy","format":"E-learning","duration_h":2,
     "skill_level":["Beginner","Intermediate"],
     "target_roles":["Pharmacist","Pharmacy Manager","System Manager"],
     "products":["BD Rowa™","Pyxis ES"],
     "description":"Self-paced BDLA module introducing automated dispensing cabinet workflows.","opco":False},
    {"id":"M005","title":"Infection Prevention in Critical Care",
     "type":"External Partners","format":"Webinar","duration_h":2,
     "skill_level":["Beginner","Intermediate","Advanced"],
     "target_roles":["ICU Specialist","Nurse","Physician"],
     "products":["BD PICCline","BD Foley","BD Provena™"],
     "description":"Expert-led webinar on CRBSI and CAUTI prevention protocols.","opco":False},
    {"id":"M006","title":"Foley Catheter – Clinical Best Practices",
     "type":"Product Training","format":"On-site","duration_h":3,
     "skill_level":["Beginner","Intermediate"],
     "target_roles":["Nurse","Nurse Practitioner"],
     "products":["BD Foley"],
     "description":"On-site hands-on training for urinary catheter insertion and care bundle.","opco":False},
    {"id":"M007","title":"BD Alaris™ System Administration",
     "type":"BD Learning Academy","format":"E-learning","duration_h":4,
     "skill_level":["Advanced","Expert"],
     "target_roles":["System Manager","Biomedical Engineer"],
     "products":["BD Alaris™"],
     "description":"Technical BDLA module on configuring and maintaining the BD Alaris™ system.","opco":False},
    {"id":"M008","title":"Vascular Access – From Basics to Complex Cases",
     "type":"Qualiopi-Certified","format":"Blended","duration_h":16,
     "skill_level":["Intermediate","Advanced","Expert"],
     "target_roles":["Physician","ICU Specialist","Nurse Practitioner"],
     "products":["BD PICCline","BD A-Line™","BD Nexiva™"],
     "description":"Comprehensive Qualiopi-certified pathway covering all vascular access device types.","opco":True},
    {"id":"M009","title":"BD Learning Academy – Urinary Catheter Best Practices",
     "type":"BD Learning Academy","format":"E-learning","duration_h":3,
     "skill_level":["Beginner","Intermediate","Advanced"],
     "target_roles":["Nurse","Nurse Practitioner","Physician"],
     "products":["BD Foley"],
     "description":"Evidence-based training on catheter insertion, care bundles, and CAUTI prevention using BD Foley systems.","opco":False},
]

TYPE_ORDER   = ["Qualiopi","BDLA","Product Training","Premium","External"]
TYPE_ICONS   = {"Qualiopi":"🏅","BDLA":"📘","Product Training":"🔧","Premium":"⭐","External":"🤝"}
TYPE_ICON_BG = {"Qualiopi":"#FFF3CD","BDLA":"#CCE5FF","Product Training":"#D4EDDA","Premium":"#F8D7DA","External":"#E2D9F3"}
BADGE_CLASS  = {"Qualiopi":"badge-qualiopi","BDLA":"badge-bdla","Product Training":"badge-product","Premium":"badge-premium","External":"badge-external"}

FORMAT_OPTIONS = ["E-learning","Blended","Masterclass","On-site","Webinar","No Preference"]
SKILL_OPTIONS  = ["Beginner","Intermediate","Advanced","Expert"]
TIME_OPTIONS   = [2,4,8,16,24,40]


def filter_modules(role, skill, formats, product, available_hours):
    results = []
    for m in MODULES:
        if role and role not in m["target_roles"]: continue
        if skill and skill not in m["skill_level"]: continue
        if formats and "No Preference" not in formats:
            if m["format"] not in formats: continue
        if product and product != "No preference":
            if product not in m["products"]: continue
        if available_hours and m["duration_h"] > available_hours: continue
        results.append(m)
    return results


if "page"             not in st.session_state: st.session_state.page = "profile"
if "profile_data"     not in st.session_state: st.session_state.profile_data = {}
if "selected_formats" not in st.session_state: st.session_state.selected_formats = []
if "selected_skill"   not in st.session_state: st.session_state.selected_skill = None


# ── NAVBAR ───────────────────────────────────────────────────────────────────
page = st.session_state.page
profile_active    = "active" if page == "profile"    else ""
curriculum_active = "active" if page == "curriculum" else ""

st.markdown(f"""
<div class="navbar">
  <div class="navbar-left">
    <img class="navbar-logo" src="data:image/png;base64,{BD_LOGO_B64}" alt="BD">
    <div class="navbar-divider"></div>
    <span class="navbar-brand">CURSUS</span>
  </div>
  <div class="navbar-right">
    <span class="nav-link {profile_active}">My Profile</span>
    <span class="nav-link {curriculum_active}">My Curriculum</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — PROFILE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "profile":

    st.markdown("""
    <div class="hero-orange">
      <div class="hero-eyebrow">✦ PERSONALIZED LEARNING</div>
      <div class="hero-title">Build Your Training Profile</div>
      <div class="hero-subtitle">
        Your profile, your pathway — let CURSUS match you with the right BD training in seconds.
      </div>
    </div>
    """, unsafe_allow_html=True)

    roles       = sorted(df["Customer_Role"].dropna().unique().tolist())
    specialties = sorted(df["Specialty_Service"].dropna().unique().tolist())
    countries   = sorted(df["Country"].dropna().unique().tolist())
    languages   = sorted(df["Language"].dropna().unique().tolist())
    products    = ["No preference"] + sorted(df["Preferred_BD_Product"].dropna().unique().tolist())

    # ── Professional Identity ─────────────────────────────────────────────────
    st.markdown("""
    <div class="section-card">
      <div class="section-header">
        <div class="section-icon">👤</div>
        <div class="section-title">Professional Identity</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<label>ROLE *</label>", unsafe_allow_html=True)
        role = st.selectbox("role_hidden", ["Select your role"] + roles, label_visibility="collapsed")
        st.markdown("<label>COUNTRY</label>", unsafe_allow_html=True)
        country = st.selectbox("country_hidden", ["Select country"] + countries, label_visibility="collapsed")
    with col2:
        st.markdown("<label>SPECIALTY / SERVICE</label>", unsafe_allow_html=True)
        specialty = st.selectbox("spec_hidden", ["Select your specialty"] + specialties, label_visibility="collapsed")
        st.markdown("<label>LANGUAGE</label>", unsafe_allow_html=True)
        language = st.selectbox("lang_hidden", ["Select language"] + languages, label_visibility="collapsed")

    # ── Training Preferences ──────────────────────────────────────────────────
    st.markdown("""
    <div class="section-card">
      <div class="section-header">
        <div class="section-icon">📚</div>
        <div class="section-title">Training Preferences</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

        # Skill level — horizontal radio (single select)
    st.markdown("<label>SKILL LEVEL *</label>", unsafe_allow_html=True)
    selected_skill = st.radio(
        "skill_hidden",
        SKILL_OPTIONS,
        index=SKILL_OPTIONS.index(st.session_state.selected_skill) if st.session_state.selected_skill in SKILL_OPTIONS else 0,
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.selected_skill = selected_skill

    st.markdown("<br>", unsafe_allow_html=True)

    pref_col2, pref_col3 = st.columns([1.4, 1.4], gap="large")

    # Format multi-select
    with pref_col2:
        st.markdown("<label>PREFERRED FORMAT * (multi-select)</label>", unsafe_allow_html=True)
        for fmt in FORMAT_OPTIONS:
            checked = fmt in st.session_state.selected_formats
            val = st.checkbox(fmt, value=checked, key=f"fmt_{fmt}")
            if val and fmt not in st.session_state.selected_formats:
                if fmt == "No Preference":
                    st.session_state.selected_formats = ["No Preference"]
                else:
                    if "No Preference" in st.session_state.selected_formats:
                        st.session_state.selected_formats = [fmt]
                    else:
                        st.session_state.selected_formats.append(fmt)
                st.rerun()
            elif not val and fmt in st.session_state.selected_formats:
                st.session_state.selected_formats.remove(fmt)
                st.rerun()

    # Available time radio
    with pref_col3:
        st.markdown("<label>AVAILABLE TIME *</label>", unsafe_allow_html=True)
        time_labels = [f"⏱ {t} hours" for t in TIME_OPTIONS]
        selected_time_label = st.radio("time_hidden", time_labels, index=1, label_visibility="collapsed")
        selected_time = TIME_OPTIONS[time_labels.index(selected_time_label)]

    # ── Product & Learning Goal ───────────────────────────────────────────────
    st.markdown("""
    <div class="section-card">
      <div class="section-header">
        <div class="section-icon">📦</div>
        <div class="section-title">Product &amp; Learning Goal</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    prod_col, obj_col = st.columns(2, gap="large")
    with prod_col:
        st.markdown("<label>PREFERRED BD PRODUCT (OPTIONAL)</label>", unsafe_allow_html=True)
        product = st.selectbox("prod_hidden", products, label_visibility="collapsed")
    with obj_col:
        st.markdown("<label>TRAINING OBJECTIVE</label>", unsafe_allow_html=True)
        objective = st.text_area("obj_hidden",
            placeholder="e.g. Reduce CRBSI rates in my ICU, onboard new nurses to IV therapy...",
            height=90, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([2,1,2])
    with btn_col:
        st.markdown('<div class="submit-btn">', unsafe_allow_html=True)
        if st.button("Generate My Curriculum →", use_container_width=True):
            if role == "Select your role" or st.session_state.selected_skill is None:
                st.error("Please select at least your Role and Skill Level.")
            else:
                st.session_state.profile_data = {
                    "role": role, "specialty": specialty,
                    "skill": st.session_state.selected_skill,
                    "country": country, "language": language,
                    "product": product, "hours": selected_time,
                    "formats": list(st.session_state.selected_formats),
                    "objective": objective,
                }
                st.session_state.page = "curriculum"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — CURRICULUM
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "curriculum":

    p = st.session_state.profile_data

    # ── Call your real model ──────────────────────────────────────────────────
    model_profile = {
        "Customer_Role":             p["role"],
        "Specialty_Service":         p.get("specialty", ""),
        "Skill_Level_Self_Assessed": p["skill"],
        "Format_Preference":         p["formats"][0] if p["formats"] and "No Preference" not in p["formats"] else "",
        "Available_Time_Hours":      p["hours"],
        "Country":                   p.get("country", ""),
        "Language":                  p.get("language", ""),
        "Preferred_BD_Product":      p.get("product", ""),
        "Training_Objective":        p.get("objective", ""),
        "OPCO_Eligibility":          "No",
        "Establishment_Type":        "",
    }
    matched_df = recommend(model_profile, top_k=5)
    match_h = int(matched_df["Duration_Hours"].sum())

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Edit Profile"):
        st.session_state.page = "profile"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    fmt_display = ", ".join(p["formats"]) if p["formats"] else "Any format"
    product_tag = f'<span class="profile-tag">📦 {p["product"]}</span>' if p["product"] != "No preference" else ""

    st.markdown(f"""
    <div class="hero-blue">
      <div class="hero-eyebrow">✦ YOUR PERSONALIZED PATHWAY</div>
      <div class="hero-title">Training Curriculum</div>
      <div class="profile-tags">
        <span class="profile-tag">👤 {p["role"]}</span>
        <span class="profile-tag">📋 {fmt_display}</span>
        <span class="profile-tag">⏱ {p["hours"]}h available</span>
        {product_tag}
      </div>
      <div class="stats-row">
        <div class="stat-box"><div class="stat-num">{len(matched_df)}</div><div class="stat-lbl">Matched</div></div>
        <div class="stat-box"><div class="stat-num">{match_h}h</div><div class="stat-lbl">Learning</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if matched_df.empty:
        st.info("No modules matched your profile. Try broadening your preferences.")
    else:
        st.markdown(f"""
        <div class="results-bar">
          <span class="results-label">Showing <strong>{len(matched_df)} module(s)</strong> — best matches for your profile</span>
        </div>
        """, unsafe_allow_html=True)

        for mtype in TYPE_ORDER:
            group = matched_df[matched_df["Training_Type"] == mtype]
            if group.empty:
                continue
            icon    = TYPE_ICONS.get(mtype, "📋")
            icon_bg = TYPE_ICON_BG.get(mtype, "#EEF3FA")
            badge_cls = BADGE_CLASS.get(mtype, "badge-product")

            st.markdown(f"""
            <div class="type-group-header">
              <div class="type-icon" style="background:{icon_bg};">{icon}</div>
              <span class="type-label">{mtype}</span>
              <span class="type-count">{len(group)}</span>
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(min(len(group), 2), gap="medium")
            for i, (_, m) in enumerate(group.iterrows()):
                with cols[i % 2]:
                    opco_html = '<span class="meta-pill">✅ OPCO</span>' if str(m.get("OPCO_Eligible","")).lower() == "yes" else ""
                    score_pct = int(float(m.get("Fusion_Score", 0)) * 100)
                    desc = str(m.get("Description", ""))[:150] + "…"
                    st.markdown(f"""
                    <div class="module-card">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <span class="module-type-badge {badge_cls}">{mtype.upper()}</span>
                        <span class="match-badge">⭐ {score_pct}% match</span>
                      </div>
                      <div class="module-title">{m.get("Module_Title","")}</div>
                      <div class="module-desc">{desc}</div>
                      <div style="margin-bottom:10px;">
                        <span class="meta-pill">📋 {m.get("Delivery_Format","")}</span>
                        <span class="meta-pill">⏱ {m.get("Duration_Hours","")}h</span>
                        <span class="meta-pill">🎯 {m.get("Topic_Domain","")}</span>
                        {opco_html}
                      </div>
                      <a class="enroll-btn-html" href="#" onclick="return false;">📖 Enroll Now</a>
                    </div>
                    """, unsafe_allow_html=True)

    if p.get("objective"):
        st.markdown(f"""
        <div class="section-card" style="margin-top:24px;border-left:4px solid var(--orange);">
          <div class="section-header">
            <div class="section-icon">🎯</div>
            <div class="section-title">Your Training Objective</div>
          </div>
          <p style="font-size:15px;font-style:italic;color:var(--muted);margin:0;">"{p["objective"]}"</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Edit Profile", key= "back_btn_top"):
        st.session_state.page = "profile"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # fmt_display = ", ".join(p["formats"]) if p["formats"] else "Any format"
    # product_tag = f'''<span class="profile-tag">📦 {p["product"]}</span>''' if p["product"] != "No preference" else ""

    # st.markdown(f"""
    # <div class="hero-blue">
    #   <div class="hero-eyebrow">✦ YOUR PERSONALIZED PATHWAY</div>
    #   <div class="hero-title">Training Curriculum</div>
    #   <div class="profile-tags">
    #     <span class="profile-tag">👤 {p["role"]}</span>
    #     <span class="profile-tag">📋 {fmt_display}</span>
    #     <span class="profile-tag">⏱ {p["hours"]}h available</span>
    #     {product_tag}
    #   </div>
    #   <div class="stats-row">
    #     <div class="stat-box"><div class="stat-num">{len(matched_df)}</div><div class="stat-lbl">Matched</div></div>
    #     <div class="stat-box"><div class="stat-num">{len(MODULES)}</div><div class="stat-lbl">Total</div></div>
    #     <div class="stat-box"><div class="stat-num">{match_h}h</div><div class="stat-lbl">Learning</div></div>
    #   </div>
    # </div>
    # """, unsafe_allow_html=True)

    # if matched_df.empty:
    #     st.info("No modules matched your exact profile. Try broadening your format preferences or available time.")
    # else:
    #     st.markdown(f"""
    #     <div class="results-bar">
    #       <span class="results-label">Showing <strong>{len(matched_df)} module(s)</strong> — best matches for your profile</span>
    #     </div>
    #     """, unsafe_allow_html=True)

    #     for mtype in TYPE_ORDER:
    #         group = [m for m in matched_df if m["type"] == mtype]
    #         if not group: continue
    #         icon    = TYPE_ICONS[mtype]
    #         icon_bg = TYPE_ICON_BG[mtype]
    #         st.markdown(f"""
    #         <div class="type-group-header">
    #           <div class="type-icon" style="background:{icon_bg};">{icon}</div>
    #           <span class="type-label">{mtype}</span>
    #           <span class="type-count">{len(group)}</span>
    #         </div>
    #         """, unsafe_allow_html=True)

    #         cols = st.columns(min(len(group), 2), gap="medium")
    #         for i, m in enumerate(group):
    #             with cols[i % 2]:
    #                 badge_cls  = BADGE_CLASS[m["type"]]
    #                 opco_html  = '<span class="meta-pill">✅ OPCO</span>' if m["opco"] else ""
    #                 prods_html = " ".join(f'<span class="meta-pill">📦 {p_}</span>' for p_ in m["products"][:2])
    #                 st.markdown(f"""
    #                 <div class="module-card">
    #                   <div style="display:flex;justify-content:space-between;align-items:flex-start;">
    #                     <span class="module-type-badge {badge_cls}">{m["type"].upper()}</span>
    #                     <span class="match-badge">⭐ Match</span>
    #                   </div>
    #                   <div class="module-title">{m["title"]}</div>
    #                   <div class="module-desc">{m["description"]}</div>
    #                   <div style="margin-bottom:10px;">{prods_html} <span class="meta-pill">📋 {m["format"]}</span> <span class="meta-pill">⏱ {m["duration_h"]}h</span> {opco_html}</div>
    #                   <a class="enroll-btn-html" href="#" onclick="return false;">📖 Enroll Now</a>
    #                 </div>
    #                 """, unsafe_allow_html=True)

    # if p.get("objective"):
    #     st.markdown(f"""
    #     <div class="section-card" style="margin-top:24px;border-left:4px solid var(--orange);">
    #       <div class="section-header">
    #         <div class="section-icon">🎯</div>
    #         <div class="section-title">Your Training Objective</div>
    #       </div>
    #       <p style="font-size:15px;font-style:italic;color:var(--muted);margin:0;">"{p["objective"]}"</p>
    #     </div>
    #     """, unsafe_allow_html=True)