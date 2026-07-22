import re
from typing import Dict, Any

STOPWORDS = {
    "para", "como", "uma", "dos", "sua", "pode", "pelo", "ser", "que", "com",
    "por", "mais", "tem", "das", "seu", "sua", "ou", "quando", "sem", "sobre",
    "este", "esta", "isso", "aqui", "ate", "mesmo", "forma", "modo", "onde",
    "voce", "voces", "opcao", "seja", "sao", "eh", "seria", "caso", "quais"
}


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
            return set(w for w in words if len(w) > 2 and w not in STOPWORDS)

        q_tokens = tokenize(question)
        ans_tokens = tokenize(generated_answer)

        if not q_tokens:
            return {"score": 1.0, "reason": "Pergunta sem palavras chave"}

        overlap = q_tokens.intersection(ans_tokens)
        overlap_score = len(overlap) / len(q_tokens) if q_tokens else 1.0

        ans_word_count = len(generated_answer.split())
        length_penalty = 0.0
        if ans_word_count < 3:
            length_penalty = 0.3

        final_score = round(max(0.0, min(1.0, overlap_score * 0.7 + 0.3 - length_penalty)), 2)

        return {
            "score": final_score,
            "keyword_overlap_ratio": round(len(overlap) / len(q_tokens), 2) if q_tokens else 1.0,
            "is_relevant": final_score >= 0.70
        }
