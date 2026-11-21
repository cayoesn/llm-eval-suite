import re
from typing import Dict, Any, List


STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
    "will", "can", "could", "would", "should", "have", "has", "had", "not", "but",
    "you", "your", "our", "its", "they", "their", "what", "when", "where", "how",
    "which", "who", "all", "any", "into", "about", "than", "then", "also", "been",
    "being", "may", "might", "must", "shall", "here", "there", "more", "most",
    "some", "such", "only", "very", "just", "over", "under", "after", "before",
    "between", "through", "during", "within", "without", "option", "case", "way"
}

CONVERSATIONAL_FILLERS = {
    "certainly", "here is", "hello", "good morning", "good afternoon",
    "with pleasure", "of course", "here is the answer", "hope this helps"
}


class FaithfulnessEvaluator:
    """Factual Faithfulness Evaluator with Atomic Claim Decomposition."""

    @staticmethod
    def decompose_claims(text: str) -> List[str]:
        """Splits the generated answer into unitary atomic claims."""
        # Split on terminal punctuation (. ? ! or newline)
        raw_sentences = re.split(r"[.!?\n]+", text)
        claims = []
        for s in raw_sentences:
            cleaned = s.strip()
            # Ignore empty, overly short, or purely conversational filler sentences
            if len(cleaned) > 10 and not any(filler in cleaned.lower() for filler in CONVERSATIONAL_FILLERS):
                claims.append(cleaned)
        return claims or ([text.strip()] if text.strip() else [])

    @staticmethod
    def _is_claim_supported(claim: str, context: str) -> bool:
        """Checks whether a specific atomic claim has semantic and numerical support in the context."""
        claim_lower = claim.lower()
        context_lower = context.lower()

        # 1. Strict numerical integrity check
        claim_numbers = set(re.findall(r"\b\d+(?:[.,]\d+)?\b", claim_lower))
        ctx_numbers = set(re.findall(r"\b\d+(?:[.,]\d+)?\b", context_lower))
        if claim_numbers - ctx_numbers:
            return False  # Hallucinated number not present in the context

        # 2. Informative token check (nouns / entities)
        words = re.findall(r"\b\w+\b", claim_lower)
        informative_tokens = [w for w in words if len(w) > 2 and w not in STOPWORDS]
        if not informative_tokens:
            return True

        # At least 60% of the claim's informative terms must appear in the context
        matching_tokens = [w for w in informative_tokens if w in context_lower]
        coverage = len(matching_tokens) / len(informative_tokens)
        return coverage >= 0.60

    def evaluate(self, generated_answer: str, context: str) -> Dict[str, Any]:
        """
        Computes the answer faithfulness metric based on the ratio of supported atomic claims:
            Faithfulness = (supported claims) / (total claims)
        """
        if not context or not generated_answer:
            return {
                "score": 0.0,
                "reason": "Empty context or answer",
                "claims": [],
                "supported_claims": [],
                "unsupported_claims": [],
                "is_faithful": False
            }

        claims = self.decompose_claims(generated_answer)
        if not claims:
            return {
                "score": 1.0,
                "reason": "No informative claims identified",
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
