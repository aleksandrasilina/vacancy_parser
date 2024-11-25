import psycopg2

from config import config
from src.db_manager import DBManager
from src.head_hunter_api import HeadHunterAPI


def main():
    database_name = "coursework_5"
    conn = None

    user_keywords = (
        input("Введите ключевые слова через пробел для поиска вакансий").lower().split()
    )

    params = config()
    db_manager = DBManager()
    hh_api = HeadHunterAPI()
    hh_api.load_employers()
    hh_api.load_vacancies()

    db_manager.create_database(database_name, params)
    print(f"БД {database_name} успешно создана")

    params.update({"dbname": database_name})

    db_manager.create_employers_table(params)
    print("Таблица employers успешно создана")

    db_manager.create_vacancies_table(params)
    print("Таблица vacancies успешно создана")

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                db_manager.insert_employers_data(cur, hh_api.employers)
                print("Таблица employers успешно заполнена")

                db_manager.insert_vacancies_data(cur, hh_api.vacancies)
                print("Таблица vacancies успешно заполнена")

                print("Компании и количество вакансий:")
                print(db_manager.get_companies_and_vacancies_count(cur))

                print(
                    "Вакансии с указанием названия компании, "
                    "названия вакансии, зарплаты и ссылки на вакансию:"
                )
                print(db_manager.get_all_vacancies(cur))

                print("Средняя зарплата по вакансиям:")
                print(db_manager.get_avg_salary(cur))

                print("Вакансии, у которых зарплата выше средней:")
                print(db_manager.get_vacancies_with_higher_salary(cur))

                print("Вакансии, в названии которых содержатся ключевые слова:")
                print(db_manager.get_vacancies_with_keyword(cur, user_keywords))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
