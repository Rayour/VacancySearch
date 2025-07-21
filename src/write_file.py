import datetime
import json
import logging
import os.path
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

ROOT_PATH = Path(__file__).resolve().parents[1]
date_today = datetime.datetime.today().strftime("%d-%m-%Y")
file_name = f"{date_today}_logs.log"
log_path = os.path.join(ROOT_PATH, "logs", file_name)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=log_path,
    filemode="a",
    encoding="utf-8",
)
logger = logging.getLogger("write_file")


class WriteDataToFile(ABC):
    """Абстрактный класс для сохранения данных в файл"""

    data: Any
    file_path: str

    def __init__(self, data: Any, file_path: str) -> None:
        """Метод инициализации объекта абстрактного класса для записи данных в файл"""

        self.data = data
        self.file_path = file_path

    @abstractmethod
    def write_data(self) -> None:
        """Абстрактный метод для записи данных в файл"""
        pass


class WriteDataToJson(WriteDataToFile):
    """Класс для записи данных в JSON файл"""

    def write_data(self) -> None:
        """Метод для сохранения данных в JSON файл"""

        try:
            with open(os.path.join(ROOT_PATH, self.file_path), 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=4)
        except TypeError as e:
            logger.critical(f"Некорректный JSON: {e}")


if __name__ == "__main__":
    json_writer = WriteDataToJson({"data": "some data"}, os.path.join("data", "vacancies.json"))
    json_writer.write_data()
