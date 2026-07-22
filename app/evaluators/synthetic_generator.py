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
    
    Gera automaticamente pares de Pergunta/Resposta e Contextos de Teste (Golden Dataset)
    a partir de documentos brutos para benchmark contínuo de RAG e Agentes.
    """

    def generate_from_raw_text(self, document_text: str, num_samples: int = 3) -> list[SyntheticQAPair]:
        sentences = [s.strip() for s in document_text.split(".") if len(s.strip()) > 15]
        dataset: list[SyntheticQAPair] = []

        for i in range(min(num_samples, len(sentences))):
            sentence = sentences[i]
            question = f"O que é afirmado sobre '{sentence[:20]}...'?"
            ground_truth = sentence
            
            # Adiciona contexto ruidoso/distrator para simular RAG real
            distractor = f"Distrator aleatório {random.randint(100, 999)} para teste de precisão de contexto."
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


# Instância Singleton
synthetic_generator = SyntheticDatasetGenerator()
