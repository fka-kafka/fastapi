from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str
    db_hostname: str
    db_port: str
    db_username: str
    db_password: str
    secret_key: str
    algorithm: str
    token_expiry: int

    class Config:
        env_file = ".env"

settings = Settings()
