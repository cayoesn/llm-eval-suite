# LLM Evaluation Analytics Report 📊

> **Overall Benchmark Result:** 🟩 PASSED

---

## 📈 Golden Dataset Metrics Summary

| Metric | Average Score | Minimum SLA | Status |
| :--- | :---: | :---: | :---: |
| **Faithfulness** | `1.00` | `0.80` | ✅ PASS |
| **Answer Relevance** | `0.95` | `0.80` | ✅ PASS |
| **G-Eval (LLM-as-a-Judge)** | `0.95` | `0.75` | ✅ PASS |

---

## 🔍 Test Case Breakdown (Reference Cases)

### Test Case `tc_001` - Domain: **E-commerce**
- **Question:** What is the delivery timeframe for New York?
- **Context:** *"Deliveries to the Northeast region (NY, NJ, PA, MA) have a standard delivery timeframe of 2 to 4 business days. For major cities like New York, express delivery arrives within 24 hours."*
- **Generated Answer:** *"For New York, the standard delivery timeframe is 2 to 4 business days, with an express delivery option within 24 hours."*
- **Ground Truth:** *"The standard delivery timeframe for New York is 2 to 4 business days, with express delivery available within 24 hours."*
- **Scores:**
  - Faithfulness: `1.0`
  - Relevance: `1.0`
  - G-Eval Score: `0.96`

---
### Test Case `tc_002` - Domain: **Technical Support**
- **Question:** How do I safely restart the Wi-Fi router?
- **Context:** *"To safely restart the Wi-Fi router, unplug the power cable from the outlet, wait 30 seconds for the capacitors to fully discharge, and plug the power cable back in."*
- **Generated Answer:** *"To safely restart your Wi-Fi router, unplug the power cable from the outlet, wait 30 seconds, and plug it back in."*
- **Ground Truth:** *"Unplug the power cable from the outlet, wait 30 seconds, and plug it back in."*
- **Scores:**
  - Faithfulness: `1.0`
  - Relevance: `1.0`
  - G-Eval Score: `0.98`

---
### Test Case `tc_003` - Domain: **Finance**
- **Question:** What are the cancellation fees for the annual plan?
- **Context:** *"Canceling the annual plan before the end of 12 months incurs an administrative cancellation fee of 10% on the remaining contract balance."*
- **Generated Answer:** *"If you cancel the annual plan before 12 months, there is a 10% administrative cancellation fee charged on the remaining contract balance."*
- **Ground Truth:** *"The early cancellation fee for the annual plan is 10% calculated on the remaining contract balance."*
- **Scores:**
  - Faithfulness: `1.0`
  - Relevance: `0.82`
  - G-Eval Score: `0.89`

---
### Test Case `tc_004` - Domain: **Customer Support**
- **Question:** Do you accept instant bank transfer payments?
- **Context:** *"We accept instant bank transfer payments with immediate approval, credit cards in up to 12 installments, and wire transfers."*
- **Generated Answer:** *"Yes! We accept instant bank transfer payments with immediate approval."*
- **Ground Truth:** *"Yes, we accept instant bank transfer payments with immediate approval."*
- **Scores:**
  - Faithfulness: `1.0`
  - Relevance: `1.0`
  - G-Eval Score: `0.98`

---
