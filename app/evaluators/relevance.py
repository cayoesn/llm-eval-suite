import re
from typing import Dict, Any

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
    "will", "can", "could", "would", "should", "have", "has", "had", "not", "but",
    "you", "your", "our", "its", "they", "their", "what", "when", "where", "how",
    "which", "who", "all", "any", "into", "about", "than", "then", "also", "been",
    "being", "may", "might", "must", "shall", "here", "there", "more", "most",
    "some", "such", "only", "very", "just", "over", "under", "after", "before",
    "between", "through", "during", "within", "without", "option", "case", "way",
    "does", "did"
}


class AnswerRelevanceEvaluator:
    """Evaluator for Answer Relevance and Alignment with the Question."""

    def evaluate(self, question: str, generated_answer: str) -> Dict[str, Any]:
        """
        Computes the relevance metric of the generated answer with respect to the question.
        """
        if not question or not generated_answer:
            return {"score": 0.0, "reason": "Empty question or answer"}

        def tokenize(text: str):
            words = re.findall(r"\b\w+\b", text.lower())
            return set(w for w in words if len(w) > 2 and w not in STOPWORDS)

        q_tokens = tokenize(question)
        ans_tokens = tokenize(generated_answer)

        if not q_tokens:
            return {"score": 1.0, "reason": "Question contains no informative keywords"}

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
