def test_head_hunter_api_init(hh_api):
    """Тестирует конструктор для API HeadHunter."""

    assert hh_api.employers_ids == [
        "1122462",
        "1740",
        "9764865",
        "3529",
        "4219",
        "15478",
        "23427",
        "5779602",
        "3127",
        "740",
    ]
    assert hh_api.employers_url == "https://api.hh.ru/employers/"
    assert hh_api.vacancies_url == "https://api.hh.ru/vacancies"
    assert hh_api.headers == {"User-Agent": "HH-User-Agent"}
    assert hh_api.params == {"employer_id": "", "area": "1", "page": 0, "per_page": 100}
    assert hh_api.vacancies == {}
    assert hh_api.employers == []


def test_head_hunter_api_load_employers(hh_api):
    """Тестирует метод для загрузки списка работодателей с API HeadHunter"""

    hh_api.load_employers()
    assert len(hh_api.employers) == 10


def test_head_hunter_api_load_vacancies(hh_api):
    """Тестирует метод для загрузки списка вакансий с API HeadHunter"""

    hh_api.load_vacancies()
    assert len(hh_api.vacancies) > 0
