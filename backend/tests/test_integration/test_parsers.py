from jobparser.parsers import (
    HHParser, SuperjobParser, FarpostParser, VkParser
)
import config

import aiohttp
import pytest


@pytest.mark.skip(reason="no way of currently testing this")
async def test_farpost(loop):
    parser_config = config.PARSERS_CONFIG['farpost']

    async with aiohttp.ClientSession() as session:
        parser = FarpostParser(session, parser_config)
        vacancies = await parser.get_vacancies()
        
        assert len(vacancies) > 0
        for vacancy in vacancies:
            assert vacancy['name']
            assert vacancy['source']
            assert vacancy['source_name'] == parser.name


async def test_hh(loop):
    parser_config = config.PARSERS_CONFIG['hh']

    async with aiohttp.ClientSession() as session:
        parser = HHParser(session, parser_config)
        vacancies = await parser.get_vacancies()
        
        assert len(vacancies) > 0
        for vacancy in vacancies:
            assert vacancy['name']
            assert vacancy['source']
            assert vacancy['source_name'] == parser.name


async def test_superjob(loop):
    parser_config = config.PARSERS_CONFIG['superjob']

    async with aiohttp.ClientSession() as session:
        parser = SuperjobParser(session, parser_config)
        vacancies = await parser.get_vacancies()
        
        assert len(vacancies) > 0
        for vacancy in vacancies:
            assert vacancy['name']
            assert vacancy['source']
            assert vacancy['source_name'] == parser.name


@pytest.mark.skip(reason='Run separately, frequent case when no todays vacancies in VK')
async def test_vk(loop):
    parser_config = config.PARSERS_CONFIG['vk']

    async with aiohttp.ClientSession() as session:
        parser = VkParser(session, parser_config)
        vacancies = await parser.get_vacancies()
        
        assert len(vacancies) > 0 # Possible fail if no todays vacancies from vk
        for vacancy in vacancies:
            assert vacancy['name']
            assert vacancy['source']
            assert vacancy['source_name'] == parser.name
    