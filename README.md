# 📊 LLM Evaluation Suite (Enterprise Edition)

Suíte Industrial de Avaliação e Benchmark para Aplicações LLM com **Ragas**, **DeepEval**, **G-Eval** e **Geração Sintética de Dados**.

## 🌟 Arquitetura & Recursos Big-Tech
- **Synthetic Data Generator**: Geração automatizada de pares de pergunta/resposta e contextos para testes de estresse.
- **Ragas & DeepEval Metrics Engine**: Avaliação quantitativa de *Faithfulness*, *Answer Relevancy*, *Context Recall* e *Context Precision*.
- **G-Eval LLM-as-a-Judge**: Avaliação qualitativa baseada em LLM com raciocínio explicável via *Chain-of-Thought* (CoT).

## 🚀 Como Executar no Docker
```bash
docker compose up -d --build
```

## 🧪 Testes Unitários e Integração (>96% Cobertura)
```bash
docker run --rm -v $(pwd):/app -w /app python:3.12-slim bash -c "pip install pytest pytest-asyncio pytest-cov pydantic pydantic-settings httpx fastapi uvicorn && PYTHONPATH=. pytest"
```
