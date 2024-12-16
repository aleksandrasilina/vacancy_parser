import requests

from src.parser import Parser


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        """Конструктор для API HeadHunter"""

        self.__employers_ids = [
            "1122462",  # SkyEng
            "1740",  # Яндекс
            "9764865",  # Роскосмос
            "3529",  # Сбер
            "4219",  # TELE2
            "15478",  # VK
            "23427",  # РЖД
            "5779602",  # Авито
            "3127",  # МегаФон
            "740",  # Норникель
        ]

        self.__employers_url = "https://api.hh.ru/employers/"
        self.__vacancies_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"employer_id": "", "area": "1", "page": 0, "per_page": 100}
        self.__vacancies = {}
        self.__employers = []

    def load_employers(self) -> None:
        """Загружает список работодателей с API HeadHunter по их id"""

        for employer_id in self.__employers_ids:
            response = requests.get(
                f"{self.__employers_url}{employer_id}", headers=self.__headers
            )
            employers = response.json()
            self.__employers.append(employers)

    def load_vacancies(self) -> None:
        """Загружает список вакансий в Москве с API HeadHunter по id работодателя"""

        for employer_id in self.__employers_ids:
            total_vacancies = []
            vacancies_per_page = 100
            self.__params["page"] = 0
            self.__params["employer_id"] = employer_id

            while self.__params.get("page") != 3 and vacancies_per_page == 100:
                response = requests.get(
                    self.__vacancies_url, headers=self.__headers, params=self.__params
                )
                vacancies = response.json()["items"]
                total_vacancies.extend(vacancies)
                self.__params["page"] += 1
                vacancies_per_page = len(vacancies)

            self.__vacancies[employer_id] = total_vacancies

    @property
    def employers_ids(self):
        """Геттер для employers_ids."""
        return self.__employers_ids

    @property
    def employers_url(self):
        """Геттер для employers_url."""
        return self.__employers_url

    @property
    def vacancies_url(self):
        """Геттер для vacancies_url."""

        return self.__vacancies_url

    @property
    def headers(self):
        """Геттер для headers"""
        return self.__headers

    @property
    def params(self):
        """Геттер для params"""
        return self.__params

    @property
    def vacancies(self):
        """Геттер для словаря вакансий"""
        return self.__vacancies

    @property
    def employers(self):
        """Геттер для списка работодателей"""
        return self.__employers
