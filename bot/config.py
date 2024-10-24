from functools import lru_cache

from environs import Env
from pydantic import SecretStr, NatsDsn
from pydantic_settings import BaseSettings

env = Env()
env.read_env()


class Config(BaseSettings):
    bot_token: SecretStr

    db_url: SecretStr
    nats_servers: list[NatsDsn]

    webhook: bool
    debug: bool

    flood_timeout: float


@lru_cache(maxsize=1)
def parse_config() -> Config:
    return Config()
