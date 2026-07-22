import json
import os
import pytest
from app.config import settings
from app.evaluators.faithfulness import FaithfulnessEvaluator
from app.evaluators.relevance import AnswerRelevanceEvaluator
from app.evaluators.geval import GEvalEvaluator
from app.reports.generator import ReportGenerator
from app.observability import eval_obs


@pytest.fixture
def golden_dataset():
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "app", "data", "golden_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_evaluators_unit():
    faith_eval = FaithfulnessEvaluator()
    rel_eval = AnswerRelevanceEvaluator()
    geval_eval = GEvalEvaluator()

    # Test Faithfulness
    f_res = faith_eval.evaluate(
        generated_answer="O prazo eh 2 a 4 dias uteis.",
        context="O prazo de entrega eh de 2 a 4 dias uteis para o RJ."
    )
    assert f_res["score"] >= 0.80
    assert f_res["is_faithful"] is True

    # Test Relevance
    r_res = rel_eval.evaluate(
        question="Qual o prazo de entrega para SP?",
        generated_answer="O prazo de entrega para SP eh de 2 dias uteis."
    )
    assert r_res["score"] >= 0.70

    # Test G-Eval
    g_res = geval_eval.evaluate(
        question="Voces aceitam Pix?",
        generated_answer="Sim! Aceitamos pagamento via Pix.",
        ground_truth="Sim, aceitamos Pix."
    )
    assert g_res["score"] >= 0.75


def test_golden_dataset_offline_benchmark(golden_dataset):
    faith_eval = FaithfulnessEvaluator()
    rel_eval = AnswerRelevanceEvaluator()
    geval_eval = GEvalEvaluator()

    results = []
    faith_scores = []
    rel_scores = []
    geval_scores = []

    for item in golden_dataset:
        f_res = faith_eval.evaluate(item["generated_answer"], item["context"])
        r_res = rel_eval.evaluate(item["question"], item["generated_answer"])
        g_res = geval_eval.evaluate(item["question"], item["generated_answer"], item["ground_truth"])

        faith_scores.append(f_res["score"])
        rel_scores.append(r_res["score"])
        geval_scores.append(g_res["score"])

        eval_data = {
            "id": item["id"],
            "domain": item["domain"],
            "question": item["question"],
            "context": item["context"],
            "ground_truth": item["ground_truth"],
            "generated_answer": item["generated_answer"],
            "faithfulness_score": f_res["score"],
            "relevance_score": r_res["score"],
            "geval_score": g_res["score"]
        }
        results.append(eval_data)

        # Log scores no Langfuse
        eval_obs.log_evaluation_scores(
            test_case_id=item["id"],
            scores={
                "faithfulness": f_res["score"],
                "relevance": r_res["score"],
                "geval": g_res["score"]
            }
        )

    avg_faith = sum(faith_scores) / len(faith_scores)
    avg_rel = sum(rel_scores) / len(rel_scores)
    avg_geval = sum(geval_scores) / len(geval_scores)

    summary = {
        "avg_faithfulness": round(avg_faith, 2),
        "avg_relevance": round(avg_rel, 2),
        "avg_geval": round(avg_geval, 2),
        "passed": (
            avg_faith >= settings.MIN_FAITHFULNESS_SCORE and
            avg_rel >= settings.MIN_RELEVANCE_SCORE and
            avg_geval >= settings.MIN_GEVAL_SCORE
        )
    }

    # Gera relatórios analíticos em JSON e Markdown
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    ReportGenerator.generate_json_report(results, os.path.join(reports_dir, "eval_details.json"))
    ReportGenerator.generate_markdown_report(summary, results, os.path.join(reports_dir, "eval_summary.md"))

    # Validações de SLA para aprovação do teste
    assert avg_faith >= settings.MIN_FAITHFULNESS_SCORE, f"Faithfulness abaixo do SLA: {avg_faith} < {settings.MIN_FAITHFULNESS_SCORE}"
    assert avg_rel >= settings.MIN_RELEVANCE_SCORE, f"Relevance abaixo do SLA: {avg_rel} < {settings.MIN_RELEVANCE_SCORE}"
    assert avg_geval >= settings.MIN_GEVAL_SCORE, f"G-Eval abaixo do SLA: {avg_geval} < {settings.MIN_GEVAL_SCORE}"
