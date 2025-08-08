import os.path
from src.api_connector import HHApiConnector
from src.write_file import WriteDataToJson
from src.vacancy_list import VacancyList

ROOT_PATH = os.getcwd()


def user_request() -> None:
    """Функция взаимодействия с пользователем"""

    while True:
        user_search = input("Введите ключевое слово для запроса вакансий: ")
        hh_api = HHApiConnector(params={"text": user_search})
        hh_vacancies = hh_api.get_data()
        if len(hh_vacancies) > 0:
            break
        else:
            print("По Вашему запросу ничего не найдено. Введите другое ключевое слово.")
            print()

    json_writer = WriteDataToJson(hh_vacancies, os.path.join("data", user_search + ".json"))
    json_writer.write_data()
    v_list = VacancyList()
    v_list.get_data_from_json(os.path.join(ROOT_PATH, "data", user_search + ".json"))
    v_list.sort_by_salary()

    print()
    keywords = input("Введите слова для фильтрации вакансий через пробел: ").split()
    v_filtered_by_keywords = VacancyList(v_list.keywords_search(keywords))
    print()

    while True:
        try:
            min, max = map(int, input("Введите диапазон ЗП (Например 100000 - 200000): ").split(" - "))
        except TypeError:
            print("Введите два числа через дефис с пробелами, как в примере.")
        except ValueError:
            print("Введите два числа через дефис с пробелами, как в примере.")
        else:
            break

    v_filtered_by_salary = VacancyList(v_filtered_by_keywords.salary_filter(min, max))
    print()

    while True:
        try:
            n = int(input("Введите количество вакансий для вывода в топ: "))
        except TypeError:
            print("Введите целое число")
        else:
            break

    v_filtered_by_salary.get_top_n(n)


if __name__ == "__main__":
    user_request()
