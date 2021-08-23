import aiohttp
from typing import List, Optional

from jobparser.parsers import HHParser, SuperjobParser, AvitoParser, FarpostParser
import config


PARSERS_CONFIG = config.PARSERS_CONFIG


parsers_registry = {
    'avito': AvitoParser,
    'farpost': FarpostParser,
    'superjob': SuperjobParser,
    'hh': HHParser,
}

# async def run_parsers(parsers=Optional[List[str]]=None):
#     """
#     Run parsers from parsers registry.
    
#     :param parsers: If passed then only passed parsers will be run.
#     """
#     async with aiohttp.ClientSession() as session:
#         if parsers is None:
#             parsers = PARSERS_CONFIG.keys()

#         for parser in parsers:
#             parser_

    
