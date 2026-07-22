import re
from typing import Dict, Any


class FaithfulnessEvaluator:
    """Avaliador de Fidedignidade Factual (Faithfulness / Groundedness)."""

    def evaluate(self, generated_answer: str, context: str) -> Dict[str, Any]:
        """
        Calcula a métrica de fidedignidade da resposta em relação ao contexto fornecido.
        Retorna score de 0.0 a 1.0.
        """
        if not context or not generated_answer:
            return {"score": 0.0, "reason": "Contexto ou resposta vazios"}

        def tokenize(text: str):
            words = re.findall(r"\b\w+\b", text.lower())
            # Filtra stopwords curtas para focar em termos informativos
            return set(w for w in words if len(w) > 2)

        ans_tokens = tokenize(generated_answer)
        ctx_tokens = tokenize(context)

        if not ans_tokens:
            return {"score": 1.0, "reason": "Sem palavras informativas significativas"}

        intersection = ans_tokens.intersection(ctx_tokens)
        faithfulness_score = len(intersection) / len(ans_tokens)

        # Penalização leve se houver números na resposta que não estão no contexto
        ans_numbers = set(re.findall(r"\b\d+\b", generated_answer))
        ctx_numbers = set(re.findall(r"\b\d+\b", context))
        unsupported_numbers = ans_numbers - ctx_numbers

        if unsupported_numbers:
            faithfulness_score = max(0.0, faithfulness_score - 0.25)

        score = round(min(1.0, max(0.0, faithfulness_score)), 2)

        return {
            "score": score,
            "supported_claims_ratio": score,
            "unsupported_numbers": list(unsupported_numbers),
            "is_faithful": score >= 0.80
        }
