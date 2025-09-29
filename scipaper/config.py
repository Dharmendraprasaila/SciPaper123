from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str
    supabase_db_url: str

    # Elasticsearch
    elasticsearch_url: str
    elasticsearch_api_key: str

    # Neo4j
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str

    # Celery
    redis_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
