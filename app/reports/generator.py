import json
import os
from typing import Dict, Any, List


class ReportGenerator:
    """Gerador de Relatórios Analíticos de Avaliação de LLMs."""

    @staticmethod
    def generate_json_report(eval_results: List[Dict[str, Any]], output_path: str) -> str:
        """Salva os resultados detalhados em formato JSON."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(eval_results, f, indent=2, ensure_ascii=False)
        return output_path

    @staticmethod
    def generate_markdown_report(summary: Dict[str, Any], eval_results: List[Dict[str, Any]], output_path: str) -> str:
        """Gera um relatório sintético e bonito em Markdown."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        md_content = f"""# Relatório Analítico de Avaliação de LLMs 📊

> **Resultado Geral do Benchmark:** {"🟩 APROVADO" if summary.get("passed") else "🟥 REPROVADO"}

---

## 📈 Resumo das Métricas do Golden Dataset

| Métrica | Média Obtida | SLA Mínimo | Status |
| :--- | :---: | :---: | :---: |
| **Faithfulness (Fidedignidade)** | `{summary.get("avg_faithfulness", 0.0):.2f}` | `0.80` | {"✅ PASS" if summary.get("avg_faithfulness", 0.0) >= 0.80 else "❌ FAIL"} |
| **Answer Relevance (Relevância)** | `{summary.get("avg_relevance", 0.0):.2f}` | `0.80` | {"✅ PASS" if summary.get("avg_relevance", 0.0) >= 0.80 else "❌ FAIL"} |
| **G-Eval (LLM-as-a-Judge)** | `{summary.get("avg_geval", 0.0):.2f}` | `0.75` | {"✅ PASS" if summary.get("avg_geval", 0.0) >= 0.75 else "❌ FAIL"} |

---

## 🔍 Detalhamento dos Casos de Teste (Casos de Referência)

"""
        for res in eval_results:
            md_content += f"""### Test Case `{res.get("id")}` - Domain: **{res.get("domain")}**
- **Pergunta:** {res.get("question")}
- **Contexto:** *"{res.get("context")}"*
- **Resposta Gerada:** *"{res.get("generated_answer")}"*
- **Ground Truth:** *"{res.get("ground_truth")}"*
- **Pontuações:**
  - Faithfulness: `{res.get("faithfulness_score")}`
  - Relevance: `{res.get("relevance_score")}`
  - G-Eval Score: `{res.get("geval_score")}`

---
"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return output_path
