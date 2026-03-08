# 🎯 InterviewIQ — AI Interview Simulator

> **Resume-powered AI interview simulator that generates personalised technical, project, and behavioural questions from your actual resume — with real-time scored feedback on every answer.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

---

## 📌 The Real-World Problem This Solves

Technical recruiters spend under **90 seconds** screening a candidate. Most developers know how to code — but struggle to communicate their experience clearly under pressure.

**InterviewIQ addresses four core pain points:**

1. Generic prep tools ask the same questions for every user, ignoring your actual background
2. Practicing alone gives zero signal on whether you are actually improving
3. Developers build great projects but cannot explain their trade-offs, decisions, and impact
4. Most candidates know the STAR method but have never practiced it with scored feedback

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Smart Resume Parsing** | Extracts 50+ skills, project names, and experience from PDF and TXT resumes |
| 🎯 **Personalised Questions** | Technical, Project, and HR questions generated from YOUR profile |
| ⭐ **Real-Time Scoring** | 1–5 star rating using word count, impact keywords, STAR signals, and quantification |
| 💡 **Targeted Feedback** | One specific, actionable improvement tip per answer |
| 📊 **Session Dashboard** | End-of-session breakdown: avg score, question review, excellent/good/weak counts |
| 🔀 **Realistic Flow** | Questions interleaved across categories to simulate a real interview rhythm |
| 🎨 **Premium Dark UI** | Custom CSS with Sora and JetBrains Mono typography, gradient animations |

---

## 🚀 Quick Start

```bash
git clone https://github.com/kiransindam/interviewiq.git
cd interviewiq
pip install streamlit PyPDF2 pdfminer.six
streamlit run app.py
```

Open your browser to `http://localhost:8501`

---

## 📁 Project Structure

```
interviewiq/
├── app.py              # Streamlit UI — dark-mode interface
├── interview_engine.py # Core engine — question generation and answer evaluation
├── resume_parser.py    # Resume intelligence — PDF/TXT parsing, skill extraction
├── README.md
└── requirements.txt
```

---

## 🐛 Critical Bug Fixed (v1 to v2)

The original `resume_parser.py` had a regex escape bug that meant **zero skills were ever detected**:

```python
# BROKEN original — \b not a word boundary inside re.escape()
re.search(rf"\b{re.escape(skill)}\b", text, re.I)

# FIXED v2 — correct lookahead/lookbehind word-boundary detection
re.search(r"(?<![a-z0-9\.\+#])" + re.escape(skill) + r"(?![a-z0-9\.\+#])", lower)
```

Other v2 improvements: 50+ skills (was 11), 4 project extraction patterns (was 1), scoring using 25 impact keywords + STAR signals + number detection, interleaved question ordering for realistic pacing.

---

## 🗺️ Roadmap

- [ ] Claude API for LLM-powered semantic answer scoring
- [ ] Voice input support
- [ ] Company-specific interview modes
- [ ] PDF session report export
- [ ] GitHub OAuth for public project data

---

## 👨‍💻 Author

**Kiran Sindam** — Full-Stack Developer and ML Enthusiast  
[GitHub](https://github.com/kiransindam) · [LinkedIn](https://linkedin.com/in/kiransindam) .[Portfolio](https://aistudio.google.com/apps/80abc1d3-fe16-48f2-a577-f20e4c746d99?fullscreenApplet=true&showPreview=true&showAssistant=true).

## 🤖 AI Project Mentor

**Claude (Anthropic)** — Architecture guidance, code review, bug identification, UI design, and PRD documentation.

---

<div align="center"><strong>Built with love by Kiran Sindam · Mentored by Claude (Anthropic)</strong></div>