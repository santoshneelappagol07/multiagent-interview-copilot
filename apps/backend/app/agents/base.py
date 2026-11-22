from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        pass
