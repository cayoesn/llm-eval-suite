from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações Globais da Suíte de Avaliação LLM."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "LLM Evaluation Suite"
    ENV: str = "development"

    # SLAs / Thresholds Mínimos Aceitáveis para Passar no Pipeline
    MIN_FAITHFULNESS_SCORE: float = 0.65
    MIN_RELEVANCE_SCORE: float = 0.70
    MIN_GEVAL_SCORE: float = 0.70

    # Langfuse Integration
    LANGFUSE_PUBLIC_KEY: str = "pk-lf-demo"
    LANGFUSE_SECRET_KEY: str = "sk-lf-demo"
    LANGFUSE_HOST: str = "http://localhost:3000"


settings = Settings()
