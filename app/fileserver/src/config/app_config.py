from pydantic_settings import BaseSettings


class Config(BaseSettings):
    env: str
    persistance_type: str
    max_file_size: int
    allowed_files: list[str]
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_s3_bucket: str | None = None


config = Config()