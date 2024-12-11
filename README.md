# Парсер вакансий с [hh.ru](https://hh.ru/)

## Содержание
- [Описание](#описание)
- [Технологии](#технологии)
- [Запуск проекта](#запуск-проекта)
- [Использование](#использование)
- [Тестирование](#тестирование)

## Технологии
- Python
- PostgreSQL

## Описание
- Программа для сбора данных о вакансиях с сайта [hh.ru](https://hh.ru/).
- Поиск осуществляется по 10 компаниям: SkyEng, Яндекс, Роскосмос, Сбер, TELE2, VK, РЖД, Авито, МегаФон, Норникель.
- Информация сохраняется в базу данных PostgreSQL.


## Запуск проекта
1. Клонируйте проект
```
git clone git@github.com:aleksandrasilina/vacancy_parser.git
```
2. Установите зависимости
```
pip install poetry
```
```
poetry install
```
3. Создайте файл database.ini в соответствии с шаблоном database.sample.ini
4.  Запустите проект
```
python main.py
```

## Использование
1. При запуске скрипт запросит у пользователя ключевые слова для вывода вакансий. ключевые слова вводятся через пробел.
2. Скрипт получит данные о компаниях и их вакансиях в Москве от API hh.ru и сохранит их в базу данных.
3. На экран выведется следующая информация:
   * список всех компаний и количество вакансий у каждой компании;
   * список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию;
   * средняя зарплата по вакансиям;
   * список всех вакансий, у которых зарплата выше средней по всем вакансиям;
   * список всех вакансий, в названии которых содержатся переданные ключевые слова.

## Тестирование:
```
pytest
```
Оценка покрытия:
```
pytest --cov src --cov-report term-missing
```