import streamlit as st
from ai_engine import analyze_message

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Customer Support Analyzer",
    page_icon="🤖",
    layout="centered",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');

    /* ── Force dark background everywhere ── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    [data-testid="block-container"],
    .main, .block-container,
    [data-testid="stVerticalBlock"] {
        background-color: #080c14 !important;
        color: #e2e8f0 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: #080c14 !important;
    }

    /* ── Textarea ── */
    textarea {
        background-color: #111827 !important;
        color: #f1f5f9 !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
    }
    textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
    }
    textarea::placeholder { color: #4b5563 !important; }

    /* ── Labels ── */
    label, .stTextArea label {
        color: #94a3b8 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    /* ── Primary button ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1d4ed8, #4f46e5) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 20px rgba(79,70,229,0.4) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563eb, #6366f1) !important;
        box-shadow: 0 6px 28px rgba(99,102,241,0.5) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Secondary / clear button ── */
    .stButton > button:not([kind="primary"]) {
        background: #1e293b !important;
        color: #94a3b8 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stButton > button:not([kind="primary"]):hover {
        background: #273549 !important;
        color: #e2e8f0 !important;
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #6366f1 !important; }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: #0d1526 !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 12px !important;
    }
    [data-testid="stExpander"] summary {
        color: #94a3b8 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Alert / warning / error ── */
    [data-testid="stAlert"] {
        background: #0d1526 !important;
        border-radius: 10px !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #080c14; }
    ::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 4px; }

    /* ─────────────────────────────────────── */
    /*   COMPONENT STYLES                      */
    /* ─────────────────────────────────────── */

    .hero {
        text-align: center;
        padding: 3rem 1rem 2rem;
    }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #1d3461, #1e3a5f);
        color: #60a5fa;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.3rem 1rem;
        border-radius: 999px;
        border: 1px solid #1e4080;
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        font-family: 'Syne', sans-serif !important;
        font-size: 2.6rem;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.2;
        margin-bottom: 0.8rem;
        background: none !important;
        -webkit-text-fill-color: unset !important;
    }
    .grad-text {
        font-family: 'Syne', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.2;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: inline-block;
    }
    .hero p {
        color: #64748b;
        font-size: 1rem;
        max-width: 420px;
        margin: 0 auto;
        line-height: 1.6;
    }

    .stat-row {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1.8rem 0 0.5rem;
        flex-wrap: wrap;
    }
    .stat-pill {
        background: #0d1526;
        border: 1px solid #1e3a5f;
        border-radius: 999px;
        padding: 0.4rem 1.1rem;
        font-size: 0.8rem;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .stat-pill strong { color: #94a3b8; }

    .divider {
        border: none;
        border-top: 1px solid #111f35;
        margin: 1.8rem 0;
    }

    .glow-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #3b82f6, #818cf8, #a78bfa, transparent);
        border: none;
        margin: 0.5rem 0 2rem;
        opacity: 0.6;
    }

    .input-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }

    .results-header {
        font-family: 'Syne', sans-serif !important;
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 1.2rem;
    }

    .result-card {
        border-radius: 14px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
        position: relative;
        overflow: hidden;
    }

    .card-category  {
        background: linear-gradient(135deg, #0d1526, #111d38);
        border-color: #6366f1;
    }
    .card-sentiment {
        background: linear-gradient(135deg, #0a1a15, #0d2020);
        border-color: #10b981;
    }
    .card-reply {
        background: linear-gradient(135deg, #1a1508, #1f1a08);
        border-color: #f59e0b;
    }

    .card-label {
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        margin-bottom: 0.6rem;
    }
    .label-category  { color: #818cf8; }
    .label-sentiment { color: #34d399; }
    .label-reply     { color: #fbbf24; }

    .badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 999px;
        font-size: 0.88rem;
        font-weight: 700;
    }
    .badge-positive { background: #052e1c; color: #34d399; border: 1px solid #065f46; }
    .badge-neutral  { background: #0f172a; color: #94a3b8; border: 1px solid #1e293b; }
    .badge-negative { background: #2d0a0a; color: #f87171; border: 1px solid #5c1414; }

    .badge-category {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 999px;
        font-size: 0.88rem;
        font-weight: 700;
        background: #1e1b4b;
        color: #a5b4fc;
        border: 1px solid #312e81;
    }

    .card-text {
        font-size: 0.97rem;
        color: #cbd5e1;
        line-height: 1.7;
        font-style: italic;
    }

    .history-item {
        background: #0d1526;
        border-radius: 10px;
        padding: 0.9rem 1.3rem;
        margin-bottom: 0.6rem;
        border: 1px solid #1e3a5f;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ Powered by Groq · LLaMA 3.3-70B</div>
    <div style="font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800; color:#f8fafc; letter-spacing:-0.01em; margin-bottom:0.2rem;">AI Customer Support</div>
    <div class="grad-text">Analyzer</div>
    <p>Instantly classify messages, detect sentiment, and generate professional replies — in seconds.</p>
    <div class="stat-row">
        <div class="stat-pill">📂 <strong>7</strong> Categories</div>
        <div class="stat-pill">❤️ <strong>3</strong> Sentiments</div>
        <div class="stat-pill">💬 <strong>Auto</strong> Reply</div>
    </div>
</div>
<hr class="glow-line">
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─── Input Area ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-label">✏️ Customer Message</div>', unsafe_allow_html=True)

message = st.text_area(
    label="customer_message",
    label_visibility="collapsed",
    height=145,
    placeholder="e.g. My order hasn't arrived in 3 weeks and nobody is helping me. This is unacceptable!",
)

analyze_btn = st.button("🚀 Analyze Message", use_container_width=True, type="primary")

# ─── Analysis ──────────────────────────────────────────────────────────────────
if analyze_btn:
    if not message.strip():
        st.warning("⚠️ Please enter a customer message first.")
    else:
        with st.spinner("🔍 Analyzing with Groq AI..."):
            result = analyze_message(message.strip())

        if "error" in result:
            st.error(f"❌ Error: {result['error']}")
        else:
            category  = result.get("category", "Unknown")
            sentiment = result.get("sentiment", "Neutral")
            reply     = result.get("auto_reply", "")

            s_class = {
                "Positive": "badge-positive",
                "Neutral":  "badge-neutral",
                "Negative": "badge-negative",
            }.get(sentiment, "badge-neutral")

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<div class="results-header">📊 Analysis Results</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card card-category">
                <div class="card-label label-category">📂 &nbsp;Category</div>
                <span class="badge-category">{category}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card card-sentiment">
                <div class="card-label label-sentiment">❤️ &nbsp;Sentiment</div>
                <span class="badge {s_class}">{sentiment}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card card-reply">
                <div class="card-label label-reply">💬 &nbsp;Auto-Reply</div>
                <div class="card-text">"{reply}"</div>
            </div>
            """, unsafe_allow_html=True)

            st.session_state.history.insert(0, {
                "message":   message.strip(),
                "category":  category,
                "sentiment": sentiment,
                "reply":     reply,
            })

# ─── History ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    with st.expander(f"🕓 Analysis History  ({len(st.session_state.history)} messages)"):
        for i, item in enumerate(st.session_state.history):
            s_emoji = {"Positive": "🟢", "Negative": "🔴", "Neutral": "🟡"}.get(item['sentiment'], "🟡")
            st.markdown(f"""
            <div class="history-item">
                <span style="color:#818cf8; font-weight:700;">#{i+1}</span>
                &nbsp;<span style="color:#a5b4fc; font-weight:600;">{item['category']}</span>
                &nbsp;·&nbsp; {s_emoji} {item['sentiment']}<br>
                <span style="color:#475569; font-size:0.82rem; margin-top:0.3rem; display:block;">
                    "{item['message'][:90]}{'...' if len(item['message']) > 90 else ''}"
                </span>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    "<center><small style='color:#1e3a5f; font-size:0.78rem;'>Built with Streamlit · Groq LLaMA 3.3-70B · AI Engineer Selection Task</small></center>",
    unsafe_allow_html=True,
)