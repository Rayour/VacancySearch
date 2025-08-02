import datetime
import json
import logging
import os.path
from pathlib import Path

from src.vacancy import Vacancy

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
logger = logging.getLogger("vacancy_list")


class VacancyList:
    """Класс для работы со списком вакансий"""

    vacancy_list: list[Vacancy]

    def __init__(self, vacancy_list: list | None = None) -> None:
        """Метод инициализации списка вакансий"""

        self.vacancy_list = vacancy_list if vacancy_list else []

    def __str__(self) -> str:
        """Метод строкового представления списка вакансий"""

        result = ""
        for vacancy in self.vacancy_list:
            result += str(vacancy)
        return f"[{result}]"

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для добавления вакансии в список"""

        self.vacancy_list.append(vacancy)

    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для удаления вакансии из списка"""

        self.vacancy_list.remove(vacancy)

    def get_data_from_json(self, file_path: str) -> None:
        """Метод получения данных из JSON файла"""

        try:
            logger.info(f"Попытка чтения данных о вакансиях из файла {file_path}")
            with open(os.path.join(ROOT_PATH, file_path), 'r', encoding='utf-8') as file:
                vacancies_list = json.load(file)
        except Exception as e:
            logger.critical(f"Ошибка чтения данных из файла: {e}")
        else:
            logger.info(f"Данные из файла {file_path} успешно прочитаны")
            logger.info("Создаем вакансии...")

            for vacancy in vacancies_list:
                id = vacancy["id"]
                name = vacancy["name"]
                requirement = vacancy["snippet"]["requirement"]
                responsibility = vacancy["snippet"]["responsibility"]
                if vacancy["salary"] and vacancy["salary"]["from"]:
                    salary_from = vacancy["salary"]["from"]
                else:
                    salary_from = None
                if vacancy["salary"] and vacancy["salary"]["to"]:
                    salary_to = vacancy["salary"]["to"]
                else:
                    salary_to = None

                try:
                    new_vacancy = Vacancy.create_vacancy(
                        id,
                        name,
                        requirement,
                        responsibility,
                        salary_from=salary_from,
                        salary_to=salary_to
                    )
                except Exception as e:
                    logger.info(f"При попытке создания вакансии произошла ошибка: {e}")
                else:
                    self.add_vacancy(new_vacancy)

    def sort_by_salary(self) -> None:
        """Метод для сортировки вакансий по ЗП.
        Если у вакансии указан и верхний и нижний диапазон ЗП, то для сравнения будет взят средний уровень ЗП.
        Если у вакансии есть только одна граница ЗП, то для сравнения будет взята она.
        Вакансии без указания ЗП будут исключены при сортировке"""

        self.vacancy_list.sort(key=lambda x: x.avg_salary if x.avg_salary else 0, reverse=True)

    def keywords_search(self, keywords: list[str]) -> list[Vacancy]:
        """Метод возвращает вакансии, в которых встречается одно из ключевых слов"""

        filtered_list = []
        logger.info(f"Фильтруем вакансии по списку ключевых слов {keywords}...")
        for vacancy in self.vacancy_list:
            for keyword in keywords:
                if (vacancy.requirement and keyword.lower() in vacancy.requirement.lower()) or (
                        vacancy.responsibility and keyword.lower() in vacancy.responsibility.lower()):
                    filtered_list.append(vacancy)

        logger.info(f"По списку ключевых слов {keywords} найдено {len(filtered_list)} вакансий")
        return filtered_list

    def salary_filter(self, min: int, max: int) -> list[Vacancy]:
        """Метод возвращает список вакансий, пересекающихся по ЗП с заданным диапазоном"""

        filtered_list = []
        logger.info(f"Фильтруем вакансии по диапазону ЗП от {min} до {max}...")
        for vacancy in self.vacancy_list:
            if vacancy.avg_salary and min <= vacancy.avg_salary <= max:
                filtered_list.append(vacancy)

        logger.info(f"Найдено {len(filtered_list)} вакансий в диапазоне ЗП {min} - {max}")
        return filtered_list

    def get_top_n(self, n: int) -> None:
        """Метод выводит в консоль топ N вакансий"""

        amount = min(n, len(self.vacancy_list))
        for i in range(amount):
            print(self.vacancy_list[i])


if __name__ == "__main__":
    v_list = VacancyList()
    v_list.get_data_from_json(os.path.join(ROOT_PATH, "data", "vacancies.json"))
    v_list.sort_by_salary()
