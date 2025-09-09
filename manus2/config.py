from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "manus2"
    version: str = "0.1.1"
    log_level: str = "INFO"

    # Adapter configuration
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    ollama_base_url: str = "http://localhost:11434"

    github_token: str | None = None
    repo_owner: str | None = None
    repo_name: str | None = None

    n8n_base_url: str | None = None
    n8n_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
