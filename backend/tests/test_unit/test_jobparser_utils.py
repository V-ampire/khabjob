from jobparser import utils
import aiohttp


async def test_parse_vacancies_to_db_all_parsers(loop, aio_patch, postgres):
    expected_farpost = [{'name': 'farpost'}]
    expected_superjob = [{'name': 'superjob'}]
    expected_hh = [{'name': 'hh'}]
    expected_vk = [{'name': 'vk'}]

    farpost_mock = aio_patch(f'jobparser.utils.FarpostParser.get_vacancies')
    farpost_mock.return_value = expected_farpost
    superjob_mock = aio_patch(f'jobparser.utils.SuperjobParser.get_vacancies')
    superjob_mock.return_value = expected_superjob
    hh_mock = aio_patch(f'jobparser.utils.HHParser.get_vacancies')
    hh_mock.return_value = expected_hh
    vk_mock = aio_patch(f'jobparser.utils.VkParser.get_vacancies')
    vk_mock.return_value = expected_vk

    mock_create = aio_patch('jobparser.utils.create_vacancy_batch')

    await utils.parse_vacancies_to_db()

    mock_create_vacancies_data_list = [
        call.args[1] for call in mock_create.await_args_list
    ]

    assert farpost_mock.await_count == 1
    assert superjob_mock.await_count == 1
    assert hh_mock.await_count == 1
    assert vk_mock.await_count == 1

    assert expected_farpost in mock_create_vacancies_data_list
    assert expected_superjob in mock_create_vacancies_data_list
    assert expected_hh in mock_create_vacancies_data_list
    assert expected_vk in mock_create_vacancies_data_list


async def test_parse_vacancies_to_db_concrete_parsers(loop, aio_patch, postgres):
    expected_hh = [{'name': 'hh'}]
    expected_vk = [{'name': 'vk'}]

    farpost_mock = aio_patch(f'jobparser.utils.FarpostParser.get_vacancies')
    superjob_mock = aio_patch(f'jobparser.utils.SuperjobParser.get_vacancies')
    hh_mock = aio_patch(f'jobparser.utils.HHParser.get_vacancies')
    hh_mock.return_value = expected_hh
    vk_mock = aio_patch(f'jobparser.utils.VkParser.get_vacancies')
    vk_mock.return_value = expected_vk

    mock_create = aio_patch('jobparser.utils.create_vacancy_batch')

    await utils.parse_vacancies_to_db(parsers=['vk', 'hh'])

    mock_create_vacancies_data_list = [
        call.args[1] for call in mock_create.await_args_list
    ]

    assert farpost_mock.await_count == 0
    assert superjob_mock.await_count == 0
    assert hh_mock.await_count == 1
    assert vk_mock.await_count == 1

    assert expected_hh in mock_create_vacancies_data_list
    assert expected_vk in mock_create_vacancies_data_list



        
