import pytest
from src.vacancy import Vacancy
from src.vacancy_list import VacancyList
from src.write_file import WriteDataToJson
from src.api_connector import HHApiConnector

@pytest.fixture
def vacancy_1() -> Vacancy:
    """Фикстура возвращает объект вакансии"""

    return Vacancy("111", "Вакансия 1", "Требования 1", "Обязанности 1", 1000, 2000)


@pytest.fixture
def vacancy_2() -> Vacancy:
    """Фикстура возвращает объект вакансии"""

    return Vacancy("222", "Вакансия 2", "Требования 2", "Обязанности 2", 2000)


@pytest.fixture
def vacancy_3() -> Vacancy:
    """Фикстура возвращает объект вакансии"""

    return Vacancy("333", "Вакансия 3", "Требования 3", "Обязанности 3", salary_to=3000)


@pytest.fixture
def vacancy_4() -> Vacancy:
    """Фикстура возвращает объект вакансии"""

    return Vacancy("444", "Вакансия 4", "Требования 4", "Обязанности 4")
