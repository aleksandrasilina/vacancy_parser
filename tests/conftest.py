import pytest
import psycopg2

from src.head_hunter_api import HeadHunterAPI
from src.db_manager import DBManager
from config import config


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


@pytest.fixture
def db_manager():
    return DBManager()


@pytest.fixture
def params():
    return config()


@pytest.fixture
def params_with_db_name(params):
    params.update({'dbname': 'coursework_5'})
    return params


@pytest.fixture(autouse=True)
def database(db_manager, params):
    database_name = 'coursework_5'
    db_manager.create_database(database_name, params)


@pytest.fixture
def employers():
    return [{
        "id": 1,
        "name": "employer_1",
        "area": {
            "name": "employer_1"
        },
        "alternate_url": "employer_1",
        "site_url": "employer_1",
        "open_vacancies": 1
    },
        {
            "id": 2,
            "name": "employer_2",
            "area": {
                "name": "employer_2"
            },
            "alternate_url": "employer_2",
            "site_url": "employer_2",
            "open_vacancies": 2
        }
    ]


@pytest.fixture
def vacancies():
    return {
        '1': [{
            'id': 1,
            'name': "vacancy_1",
            "salary": {
                "currency": "RUR",
                "from": 30000,
                "to": 50000
            },
            'alternate_url': 'vacancy_1',
            'snippet': {'requirement': 'vacancy_1',
                        'responsibility': 'vacancy_1'},
            'schedule': {'id': 'remote', 'name': 'Удаленная работа'},
            'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'},
            'employment': {'id': 'full', 'name': 'Полная занятость'}

        },
            {
                'id': 2,
                'name': "vacancy_2",
                "salary": {
                    "currency": "RUR",
                    "from": 50000,
                    "to": 70000
                },
                'alternate_url': 'vacancy_2',
                'snippet': {'requirement': 'vacancy_2',
                            'responsibility': 'vacancy_2'},
                'schedule': {'id': 'remote', 'name': 'Удаленная работа'},
                'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'},
                'employment': {'id': 'full', 'name': 'Полная занятость'}
            }
        ]
    }

@pytest.fixture()
def database_with_tables(db_manager, params_with_db_name, employers, vacancies):
    db_manager.create_employers_table(params_with_db_name)
    db_manager.create_vacancies_table(params_with_db_name)

    with psycopg2.connect(**params_with_db_name) as conn:
        with conn.cursor() as cur:
            db_manager.insert_employers_data(cur, employers)
            db_manager.insert_vacancies_data(cur, vacancies)
    conn.close()
