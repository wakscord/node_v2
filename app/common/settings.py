import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from uuid import uuid4

from dotenv import dotenv_values

env_path = Path.joinpath(Path(__file__).parent.parent.parent.resolve(), ".env")
if not os.path.exists(env_path):
    raise Exception("Dotenv is not exists.")


@dataclass(frozen=True)
class Settings:
    NODE_ID: str
    MAX_CONCURRENT: int

    REDIS_URL: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    PROXY_USER: str | None = None
    PROXY_PASSWORD: str | None = None


to_int: Callable[[str, int], int] = lambda value, else_value: int(value) if value else else_value

raw_settings = dotenv_values(env_path)
settings = Settings(
    NODE_ID=f"node_{uuid4()}",
    MAX_CONCURRENT=to_int(raw_settings.get("MAX_CONCURRENT"), 2000),
    REDIS_URL=raw_settings.get("REDIS_URL") or "localhost",
    REDIS_PORT=to_int(raw_settings.get("REDIS_PORT"), 6379),
    REDIS_PASSWORD=raw_settings.get("REDIS_PASSWORD"),
    PROXY_USER=raw_settings.get("PROXY_USER"),
    PROXY_PASSWORD=raw_settings.get("PROXY_PASSWORD"),
)
