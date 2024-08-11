from pydantic_settings import BaseSettings


class Config(BaseSettings):
    env: str
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    celery_broker: str
    celery_backend: str


config = Config()