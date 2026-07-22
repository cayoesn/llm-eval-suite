import pytest
from app.evaluators.synthetic_generator import SyntheticDatasetGenerator, synthetic_generator
from app.evaluators.ragas_deepeval import RagasDeepEvalEngine, ragas_engine
from app.evaluators.geval import GEvalEvaluator


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
