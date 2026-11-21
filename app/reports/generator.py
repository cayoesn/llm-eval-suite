import json
import os
from typing import Dict, Any, List


class ReportGenerator:
    """Analytical Report Generator for LLM Evaluations."""

    @staticmethod
    def generate_json_report(eval_results: List[Dict[str, Any]], output_path: str) -> str:
        """Saves detailed evaluation results in JSON format."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(eval_results, f, indent=2, ensure_ascii=False)
        return output_path

    @staticmethod
    def generate_markdown_report(summary: Dict[str, Any], eval_results: List[Dict[str, Any]], output_path: str) -> str:
        """Generates a clean summary report in Markdown format."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        md_content = f"""# LLM Evaluation Analytics Report 📊

> **Overall Benchmark Result:** {"🟩 PASSED" if summary.get("passed") else "🟥 FAILED"}

---

## 📈 Golden Dataset Metrics Summary

| Metric | Average Score | Minimum SLA | Status |
| :--- | :---: | :---: | :---: |
| **Faithfulness** | `{summary.get("avg_faithfulness", 0.0):.2f}` | `0.80` | {"✅ PASS" if summary.get("avg_faithfulness", 0.0) >= 0.80 else "❌ FAIL"} |
| **Answer Relevance** | `{summary.get("avg_relevance", 0.0):.2f}` | `0.80` | {"✅ PASS" if summary.get("avg_relevance", 0.0) >= 0.80 else "❌ FAIL"} |
| **G-Eval (LLM-as-a-Judge)** | `{summary.get("avg_geval", 0.0):.2f}` | `0.75` | {"✅ PASS" if summary.get("avg_geval", 0.0) >= 0.75 else "❌ FAIL"} |

---

## 🔍 Test Case Breakdown (Reference Cases)

"""
        for res in eval_results:
            md_content += f"""### Test Case `{res.get("id")}` - Domain: **{res.get("domain")}**
- **Question:** {res.get("question")}
- **Context:** *"{res.get("context")}"*
- **Generated Answer:** *"{res.get("generated_answer")}"*
- **Ground Truth:** *"{res.get("ground_truth")}"*
- **Scores:**
  - Faithfulness: `{res.get("faithfulness_score")}`
  - Relevance: `{res.get("relevance_score")}`
  - G-Eval Score: `{res.get("geval_score")}`

---
"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return output_path
