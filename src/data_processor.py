from typing import List, Dict
from src.interfaces.output_strategy import OutputStrategy


class DataProcessor:

    def __init__(self, strategy: OutputStrategy):
        self._strategy = strategy

    def process(self, data: List[Dict[str, str]]) -> None:
        self._strategy.output(data)
