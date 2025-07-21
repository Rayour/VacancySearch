import datetime
import json
import logging
import os.path
from pathlib import Path
from typing import Any
from src.api_connector import HHApiConnector
from src.write_file import WriteDataToJson

ROOT_PATH = Path(__file__)




def user_request() -> None:
    """Функция взаимодействия с пользователем"""

    user_search = input("Введите ключевое слово для запроса вакансий: ")
    hh_api = HHApiConnector(params={"text": user_search})
    hh_vacancies = hh_api._get_data()
    json_writer = WriteDataToJson(hh_vacancies, os.path.join("data", "vacancies.json"))
    json_writer.write_data()


if __name__ == "__main__":
    user_request()
