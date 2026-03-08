"""
interview_engine.py — InterviewIQ · Core Intelligence
-------------------------------------------------------
Generates personalised, resume-driven interview questions across three
categories and evaluates answers with structured, actionable feedback.

Author  : Kiran Sindam
Mentor  : Claude (Anthropic)
Version : 2.0
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ─── Question Banks ───────────────────────────────────────────────────────────

HR_QUESTIONS: List[str] = [
    "Tell me about yourself and what led you to pursue this career path.",
    "What motivates you most when working on a challenging problem?",
    "Describe a time you had to deal with a significant setback. What did you do?",
    "How do you manage competing priorities when everything feels urgent?",
    "Tell me about a time you disagreed with a team decision. How did you handle it?",
    "Where do you see your career in 3–5 years, and how does this role fit?",
    "Describe the most complex project you have worked on. What was your role?",
    "What is your biggest professional strength — and one area you are actively improving?",
    "Tell me about a time you had to learn something completely new under a tight deadline.",
    "How do you approach giving or receiving constructive criticism?",
    "Describe a situation where you had to persuade someone who disagreed with you.",
    "What does a great day at work look like for you?",
]

TECH_TEMPLATES: List[str] = [
    "Walk me through a real project where you used {skill}. What specific problems did it solve?",
    "What are the key strengths and trade-offs of {skill} compared to its alternatives?",
    "Describe the most complex bug or issue you debugged involving {skill}. How did you approach it?",
    "How would you architect a scalable system using {skill} for 1 million daily users?",
    "What best practices and design patterns do you follow when working with {skill}?",
    "If a junior colleague asked you to explain {skill} from scratch, what core concept would you start with?",
    "How has {skill} evolved recently, and have you kept up with those changes?",
    "What is one common misconception developers have about {skill}?",
]

PROJECT_TEMPLATES: List[str] = [
    "Walk me through the high-level architecture of '{project}'. What were the key design decisions?",
    "What was your specific contribution to '{project}', and how did you measure its impact?",
    "What was the hardest technical problem you solved in '{project}'? How did you approach it?",
    "If you rebuilt '{project}' today from scratch, what would you do differently and why?",
    "How did you ensure quality and reliability in '{project}'? What testing strategy did you use?",
    "How did you handle scope creep or changing requirements during '{project}'?",
    "What trade-offs did you make in '{project}' between speed of delivery and code quality?",
    "If '{project}' needed to support 10x the current load, how would you scale it?",
]

# ─── Data Models ─────────────────────────────────────────────────────────────

@dataclass
class Question:
    category: str              # "technical" | "project" | "hr"
    question: str
    context: Optional[str] = None   # skill or project name, for targeted follow-ups


@dataclass
class FeedbackResult:
    score: int                          # 1–5
    label: str                          # e.g. "Strong Answer"
    tip: str                            # one concrete, actionable improvement
    keywords_found: List[str] = field(default_factory=list)
    word_count: int = 0


# ─── Engine ───────────────────────────────────────────────────────────────────

class InterviewEngine:
    """
    Orchestrates a full AI interview session tailored to a candidate's resume.

    Parameters
    ----------
    resume_info : dict
        Keys: ``skills`` (list[str]), ``projects`` (list[str]),
              ``experience`` (list[str]), ``summary`` (str).
    max_tech : int
        Max technical questions per detected skill (default 2).
    max_project : int
        Max project questions per detected project (default 2).
    hr_count : int
        Number of behavioural/HR questions (default 3).
    """

    def __init__(
        self,
        resume_info: dict,
        max_tech: int = 2,
        max_project: int = 2,
        hr_count: int = 3,
    ) -> None:
        self.resume_info  = resume_info
        self.max_tech     = max_tech
        self.max_project  = max_project
        self.hr_count     = hr_count
        self.questions: List[Question]              = self._build_question_set()
        self.answers: Dict[int, str]               = {}
        self.feedback_log: Dict[int, FeedbackResult] = {}

    # ── Public API ────────────────────────────────────────────────────────────

    def total_questions(self) -> int:
        return len(self.questions)

    def get_question(self, idx: int) -> Optional[Question]:
        return self.questions[idx] if 0 <= idx < len(self.questions) else None

    def submit_answer(self, idx: int, answer: str) -> FeedbackResult:
        """Store the answer and return structured feedback."""
        self.answers[idx] = answer
        fb = self._evaluate(self.questions[idx], answer)
        self.feedback_log[idx] = fb
        return fb

    def session_score(self) -> Dict:
        if not self.feedback_log:
            return {"attempted": 0, "average_score": 0.0, "total": self.total_questions()}
        scores = [fb.score for fb in self.feedback_log.values()]
        return {
            "attempted":     len(scores),
            "total":         self.total_questions(),
            "average_score": round(sum(scores) / len(scores), 1),
            "max_score":     5,
            "breakdown": {
                "excellent": sum(1 for s in scores if s == 5),
                "good":      sum(1 for s in scores if s == 4),
                "average":   sum(1 for s in scores if s == 3),
                "weak":      sum(1 for s in scores if s <= 2),
            }
        }

    # ── Private helpers ───────────────────────────────────────────────────────

    def _build_question_set(self) -> List[Question]:
        qs: List[Question] = []
        skills   = self.resume_info.get("skills",   [])
        projects = self.resume_info.get("projects", [])

        # Technical questions — sample templates per skill
        for skill in skills:
            templates = random.sample(TECH_TEMPLATES, min(self.max_tech, len(TECH_TEMPLATES)))
            for t in templates:
                qs.append(Question(
                    category="technical",
                    question=t.format(skill=skill),
                    context=skill,
                ))

        # Project questions — sample templates per project
        for project in projects[:5]:   # cap at 5 projects max
            templates = random.sample(PROJECT_TEMPLATES, min(self.max_project, len(PROJECT_TEMPLATES)))
            for t in templates:
                qs.append(Question(
                    category="project",
                    question=t.format(project=project),
                    context=project,
                ))

        # HR / Behavioural questions
        for q_text in random.sample(HR_QUESTIONS, min(self.hr_count, len(HR_QUESTIONS))):
            qs.append(Question(category="hr", question=q_text))

        # Interleave categories for a realistic interview flow
        technical = [q for q in qs if q.category == "technical"]
        project   = [q for q in qs if q.category == "project"]
        hr        = [q for q in qs if q.category == "hr"]

        merged: List[Question] = []
        i, j, k = 0, 0, 0
        while i < len(technical) or j < len(project) or k < len(hr):
            if i < len(technical): merged.append(technical[i]); i += 1
            if k < len(hr):        merged.append(hr[k]);        k += 1
            if j < len(project):   merged.append(project[j]);   j += 1

        return merged

    # ── Evaluation ────────────────────────────────────────────────────────────

    # Keywords that indicate analytical depth and impact orientation
    _IMPACT_KW = [
        "because", "therefore", "resulted", "achieved", "improved", "reduced",
        "increased", "optimised", "designed", "implemented", "led", "delivered",
        "solved", "identified", "collaborated", "measured", "learned", "impact",
        "outcome", "challenge", "decision", "trade-off", "approach", "solution",
    ]

    # STAR method signal words
    _STAR_KW = [
        "situation", "task", "action", "result", "challenge", "goal",
        "responsibility", "steps", "outcome", "impact",
    ]

    def _evaluate(self, question: Question, answer: str) -> FeedbackResult:
        """
        Heuristic evaluator scoring 1–5 based on:
          - Length (depth of response)
          - Keyword presence (impact-oriented language)
          - STAR structure signals
          - Category-specific bonuses

        Replace or augment with an LLM call for semantic scoring in production.
        """
        words     = answer.strip().split()
        wc        = len(words)
        lower     = answer.lower()

        impact_found = [kw for kw in self._IMPACT_KW if kw in lower]
        star_found   = [kw for kw in self._STAR_KW   if kw in lower]
        has_numbers  = bool(re.search(r"\d+\s*(%|x|times|ms|seconds|users|hours|days)", lower))

        # Scoring matrix
        if wc == 0:
            score, label = 1, "No Answer"
        elif wc < 20:
            score, label = 2, "Too Brief"
        elif wc < 50:
            score = 3 if len(impact_found) >= 1 else 2
            label = "Needs More Depth" if score == 2 else "Acceptable"
        elif wc < 100:
            if len(impact_found) >= 3 and len(star_found) >= 1:
                score, label = 4, "Good Answer"
            else:
                score, label = 3, "Acceptable"
        else:  # >= 100 words
            if len(impact_found) >= 4 and (has_numbers or len(star_found) >= 2):
                score, label = 5, "Excellent Answer"
            elif len(impact_found) >= 3:
                score, label = 4, "Good Answer"
            else:
                score, label = 3, "Acceptable"

        tip = self._craft_tip(score, question, impact_found, star_found, has_numbers, wc)
        return FeedbackResult(
            score=score,
            label=label,
            tip=tip,
            keywords_found=impact_found,
            word_count=wc,
        )

    def _craft_tip(
        self,
        score: int,
        question: Question,
        impact_found: List[str],
        star_found: List[str],
        has_numbers: bool,
        wc: int,
    ) -> str:
        if score == 1:
            return (
                "Even a brief answer shows engagement. Start with 'In my experience…' "
                "and describe a specific situation you faced."
            )
        if score == 2:
            return (
                "Use the STAR method: describe the Situation, your Task, "
                "the Actions you took, and the Result. Aim for at least 50 words."
            )
        if score == 3:
            if not has_numbers:
                return (
                    "Quantify your impact to stand out — e.g. "
                    "'reduced latency by 40%', 'onboarded 500 users', 'cut build time to 2 min'. "
                    "Numbers make achievements concrete and memorable."
                )
            if not star_found:
                return (
                    "Add a brief context: what was the problem, why did it matter, "
                    "and what specific actions did YOU take? This depth differentiates a 3★ from a 5★."
                )
            return "Good foundation. Add one more concrete outcome or lesson learned to push to 4★."
        if score == 4:
            return (
                "Strong answer! To reach 5★, add a quantified outcome "
                "(%, time saved, scale) and briefly mention what you'd do differently. "
                "Reflection signals maturity to interviewers."
            )
        # score == 5
        return (
            "Outstanding depth and specificity! This is exactly the structured, "
            "impact-driven response top companies look for. Keep this energy for the real interview."
        )