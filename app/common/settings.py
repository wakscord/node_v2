import os
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from dacite import from_dict
from dotenv import dotenv_values

env_path = Path.joinpath(Path(__file__).parent.parent.parent.resolve(), ".env")
if not os.path.exists(env_path):
    raise Exception("Dotenv is not exists.")

_settings = dotenv_values(env_path)

is_dev = _settings.get("ENV") == "dev"
_settings["NODE_ID"] = "node_dev" if is_dev else f"node_{uuid4()}"


@dataclass(frozen=True)
class Settings:
    ENV: str
    NODE_ID: str
    REDIS_URL: str
    REDIS_PASSWORD: str
    PROXY_USER: str
    PROXY_PASSWORD: str


settings = from_dict(data_class=Settings, data=_settings)
