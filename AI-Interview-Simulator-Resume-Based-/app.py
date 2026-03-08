"""
app.py — InterviewIQ · AI Interview Simulator
----------------------------------------------
Streamlit entry point. Premium dark-mode UI with animated transitions,
resume parsing, live progress tracking, and score dashboard.

Author  : Kiran Sindam
Mentor  : Claude (Anthropic)
Version : 2.0
"""

import streamlit as st
from resume_parser import parse_resume
from interview_engine import InterviewEngine

st.set_page_config(
    page_title="InterviewIQ — AI Interview Simulator",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --bg:#070b12; --surface:#0f1520; --surface2:#161d2e;
  --cyan:#00d4ff; --indigo:#6366f1; --purple:#a78bfa;
  --green:#10b981; --amber:#f59e0b; --red:#ef4444;
  --text:#e5e7eb; --muted:#6b7280; --border:rgba(255,255,255,0.07);
}
html,body,[class*="css"] { font-family:'Sora',sans-serif !important; }
.main { background:var(--bg) !important; }
.block-container { padding-top:1.5rem !important; max-width:800px !important; }
#MainMenu,footer,header { visibility:hidden; }

.hero { text-align:center; padding:2.8rem 1rem 1.6rem; animation:fadeUp .8s ease; }
.hero-icon { font-size:4rem; display:block; margin-bottom:.5rem; animation:pop 1s cubic-bezier(.36,.07,.19,.97); }
.hero-title {
  font-size:3rem; font-weight:800; letter-spacing:-.03em; line-height:1.05;
  background:linear-gradient(135deg,#00d4ff 0%,#6366f1 45%,#a78bfa 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:.4rem;
}
.hero-sub  { color:var(--muted); font-size:.95rem; font-weight:300; max-width:480px; margin:0 auto 1rem; line-height:1.7; }
.hero-meta { font-size:.72rem; color:#374151; font-family:'JetBrains Mono',monospace; margin-top:.4rem; }
.hero-meta span { color:var(--indigo); }
.badge-row { display:flex; justify-content:center; gap:8px; flex-wrap:wrap; margin-bottom:.4rem; }
.badge { background:rgba(99,102,241,.1); border:1px solid rgba(99,102,241,.3); border-radius:20px; padding:3px 14px; font-size:.7rem; font-weight:700; color:var(--purple); letter-spacing:.05em; text-transform:uppercase; }

.card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:1.4rem 1.6rem; margin-bottom:1rem; animation:fadeUp .55s ease; }
.card-cyan   { border-left:3px solid var(--cyan); }
.card-indigo { border-left:3px solid var(--indigo); }
.card-green  { border-left:3px solid var(--green); }
.card-label { font-size:.66rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); margin-bottom:.45rem; }
.card-title { font-size:1.05rem; font-weight:600; color:var(--text); line-height:1.5; }
.card-body  { font-size:.9rem; color:#9ca3af; line-height:1.75; }

.upload-zone { background:linear-gradient(135deg,rgba(0,212,255,.04),rgba(99,102,241,.05)); border:1.5px dashed rgba(99,102,241,.35); border-radius:18px; padding:2.2rem 1.5rem; text-align:center; margin:1rem 0; }
.upload-zone .uz-icon { font-size:2.6rem; }
.upload-zone p { color:var(--muted); font-size:.88rem; margin:.5rem 0 0; line-height:1.6; }

.stats-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:.8rem 0; }
.stat-box { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:.9rem; text-align:center; }
.stat-num { font-size:2rem; font-weight:800; color:var(--text); }
.stat-lbl { font-size:.68rem; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; margin-top:2px; }

.prog { margin:1.2rem 0 .6rem; }
.prog-meta { display:flex; justify-content:space-between; margin-bottom:5px; }
.prog-meta span { font-size:.75rem; color:var(--muted); }
.prog-bg { height:5px; background:rgba(255,255,255,.05); border-radius:999px; overflow:hidden; }
.prog-fill { height:100%; border-radius:999px; background:linear-gradient(90deg,var(--cyan),var(--indigo)); }

.q-tag { display:inline-block; border-radius:7px; padding:2px 10px; font-size:.68rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; margin-bottom:.75rem; }
.q-tag-technical { background:rgba(0,212,255,.1);   color:var(--cyan); }
.q-tag-project   { background:rgba(99,102,241,.14); color:#818cf8; }
.q-tag-hr        { background:rgba(16,185,129,.11); color:#34d399; }

.fb { border-radius:13px; padding:1rem 1.25rem; margin-top:.75rem; }
.fb-5 { background:rgba(16,185,129,.09);  border:1px solid rgba(16,185,129,.22); }
.fb-4 { background:rgba(99,102,241,.09);  border:1px solid rgba(99,102,241,.22); }
.fb-3 { background:rgba(245,158,11,.08);  border:1px solid rgba(245,158,11,.22); }
.fb-2 { background:rgba(239,68,68,.07);   border:1px solid rgba(239,68,68,.2);  }
.fb-1 { background:rgba(239,68,68,.07);   border:1px solid rgba(239,68,68,.2);  }
.fb-heading { font-size:.98rem; font-weight:700; margin-bottom:.3rem; }
.fb-tip     { font-size:.87rem; color:#9ca3af; line-height:1.65; }
.fb-meta    { font-size:.7rem; color:var(--muted); margin-top:.5rem; font-family:'JetBrains Mono',monospace; }

.breakdown-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin:.8rem 0; }
.bk-box { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:.7rem; text-align:center; }
.bk-num { font-size:1.5rem; font-weight:800; }
.bk-lbl { font-size:.65rem; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }

.stTextArea textarea { background:var(--surface2) !important; border:1px solid rgba(255,255,255,.1) !important; border-radius:12px !important; color:var(--text) !important; font-family:'Sora',sans-serif !important; font-size:.9rem !important; min-height:130px !important; }
.stTextArea textarea:focus { border-color:rgba(99,102,241,.55) !important; box-shadow:0 0 0 3px rgba(99,102,241,.1) !important; }
.stButton>button { background:linear-gradient(135deg,var(--indigo),#4f46e5) !important; color:#fff !important; border:none !important; border-radius:10px !important; font-family:'Sora',sans-serif !important; font-weight:600 !important; font-size:.9rem !important; padding:.65rem 2rem !important; width:100% !important; box-shadow:0 4px 24px rgba(99,102,241,.3) !important; }
hr { border-color:rgba(255,255,255,.06) !important; margin:1.4rem 0 !important; }
.footer { text-align:center; color:#374151; font-size:.73rem; padding:2rem 0 1rem; border-top:1px solid var(--border); margin-top:2.5rem; }
.footer strong { color:var(--indigo); }
.footer em { color:var(--muted); font-style:normal; }

@keyframes fadeUp { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:none} }
@keyframes pop { 0%{transform:scale(.3);opacity:0} 55%{transform:scale(1.06)} 75%{transform:scale(.96)} 100%{transform:scale(1);opacity:1} }
</style>
""", unsafe_allow_html=True)

def stars(n):        return "★" * n + "☆" * (5 - n)
def score_clr(n):    return {5:"#10b981",4:"#818cf8",3:"#f59e0b",2:"#ef4444",1:"#ef4444"}.get(n,"#6b7280")
CATS = {"technical":("🛠️ Technical","q-tag-technical"),"project":("📁 Project","q-tag-project"),"hr":("🤝 Behavioural","q-tag-hr")}

st.markdown("""
<div class="hero">
  <span class="hero-icon">🎯</span>
  <div class="hero-title">InterviewIQ</div>
  <div class="hero-sub">Resume-powered AI interview simulator that tailors every question to your real skills, projects and experience.</div>
  <div class="badge-row">
    <span class="badge">AI-Powered</span><span class="badge">Resume-Aware</span>
    <span class="badge">Real-Time Feedback</span><span class="badge">Score Tracking</span>
  </div>
  <div class="hero-meta">Built by <span>Kiran Sindam</span> &nbsp;·&nbsp; Mentored by <span>Claude (Anthropic)</span></div>
</div>
""", unsafe_allow_html=True)
st.divider()

# ── UPLOAD STAGE ──────────────────────────────────────────────────────────────
if "engine" not in st.session_state:
    st.markdown("""
    <div class="upload-zone">
      <div class="uz-icon">📄</div>
      <p>Upload your resume (PDF or TXT) to generate a personalised interview<br>tailored to your skills, projects and experience.</p>
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload resume", type=["pdf","txt"], label_visibility="collapsed")

    if uploaded:
        with st.spinner("Parsing resume…"):
            profile = parse_resume(uploaded)

        skills, projects = profile.get("skills",[]), profile.get("projects",[])
        total_q = len(skills)*2 + min(len(projects),5)*2 + 3

        st.markdown("""<div class="card card-green">
          <div class="card-label">✅ Resume parsed successfully</div>
          <div class="card-title">Your profile has been extracted and your interview is ready.</div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="stats-grid">
          <div class="stat-box"><div class="stat-num">{len(skills)}</div><div class="stat-lbl">Skills</div></div>
          <div class="stat-box"><div class="stat-num">{len(projects)}</div><div class="stat-lbl">Projects</div></div>
          <div class="stat-box"><div class="stat-num">~{total_q}</div><div class="stat-lbl">Questions</div></div>
        </div>""", unsafe_allow_html=True)

        if skills:
            st.markdown(f"""<div class="card card-cyan">
              <div class="card-label">🛠️ Detected Skills</div>
              <div class="card-body">{" &nbsp;·&nbsp; ".join(skills[:12])}</div>
            </div>""", unsafe_allow_html=True)
        if projects:
            phtml = "<br>".join(f"• {p}" for p in projects[:5])
            st.markdown(f"""<div class="card card-indigo">
              <div class="card-label">📁 Detected Projects</div>
              <div class="card-body">{phtml}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀  Start Interview Session"):
            st.session_state.engine = InterviewEngine(profile)
            st.session_state.q_idx  = 0
            st.session_state.feedback = None
            st.rerun()

    st.markdown("""<div class="footer">Made with ❤️ by <strong>Kiran Sindam</strong> &nbsp;·&nbsp; Mentored by <strong>Claude (Anthropic)</strong> &nbsp;·&nbsp; <em>InterviewIQ v2.0</em></div>""", unsafe_allow_html=True)
    st.stop()

engine: InterviewEngine = st.session_state.engine
q_idx: int = st.session_state.q_idx
total: int = engine.total_questions()

# ── COMPLETE SCREEN ───────────────────────────────────────────────────────────
if q_idx >= total:
    stats = engine.session_score()
    avg   = stats["average_score"]
    bk    = stats.get("breakdown", {})
    clr   = "#10b981" if avg>=4 else "#f59e0b" if avg>=2.5 else "#ef4444"

    st.markdown("""<div class="hero" style="padding-top:.8rem">
      <span class="hero-icon">🏆</span>
      <div class="hero-title" style="font-size:2.2rem">Interview Complete!</div>
      <div class="hero-sub">Full breakdown of your performance below.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="stats-grid">
      <div class="stat-box"><div class="stat-num" style="color:{clr}">{avg}</div><div class="stat-lbl">Avg Score / 5</div></div>
      <div class="stat-box"><div class="stat-num">{stats['attempted']}</div><div class="stat-lbl">Answered</div></div>
      <div class="stat-box"><div class="stat-num">{total}</div><div class="stat-lbl">Total Qs</div></div>
    </div>""", unsafe_allow_html=True)

    if bk:
        st.markdown(f"""<div class="breakdown-grid">
          <div class="bk-box"><div class="bk-num" style="color:#10b981">{bk.get('excellent',0)}</div><div class="bk-lbl">5★ Excellent</div></div>
          <div class="bk-box"><div class="bk-num" style="color:#818cf8">{bk.get('good',0)}</div><div class="bk-lbl">4★ Good</div></div>
          <div class="bk-box"><div class="bk-num" style="color:#f59e0b">{bk.get('average',0)}</div><div class="bk-lbl">3★ Average</div></div>
          <div class="bk-box"><div class="bk-num" style="color:#ef4444">{bk.get('weak',0)}</div><div class="bk-lbl">1–2★ Weak</div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("#### 📋 Full Question Review")
    for i, q in enumerate(engine.questions):
        fb = engine.feedback_log.get(i)
        lbl, tcls = CATS.get(q.category, ("General","q-tag-hr"))
        clr2 = score_clr(fb.score) if fb else "#6b7280"
        tip_html = f'<div class="fb-tip" style="margin-top:.35rem">💡 {fb.tip}</div>' if fb else ""
        st.markdown(f"""<div class="card">
          <div class="q-tag {tcls}">{lbl}</div>
          <div class="card-body" style="color:#d1d5db;margin-bottom:.4rem">{q.question}</div>
          <span style="color:{clr2}">{stars(fb.score) if fb else "Skipped"}</span>{tip_html}
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  Start a New Interview"):
        for k in ["engine","q_idx","feedback"]: st.session_state.pop(k,None)
        st.rerun()

    st.markdown("""<div class="footer">Made with ❤️ by <strong>Kiran Sindam</strong> &nbsp;·&nbsp; Mentored by <strong>Claude (Anthropic)</strong> &nbsp;·&nbsp; <em>InterviewIQ v2.0</em></div>""", unsafe_allow_html=True)
    st.stop()

# ── ACTIVE QUESTION ───────────────────────────────────────────────────────────
question = engine.get_question(q_idx)
lbl, tcls = CATS.get(question.category, ("General","q-tag-hr"))
pct = int((q_idx / total) * 100)

st.markdown(f"""<div class="prog">
  <div class="prog-meta"><span>Progress</span><span>{q_idx} / {total} questions</span></div>
  <div class="prog-bg"><div class="prog-fill" style="width:{pct}%"></div></div>
</div>""", unsafe_allow_html=True)

st.markdown(f"""<div class="card card-indigo">
  <div class="q-tag {tcls}">{lbl}</div>
  <div class="card-label">Question {q_idx+1} of {total}</div>
  <div class="card-title">{question.question}</div>
</div>""", unsafe_allow_html=True)

prev = st.session_state.feedback
if prev:
    clr = score_clr(prev.score)
    wc_note = f"&nbsp; {prev.word_count} words" if prev.word_count else ""
    kw = ', '.join(prev.keywords_found[:5]) or 'none'
    st.markdown(f"""<div class="fb fb-{prev.score}">
      <div class="fb-heading" style="color:{clr}">{stars(prev.score)} &nbsp; {prev.label}</div>
      <div class="fb-tip">💡 {prev.tip}</div>
      <div class="fb-meta">Keywords: {kw}{wc_note}</div>
    </div><br>""", unsafe_allow_html=True)

user_ans = st.text_area("Your answer",
    placeholder="Use the STAR method: Situation → Task → Action → Result. Be specific and quantify your impact.",
    key=f"ans_{q_idx}", label_visibility="collapsed")

c1, c2 = st.columns([4,1])
with c1:
    if st.button("Submit Answer →"):
        fb = engine.submit_answer(q_idx, user_ans)
        st.session_state.feedback = fb
        st.session_state.q_idx += 1
        st.rerun()
with c2:
    if st.button("Skip →"):
        st.session_state.feedback = None
        st.session_state.q_idx += 1
        st.rerun()

st.markdown("""<div class="footer">Made with ❤️ by <strong>Kiran Sindam</strong> &nbsp;·&nbsp; Mentored by <strong>Claude (Anthropic)</strong> &nbsp;·&nbsp; <em>InterviewIQ v2.0</em></div>""", unsafe_allow_html=True)