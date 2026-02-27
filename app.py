import streamlit as st
import pickle
import re
import os

st.set_page_config(page_title="LexAI · Contract Analyzer", page_icon="⚖️", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Outfit:wght@300;400;500;600&display=swap');
:root {
    --gold:#c9a84c; --gold-light:#e8c97a; --cream:#f5f0e8;
    --dark:#0c0c0e; --dark2:#141416; --dark3:#1c1c20;
    --border:rgba(201,168,76,0.2); --muted:#6b6b7a;
}
* { font-family:'Outfit',sans-serif; box-sizing:border-box; }
.stApp { background:var(--dark); color:var(--cream); }
.stApp::before {
    content:''; position:fixed; inset:0;
    background-image:linear-gradient(rgba(201,168,76,0.03) 1px,transparent 1px),
                     linear-gradient(90deg,rgba(201,168,76,0.03) 1px,transparent 1px);
    background-size:60px 60px; pointer-events:none; z-index:0;
}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:2rem 3rem !important; position:relative; z-index:1;}

/* HERO */
.hero{text-align:center;padding:2.5rem 0 1.5rem;}
.hero-badge{display:inline-block;border:1px solid var(--border);border-radius:30px;padding:0.3rem 1.2rem;font-size:0.75rem;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);background:rgba(201,168,76,0.08);margin-bottom:1.2rem;}
.hero-title{font-family:'Playfair Display',serif;font-size:4rem;font-weight:900;margin:0 0 0.8rem;background:linear-gradient(135deg,#f5f0e8 0%,#c9a84c 50%,#f5f0e8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero-sub{color:var(--muted);font-size:1rem;font-weight:300;max-width:480px;margin:0 auto 1.5rem;line-height:1.6;}
.hero-divider{width:80px;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:0 auto 2rem;}

/* PANEL */
.panel{background:var(--dark2);border:1px solid var(--border);border-radius:20px;padding:1.8rem;position:relative;overflow:hidden;margin-bottom:1rem;}
.panel::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);}
.panel-label{font-size:0.7rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--gold);margin-bottom:1rem;display:flex;align-items:center;gap:0.5rem;}
.panel-label::after{content:'';flex:1;height:1px;background:var(--border);}

/* TEXTAREA */
.stTextArea textarea{background:var(--dark3) !important;border:1px solid var(--border) !important;border-radius:14px !important;color:var(--cream) !important;font-family:'Outfit',sans-serif !important;font-size:0.9rem !important;font-weight:300 !important;line-height:1.7 !important;padding:1.2rem !important;}
.stTextArea textarea:focus{border-color:var(--gold) !important;box-shadow:0 0 0 3px rgba(201,168,76,0.1) !important;}

/* BUTTON */
.stButton>button{background:linear-gradient(135deg,#c9a84c,#a8873a) !important;color:#0c0c0e !important;border:none !important;border-radius:12px !important;padding:0.8rem 0 !important;font-family:'Outfit',sans-serif !important;font-weight:600 !important;font-size:0.95rem !important;width:100% !important;box-shadow:0 4px 20px rgba(201,168,76,0.3) !important;transition:all 0.3s !important;}
.stButton>button:hover{transform:translateY(-2px) !important;box-shadow:0 8px 30px rgba(201,168,76,0.4) !important;}

/* STATS */
.stats-row{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.2rem;}
.stat-box{background:var(--dark3);border:1px solid var(--border);border-radius:14px;padding:1.1rem;text-align:center;position:relative;overflow:hidden;}
.stat-box::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;}
.stat-box.total::after{background:linear-gradient(90deg,#c9a84c,#e8c97a);}
.stat-box.found::after{background:linear-gradient(90deg,#22c55e,#4ade80);}
.stat-box.missing::after{background:linear-gradient(90deg,#ef4444,#f87171);}
.stat-num{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:900;line-height:1;margin-bottom:0.2rem;}
.stat-box.total .stat-num{color:var(--gold);}
.stat-box.found .stat-num{color:#4ade80;}
.stat-box.missing .stat-num{color:#f87171;}
.stat-label{font-size:0.7rem;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;color:var(--muted);}

/* RISK METER */
.risk-panel{border-radius:16px;padding:1.5rem;margin-bottom:1.2rem;position:relative;overflow:hidden;}
.risk-panel.low{background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.3);}
.risk-panel.medium{background:rgba(251,146,60,0.08);border:1px solid rgba(251,146,60,0.3);}
.risk-panel.high{background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);}
.risk-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;}
.risk-title{font-size:0.7rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--muted);}
.risk-badge{font-size:0.85rem;font-weight:700;letter-spacing:0.05em;padding:0.4rem 1.2rem;border-radius:30px;}
.risk-badge.low{background:rgba(34,197,94,0.15);color:#4ade80;border:1px solid rgba(34,197,94,0.3);}
.risk-badge.medium{background:rgba(251,146,60,0.15);color:#fb923c;border:1px solid rgba(251,146,60,0.3);}
.risk-badge.high{background:rgba(239,68,68,0.15);color:#f87171;border:1px solid rgba(239,68,68,0.3);}
.risk-score-row{display:flex;align-items:center;gap:1rem;margin-bottom:0.8rem;}
.risk-score-num{font-family:'Playfair Display',serif;font-size:3rem;font-weight:900;}
.risk-panel.low .risk-score-num{color:#4ade80;}
.risk-panel.medium .risk-score-num{color:#fb923c;}
.risk-panel.high .risk-score-num{color:#f87171;}
.risk-score-label{font-size:0.82rem;color:var(--muted);line-height:1.5;}

/* METER BAR */
.meter-track{background:rgba(255,255,255,0.05);border-radius:10px;height:8px;overflow:hidden;margin-bottom:0.5rem;}
.meter-fill{height:100%;border-radius:10px;transition:width 1s ease;}
.meter-fill.low{background:linear-gradient(90deg,#22c55e,#4ade80);}
.meter-fill.medium{background:linear-gradient(90deg,#f97316,#fb923c);}
.meter-fill.high{background:linear-gradient(90deg,#dc2626,#ef4444);}
.meter-labels{display:flex;justify-content:space-between;font-size:0.65rem;color:var(--muted);letter-spacing:0.05em;}

/* RISK CLAUSES */
.risk-clause-item{display:flex;justify-content:space-between;align-items:center;padding:0.55rem 0.9rem;border-radius:8px;margin-bottom:0.3rem;}
.risk-clause-item.high-risk{background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);}
.risk-clause-item.medium-risk{background:rgba(251,146,60,0.08);border:1px solid rgba(251,146,60,0.2);}
.risk-clause-name{font-size:0.82rem;color:var(--cream);}
.risk-tag{font-size:0.65rem;font-weight:700;padding:0.2rem 0.6rem;border-radius:20px;letter-spacing:0.05em;}
.risk-tag.high{background:rgba(239,68,68,0.15);color:#f87171;border:1px solid rgba(239,68,68,0.3);}
.risk-tag.medium{background:rgba(251,146,60,0.15);color:#fb923c;border:1px solid rgba(251,146,60,0.3);}

/* CLAUSE ITEMS */
.clause-section-title{font-size:0.68rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--muted);margin:1rem 0 0.5rem;}
.clause-item{display:flex;justify-content:space-between;align-items:center;padding:0.6rem 0.9rem;border-radius:10px;margin-bottom:0.35rem;}
.clause-item.yes{background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.18);}
.clause-item.no{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);opacity:0.45;}
.clause-name-text{font-size:0.83rem;color:var(--cream);}
.badge{font-size:0.65rem;font-weight:700;letter-spacing:0.08em;padding:0.22rem 0.65rem;border-radius:20px;}
.badge.yes{background:rgba(34,197,94,0.15);color:#4ade80;border:1px solid rgba(34,197,94,0.3);}
.badge.no{background:rgba(107,107,122,0.15);color:#6b7280;border:1px solid rgba(107,107,122,0.2);}

/* SCROLL */
.results-scroll{max-height:420px;overflow-y:auto;padding-right:4px;}
.results-scroll::-webkit-scrollbar{width:4px;}
.results-scroll::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px;}

/* EMPTY */
.empty-state{text-align:center;padding:3rem 1rem;color:var(--muted);}
.empty-icon{font-size:3rem;margin-bottom:1rem;opacity:0.3;}
.empty-text{font-size:0.88rem;font-weight:300;line-height:1.6;}

/* FOOTER */
.footer{text-align:center;padding:1.5rem 0 1rem;color:var(--muted);font-size:0.75rem;letter-spacing:0.05em;border-top:1px solid var(--border);margin-top:2rem;}
.footer span{color:var(--gold);}
</style>
""", unsafe_allow_html=True)


# ── Load Model ──
@st.cache_resource
def load_model():
    model       = pickle.load(open(os.path.join(BASE_DIR, 'model.pkl'), 'rb'))
    tfidf       = pickle.load(open(os.path.join(BASE_DIR, 'tfidf.pkl'), 'rb'))
    binary_cols = pickle.load(open(os.path.join(BASE_DIR, 'binary_cols.pkl'), 'rb'))
    return model, tfidf, binary_cols

model, tfidf, binary_cols = load_model()

# ── Risk Config ──
HIGH_RISK_CLAUSES = [
    'Cap On Liability-Answer',
    'Anti-Assignment-Answer',
    'Termination For Convenience-Answer',
    'Governing Law-Answer',
    'License Grant-Answer',
    'Uncapped Liability-Answer',
]
MEDIUM_RISK_CLAUSES = [
    'Audit Rights-Answer',
    'Non-Compete-Answer',
    'Insurance-Answer',
    'Exclusivity-Answer',
    'Change Of Control-Answer',
    'Ip Ownership Assignment-Answer',
]

def compute_risk(results):
    score = 0
    risky_missing = []
    for clause, val in results.items():
        if val == 0:
            if clause in HIGH_RISK_CLAUSES:
                score += 3
                risky_missing.append((clause.replace('-Answer',''), 'high'))
            elif clause in MEDIUM_RISK_CLAUSES:
                score += 1
                risky_missing.append((clause.replace('-Answer',''), 'medium'))

    high_missing = sum(1 for c in HIGH_RISK_CLAUSES if results.get(c, 0) == 0)
    medium_missing = sum(1 for c in MEDIUM_RISK_CLAUSES if results.get(c, 0) == 0)

    if high_missing <= 3:
        level = 'low'
    elif high_missing <= 5:
        level = 'medium'
    else:
        level = 'high'
    return score, level, risky_missing

def clean_text(text):
    if not text or text.strip() == '': return ''
    text = str(text)
    text = re.sub(r"[\[\]']", '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower()
    return re.sub(r'\s+', ' ', text).strip()


# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚖️ &nbsp; AI-Powered Legal Intelligence</div>
    <div class="hero-title">LexAI</div>
    <div class="hero-sub">Paste any contract and instantly detect clauses + assess legal risk</div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.1, 1], gap="large")

with left:
    st.markdown('<div class="panel"><div class="panel-label">📋 &nbsp; Contract Input</div>', unsafe_allow_html=True)
    contract_text = st.text_area(
        label="contract",
        placeholder="Paste your contract text here...\n\nThis Agreement is entered into between Company A and Company B. The licensor hereby grants a non-exclusive license...",
        height=360,
        label_visibility="collapsed"
    )
    analyze = st.button("⚖️  Analyze Contract & Assess Risk")
    st.markdown("""</div>
    <div style="margin-top:0.8rem;padding:0.9rem 1rem;background:rgba(201,168,76,0.05);border:1px solid rgba(201,168,76,0.1);border-radius:10px;">
        <div style="font-size:0.72rem;color:#6b6b7a;line-height:1.8;">
            🔍 &nbsp;Detects <strong style="color:#c9a84c;">33 clause types</strong> &nbsp;·&nbsp;
            🛡️ &nbsp;Risk scoring &nbsp;·&nbsp;
            ⚡ &nbsp;Instant analysis
        </div>
    </div>""", unsafe_allow_html=True)

with right:
    if analyze and contract_text.strip():
        cleaned    = clean_text(contract_text)
        X_input    = tfidf.transform([cleaned])
        prediction = model.predict(X_input)[0]

        results      = dict(zip(binary_cols, prediction))
        detected     = {k: v for k, v in results.items() if v == 1}
        not_detected = {k: v for k, v in results.items() if v == 0}
        total, found, missing = len(results), len(detected), len(not_detected)

        # Stats
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-box total"><div class="stat-num">{total}</div><div class="stat-label">Checked</div></div>
            <div class="stat-box found"><div class="stat-num">{found}</div><div class="stat-label">Detected</div></div>
            <div class="stat-box missing"><div class="stat-num">{missing}</div><div class="stat-label">Missing</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Risk Score
        score, level, risky_missing = compute_risk(results)
        max_score = len(HIGH_RISK_CLAUSES) * 3 + len(MEDIUM_RISK_CLAUSES)
        pct = min(int((score / max_score) * 100), 100)

        emoji = "✅" if level == "low" else "⚠️" if level == "medium" else "🔴"
        label_text = "LOW RISK" if level == "low" else "MEDIUM RISK" if level == "medium" else "HIGH RISK"
        desc = "Contract looks safe. Key clauses are present." if level == "low" \
               else "Some important clauses are missing. Review recommended." if level == "medium" \
               else "Critical clauses are missing! Legal review strongly advised."

        risky_html = ""
        if risky_missing:
            risky_html = '<div style="margin-top:0.8rem;"><div style="font-size:0.68rem;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;color:#6b6b7a;margin-bottom:0.5rem;">⚠️ &nbsp; Missing Risk Clauses</div>'
            for name, risk in risky_missing:
                risky_html += f'<div class="risk-clause-item {risk}-risk"><span class="risk-clause-name">{name}</span><span class="risk-tag {risk}">{"HIGH RISK" if risk == "high" else "MEDIUM RISK"}</span></div>'
            risky_html += '</div>'

        st.markdown(f"""
        <div class="risk-panel {level}">
            <div class="risk-header">
                <span class="risk-title">🛡️ &nbsp; Contract Risk Assessment</span>
                <span class="risk-badge {level}">{emoji} &nbsp; {label_text}</span>
            </div>
            <div class="risk-score-row">
                <div class="risk-score-num">{score}</div>
                <div class="risk-score-label">Risk Score<br><span style="font-size:0.75rem;">out of {max_score} max points</span></div>
            </div>
            <div class="meter-track"><div class="meter-fill {level}" style="width:{pct}%"></div></div>
            <div class="meter-labels"><span>Safe</span><span>Moderate</span><span>Danger</span></div>
            <div style="margin-top:0.8rem;font-size:0.82rem;color:#9ca3af;">{desc}</div>
            {risky_html}
        </div>
        """, unsafe_allow_html=True)

        # Clause Results
        detected_html = '<div class="clause-section-title">✅ &nbsp; Present Clauses</div>'
        for clause in detected:
            name = clause.replace('-Answer', '')
            detected_html += f'<div class="clause-item yes"><span class="clause-name-text">{name}</span><span class="badge yes">PRESENT</span></div>'

        not_detected_html = '<div class="clause-section-title">❌ &nbsp; Absent Clauses</div>'
        for clause in not_detected:
            name = clause.replace('-Answer', '')
            not_detected_html += f'<div class="clause-item no"><span class="clause-name-text">{name}</span><span class="badge no">ABSENT</span></div>'

        st.markdown(f"""
        <div class="panel">
            <div class="panel-label">📊 &nbsp; Clause Breakdown</div>
            <div class="results-scroll">{detected_html}{not_detected_html}</div>
        </div>
        """, unsafe_allow_html=True)

    elif analyze and not contract_text.strip():
        st.warning("⚠️ Please paste some contract text first!")
    else:
        st.markdown("""
        <div class="panel">
            <div class="panel-label">📊 &nbsp; Analysis Results</div>
            <div class="empty-state">
                <div class="empty-icon">⚖️</div>
                <div class="empty-text">Paste your contract text on the left<br>and click <strong style="color:#c9a84c;">Analyze</strong> to detect clauses and assess risk</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Built with <span>♥</span> using Streamlit &nbsp;·&nbsp;
    <span>Master Clauses Dataset</span> &nbsp;·&nbsp;
    Multi-Label Classification &nbsp;·&nbsp;
    <span>LexAI v2.0</span>
</div>
""", unsafe_allow_html=True)
