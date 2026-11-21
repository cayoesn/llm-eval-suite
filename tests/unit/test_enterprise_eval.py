import pytest
from app.evaluators.synthetic_generator import SyntheticDatasetGenerator, synthetic_generator
from app.evaluators.ragas_deepeval import RagasDeepEvalEngine, ragas_engine
from app.evaluators.geval import GEvalEvaluator
from app.evaluators.faithfulness import FaithfulnessEvaluator


def test_synthetic_dataset_generator():
    doc = "StoreCore AI is a sales intelligence platform. It supports RAG powered by a Knowledge Graph. The negotiation FSM enforces discount rules without hallucination."
    dataset = synthetic_generator.generate_from_raw_text(doc, num_samples=2)

    assert len(dataset) == 2
    assert dataset[0].question is not None
    assert len(dataset[0].context) == 2


def test_ragas_metrics_evaluation():
    question = "What is the order delivery timeframe?"
    generated_answer = "The order delivery timeframe is 3 business days."
    retrieved_contexts = ["The standard delivery timeframe for orders is 3 business days."]
    ground_truth = "3 business days"

    metrics = ragas_engine.evaluate_rag_triad(
        question=question,
        generated_answer=generated_answer,
        retrieved_contexts=retrieved_contexts,
        ground_truth=ground_truth,
    )

    assert metrics.faithfulness > 0.5
    assert metrics.hallucination_rate < 0.5
    assert metrics.overall_rag_score > 0.0


def test_geval_evaluator_rubrics():
    evaluator = GEvalEvaluator()
    res = evaluator.evaluate(
        question="What is the status of my order?",
        generated_answer="Your order is in transit and will arrive tomorrow.",
        ground_truth="Order in transit arriving tomorrow.",
    )

    assert res["score"] > 0.5
    assert "rubrics_breakdown" in res
    assert res["is_approved"] is True


def test_atomic_claim_decomposition_faithfulness():
    """Validates factual faithfulness decomposed into atomic claims with controlled hallucination."""
    evaluator = FaithfulnessEvaluator()
    context = (
        "The Enterprise plan costs 99 dollars per month. "
        "It includes 24-hour support and automatic daily backups."
    )
    # Answer containing 3 claims:
    # 1. The Enterprise plan costs 99 dollars per month (Supported)
    # 2. The plan includes 24-hour support (Supported)
    # 3. The plan offers 100 terabytes of free storage (Complete hallucination)
    answer = (
        "The Enterprise plan costs 99 dollars per month. "
        "It includes 24-hour support. "
        "Additionally, it offers 100 terabytes of free storage."
    )

    res = evaluator.evaluate(answer, context)

    assert res["total_claims"] == 3
    assert len(res["supported_claims"]) == 2
    assert len(res["unsupported_claims"]) == 1
    assert abs(res["score"] - 0.667) < 0.01
    assert res["is_faithful"] is False


def test_geval_cohens_kappa_inter_judge_agreement():
    """Validates Cohen's Kappa statistical agreement coefficient between two LLM judges."""
    evaluator = GEvalEvaluator()

    # High agreement scenario
    judge_1 = [True, True, False, True, False, True, False, False, True, True]
    judge_2 = [True, True, False, True, False, True, False, False, True, False]  # 9/10 identical

    kappa_high = evaluator.calculate_cohens_kappa(judge_1, judge_2)
    assert kappa_high > 0.70

    # Disagreement / noise scenario
    judge_noisy = [not x for x in judge_1]
    kappa_low = evaluator.calculate_cohens_kappa(judge_1, judge_noisy)
    assert kappa_low <= 0.0
