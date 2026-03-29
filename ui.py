import streamlit as st
import time
from api import predict_spam
# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SpamShield · Message Detector",
    page_icon="🛡️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #0d0f14;
    --surface:   #13161e;
    --border:    #1f2535;
    --accent:    #4fffb0;
    --danger:    #ff4f6d;
    --muted:     #4a5068;
    --text:      #e8ecf5;
    --subtext:   #8891aa;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* ── Main container ── */
.block-container {
    max-width: 680px !important;
    padding: 3rem 2rem 4rem !important;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    margin-bottom: 2.5rem;
}
.hero-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: 2px;
    padding: 4px 12px;
    margin-bottom: 1.2rem;
    opacity: 0.85;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.15;
    color: var(--text);
    margin: 0 0 0.6rem;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    font-size: 0.95rem;
    color: var(--subtext);
    font-weight: 300;
    margin: 0;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 0 0 2rem;
}

/* ── Textarea override ── */
textarea {
    background-color: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    resize: vertical !important;
    transition: border-color 0.2s !important;
}
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,255,176,0.08) !important;
    outline: none !important;
}
label[data-testid="stWidgetLabel"] p {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--subtext) !important;
}

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: var(--accent) !important;
    color: #0d0f14 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.15s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    opacity: 1 !important;
}

/* ── Result cards ── */
.result-card {
    margin-top: 2rem;
    border-radius: 8px;
    padding: 1.6rem 1.8rem;
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    animation: slideUp 0.35s ease both;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-card.ham {
    background: rgba(79,255,176,0.07);
    border: 1px solid rgba(79,255,176,0.25);
}
.result-card.spam {
    background: rgba(255,79,109,0.07);
    border: 1px solid rgba(255,79,109,0.25);
}
.result-icon {
    font-size: 2rem;
    line-height: 1;
    flex-shrink: 0;
}
.result-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.result-card.ham  .result-label { color: var(--accent); }
.result-card.spam .result-label { color: var(--danger); }
.result-verdict {
    font-size: 1.35rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.3rem;
    line-height: 1.2;
}
.result-desc {
    font-size: 0.86rem;
    color: var(--subtext);
    line-height: 1.55;
}

/* ── Char counter ── */
.char-counter {
    text-align: right;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 0.3rem;
    margin-bottom: 1rem;
}

/* ── History section ── */
.history-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 2.5rem 0 1rem;
}
.history-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.7rem 1rem;
    border-radius: 6px;
    background: var(--surface);
    border: 1px solid var(--border);
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
    color: var(--subtext);
}
.history-row .badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 2px;
    flex-shrink: 0;
}
.badge.ham-badge  { background: rgba(79,255,176,0.15); color: var(--accent); }
.badge.spam-badge { background: rgba(255,79,109,0.15); color: var(--danger); }
.history-msg {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
}
</style>
""", unsafe_allow_html=True)



# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []   # list of (message, label)

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI · Detection Engine</div>
    <h1 class="hero-title">Spam<span>Shield</span></h1>
    <p class="hero-sub">Paste any message below — we'll tell you if it's spam or ham in milliseconds.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)



# ── Input ─────────────────────────────────────────────────────────────────────
message = st.text_area(
    "Message to analyse",
    placeholder="Paste or type a message here…",
    height=160,
    max_chars=2000,
    label_visibility="visible",
)

char_count = len(message)
st.markdown(f'<div class="char-counter">{char_count} / 2000</div>', unsafe_allow_html=True)

analyse_btn = st.button("⟶  Analyse Message", use_container_width=True)

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyse_btn:
    if not message.strip():
        st.markdown("""
        <div style="text-align:center;padding:1.2rem;color:#4a5068;
                    font-family:'Space Mono',monospace;font-size:0.78rem;">
            Please enter a message before analysing.
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner(""):
            time.sleep(0.4)          # small UX delay for perceived thinking
            result = predict_spam(message)

        label = "spam" if result == 1 else "ham"

        # Save to history (newest first, cap at 10)
        st.session_state.history.insert(0, (message, label))
        st.session_state.history = st.session_state.history[:10]

        if result == 0:
            st.markdown(f"""
            <div class="result-card ham">
                <div class="result-icon">✅</div>
                <div>
                    <div class="result-label">Verdict</div>
                    <div class="result-verdict">Ham Message</div>
                    <div class="result-desc">
                        Our model classified this message as <strong>ham</strong> —
                        it does not exhibit characteristics commonly associated with spam.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card spam">
                <div class="result-icon">🚨</div>
                <div>
                    <div class="result-label">Verdict</div>
                    <div class="result-verdict">Spam Detected</div>
                    <div class="result-desc">
                        Our model flagged this message as <strong>spam</strong>.
                        It may contain unsolicited content, phishing attempts, or deceptive language.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── History ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="history-title">Recent Checks</div>', unsafe_allow_html=True)

    for msg, lbl in st.session_state.history:
        badge_class = "ham-badge" if lbl == "ham" else "spam-badge"
        badge_text  = "HAM" if lbl == "ham" else "SPAM"
        preview     = (msg[:80] + "…") if len(msg) > 80 else msg
        preview     = preview.replace("<", "&lt;").replace(">", "&gt;")

        st.markdown(f"""
        <div class="history-row">
            <span class="badge {badge_class}">{badge_text}</span>
            <span class="history-msg">{preview}</span>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Clear history", key="clear_hist"):
        st.session_state.history = []
        st.rerun()