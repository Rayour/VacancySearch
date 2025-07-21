import datetime
import logging
import os.path
from abc import ABC, abstractmethod
from pathlib import Path

import requests

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
logger = logging.getLogger("api_connector")


class ApiConnector(ABC):
    """Абстрактный класс для API взаимодействий"""

    @abstractmethod
    def _get_data(self) -> list:
        """Метод для получения данных по API"""
        pass


class HHApiConnector(ApiConnector):
    """Класс для работы с api HH"""

    __url: str
    __params: dict
    __headers: dict

    def __init__(self, params: dict | None = None, headers: dict | None = None):
        """Метод инициализации объекта абстрактного класса API взаимодействия"""

        self.__url = "https://api.hh.ru/vacancies"
        self.__params = params if params else {}
        self.__headers = headers if headers else {}

    def _get_data(self) -> list:
        data = []
        max_page = 1
        self.__params["page"] = 0
        self.__params["per_page"] = 100
        self.__headers["User-Agent"] = "PostmanRuntime/7.44.1"

        while self.__params["page"] < max_page:
            try:
                logger.info(
                    f"Запрос страницы {self.__params["page"]} c вакансиями по ключевому слову {self.__params["text"]}")
                response = requests.get(self.__url, params=self.__params, headers=self.__headers)
            except requests.RequestException as e:
                logger.critical(f"Ошибка при запрос страницы {self.__params["page"]} c вакансиями по ключевому \
слову {self.__params["text"]}: {e}")
            else:
                self.__params["page"] += 1
                max_page = response.json()["pages"]
                data.extend(response.json()["items"])

        return data
