from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisStreamConfig(BaseModel):
    stream: str = "add_stream"
    consumer: str = "add_consumer"
    group: str = "add_group"
    maxlen: int = 1000


class MessageLinksConfig(RedisStreamConfig):
    stream: str = "message_links_stream"
    consumer: str = "message_links_consumer"
    group: str = "message_links_group"


class RedisConfig(BaseModel):
    url: str = "redis://localhost:6379"
    add_stream: RedisStreamConfig = RedisStreamConfig()
    message_links: MessageLinksConfig = MessageLinksConfig()


class RunConfig(BaseModel):
    port: int = 8000
    host: str = "0.0.0.0"


class ProjectConfig(BaseModel):
    name: str = "Home"
    version: str = "0.1.0"
    v1_prefix: str = "v1"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )
    redis: RedisConfig = RedisConfig()
    db: DatabaseConfig
    run: RunConfig = RunConfig()
    project: ProjectConfig = ProjectConfig()


settings = Settings()