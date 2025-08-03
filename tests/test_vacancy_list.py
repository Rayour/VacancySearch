import os.path

from unittest.mock import patch
from src.vacancy import Vacancy
from src.vacancy_list import VacancyList
from pathlib import Path
from typing import Any

ROOT_PATH = Path(__file__).resolve().parents[1]


def test_vacancy_list_init(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """Функция для тестирования инициализации списка вакансий"""

    test_list = VacancyList([vacancy_1, vacancy_2])
    assert test_list.vacancy_list[0].name == "Вакансия 1"
    assert test_list.vacancy_list[1].name == "Вакансия 2"
    assert len(test_list.vacancy_list) == 2

    test_list_2 = VacancyList()
    assert len(test_list_2.vacancy_list) == 0


def test_add_vacancy(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """Функция для тестирования метода добавления вакансии"""

    test_list = VacancyList([vacancy_1])
    assert len(test_list.vacancy_list) == 1
    test_list.add_vacancy(vacancy_2)
    assert len(test_list.vacancy_list) == 2


def test_remove_vacancy(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """Функция для тестирования метода удаления вакансии"""

    test_list = VacancyList([vacancy_1, vacancy_2])
    assert len(test_list.vacancy_list) == 2
    test_list.remove_vacancy(vacancy_2)
    assert len(test_list.vacancy_list) == 1


@patch("json.load")
def test_get_data_from_json(mocked_file: Any, vacancies_list_json: list) -> None:
    """Функция для тестирования создания вакансий из JSON-файла"""

    test_list = VacancyList()
    test_file_path = os.path.join(ROOT_PATH, "tests", "data", "test.json")
    mocked_file.return_value = vacancies_list_json

    test_list.get_data_from_json(test_file_path)

    assert len(test_list.vacancy_list) == 2


def test_sort_by_salary(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """Функция для тестирования сортировки по зарплате"""

    test_list = VacancyList([vacancy_1, vacancy_2])
    test_list.sort_by_salary()
    assert test_list.vacancy_list[0].name == "Вакансия 2"


def test_keyword_search(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """Функция для тестирования поиска по ключевым словам"""

    test_list = VacancyList([vacancy_1, vacancy_2])
    kw_test_list = test_list.keywords_search(["2"])
    assert len(kw_test_list) == 1


def test_salary_filter(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """Функция для тестирования фильтрации вакансий по цене"""

    test_list = VacancyList([vacancy_1, vacancy_2])
    filtered_test_list = test_list.salary_filter(1000, 1500)
    assert len(filtered_test_list) == 1
