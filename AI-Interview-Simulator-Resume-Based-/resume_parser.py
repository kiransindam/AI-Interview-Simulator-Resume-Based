"""
resume_parser.py — InterviewIQ · Resume Intelligence Layer
-----------------------------------------------------------
Extracts structured profile data from PDF and TXT resumes.
Covers skills, projects, experience, education, and a summary.

Author  : Kiran Sindam
Mentor  : Claude (Anthropic)
Version : 2.0
"""

from __future__ import annotations
import re
import io
from typing import Dict, List


# ─── PDF text extraction ──────────────────────────────────────────────────────

def _extract_text_pdf(file) -> str:
    """Read all pages from a PDF file object and return joined text."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except ImportError:
        # Fallback: try pdfminer
        try:
            from pdfminer.high_level import extract_text_to_fp
            from pdfminer.layout import LAParams
            out = io.StringIO()
            extract_text_to_fp(file, out, laparams=LAParams())
            return out.getvalue()
        except Exception:
            return ""
    except Exception:
        return ""


def _extract_text_txt(file) -> str:
    raw = file.read()
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


# ─── Section splitter ─────────────────────────────────────────────────────────

_SECTION_HEADERS = re.compile(
    r"(?im)^[\s]*"
    r"(skills?|technical skills?|core competencies|"
    r"projects?|personal projects?|academic projects?|"
    r"experience|work experience|professional experience|internship|"
    r"education|academic background|"
    r"certifications?|achievements?|awards?|"
    r"summary|objective|profile)"
    r"[\s:]*$"
)


def _split_sections(text: str) -> Dict[str, str]:
    """Split resume text into named sections."""
    sections: Dict[str, str] = {"__preamble__": ""}
    current = "__preamble__"
    for line in text.splitlines():
        m = _SECTION_HEADERS.match(line)
        if m:
            current = m.group(1).lower().split()[0]   # normalise e.g. "technical" → "technical"
            sections.setdefault(current, "")
        else:
            sections[current] = sections.get(current, "") + line + "\n"
    return sections


# ─── Skills extraction ────────────────────────────────────────────────────────

# Ordered by category for readable output
_SKILL_DB: List[str] = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "kotlin", "swift", "php", "ruby", "scala", "r", "matlab", "bash",
    # Web
    "react", "next.js", "vue", "angular", "html", "css", "tailwind",
    "node.js", "express", "fastapi", "flask", "django", "spring boot",
    # Data / ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "hugging face", "langchain", "openai api",
    # Data Engineering
    "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "spark", "hadoop", "kafka", "airflow", "dbt",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "github actions", "ci/cd", "jenkins", "linux",
    # Tools
    "git", "rest api", "graphql", "microservices", "agile", "scrum",
]


def extract_skills(text: str) -> List[str]:
    """Return skills found in the text, preserving original capitalisation."""
    lower = text.lower()
    found = []
    for skill in _SKILL_DB:
        # Whole-word match; allow slash separators
        pattern = r"(?<![a-z0-9\.\+#])" + re.escape(skill) + r"(?![a-z0-9\.\+#])"
        if re.search(pattern, lower):
            found.append(skill.title() if len(skill) > 3 else skill.upper())
    return found


# ─── Projects extraction ──────────────────────────────────────────────────────

_PROJECT_PATTERNS = [
    re.compile(r"(?im)^[-•▪✓]\s*(.{8,80})$"),              # bullet list items
    re.compile(r"(?im)^project\s*[:\-]\s*(.{4,80})$"),      # "Project: X"
    re.compile(r"(?im)^([A-Z][A-Za-z0-9 &\-]{3,50})\s*\|"), # "Project Name | tech"
    re.compile(r"(?im)^\d+\.\s+(.{8,80})$"),                # numbered list
]


def extract_projects(text: str) -> List[str]:
    """Extract project names / titles from resume text."""
    projects: List[str] = []
    seen: set = set()
    for pat in _PROJECT_PATTERNS:
        for m in pat.finditer(text):
            name = m.group(1).strip().rstrip(".,:")
            key  = name.lower()
            if key not in seen and len(name) > 5:
                projects.append(name)
                seen.add(key)
    return projects[:10]   # cap at 10 to keep interview session sane


# ─── Experience extraction ────────────────────────────────────────────────────

def extract_experience(text: str) -> List[str]:
    """Extract non-empty lines from the experience section."""
    sections = _split_sections(text)
    exp_text = sections.get("experience", sections.get("professional", ""))
    lines = [l.strip() for l in exp_text.splitlines() if len(l.strip()) > 10]
    return lines[:15]


# ─── Education extraction ─────────────────────────────────────────────────────

def extract_education(text: str) -> List[str]:
    sections = _split_sections(text)
    edu_text = sections.get("education", sections.get("academic", ""))
    lines = [l.strip() for l in edu_text.splitlines() if len(l.strip()) > 8]
    return lines[:8]


# ─── Public API ───────────────────────────────────────────────────────────────

def parse_resume(file) -> Dict:
    """
    Parse an uploaded resume file and return a structured profile dict.

    Returns
    -------
    dict with keys:
        skills      : List[str]
        projects    : List[str]
        experience  : List[str]
        education   : List[str]
        summary     : str
        raw_text    : str
    """
    file_type = getattr(file, "type", "")
    if "pdf" in file_type:
        raw_text = _extract_text_pdf(file)
    else:
        raw_text = _extract_text_txt(file)

    skills     = extract_skills(raw_text)
    projects   = extract_projects(raw_text)
    experience = extract_experience(raw_text)
    education  = extract_education(raw_text)

    lines = []
    if skills:
        lines.append(f"Skills: {', '.join(skills[:10])}")
    if projects:
        lines.append(f"Projects: {len(projects)} detected")
    if experience:
        lines.append(f"Experience: {len(experience)} entries")

    return {
        "skills":     skills,
        "projects":   projects,
        "experience": experience,
        "education":  education,
        "summary":    "\n".join(lines) if lines else "Profile parsed.",
        "raw_text":   raw_text,
    }