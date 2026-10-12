import pytest
from app.evaluators.synthetic_generator import SyntheticDatasetGenerator, synthetic_generator
from app.evaluators.ragas_deepeval import RagasDeepEvalEngine, ragas_engine
from app.evaluators.geval import GEvalEvaluator
from app.evaluators.faithfulness import FaithfulnessEvaluator


def test_synthetic_dataset_generator():
    doc = "O StoreCore AI é um sistema de vendas. Ele possui suporte a RAG com Grafo de Conhecimento. A FSM de negociação garante descontos sem alucinação."
    dataset = synthetic_generator.generate_from_raw_text(doc, num_samples=2)
    
    assert len(dataset) == 2
    assert dataset[0].question is not None
    assert len(dataset[0].context) == 2


def test_ragas_metrics_evaluation():
    question = "Qual é o prazo de entrega do pedido?"
    generated_answer = "O prazo de entrega do pedido é de 3 dias úteis."
    retrieved_contexts = ["O prazo de entrega padrão para pedidos é de 3 dias úteis."]
    ground_truth = "3 dias úteis"

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
        question="Qual o status do meu pedido?",
        generated_answer="O seu pedido está em transporte e chega amanhã.",
        ground_truth="Pedido em transporte com entrega amanhã.",
    )

    assert res["score"] > 0.5
    assert "rubrics_breakdown" in res
    assert res["is_approved"] is True


def test_atomic_claim_decomposition_faithfulness():
    """Valida a fidelidade factual decomposta em claims atômicos com alucinação controlada."""
    evaluator = FaithfulnessEvaluator()
    context = (
        "O plano Enterprise custa 99 dólares por mês. "
        "Ele inclui suporte 24 horas por dia e backup diário automático."
    )
    # Resposta com 3 claims:
    # 1. O plano Enterprise custa 99 dólares mensais (Suportado)
    # 2. O plano inclui suporte 24 horas por dia (Suportado)
    # 3. O plano oferece 100 terabytes de armazenamento gratuito (Alucinação total)
    answer = (
        "O plano Enterprise custa 99 dólares mensais. "
        "Ele inclui suporte 24 horas por dia. "
        "Além disso, ele oferece 100 terabytes de armazenamento gratuito."
    )

    res = evaluator.evaluate(answer, context)

    assert res["total_claims"] == 3
    assert len(res["supported_claims"]) == 2
    assert len(res["unsupported_claims"]) == 1
    assert abs(res["score"] - 0.667) < 0.01
    assert res["is_faithful"] is False


def test_geval_cohens_kappa_inter_judge_agreement():
    """Valida o cálculo do coeficiente de concordância estatística Cohen's Kappa entre dois juízes LLM."""
    evaluator = GEvalEvaluator()

    # Cenário de alta concordância
    judge_1 = [True, True, False, True, False, True, False, False, True, True]
    judge_2 = [True, True, False, True, False, True, False, False, True, False]  # 9/10 iguais

    kappa_high = evaluator.calculate_cohens_kappa(judge_1, judge_2)
    assert kappa_high > 0.70

    # Cenário de desacordo / ruído
    judge_noisy = [not x for x in judge_1]
    kappa_low = evaluator.calculate_cohens_kappa(judge_1, judge_noisy)
    assert kappa_low <= 0.0
