import re
from typing import Dict, Any, List


STOPWORDS = {
    "para", "como", "uma", "dos", "sua", "pode", "pelo", "ser", "que", "com",
    "por", "mais", "tem", "das", "seu", "sua", "ou", "quando", "sem", "sobre",
    "este", "esta", "isso", "aqui", "ate", "mesmo", "forma", "modo", "onde",
    "voce", "voces", "opcao", "seja", "sao", "eh", "seria", "caso"
}

CONVERSATIONAL_FILLERS = {
    "com certeza", "aqui esta", "ola", "bom dia", "boa tarde", "com prazer",
    "certamente", "segue a resposta", "espero ter ajudado"
}


class FaithfulnessEvaluator:
    """Avaliador de Fidedignidade Factual (Faithfulness) com Decomposição Atômica de Claims."""

    @staticmethod
    def decompose_claims(text: str) -> List[str]:
        """Quebra a resposta gerada em declarações/claims atômicas unitárias."""
        # Divide por pontuação final (. ? ! ou quebra de linha)
        raw_sentences = re.split(r"[.!?\n]+", text)
        claims = []
        for s in raw_sentences:
            cleaned = s.strip()
            # Ignora sentenças vazias, muito curtas ou meros cumprimentos conversacionais
            if len(cleaned) > 10 and not any(filler in cleaned.lower() for filler in CONVERSATIONAL_FILLERS):
                claims.append(cleaned)
        return claims or ([text.strip()] if text.strip() else [])

    @staticmethod
    def _is_claim_supported(claim: str, context: str) -> bool:
        """Verifica se um claim atômico específico tem respaldo semântico e numérico no contexto."""
        claim_lower = claim.lower()
        context_lower = context.lower()

        # 1. Checagem estrita de integridade numérica
        claim_numbers = set(re.findall(r"\b\d+(?:[.,]\d+)?\b", claim_lower))
        ctx_numbers = set(re.findall(r"\b\d+(?:[.,]\d+)?\b", context_lower))
        if claim_numbers - ctx_numbers:
            return False  # Alucinação de número inexistente no contexto

        # 2. Checagem de tokens informativos (substantivos / entidades)
        words = re.findall(r"\b\w+\b", claim_lower)
        informative_tokens = [w for w in words if len(w) > 2 and w not in STOPWORDS]
        if not informative_tokens:
            return True

        # Pelo menos 60% dos termos informativos do claim devem estar presentes no contexto
        matching_tokens = [w for w in informative_tokens if w in context_lower]
        coverage = len(matching_tokens) / len(informative_tokens)
        return coverage >= 0.60

    def evaluate(self, generated_answer: str, context: str) -> Dict[str, Any]:
        """
        Calcula a métrica de fidedignidade da resposta baseada na proporção de claims atômicos respaldados:
            Faithfulness = (claims suportados) / (total de claims)
        """
        if not context or not generated_answer:
            return {
                "score": 0.0,
                "reason": "Contexto ou resposta vazios",
                "claims": [],
                "supported_claims": [],
                "unsupported_claims": [],
                "is_faithful": False
            }

        claims = self.decompose_claims(generated_answer)
        if not claims:
            return {
                "score": 1.0,
                "reason": "Sem claims informativos identificados",
                "claims": [],
                "supported_claims": [],
                "unsupported_claims": [],
                "is_faithful": True
            }

        supported = []
        unsupported = []

        for claim in claims:
            if self._is_claim_supported(claim, context):
                supported.append(claim)
            else:
                unsupported.append(claim)

        score = round(len(supported) / len(claims), 3)

        return {
            "score": score,
            "total_claims": len(claims),
            "supported_claims_ratio": score,
            "supported_claims": supported,
            "unsupported_claims": unsupported,
            "is_faithful": score >= 0.70
        }
