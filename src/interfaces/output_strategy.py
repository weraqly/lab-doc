from abc import ABC, abstractmethod
from typing import List, Dict


class OutputStrategy(ABC):

    @abstractmethod
    def output(self, data: List[Dict[str, str]]) -> None:
        pass
