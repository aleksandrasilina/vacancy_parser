import psycopg2


def test_create_employers_table(db_manager, params_with_db_name):
    db_manager.create_employers_table(params_with_db_name)

    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'employers'")
            columns = cur.fetchall()
            assert columns[0][0] == 6
    conn.close()


def test_create_vacancies_table(db_manager, params_with_db_name):
    db_manager.create_employers_table(params_with_db_name)
    db_manager.create_vacancies_table(params_with_db_name)

    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'vacancies'")
            columns = cur.fetchall()
            assert columns[0][0] == 12
    conn.close()


def test_insert_employers_data(db_manager, params_with_db_name, employers):
    db_manager.create_employers_table(params_with_db_name)

    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            db_manager.insert_employers_data(cur, employers)
            cur.execute("SELECT COUNT(*) FROM employers")

            assert cur.fetchall()[0][0] == 2
    conn.close()


def test_insert_vacancies_data(db_manager, params_with_db_name, employers, vacancies):
    db_manager.create_employers_table(params_with_db_name)
    db_manager.create_vacancies_table(params_with_db_name)

    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            db_manager.insert_employers_data(cur, employers)
            db_manager.insert_vacancies_data(cur, vacancies)
            cur.execute("SELECT COUNT(*) FROM employers")

            assert cur.fetchall()[0][0] == 2
    conn.close()


def test_get_companies_and_vacancies_count(database_with_tables, db_manager, params_with_db_name):
    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            assert db_manager.get_companies_and_vacancies_count(cur) == [('employer_1', 2)]


def test_get_all_vacancies(database_with_tables, db_manager, params_with_db_name):
    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            assert db_manager.get_all_vacancies(cur)[0] == ('employer_1', 'vacancy_1', 30000, 50000, 'RUR', 'vacancy_1')
            assert db_manager.get_all_vacancies(cur)[1] == ('employer_1', 'vacancy_2', 50000, 70000, 'RUR', 'vacancy_2')


def test_get_avg_salary(database_with_tables, db_manager, params_with_db_name):
    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            assert float(db_manager.get_avg_salary(cur)[0][1]) == 40000.00


def test_get_vacancies_with_higher_salary(database_with_tables, db_manager, params_with_db_name):
    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            assert db_manager.get_vacancies_with_higher_salary(cur)[0] == (
                2, 1, 'vacancy_2', 50000, 70000, 'RUR', 'vacancy_2', 'vacancy_2',
                'vacancy_2', 'Удаленная работа', 'От 1 года до 3 лет', 'Полная занятость'
            )


def test_get_vacancies_with_keyword(database_with_tables, db_manager, params_with_db_name):
    user_keywords = ['vacancy', '_1', ]
    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            assert db_manager.get_vacancies_with_keyword(cur, user_keywords)[0] == (
                1, 1, 'vacancy_1', 30000, 50000, 'RUR', 'vacancy_1', 'vacancy_1',
                'vacancy_1', 'Удаленная работа', 'От 1 года до 3 лет', 'Полная занятость'
            )
