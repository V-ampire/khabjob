import aiohttp
from aiopg.sa import create_engine
from typing import List, Optional, Dict

from jobparser.parsers import HHParser, SuperjobParser, VkParser, FarpostParser
from config import PARSERS_CONFIG
from core.services.vacancies import create_vacancy_batch
from core.db.utils import get_postgres_dsn


PARSERS_REGISTRY = {
    'farpost': FarpostParser,
    'superjob': SuperjobParser,
    'hh': HHParser,
    'vk': VkParser,
}


async def parse_vacancies_to_db(parsers: List[str]=[]):
    """
    Parse vacancies and save to database.
    
    :param parsers: If passed then only passed parsers will be run.
    """
    if len(parsers) > 0:
        configs = dict(filter(lambda x: x[0] in parsers, PARSERS_CONFIG.items()))
    else:
        configs = PARSERS_CONFIG

    async with aiohttp.ClientSession() as session:
        for parser_name in configs.keys():
            parser_class = PARSERS_REGISTRY[parser_name]
            parser = parser_class(session, configs[parser_name])
            vacancies = await parser.get_vacancies()
            async with create_engine(get_postgres_dsn()) as aio_engine:
                async with aio_engine.acquire() as conn:
                    await create_vacancy_batch(conn, vacancies)


async def run_parsers(parsers: List[str]=[]) -> List[Dict[str, str]]:
    """Run parser and return results as list of dicts."""
    if len(parsers) > 0:
        configs = dict(filter(lambda x: x[0] in parsers, PARSERS_CONFIG.items()))
    else:
        configs = PARSERS_CONFIG

    result = []

    async with aiohttp.ClientSession() as session:
        for parser_name in configs.keys():
            parser_class = PARSERS_REGISTRY[parser_name]
            parser = parser_class(session, configs[parser_name])
            vacancies = await parser.get_vacancies()
            result.extend(vacancies)

    return result


