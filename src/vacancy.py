import datetime
import logging
import os.path
from pathlib import Path
from typing import Any

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
logger = logging.getLogger("vacancy")


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = ("__id", "__name", "__requirement", "__responsibility", "__salary_from", "__salary_to", "__avg_salary")

    __id: str
    __name: str
    __requirement: str | None
    __responsibility: str | None
    __salary_from: int | None
    __salary_to: int | None
    __avg_salary: int | None

    vacancies: dict = {}

    def __init__(self, id: str, name: str, requirement: str, responsibility: str, salary_from: int | None = None,
                 salary_to: int | None = None) -> None:
        """Метод инициализации вакансии"""

        self.__id = id
        self.__name = name
        self.__requirement = requirement
        self.__responsibility = responsibility
        self.__salary_from = salary_from
        self.__salary_to = salary_to
        if salary_from and salary_to:
            self.__avg_salary = (salary_from + salary_to) // 2
        elif salary_from:
            self.__avg_salary = salary_from
        elif salary_to:
            self.__avg_salary = salary_to
        else:
            self.__avg_salary = None

        Vacancy.vacancies[id] = self
        logger.info(f"Создана вакансия id: {id}, Название: {name}")

    def __str__(self) -> str:
        """Метод для отображения объекта вакансии"""

        result = {
            "id": self.__id,
            "name": self.__name,
            "requirement": self.__requirement,
            "responsibility": self.__responsibility,
            "salary_from": self.__salary_from,
            "salary_to": self.__salary_to
        }
        return str(result)

    @classmethod
    def create_vacancy(cls, *args: Any, **kwargs: Any) -> Any:
        """Метод создания вакансии с проверкой уникальности и валидацией типа данных идентификатора"""

        if isinstance(args[0], str):
            if args[0] in cls.vacancies:
                logger.info(f"Вакансия id={args[0]} уже существует и не будет создана")
                raise Exception(f"Вакансия с идентификатором id={args[0]} уже существует")
            else:
                return cls(*args, **kwargs)
        else:
            logger.warning(f"Идентификатор вакансии ({args[0]}) должен быть строкой")
            raise TypeError(f"Идентификатор вакансии должен быть строкой, передано {args[0]}")

    def __eq__(self, other: Any) -> bool:
        """Метод равенства вакансий по средней ЗП"""

        if self.__avg_salary:
            if other.avg_salary:
                if self.__avg_salary == other.avg_salary:
                    return True
                else:
                    return False
            else:
                raise ValueError("Невозможно сравнить вакансии по зарплате")
        else:
            raise ValueError("Невозможно сравнить вакансии по зарплате")

    def __lt__(self, other: Any) -> bool:
        """Метод сравнения вакансий по средней ЗП (меньше)"""

        if self.__avg_salary:
            if other.avg_salary:
                if self.__avg_salary < other.avg_salary:
                    return True
                else:
                    return False
            else:
                raise ValueError("Невозможно сравнить вакансии по зарплате")
        else:
            raise ValueError("Невозможно сравнить вакансии по зарплате")

    def __gt__(self, other: Any) -> bool:
        """Метод сравнения вакансий по средней ЗП (больше)"""

        if self.__avg_salary:
            if other.avg_salary:
                if self.__avg_salary > other.avg_salary:
                    return True
                else:
                    return False
            else:
                raise ValueError("Невозможно сравнить вакансии по зарплате")
        else:
            raise ValueError("Невозможно сравнить вакансии по зарплате")

    @property
    def avg_salary(self) -> int | None:
        """Свойство средней ЗП"""
        return self.__avg_salary

    @property
    def name(self) -> str:
        """Свойство названия"""
        return self.__name

    @property
    def requirement(self) -> str | None:
        """Свойство требований"""
        return self.__requirement

    @property
    def responsibility(self) -> str | None:
        """Свойство обязанностей"""
        return self.__responsibility
