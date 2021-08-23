from jobparser.parsers import (
    HHParser, SuperjobParser, FarpostParser, VkParser
)
import config

import aiohttp
import pytest


@pytest.mark.skip(reason="no way of currently testing this")
async def test_farpost():
    parser_config = config.PARSERS_CONFIG['farpost']

    async with aiohttp.ClientSession() as session:
        parser = FarpostParser(session, parser_config)
        vacancies = await parser.get_vacancies()
        
        assert len(vacancies) > 0
        for vacancy in vacancies:
            assert vacancy['name']
            assert vacancy['source']
            assert vacancy['source_name'] == parser.name


async def test_hh():
    parser_config = config.PARSERS_CONFIG['hh']

    async with aiohttp.ClientSession() as session:
        parser = HHParser(session, parser_config)
        vacancies = await parser.get_vacancies()
        
        assert len(vacancies) > 0
        for vacancy in vacancies:
            assert vacancy['name']
            assert vacancy['source']
            assert vacancy['source_name'] == parser.name


async def test_superjob():
    parser_config = config.PARSERS_CONFIG['superjob']

    async with aiohttp.ClientSession() as session:
        parser = SuperjobParser(session, parser_config)
        vacancies = await parser.get_vacancies()
        
        assert len(vacancies) > 0
        for vacancy in vacancies:
            assert vacancy['name']
            assert vacancy['source']
            assert vacancy['source_name'] == parser.name


async def test_vk():
    parser_config = config.PARSERS_CONFIG['vk']

    async with aiohttp.ClientSession() as session:
        parser = VkParser(session, parser_config)
        vacancies = await parser.get_vacancies()
        
        assert len(vacancies) > 0
        for vacancy in vacancies:
            assert vacancy['name']
            assert vacancy['source']
            assert vacancy['source_name'] == parser.name
    