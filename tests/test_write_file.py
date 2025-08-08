import json
import os.path
from pathlib import Path

from src.write_file import WriteDataToJson

ROOT_PATH = Path(__file__).resolve().parents[1]


def test_write_json_init(vacancies_list: list[dict]) -> None:
    """Функция тестирования метода инициализации"""

    test_write_json_obj = WriteDataToJson(
        vacancies_list,
        os.path.join("tests", "data", "test_write.json")
    )

    assert test_write_json_obj.file_path == os.path.join("tests", "data", "test_write.json")


def test_write_data(vacancies_list: list[dict]) -> None:
    """Функция для тестирования записи данных в файл"""

    test_write_json_obj_1 = WriteDataToJson(
        vacancies_list,
        os.path.join("tests", "data", "test_write.json")
    )
    test_write_json_obj_1.write_data()

    with open(os.path.join(ROOT_PATH, test_write_json_obj_1.file_path), "r", encoding="utf-8") as file:
        test_data_1 = json.load(file)

    assert len(test_data_1) == 2

    test_write_json_obj_2 = WriteDataToJson(
        vacancies_list,
        os.path.join("tests", "data", "test_write.json")
    )
    test_write_json_obj_2.write_data()

    with open(os.path.join(ROOT_PATH, test_write_json_obj_2.file_path), "r", encoding="utf-8") as file:
        test_data_2 = json.load(file)

    assert len(test_data_2) == 2


def test_delete_data(vacancies_list: list[dict]) -> None:
    """Функция для тестирования удаления данных из файла"""

    test_write_json_obj = WriteDataToJson(
        vacancies_list,
        os.path.join("tests", "data", "test_write.json")
    )
    test_write_json_obj.write_data()

    with open(os.path.join(ROOT_PATH, test_write_json_obj.file_path), "r", encoding="utf-8") as file:
        test_data_1 = json.load(file)

    assert len(test_data_1) == 2

    test_write_json_obj.delete_data()

    with open(os.path.join(ROOT_PATH, test_write_json_obj.file_path), "r", encoding="utf-8") as file:
        test_data_2 = file.read()

    assert len(test_data_2) == 0
