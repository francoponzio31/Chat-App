from pydantic_settings import BaseSettings


class Config(BaseSettings):
    env: str
    persistance_type: str
    max_file_size: int
    allowed_files: list[str]

config = Config()