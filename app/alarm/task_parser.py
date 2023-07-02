from dataclasses import dataclass
from typing import Any

import orjson
from dacite import from_dict

from app.alarm.exceptions import ParseInvalidArgumentException, ParseInvalidFormatException


@dataclass(frozen=True)
class AlarmTask:
    keys: list[str]
    data: dict


class AlarmTaskParser:
    def __init__(self, raw_task: list[bytes]) -> None:
        self._alarm_task: AlarmTask = self._parse_raw_task(raw_task=raw_task)

    @staticmethod
    def _parse_raw_task(raw_task: bytes):
        try:
            loaded_task = orjson.loads(raw_task[1])
            return from_dict(data_class=AlarmTask, data=loaded_task)

        except Exception as exc:
            raise ParseInvalidFormatException(message=str(exc))

    @staticmethod
    def _validate_empty(data: Any, category: str):
        if not data:
            raise ParseInvalidArgumentException(message=f"{category} is empty")

    def parse_subscribers(self) -> list[str]:
        self._validate_empty(data=self._alarm_task.keys, category="subscribers")
        return self._alarm_task.keys

    def parse_message(self) -> dict:
        self._validate_empty(data=self._alarm_task.data, category="message")
        return self._alarm_task.data
