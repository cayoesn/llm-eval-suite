# Relatório Analítico de Avaliação de LLMs 📊

> **Resultado Geral do Benchmark:** 🟥 REPROVADO

---

## 📈 Resumo das Métricas do Golden Dataset

| Métrica | Média Obtida | SLA Mínimo | Status |
| :--- | :---: | :---: | :---: |
| **Faithfulness (Fidedignidade)** | `0.63` | `0.80` | ❌ FAIL |
| **Answer Relevance (Relevância)** | `0.73` | `0.80` | ❌ FAIL |
| **G-Eval (LLM-as-a-Judge)** | `0.86` | `0.75` | ✅ PASS |

---

## 🔍 Detalhamento dos Casos de Teste (Casos de Referência)

### Test Case `tc_001` - Domain: **E-commerce**
- **Pergunta:** Qual eh o prazo de entrega para o Rio de Janeiro?
- **Contexto:** *"Entregas para a regiao Sudeste (SP, RJ, MG, ES) possuem prazo padrao de 2 a 4 dias uteis. Para capitais, a entrega expressa ocorre em ate 24 horas."*
- **Resposta Gerada:** *"Para o Rio de Janeiro, o prazo de entrega padrao eh de 2 a 4 dias uteis, com opcao de entrega expressa em ate 24 horas."*
- **Ground Truth:** *"O prazo padrao para o Rio de Janeiro eh de 2 a 4 dias uteis, podendo ser entregue em ate 24 horas via entrega expressa."*
- **Pontuações:**
  - Faithfulness: `0.69`
  - Relevance: `0.97`
  - G-Eval Score: `0.91`

---
### Test Case `tc_002` - Domain: **Suporte Tecnico**
- **Pergunta:** Como reiniciar o roteador Wi-Fi de forma segura?
- **Contexto:** *"Para reiniciar o roteador, desligue o cabo de energia da tomada, aguarde 30 segundos para a desenergizacao completa dos capacitores e reconecte o cabo."*
- **Resposta Gerada:** *"Para reiniciar seu roteador com seguranca, remova a fonte de energia da tomada, aguarde 30 segundos e conecte novamente."*
- **Ground Truth:** *"Desconecte o cabo de energia da tomada, espere 30 segundos e ligue-o novamente."*
- **Pontuações:**
  - Faithfulness: `0.5`
  - Relevance: `0.62`
  - G-Eval Score: `0.83`

---
### Test Case `tc_003` - Domain: **Financeiro**
- **Pergunta:** Quais sao as taxas de cancelamento do plano anual?
- **Contexto:** *"O cancelamento do plano anual antes do término de 12 meses implica taxa administrativa de 10% sobre o saldo devedor restante do contrato."*
- **Resposta Gerada:** *"Se voce cancelar o plano anual antes de 12 meses, havera uma taxa administrativa de 10% cobrada sobre o saldo restante do contrato."*
- **Ground Truth:** *"A taxa de cancelamento antecipado eh de 10% calculada sobre o valor dos meses restantes do contrato."*
- **Pontuações:**
  - Faithfulness: `0.67`
  - Relevance: `0.57`
  - G-Eval Score: `0.78`

---
### Test Case `tc_004` - Domain: **Atendimento**
- **Pergunta:** Voces aceitam pagamento via Pix?
- **Contexto:** *"Aceitamos pagamentos via Pix com aprovacao instantanea, cartao de credito em ate 12x e boleto bancario."*
- **Resposta Gerada:** *"Sim! Aceitamos pagamento via Pix com aprovacao instantanea na hora."*
- **Ground Truth:** *"Sim, aceitamos Pix com aprovacao imediata."*
- **Pontuações:**
  - Faithfulness: `0.67`
  - Relevance: `0.78`
  - G-Eval Score: `0.91`

---
