from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Challenge-QA-API"
    app_version: str = "250205"
    debug: bool = True
    dbdebug: bool = True

    connection_type: str = "tcp"
    dbdriver: str = "postgresql+psycopg"
    dbuser: str = "user"
    dbpass: str = "password"
    dbhost: str = "localhost:5432"
    dbschema: str = "challenge"

    port: int = 8000

    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    version: str = "250205"


config = Settings()
