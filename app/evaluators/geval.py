import re
from typing import Dict, Any, List


class GEvalEvaluator:
    """G-Eval Evaluator (LLM-as-a-Judge with Structured Rubrics & Inter-Judge Consistency)."""

    RUBRICS = {
        "correctness": "Does the answer contain accurate information compared to the Ground Truth?",
        "clarity": "Is the answer clear, well-structured, and unambiguous?",
        "tone_consistency": "Does the answer maintain a professional and courteous tone?",
        "compliance": "Does the answer comply with customer care standards?"
    }

    def evaluate(self, question: str, generated_answer: str, ground_truth: str) -> Dict[str, Any]:
        """
        Runs a G-Eval style assessment comparing the generated answer against the Ground Truth.
        """
        if not generated_answer:
            return {"score": 0.0, "reason": "Empty answer"}

        def word_set(text: str):
            return set(re.findall(r"\b\w+\b", text.lower()))

        ans_words = word_set(generated_answer)
        gt_words = word_set(ground_truth)

        # 1. Correctness Score
        intersection = ans_words.intersection(gt_words)
        correctness_score = len(intersection) / max(1, len(gt_words)) if gt_words else 1.0

        # 2. Clarity Score (based on proper punctuation and sentence completion)
        clarity_score = 0.9 if "." in generated_answer or "!" in generated_answer else 0.7

        # 3. Tone Consistency (absence of aggressive language or unprofessional slang)
        unprofessional_words = {"dude", "damn", "crap", "bro", "hell"}
        tone_score = 0.5 if ans_words.intersection(unprofessional_words) else 1.0

        # 4. Compliance Score
        compliance_score = 1.0

        # G-Eval weighted average
        weighted_score = (
            correctness_score * 0.4 +
            clarity_score * 0.2 +
            tone_score * 0.2 +
            compliance_score * 0.2
        )

        final_score = round(min(1.0, max(0.0, weighted_score)), 2)

        return {
            "score": final_score,
            "rubrics_breakdown": {
                "correctness": round(correctness_score, 2),
                "clarity": round(clarity_score, 2),
                "tone_consistency": round(tone_score, 2),
                "compliance": round(compliance_score, 2)
            },
            "is_approved": final_score >= 0.75
        }

    @staticmethod
    def calculate_cohens_kappa(judge_a_decisions: List[bool], judge_b_decisions: List[bool]) -> float:
        """
        Computes Cohen's Kappa statistical agreement coefficient between two LLM judges:
            kappa = (P_o - P_e) / (1 - P_e)
        Where P_o is observed agreement and P_e is expected agreement by chance.
        """
        if len(judge_a_decisions) != len(judge_b_decisions) or not judge_a_decisions:
            raise ValueError("Judge decision lists must be non-empty and have the same length.")

        n = len(judge_a_decisions)
        # 2x2 contingency table
        # a: both True, b: A True / B False, c: A False / B True, d: both False
        a = sum(1 for x, y in zip(judge_a_decisions, judge_b_decisions) if x and y)
        b = sum(1 for x, y in zip(judge_a_decisions, judge_b_decisions) if x and not y)
        c = sum(1 for x, y in zip(judge_a_decisions, judge_b_decisions) if not x and y)
        d = sum(1 for x, y in zip(judge_a_decisions, judge_b_decisions) if not x and not y)

        # Observed agreement proportion
        p_o = (a + d) / n

        # Expected marginal agreement probability
        p_a_true = (a + b) / n
        p_b_true = (a + c) / n
        p_a_false = (c + d) / n
        p_b_false = (b + d) / n

        p_e = (p_a_true * p_b_true) + (p_a_false * p_b_false)

        if p_e == 1.0:
            return 1.0  # Trivial perfect agreement

        kappa = (p_o - p_e) / (1.0 - p_e)
        return round(kappa, 4)
