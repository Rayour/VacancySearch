import pytest

from src.vacancy import Vacancy


def test_vacancy_init(
        vacancy_1: Vacancy,
        vacancy_2: Vacancy,
        vacancy_3: Vacancy,
        vacancy_4: Vacancy) -> None:
    """Функция для тестирования метода инициализации класса Vacancy"""

    assert vacancy_1.name == "Вакансия 1"
    assert vacancy_2.name == "Вакансия 2"
    assert vacancy_3.name == "Вакансия 3"
    assert vacancy_4.name == "Вакансия 4"
    assert vacancy_1.requirement == "Требования 1"
    assert vacancy_1.responsibility == "Обязанности 1"
    assert vacancy_1.avg_salary == 1500
    assert vacancy_2.avg_salary == 2000
    assert vacancy_3.avg_salary == 1500


def test_vacancy_str(vacancy_1: Vacancy) -> None:
    """Функция для тестирования строкового представления класса вакансий"""
    print(str(vacancy_1))
    assert str(vacancy_1) == "{'id': '111', 'name': 'Вакансия 1', 'requirement': 'Требования 1', 'responsibility': \
'Обязанности 1', 'salary_from': 1000, 'salary_to': 2000}"


def test_vacancy_eq(
        vacancy_1: Vacancy,
        vacancy_2: Vacancy,
        vacancy_3: Vacancy,
        vacancy_4: Vacancy) -> None:
    """Функция тестирования метода сравнения"""

    assert (vacancy_1 == vacancy_2) == False
    assert (vacancy_1 == vacancy_3) == True

    with pytest.raises(ValueError) as exc_info:
        vacancy_1 == vacancy_4
        assert str(exc_info.value) == "Невозможно сравнить вакансии по зарплате"


def test_vacancy_lt(
        vacancy_1: Vacancy,
        vacancy_2: Vacancy,
        vacancy_3: Vacancy,
        vacancy_4: Vacancy) -> None:
    """Функция тестирования метода сравнения"""

    assert (vacancy_1 < vacancy_2) == True
    assert (vacancy_1 < vacancy_3) == False

    with pytest.raises(ValueError) as exc_info:
        vacancy_1 < vacancy_4
        assert str(exc_info.value) == "Невозможно сравнить вакансии по зарплате"


def test_vacancy_gt(
        vacancy_1: Vacancy,
        vacancy_2: Vacancy,
        vacancy_3: Vacancy,
        vacancy_4: Vacancy) -> None:
    """Функция тестирования метода сравнения"""

    assert (vacancy_1 > vacancy_2) == False
    assert (vacancy_2 > vacancy_3) == True

    with pytest.raises(ValueError) as exc_info:
        vacancy_1 > vacancy_4
        assert str(exc_info.value) == "Невозможно сравнить вакансии по зарплате"


def test_create_vacancy() -> None:
    """Функция для тестирования класс-метода создания вакансии"""

    vacancy_test_1 = Vacancy.create_vacancy("123", "Тестовая вакансия", "Требования", "Обязанности", 1000, 2000)
    assert vacancy_test_1.name == "Тестовая вакансия"
    assert vacancy_test_1.requirement == "Требования"
    assert vacancy_test_1.responsibility == "Обязанности"
    assert vacancy_test_1.avg_salary == 1500

    with pytest.raises(Exception) as exc_info:
        Vacancy.create_vacancy("123", "Тестовая вакансия", "Требования", "Обязанности", 1000, 2000)
        assert str(exc_info.value) == "Вакансия с идентификатором id=123 уже существует"

    with pytest.raises(TypeError) as exc_info:
        Vacancy.create_vacancy(123, "Тестовая вакансия", "Требования", "Обязанности", 1000, 2000)
        assert str(exc_info.value) == "Идентификатор вакансии должен быть строкой, передано 123"
