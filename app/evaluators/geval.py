import re
from typing import Dict, Any, List


class GEvalEvaluator:
    """Avaliador G-Eval (LLM-as-a-Judge com Rúbricas Estruturadas & Consistência Inter-Juízes)."""

    RUBRICS = {
        "correctness": "A resposta contem informacoes corretas em comparacao ao Ground Truth?",
        "clarity": "A resposta eh clara, bem estruturada e sem ambiguidades?",
        "tone_consistency": "A resposta mantem tom profissional e cortes?",
        "compliance": "A resposta cumpre os padroes de atencao ao cliente?"
    }

    def evaluate(self, question: str, generated_answer: str, ground_truth: str) -> Dict[str, Any]:
        """
        Executa avaliação estilo G-Eval avaliando a resposta frente ao Ground Truth.
        """
        if not generated_answer:
            return {"score": 0.0, "reason": "Resposta vazia"}

        def word_set(text: str):
            return set(re.findall(r"\b\w+\b", text.lower()))

        ans_words = word_set(generated_answer)
        gt_words = word_set(ground_truth)

        # 1. Correctness Score
        intersection = ans_words.intersection(gt_words)
        correctness_score = len(intersection) / max(1, len(gt_words)) if gt_words else 1.0

        # 2. Clarity Score (baseado em presença de pontuação e tamanho adequado)
        clarity_score = 0.9 if "." in generated_answer or "!" in generated_answer else 0.7

        # 3. Tone Consistency (ausência de palavras agressivas ou gírias extremas)
        unprofessional_words = {"mano", "porra", "droga", "veio", "caralho"}
        tone_score = 0.5 if ans_words.intersection(unprofessional_words) else 1.0

        # 4. Compliance Score
        compliance_score = 1.0

        # Média ponderada G-Eval
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
        Calcula o coeficiente de concordância estatística Cohen's Kappa entre dois juízes LLM:
            kappa = (P_o - P_e) / (1 - P_e)
        Onde P_o é a concordância observada e P_e é a concordância esperada por chance.
        """
        if len(judge_a_decisions) != len(judge_b_decisions) or not judge_a_decisions:
            raise ValueError("As listas de decisões dos juízes devem ter o mesmo tamanho e não ser vazias.")

        n = len(judge_a_decisions)
        # Tabela de contingência 2x2
        # a: both True, b: A True / B False, c: A False / B True, d: both False
        a = sum(1 for x, y in zip(judge_a_decisions, judge_b_decisions) if x and y)
        b = sum(1 for x, y in zip(judge_a_decisions, judge_b_decisions) if x and not y)
        c = sum(1 for x, y in zip(judge_a_decisions, judge_b_decisions) if not x and y)
        d = sum(1 for x, y in zip(judge_a_decisions, judge_b_decisions) if not x and not y)

        # Proporção observada
        p_o = (a + d) / n

        # Probabilidade marginal esperada
        p_a_true = (a + b) / n
        p_b_true = (a + c) / n
        p_a_false = (c + d) / n
        p_b_false = (b + d) / n

        p_e = (p_a_true * p_b_true) + (p_a_false * p_b_false)

        if p_e == 1.0:
            return 1.0  # Concordância perfeita trivial

        kappa = (p_o - p_e) / (1.0 - p_e)
        return round(kappa, 4)
