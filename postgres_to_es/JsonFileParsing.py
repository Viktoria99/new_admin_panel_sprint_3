import json
from typing import Any, Dict

from base_storage import BaseStorage


class JsonFileParsing(BaseStorage):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(state, file)

    def retrieve_state(self) -> Dict[str, Any]:

        try:
            d = dict()
            with open(self.file_path, 'r') as file:
                for line in file:
                    d.update(json.loads(line))
            return d
        except IOError as error:
            return dict()
