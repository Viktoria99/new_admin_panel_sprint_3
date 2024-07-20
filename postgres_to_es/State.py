import abc
from typing import Any, Dict

from JsonFileParsing import JsonFileParsing
from settings import STATE_PATH


class BaseState(abc.ABC):
    @abc.abstractmethod
    def set_state(self, key: str, value: Any) -> None:
        pass

    @abc.abstractmethod
    def get_state(self, key: str) -> Any:
        pass


class State(BaseState):
    def __init__(self) -> None:
        self.file_context = JsonFileParsing(STATE_PATH)

    def set_state(self, key: str, value: Any) -> None:

        if value is None:
            return None
        self.file_context.save_state({key: value})

    def get_state(self, key: str) -> Any:
        try:
            result = self.file_context.retrieve_state()
            if result.__contains__(key):
                return result[key]
            return None
        except:
            return None
