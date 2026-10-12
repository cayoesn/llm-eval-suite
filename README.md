# 📊 LLM Evaluation Suite (Enterprise Edition)

Suíte Industrial de Avaliação Contínua e Benchmark Factual para Sistemas RAG e Agentes LLM com **Atomic Claim Decomposition**, **Cohen's Kappa Inter-Judge Agreement**, **Ragas**, **DeepEval** e **G-Eval**.

---

## 🌟 Arquitetura & Recursos Big-Tech

- **Atomic Claim Decomposition Faithfulness**:
  - Decomposição determinística das respostas geradas pelo LLM em proposições atômicas unitárias.
  - Verificação de suporte factual contextual com checagem estrita de integridade numérica e entidades:
    $$\text{Faithfulness} = \frac{\sum_{i=1}^M \mathbb{I}(\text{claim}_i \text{ tem suporte no contexto})}{M}$$
- **G-Eval LLM-as-a-Judge com Calibração Estatística**:
  - Avaliação ponderada por rúbricas explicáveis (*correctness*, *clarity*, *tone*, *compliance*).
  - Medição de concordância entre múltiplos juízes via **Cohen's Kappa**:
    $$\kappa = \frac{P_o - P_e}{1 - P_e}$$
    garantindo que scores de juízes automáticos não sofram de viés estocástico.
- **RAG Triad & DeepEval Suite**:
  - Avaliação multidimensional do pipeline de recuperação: *Faithfulness*, *Answer Relevancy*, *Context Recall* e *Context Precision*.
- **Offline Golden Dataset Benchmarking**:
  - Suíte de regressão automatizada contra datasets de referência com exportação em Markdown e JSON.

---

## 📊 Matriz de Métricas e Algoritmos

| Dimensão de Avaliação | Método / Métrica | Propósito |
| :--- | :--- | :--- |
| **Alucinação Factual** | Atomic Claim Decomposition | Identificação cirúrgica de proposições não embasadas |
| **Consistência de Juízes** | Cohen's Kappa ($\kappa$) | Validação estatística de concordância inter-LLM Judge |
| **Qualidade RAG** | RAG Triad (Context Precision/Recall) | Avaliação isolada da recuperação vs geração |

---

## 🚀 Como Executar no Docker

```bash
docker compose up -d --build
```

---

## 🧪 Testes Automatizados (100% Hermético)

```bash
docker run --rm -v $(pwd):/workspace -w /workspace -e PYTHONPATH=/workspace portfolio-spec-engine:test pytest tests -v --cov=app --cov-report=term-missing
```
