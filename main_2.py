from config import config
from src.api_connector import HHApiConnector
from src.db_manager import DBManager

COMPANIES = [
    "3529",
    "1740",
    "15478",
    "87021",
    "2180",
    "820389",
    "2451566",
    "3127",
    "4233",
    "99966"
]


def main_usage() -> None:

    print("Получаем список вакансий... Это может занять пару минут, оставайтесь с нами)")
    print()

    params = config()

    db_manager_hh = DBManager("hh_db_3", params)
    db_manager_hh.create_database()

    hh_api_connector = HHApiConnector()

    hh_vacancies_by_companies = hh_api_connector.get_data_by_companies(COMPANIES)

    db_manager_hh.write_company_and_vacancies(hh_vacancies_by_companies)

    print("Список компаний и количество вакансий:")
    db_manager_hh.get_companies_and_vacancies_count()
    print()
    print()

    print("Список всех вакансий:")
    all_vacancies = db_manager_hh.get_all_vacancies()
    print(f"Найдено {len(all_vacancies)} вакансий.")
    while True:
        user_answer = input(f"Введите количество вакансий для вывода (от 0 до {len(all_vacancies)}): ")
        if user_answer.isdigit():
            count = min(int(user_answer), len(all_vacancies))
            for i in range(count):
                print(all_vacancies[i])
            break

    print()
    print()

    print("Средняя ЗП по всем вакансиям:")
    db_manager_hh.get_avg_salary()
    print()
    print()

    print("Список вакансий с ЗП выше средней:")
    high_salary_vacancies = db_manager_hh.get_vacancies_with_higher_salary()
    print(f"Найдено {len(high_salary_vacancies)} вакансий.")
    while True:
        user_answer = input(f"Введите количество вакансий для вывода (от 0 до {len(high_salary_vacancies)}): ")
        if user_answer.isdigit():
            count = min(int(user_answer), len(high_salary_vacancies))
            for i in range(count):
                print(high_salary_vacancies[i])
            break
    print()
    print()

    keywords = input("Введите слова для поиска через пробел: ").split()
    print("Вакансии по Вашему запросу:")
    db_manager_hh.get_vacancies_with_keyword(keywords)


if __name__ == '__main__':
    main_usage()
