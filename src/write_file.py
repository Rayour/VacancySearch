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
default_file_path = os.path.join(ROOT_PATH, "data", "vacancies.json")

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

    @abstractmethod
    def write_data(self) -> None:
        """Абстрактный метод для записи данных в файл"""
        pass

    @abstractmethod
    def get_data(self) -> Any:
        """Абстрактный метод для чтения данных в файла"""
        pass

    @abstractmethod
    def delete_data(self) -> None:
        """Абстрактный метод для удаления данных из файла"""
        pass


class WriteDataToJson(WriteDataToFile):
    """Класс для записи данных в JSON файл"""

    data: Any
    __file_path: str

    def __init__(self, data: Any, file_path: str = default_file_path) -> None:
        """Метод инициализации объекта абстрактного класса для записи данных в файл"""

        self.data = data
        self.__file_path = file_path

    def write_data(self) -> None:
        """Метод для сохранения данных в JSON файл"""

        vacancy_list = []

        try:
            with open(os.path.join(ROOT_PATH, self.__file_path), 'r', encoding='utf-8') as file:
                vacancy_list = json.load(file)
        except FileNotFoundError as e:
            logger.info(f"Файл {self.__file_path} не найден: {e}, будет создан новый список")
        except Exception as e:
            logger.warning(f"При попытке чтения данных из файла {self.__file_path} произошла ошибка: {e}, \
список вакансий будет перезаписан")
        finally:
            ids = [item["id"] for item in vacancy_list]
            for vacancy in self.data:
                if not vacancy["id"] in ids:
                    ids.append(vacancy["id"])
                    vacancy_list.append(vacancy)

        try:
            with open(os.path.join(ROOT_PATH, self.__file_path), 'w', encoding='utf-8') as file:
                logger.info(f"Попытка записи данных в файл {self.__file_path}")
                json.dump(vacancy_list, file, ensure_ascii=False, indent=4)
        except TypeError as e:
            logger.critical(f"Некорректный JSON: {e}")
        except Exception as e:
            logger.critical(f"При записи данных в файл произошла ошибка: {e}")
        else:
            logger.info(f"Данные успешно записаны в файл {self.__file_path}")

    def delete_data(self) -> None:
        """Метод для удаления данных из файла"""

        try:
            with open(os.path.join(ROOT_PATH, self.__file_path), 'w', encoding='utf-8') as file:
                logger.info(f"Попытка удаления данных из файла {self.__file_path}")
                file.write("")
        except Exception as e:
            logger.critical(f"При удалении данных из файла произошла ошибка: {e}")
        else:
            logger.info(f"Данные успешно удалены из файла {self.__file_path}")

    def get_data(self) -> Any:
        """Метод для получения данных из файла"""

        try:
            with open(os.path.join(ROOT_PATH, self.__file_path), 'r', encoding='utf-8') as file:
                logger.info(f"Попытка чтения данных из файла {self.__file_path}")
                data = file.read()
        except Exception as e:
            logger.critical(f"При чтении данных из файла произошла ошибка: {e}")
        else:
            logger.info(f"Данные успешно прочитаны из файла {self.__file_path}")
            return data

    @property
    def file_path(self) -> str:
        """Свойство пути к файлу"""

        return self.__file_path


if __name__ == "__main__":
    json_writer = WriteDataToJson({"data": "some data"}, os.path.join("data", "vacancies.json"))
    json_writer.write_data()
