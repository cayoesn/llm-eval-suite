import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class EvalObservability:
    """Evaluation Score Tracing in Langfuse."""

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
            logger.info("Langfuse client initialized in Evaluation Suite.")
        except Exception as e:
            logger.warning(f"Langfuse SDK unavailable. Evaluator running offline: {e}")
            self.client = None

    def log_evaluation_scores(self, test_case_id: str, scores: Dict[str, float]) -> Optional[str]:
        """
        Records evaluation scores for a test case in Langfuse.
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
            logger.error(f"Failed to log scores to Langfuse: {e}")
            return None


eval_obs = EvalObservability()
