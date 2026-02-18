from collections import deque


class HistoryStore:
    def __init__(self, max_items: int = 100) -> None:
        self._items: deque[str] = deque(maxlen=max_items)

    def add(self, expression: str, result: str) -> None:
        self._items.append(f"{expression} = {result}")

    def all(self) -> list[str]:
        return list(self._items)

    def clear(self) -> None:
        self._items.clear()
import os