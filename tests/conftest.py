import pytest

from src.vacancy import Vacancy


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

    return Vacancy("333", "Вакансия 3", "Требования 3", "Обязанности 3", salary_to=1500)


@pytest.fixture
def vacancy_4() -> Vacancy:
    """Фикстура возвращает объект вакансии"""

    return Vacancy("444", "Вакансия 4", "Требования 4", "Обязанности 4")


@pytest.fixture
def vacancies_list() -> list:
    """Фикстура возвращает список вакансий"""

    return [
        {
            "id": "123292815",
            "name": "Mid-level Frontend Engineer",
            "salary": {
                "from": 300000,
                "to": 400000
            },
            "snippet": {
                "requirement": "Опыт разработки адаптивных дизайнов мобильных интерфейсов для финтех-приложений.",
                "responsibility": "Frontend-разработка и оптимизация: проектировать, создавать и поддерживать..."
            }
        },
        {
            "id": "123280904",
            "name": "Программист Python",
            "salary": {
                "from": 100000,
                "to": 300000
            },
            "snippet": {
                "requirement": "Знание <highlighttext>python</highlighttext> и других языков.",
                "responsibility": None
            }
        }
    ]
