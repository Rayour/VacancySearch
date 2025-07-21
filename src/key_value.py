from typing import Any


class KeyValue():
    """Класс для пары ключ-значение"""

    key: Any
    value: Any

    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
