from pydantic import BaseSettings


class Settings(BaseSettings):
    database_password: str
    database_username: str
    database_name: str
    database_hostname: str
    database_port: str
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str

    class Config:
        env_file = ".env"


settings = Settings()
