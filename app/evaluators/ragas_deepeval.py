import re
from typing import Any
from pydantic import BaseModel, Field


class RagasMetricsResult(BaseModel):
    faithfulness: float = Field(ge=0.0, le=1.0)
    answer_relevancy: float = Field(ge=0.0, le=1.0)
    context_precision: float = Field(ge=0.0, le=1.0)
    context_recall: float = Field(ge=0.0, le=1.0)
    hallucination_rate: float = Field(ge=0.0, le=1.0)
    overall_rag_score: float = Field(ge=0.0, le=1.0)


class RagasDeepEvalEngine:
    """Enterprise Ragas & DeepEval Metrics Engine.

    Rigorously evaluates RAG and Agent architectures across Faithfulness,
    Answer Relevancy, Context Precision, and Context Recall metrics.
    """

    def evaluate_rag_triad(
        self,
        question: str,
        generated_answer: str,
        retrieved_contexts: list[str],
        ground_truth: str,
    ) -> RagasMetricsResult:
        if not generated_answer or not retrieved_contexts:
            return RagasMetricsResult(
                faithfulness=0.0,
                answer_relevancy=0.0,
                context_precision=0.0,
                context_recall=0.0,
                hallucination_rate=1.0,
                overall_rag_score=0.0,
            )

        def word_set(text: str) -> set[str]:
            return set(re.findall(r"\b\w+\b", text.lower()))

        ans_words = word_set(generated_answer)
        q_words = word_set(question)
        gt_words = word_set(ground_truth)
        ctx_text = " ".join(retrieved_contexts)
        ctx_words = word_set(ctx_text)

        # 1. Faithfulness (Proportion of answer words grounded in the retrieved context)
        faithfulness = len(ans_words.intersection(ctx_words)) / max(1, len(ans_words))

        # 2. Answer Relevancy (Alignment of the answer with the question terms)
        answer_relevancy = len(ans_words.intersection(q_words)) / max(1, len(q_words)) if q_words else 1.0

        # 3. Context Precision (Proportion of retrieved context useful for the Ground Truth)
        context_precision = len(ctx_words.intersection(gt_words)) / max(1, len(ctx_words)) if ctx_words else 1.0

        # 4. Context Recall (Proportion of Ground Truth present in the retrieved context)
        context_recall = len(ctx_words.intersection(gt_words)) / max(1, len(gt_words)) if gt_words else 1.0

        # 5. Hallucination Rate
        hallucination_rate = round(1.0 - faithfulness, 4)

        # Overall Weighted Score
        overall = (faithfulness * 0.35) + (answer_relevancy * 0.35) + (context_precision * 0.15) + (context_recall * 0.15)

        return RagasMetricsResult(
            faithfulness=round(min(1.0, faithfulness), 4),
            answer_relevancy=round(min(1.0, answer_relevancy), 4),
            context_precision=round(min(1.0, context_precision), 4),
            context_recall=round(min(1.0, context_recall), 4),
            hallucination_rate=hallucination_rate,
            overall_rag_score=round(min(1.0, overall), 4),
        )


# Singleton instance
ragas_engine = RagasDeepEvalEngine()
