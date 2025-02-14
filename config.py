from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool
    TESTING: bool

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Config()