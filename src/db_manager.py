import datetime
import logging
import os.path
from pathlib import Path
from typing import Any

import psycopg2

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
logger = logging.getLogger("db_manager")


class DBManager:
    """Класс для работы с базой данных"""

    __db_name: str
    __params: dict

    def __init__(self, db_name: str, params: dict) -> None:
        """Функция инициализации объекта класса для работы с БД"""

        self.__db_name = db_name
        self.__params = params

    def create_database(self) -> None:
        """Функция для создания базы данных и таблиц"""

        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        logger.info(f"Удаление базы данных {self.__db_name}")
        cur.execute(f"DROP DATABASE IF EXISTS {self.__db_name}")
        logger.info(f"Создание базы данных {self.__db_name}")
        cur.execute(f"CREATE DATABASE {self.__db_name}")

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        logger.info("Создание таблицы companies")
        cur.execute("""CREATE TABLE companies(
                               company_id varchar PRIMARY KEY,
                               company_name text NOT NULL);
                        """)
        logger.info("Создание таблицы vacancies")
        cur.execute("""CREATE TABLE vacancies(
                               vacancy_id varchar PRIMARY KEY,
                               company_id varchar,
                               name text NOT NULL,
                               requirement text,
                               responsibility text,
                               salary_from INT,
                               salary_to INT,
                               url text,
                               FOREIGN KEY (company_id) REFERENCES companies(company_id));
                        """)
        cur.close()
        conn.close()

    def write_company_and_vacancies(self, data: list) -> None:
        """Функция для сохранения данных о вакансиях и компании в базу данных"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        for company in data:
            try:
                cur.execute("""INSERT INTO
                companies ("company_id", "company_name")
                VALUES (%s, %s)""",
                            (company["company_id"], company["company_name"]))
            except Exception as e:
                logger.critical(f"При записи компании id={company["company_id"]} произошла ошибка: {e}")
            else:
                for vacancy in company["vacancies"]:
                    if vacancy["snippet"] and vacancy["snippet"]["requirement"]:
                        requirement = vacancy["snippet"]["requirement"]
                    else:
                        requirement = None
                    if vacancy["snippet"] and vacancy["snippet"]["responsibility"]:
                        responsibility = vacancy["snippet"]["responsibility"]
                    else:
                        responsibility = None
                    if vacancy["salary"] and vacancy["salary"]["from"]:
                        salary_from = vacancy["salary"]["from"]
                    else:
                        salary_from = None
                    if vacancy["salary"] and vacancy["salary"]["to"]:
                        salary_to = vacancy["salary"]["to"]
                    else:
                        salary_to = None

                    try:
                        cur.execute("""INSERT INTO vacancies (
                            "vacancy_id",
                            "company_id",
                            "name",
                            "requirement",
                            "responsibility",
                            "salary_from",
                            "salary_to",
                            "url"
                            )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                                    (vacancy["id"],
                                     company["company_id"],
                                     vacancy["name"],
                                     requirement,
                                     responsibility,
                                     salary_from,
                                     salary_to,
                                     vacancy["url"]))
                    except Exception as e:
                        logger.critical(f"При записи вакансии id={vacancy["id"]} произошла ошибка: {e}")

        cur.close()
        conn.close()

    def get_companies_and_vacancies_count(self) -> None:
        """Метод для получения списка компаний и количества вакансий в них"""

        logger.info("Получаем список компаний с количеством вакансий")
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        cur = conn.cursor()
        cur.execute("""SELECT company_name, COUNT(*) as vacancy_count
                       FROM vacancies INNER JOIN companies USING (company_id)
                       GROUP BY company_name;""")
        rows = cur.fetchall()
        for row in rows:
            print(row)

        cur.close()
        conn.close()

    def get_all_vacancies(self) -> Any:
        """Метод для получения списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""

        logger.info("Получаем список всех вакансий")
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        cur = conn.cursor()
        cur.execute("""SELECT company_name, name, salary_from, salary_to, url
                       FROM vacancies INNER JOIN companies USING (company_id);""")
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows

    def get_avg_salary(self) -> None:
        """Метод для получения средней зарплаты по вакансиям"""

        logger.info("Получаем среднюю ЗП по всем вакансиям")
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        cur = conn.cursor()
        cur.execute("SELECT AVG((salary_from + salary_to) / 2) FROM vacancies;")
        avg = cur.fetchone()
        print(round(avg[0], 2))

        cur.close()
        conn.close()

    def get_vacancies_with_higher_salary(self) -> Any:
        """Метод для получения списка всех вакансий,
        у которых зарплата выше средней по всем вакансиям"""

        logger.info("Получаем список вакансий с ЗП выше средней")
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        cur = conn.cursor()
        cur.execute("""SELECT name, salary_from, salary_to, url
                       FROM vacancies
                       WHERE salary_from > (SELECT AVG((salary_from + salary_to) / 2) from vacancies)
                       OR salary_to > (SELECT AVG((salary_from + salary_to) / 2) from vacancies);""")
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows

    def get_vacancies_with_keyword(self, words: list) -> None:
        """Метод для получения списка всех вакансий,
        в названии которых содержатся переданные в метод слова, например python"""

        logger.info(f"Получаем список вакансий с ключевыми словами {words} в названии")
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        cur = conn.cursor()

        for word in words:
            cur.execute(f"""SELECT name, salary_from, salary_to, url
                                   FROM vacancies
                                   WHERE name LIKE '%{word}%';""")
            rows = cur.fetchall()
            for row in rows:
                print(row)

        cur.close()
        conn.close()
