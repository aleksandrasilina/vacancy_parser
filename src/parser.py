from abc import ABC, abstractmethod


class Parser(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def load_employers(self):
        """Загружает список работодателей с API сервиса с вакансиями по их id"""
        pass

    @abstractmethod
    def load_vacancies(self):
        """Загружает список вакансий с API сервиса с вакансиями по id работодателя"""
        pass
