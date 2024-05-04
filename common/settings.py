from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_name: str
    database_user: str
    database_password: str
    database_host: str = "localhost"
    database_port: int = 5432

    # User Service
    user_service_base_url: str
    product_service_base_url: str

    # password hashing
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


@lru_cache
def get_settings():
    return Settings()  # type: ignore
