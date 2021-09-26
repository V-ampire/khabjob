import asyncio

import aiohttp

from aiopg.sa import create_engine

import logging
from typing import List, Dict, Optional

from jobparser.parsers import HHParser, SuperjobParser, VkParser, FarpostParser

from core.services.vacancies import create_or_update_vacancy
from core.db.utils import get_postgres_dsn

from config import PARSERS_CONFIG


PARSERS_REGISTRY = {
    'farpost': FarpostParser,
    'superjob': SuperjobParser,
    'hh': HHParser,
    'vk': VkParser,
}


logger = logging.getLogger(__name__)


async def parse_vacancies_to_db(parsers: List[str]=[]):
    """
    Parse vacancies and save to database.
    
    :param parsers: If passed then only passed parsers will be run.
    """
    if len(parsers) > 0:
        configs = dict(filter(lambda x: x[0] in parsers, PARSERS_CONFIG.items()))
    else:
        configs = PARSERS_CONFIG

    tasks = []

    async with aiohttp.ClientSession() as session:
        for parser_name in configs.keys():
            if configs[parser_name]['is_active']:
                parser_class = PARSERS_REGISTRY[parser_name]
                parser = parser_class(session, configs[parser_name])
                tasks.append(parser.get_vacancies())
        
        async with create_engine(get_postgres_dsn()) as aio_engine:
            async with aio_engine.acquire() as conn:
                for task in asyncio.as_completed(tasks):
                    vacancies = await task
                    created = 0
                    updated = 0
                    for vacancy in vacancies:
                        is_created, v = await create_or_update_vacancy(conn, **vacancy)

                        if is_created:
                            created += 1
                        else:
                            updated +=1

                    logger.info('Created: {0}, updated: {1} vacancies'.format(
                        created,
                        updated,
                    ))

                    
async def run_parsers(parsers: List[str]=[]) -> List[Dict[str, str]]:
    """Run parser and return results as list of dicts."""
    if len(parsers) > 0:
        configs = dict(filter(lambda x: x[0] in parsers, PARSERS_CONFIG.items()))
    else:
        configs = PARSERS_CONFIG

    tasks = []

    async with aiohttp.ClientSession() as session:
        for parser_name in configs.keys():
            if configs[parser_name]['is_active']:
                parser_class = PARSERS_REGISTRY[parser_name]
                parser = parser_class(session, configs[parser_name])
                tasks.append(parser.get_vacancies())
        vacancies = await asyncio.gather(*tasks)
    return vacancies
