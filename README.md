# coursework_5 - База данных компаний и вакансий с hh.ru

## Описание
, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.
Данный скрипт использует API для получения данных о компаниях и вакансиях с сайта hh.ru и сохраняет их в базу данных PostgreSQL. 
В коде используются библиотеки `requests` и `psycopg2`.

## Запуск

1. Создайте файл database.ini в корне проекта и пропишите свои данные для подключения к базе данных PostgreSQL в формате:
    [postgresql]
    host=
    user=
    password=
    port=
2. Запустите main.py

## Использование

1. При запуске скрипт запросит у пользователя ключевые слова для вывода вакансий, в названии которых они содержатся
2. Скрипт получит данные о 10 компаниях (SkyEng, Яндекс, Роскосмос, Сбер, TELE2, VK, РЖД, Авито, МегаФон, Норникель)
   и их вакансиях в Москве от API hh.ru и запишет их в базу данных "coursework_5" в таблицы "employers" и "vacancies"
3. На экран выведется следующая информация:
   1) список всех компаний и количество вакансий у каждой компании;
   2) список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию;
   3) средняя зарплата по вакансиям;
   4) список всех вакансий, у которых зарплата выше средней по всем вакансиям;
   5) список всех вакансий, в названии которых содержатся переданные ключевые слова.
