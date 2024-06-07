import psycopg2


class DBManager:
    """Класс для работы с данными в БД"""

    @staticmethod
    def create_database(database_name: str, params: dict) -> None:
        """Создание базы данных для сохранения данных о работодателях и их вакансиях."""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
            cur.execute(f'CREATE DATABASE {database_name}')

        conn.close()

    @staticmethod
    def create_employers_table(params: dict) -> None:
        """Создание таблицы employers для сохранения данных о работодателях."""

        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE employers (
                        employer_id INT PRIMARY KEY,                        
                        company_name VARCHAR(100) NOT NULL,
                        region VARCHAR(50) NOT NULL,
                        hh_url VARCHAR(50),
                        url VARCHAR(50),
                        open_vacancies INT
                    )
                """)

        conn.close()

    @staticmethod
    def create_vacancies_table(params: dict) -> None:
        """Создание таблицы vacancies для сохранения данных о вакансии."""

        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id INT PRIMARY KEY,
                        employer_id INT NOT NULL,                        
                        vacancy_name VARCHAR(100) NOT NULL,
                        salary_from INT,
                        salary_to INT,
                        salary_currency VARCHAR(5),
                        vacancy_url VARCHAR(50),
                        requirement TEXT,
                        responsibility TEXT,
                        schedule VARCHAR(30),
                        experience VARCHAR(30),
                        employment VARCHAR(30),
                        FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                    )
                """)

        conn.close()

    @staticmethod
    def insert_employers_data(cur, employers: list[dict]) -> None:
        """Добавляет данные о работодателях из API сервиса с вакансиями в таблицу employers."""

        for employer in employers:
            cur.execute(
                """
                INSERT INTO employers (employer_id, company_name, region, hh_url, url, open_vacancies)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (employer['id'], employer['name'], employer['area']['name'],
                 employer['alternate_url'], employer['site_url'], employer['open_vacancies'])
            )

    @staticmethod
    def insert_vacancies_data(cur, vacancies: dict[str, list[dict]]) -> None:
        """Добавляет данные о вакансиях из API сервиса с вакансиями в таблицу vacancies."""

        for employer_id, employer_vacancies in vacancies.items():
            for vacancy in employer_vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, salary_from, salary_to,
                     salary_currency, vacancy_url, requirement, responsibility, schedule, experience, employment)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy.get('id'), employer_id, vacancy.get('name'), (vacancy.get('salary') or {}).get('from'),
                     (vacancy.get('salary') or {}).get('to'), (vacancy.get('salary') or {}).get('currency'),
                     vacancy.get('alternate_url'), vacancy.get('snippet').get('requirement'),
                     vacancy.get('snippet').get('responsibility'), vacancy.get('schedule').get('name'),
                     vacancy.get('experience').get('name'), vacancy.get('employment').get('name'))
                )

    @staticmethod
    def get_companies_and_vacancies_count(cur) -> list[tuple]:
        """Получает список всех компаний и количество вакансий у каждой компании."""

        cur.execute(
            """
            SELECT e.company_name, COUNT(v.*) AS total_vacancies
            FROM employers e
            JOIN vacancies v USING(employer_id)
            GROUP BY e.company_name
            """
        )

        return cur.fetchall()

    @staticmethod
    def get_all_vacancies(cur) -> list[tuple]:
        """Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию.
        """

        cur.execute(
            """
            SELECT e.company_name, v.vacancy_name, v.salary_from,
            v.salary_to, v.salary_currency, v.vacancy_url
            FROM employers e
            JOIN vacancies v USING(employer_id)
            """
        )

        return cur.fetchall()

    @staticmethod
    def get_avg_salary(cur) -> list[tuple]:
        """Получает среднюю зарплату по вакансиям."""

        cur.execute(
            """
            SELECT e.company_name, ROUND(AVG(v.salary_from), 2) AS average_salary
            FROM employers e
            JOIN vacancies v USING(employer_id)
            GROUP BY e.company_name
            """
        )

        return cur.fetchall()

    @staticmethod
    def get_vacancies_with_higher_salary(cur) -> list[tuple]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        cur.execute(
            """
            SELECT * FROM vacancies
            WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
            """
        )

        return cur.fetchall()

    @staticmethod
    def get_vacancies_with_keyword(cur, user_keywords: list[str]):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""

        vacancies = []
        for keyword in user_keywords:
            cur.execute(
                f"""
                SELECT * FROM vacancies
                WHERE vacancy_name LIKE '%{keyword}%'
                """
            )

        vacancies.extend(cur.fetchall())
        return vacancies
