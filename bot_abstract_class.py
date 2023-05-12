from abc import ABC, abstractmethod
from typing import Any

class BotAbstract(ABC):
    @abstractmethod
    def __init__(self, settings: Any):
        pass

    @abstractmethod
    def get_bot_response(self, text: str) -> str:
        pass
