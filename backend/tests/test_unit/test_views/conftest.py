import pytest


@pytest.fixture
def views_vacancy_list(fake_vacancies_data):
    """Return fabric to get response data for views returns vacancy list."""
    def gen_vacancies(sources_count=1, vacancies_count=3):
        vacancies_data = fake_vacancies_data(sources_count, vacancies_count)
        for vacancy in vacancies_data:
            vacancy.update({'count': len(vacancies_data)})
        return vacancies_data
    return gen_vacancies