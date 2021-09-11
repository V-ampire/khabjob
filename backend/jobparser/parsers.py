import asyncio

import aiofiles

from bs4 import BeautifulSoup

import json
from itertools import count
from random import uniform
import time
from typing import List, Dict

from jobparser.base import BaseParser

from config import BASE_DIR


class HHParser(BaseParser):
    """Parser for vacancies from hh.ru."""

    base_url = 'https://hh.ru'
    name = 'hh'

    async def get_vacancies(self) -> List[Dict[str, str]]:
        """Return vacancies from hh.ru."""
        vacancies = []

        params = {
            "area": 102,
            "period": 1,
            "text": "Хабаровск",
        }
        vacancies = []

        data = await self.get_json(self.parse_url, params=params)

        if data:
            for item in data['items']:
                vacancy = {
                    'name': item['name'],
                    'source': item['alternate_url'],
                    'source_name': self.name,
                }
                vacancies.append(vacancy)
        return vacancies


class SuperjobParser(BaseParser):
    """Parser for vacancies from superjob.ru."""

    base_url = "https://superjob.ru"
    name = 'superjob'

    async def get_vacancies(self) -> List[Dict[str, str]]:
        """Return vacancies from superjob.ru."""
        vacancies = []

        params = {
            'period': 1,
            'town': 56
        }
        headers = {
            'X-Api-App-Id': self.config.get('secret_key')
        }
        url = '{0}/{1}/vacancies'.format(self.parse_url, self.config.get('v'))
        
        data = await self.get_json(url, params=params, headers=headers)

        if data:
            for item in data['objects']:
                vacancy = {
                    'name': item['profession'],
                    'source': item['link'],
                    'source_name': self.name
                }
                vacancies.append(vacancy)
        return vacancies


class FarpostParser(BaseParser):
    """Parser for vacancies from farpost.ru."""

    base_url = "https://www.farpost.ru"
    name = 'farpost'

    _page_count = count(1)

    def get_next_page_url(self) -> str:
        """Return next paginated url for parse."""
        return '{0}/?page={1}'.format(self.parse_url, next(self._page_count))

    async def load_cookies(self) -> Dict[str, str]:
        """Load cookie from local json-file."""
        cookie_file = BASE_DIR.joinpath('jobparser', 'cookies', 'farpost.json')
        async with aiofiles.open(cookie_file, mode='r') as f:
            content = await f.read()
        return json.loads(content)

    async def get_vacancies(self) -> List[Dict[str, str]]:
        """Return vacancies from farpost.ru."""
        vacancies = []
        cookies = await self.load_cookies()

        while True:

            markup = await self.get_html(self.get_next_page_url(), cookies=cookies)
            html = BeautifulSoup(markup, "lxml")

            items = html.find_all('tr', class_='bull-item')
            for item in items:
                if self.is_today_vacancy(item):
                    vacancy = {
                        'name': item.find('a', class_='bulletinLink').get_text(),
                        'source': '{0}{1}'.format(
                            self.base_url,
                            item.find('a', class_='bulletinLink').get('href')
                        ),
                        'source_name': self.name,
                    }
                    vacancies.append(vacancy)

            if len(items) == 0 or not self.is_today_vacancy(items[-1]):
                return vacancies

            await asyncio.sleep(uniform(2,3))

    def is_today_vacancy(self, item) -> bool:
        """
        Todays vacancies include word 'сегодня' in the item-date node,
        or have no date at all.
        """
        date_div = item.find('div', class_='date')
        return date_div is None or date_div.get_text().find('сегодня') >= 0


class VkParser(BaseParser):
    """Parser for vacancies from vk.ru."""

    base_url = "https://vk.com"
    name = 'vk'

    async def get_vacancies(self) -> List[Dict[str, str]]:
        """Return vacancies from farpost.ru."""
        vacancies = []

        params = {
            'q': r'#РаботаХабаровск',
            'access_token': self.config.get('access_token'),
            'v': self.config.get('v'),
            'start_time': int(time.time()) - 86400,
        }

        data = await self.get_json(self.parse_url, params=params)

        if data:
            for post in data['response']['items']:
                name_end_index = post.get('text').find('\n')
                vacancy = {
                    'name': post.get('text')[:name_end_index],
                    'source': '{0}/wall{1}_{2}'.format(
                        self.base_url,
                        str(post.get('owner_id')), 
                        post.get('id'),
                    ),
                    'source_name': self.name,
                }
                vacancies.append(vacancy)
        return vacancies
        
