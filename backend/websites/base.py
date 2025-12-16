from abc import ABC, abstractmethod
from typing import List
from models import Deal


class BaseWebsite(ABC):
    @abstractmethod
    async def login(self, username: str, password: str) -> str:
        """Return auth token"""
        raise NotImplementedError

    @abstractmethod
    async def get_deals(self, token: str) -> List[Deal]:
        raise NotImplementedError