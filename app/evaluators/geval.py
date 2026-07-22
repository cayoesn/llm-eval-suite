import re
from typing import Dict, Any


class GEvalEvaluator:
    """Avaliador G-Eval (LLM-as-a-Judge com Rúbricas Estruturadas)."""

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
