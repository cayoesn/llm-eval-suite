import re
from typing import Dict, Any


class AnswerRelevanceEvaluator:
    """Avaliador de Relevância e Direcionamento da Resposta em Relação à Pergunta."""

    def evaluate(self, question: str, generated_answer: str) -> Dict[str, Any]:
        """
        Calcula a métrica de relevância da resposta em relação à pergunta.
        """
        if not question or not generated_answer:
            return {"score": 0.0, "reason": "Pergunta ou resposta vazia"}

        def tokenize(text: str):
            words = re.findall(r"\b\w+\b", text.lower())
            return set(w for w in words if len(w) > 2)

        q_tokens = tokenize(question)
        ans_tokens = tokenize(generated_answer)

        if not q_tokens:
            return {"score": 1.0, "reason": "Pergunta sem palavras chave"}

        overlap = q_tokens.intersection(ans_tokens)
        overlap_score = len(overlap) / len(q_tokens)

        # Respostas muito curtas (< 3 palavras) recebem penalidade de incompletude
        ans_word_count = len(generated_answer.split())
        length_penalty = 0.0
        if ans_word_count < 3:
            length_penalty = 0.3

        final_score = round(max(0.0, min(1.0, overlap_score * 0.8 + 0.3 - length_penalty)), 2)

        return {
            "score": final_score,
            "keyword_overlap_ratio": round(len(overlap) / len(q_tokens), 2),
            "is_relevant": final_score >= 0.80
        }
