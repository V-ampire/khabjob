from aiohttp import ClientSession
from typing import Dict, List, Any, Optional


class ParserConfigError(Exception):
    """Exception for invalid parser configuration."""


class BaseParser():
    """Base class for parsers."""

    base_url = None
    name = None

    DEFAULT_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

    def __init__(self, session: ClientSession, config: Dict) -> None:
        """Initialization."""
        if self.base_url is None:
            raise ParserConfigError(
                "You must set attribute base_url for relative url to vacancies."
            )

        if self.name is None:
            raise ParserConfigError(
                "You must set attribute name for parser."
            )

        try:
            self.parse_url = config['parse_url']
        except KeyError:
            raise ParserConfigError(
                "You must set 'parse_url' parameter in parser config."
            )

        self.config = config
        self.session = session

    async def get_html(self, url: str, **kwargs) -> str:
        """Load and return html from url."""
        headers = {
            'User-Agent': self.config.get('user_agent', self.DEFAULT_USER_AGENT)
        }
        async with self.session.get(url, headers=headers, raise_for_status=True, **kwargs) as resp:
            html = await resp.text()
        return html

    async def get_json(self, url: str, 
                       params: Optional[Dict[str, str]]=None,
                       headers: Optional[Dict[str, str]]=None,
                       **kwargs) -> Dict:
        """Get json data from url."""
        request_headers = {
            'User-Agent': self.config.get('user_agent', self.DEFAULT_USER_AGENT)
        }
        if headers is not None:
            request_headers.update(headers)

        async with self.session.get(url, params=params, headers=request_headers, raise_for_status=True, **kwargs) as resp:
            data = await resp.json()
        return data


    async def get_vacancies(self) -> Dict[str, Any]:
        """
        Return vacancies data as list of dicts in format:
        [
            {
                'name': 'vacancy-name', 
                'source': 'link-to-vacancy', 
                'source_name': 'source-name'
            },
            ...
        ]
        """
        raise NotImplementedError