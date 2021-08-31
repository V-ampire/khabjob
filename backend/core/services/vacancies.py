"""
Business logic to operate with vacancies.
"""
from core.db.schema import vacancies_table
from core.db.utils import except_tsvector_columns

from aiopg.sa import SAConnection
from aiopg.sa.result import RowProxy
from datetime import date
from sqlalchemy import select, insert

from typing import List, Dict, Optional


async def create_vacancy(conn: SAConnection, **vacancy_data):
    """Create new vacancy in database."""
    stmt = insert(vacancies_table).values(**vacancy_data)
    await conn.execute(stmt)


async def create_vacancy_batch(conn: SAConnection, vacancies_data: List[Dict[str, str]]):
    """Create batch of vacancies in database."""
    stmt = insert(vacancies_table, vacancies_data)
    await conn.execute(stmt)


async def filter_vacancies(conn: SAConnection, 
    limit: Optional[int]=None, offset: int=0, **options) -> List[RowProxy]:
    """
    Return list of filtered with options vacancies.
    
    :param limit: Number of vacancies to return.
    :param offset: Number of vacancies to skip before to collect.
    :param options: Options to filter vacancies.
    """
    columns = except_tsvector_columns(vacancies_table)
    stmt = select(*columns).filter_by(**options).limit(limit).offset(offset)
    result = await conn.execute(stmt)
    return await result.fetchall()


async def search_vacancies(conn: SAConnection, 
                            date_from: Optional[date]=None, date_to: Optional[date]=None, 
                            search_query: Optional[str]=None, published_only: bool=True, 
                            limit: Optional[int]=None, offset: int=0):
    """
    Search vacancies by params.

    :param date_from: Collect vacancies with modified_at after this date.
    :param date_to: Collect vacancies with modified_at before this date.
    :param search_query: Search this phrase in indexed fields - name.
    :param published_only: If true, return only published vacancies.
    :param limit: Number of vacancies to return.
    :param offset: Number of vacancies to skip before to collect.
    """
    columns = except_tsvector_columns(vacancies_table)
    if published_only:
        stmt = select(*columns).filter_by(is_published=True)
    else:
        stmt = select(*columns)

    if date_from is not None:
        stmt = stmt.where(vacancies_table.c.modified_at >= date_from)

    if date_to is not None:
        stmt = stmt.where(vacancies_table.c.modified_at <= date_to)

    if search_query is not None:
        stmt = stmt.where(vacancies_table.c.search_index.match(str(search_query)))

    stmt = stmt.limit(limit).offset(offset)
    result = await conn.execute(stmt)
    return await result.fetchall()
    