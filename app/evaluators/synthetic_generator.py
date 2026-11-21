import random
from typing import Any
from pydantic import BaseModel, Field


class SyntheticQAPair(BaseModel):
    id: str
    question: str
    ground_truth: str
    context: list[str]
    question_type: str = "factual"  # factual, reasoning, multi_hop


class SyntheticDatasetGenerator:
    """Enterprise Synthetic Data Generation Engine.

    Automatically generates Question/Answer pairs and Test Contexts (Golden Dataset)
    from raw documents for continuous RAG and Agent benchmarking.
    """

    def generate_from_raw_text(self, document_text: str, num_samples: int = 3) -> list[SyntheticQAPair]:
        sentences = [s.strip() for s in document_text.split(".") if len(s.strip()) > 15]
        dataset: list[SyntheticQAPair] = []

        for i in range(min(num_samples, len(sentences))):
            sentence = sentences[i]
            question = f"What is stated about '{sentence[:20]}...'?"
            ground_truth = sentence

            # Add noisy/distractor context to simulate real-world RAG retrieval
            distractor = f"Random distractor {random.randint(100, 999)} for context precision testing."
            context = [sentence, distractor]

            dataset.append(
                SyntheticQAPair(
                    id=f"syn_qa_{i+1}",
                    question=question,
                    ground_truth=ground_truth,
                    context=context,
                    question_type="factual" if i % 2 == 0 else "reasoning",
                )
            )

        return dataset


# Singleton instance
synthetic_generator = SyntheticDatasetGenerator()
