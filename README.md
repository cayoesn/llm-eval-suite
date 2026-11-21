# 📊 LLM Evaluation Suite (Enterprise Edition)

Production-grade continuous evaluation and factual benchmarking suite for RAG systems and LLM agents featuring **Atomic Claim Decomposition**, **Cohen's Kappa Inter-Judge Agreement**, **Ragas**, **DeepEval**, and **G-Eval**.

---

## 🌟 Architecture & Enterprise Capabilities

- **Atomic Claim Decomposition Faithfulness**:
  - Deterministic decomposition of LLM-generated answers into unitary atomic claims.
  - Contextual factual support verification with strict numerical and entity integrity checks:
    $$\text{Faithfulness} = \frac{\sum_{i=1}^M \mathbb{I}(\text{claim}_i \text{ is supported by context})}{M}$$
- **G-Eval LLM-as-a-Judge with Statistical Calibration**:
  - Weighted evaluation across explainable rubrics (*correctness*, *clarity*, *tone*, *compliance*).
  - Inter-judge agreement measurement via **Cohen's Kappa**:
    $$\kappa = \frac{P_o - P_e}{1 - P_e}$$
    ensuring automated judge scores do not suffer from stochastic bias.
- **RAG Triad & DeepEval Suite**:
  - Multidimensional evaluation of the retrieval pipeline: *Faithfulness*, *Answer Relevancy*, *Context Recall*, and *Context Precision*.
- **Offline Golden Dataset Benchmarking**:
  - Automated regression suite against reference datasets with Markdown and JSON report exports.

---

## 📊 Metrics & Algorithms Matrix

| Evaluation Dimension | Method / Metric | Purpose |
| :--- | :--- | :--- |
| **Factual Hallucination** | Atomic Claim Decomposition | Surgical identification of unsupported claims |
| **Judge Consistency** | Cohen's Kappa ($\kappa$) | Statistical validation of inter-LLM Judge agreement |
| **RAG Quality** | RAG Triad (Context Precision/Recall) | Isolated evaluation of retrieval vs. generation |

---

## 🚀 Running with Docker

```bash
docker compose up -d --build
```

---

## 🧪 Automated Tests (100% Hermetic)

```bash
docker run --rm -v $(pwd):/workspace -w /workspace -e PYTHONPATH=/workspace portfolio-spec-engine:test pytest tests -v --cov=app --cov-report=term-missing
```
