import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class EvalObservability:
    """Rastreamento de Scores de Avaliação no Langfuse."""

    def __init__(self) -> None:
        self.client = None
        self._init_client()

    def _init_client(self) -> None:
        try:
            from langfuse import Langfuse
            from app.config import settings
            self.client = Langfuse(
                public_key=settings.LANGFUSE_PUBLIC_KEY,
                secret_key=settings.LANGFUSE_SECRET_KEY,
                host=settings.LANGFUSE_HOST
            )
            logger.info("Langfuse Client inicializado no Evaluation Suite.")
        except Exception as e:
            logger.warning(f"Langfuse SDK indisponível. Evaluator operando offline: {e}")
            self.client = None

    def log_evaluation_scores(self, test_case_id: str, scores: Dict[str, float]) -> Optional[str]:
        """
        Grava os scores de avaliação de um caso de teste no Langfuse.
        """
        if not self.client:
            return None

        try:
            if hasattr(self.client, "trace"):
                trace = self.client.trace(
                    name=f"eval_run_{test_case_id}",
                    metadata=scores,
                    tags=["eval_suite", "offline_benchmark"]
                )
                for metric_name, score_val in scores.items():
                    if hasattr(trace, "score"):
                        trace.score(
                            name=metric_name,
                            value=float(score_val)
                        )
                return getattr(trace, "id", f"trace-{test_case_id}")
            return f"trace-{test_case_id}"
        except Exception as e:
            logger.error(f"Erro ao registrar scores no Langfuse: {e}")
            return None


eval_obs = EvalObservability()
