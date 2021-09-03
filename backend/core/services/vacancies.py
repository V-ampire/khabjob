"""
Business logic to operate with vacancies.
"""
from core.db.schema import vacancies_table
from core.db.utils import except_tsvector_columns, parse_unique_violation_fields

from aiopg.sa import SAConnection
from aiopg.sa.result import RowProxy
from datetime import date
from sqlalchemy import select, insert, over, func

from typing import List, Dict, Optional, Tuple


async def create_vacancy(conn: SAConnection, **vacancy_data) -> RowProxy:
    """Create new vacancy in database."""    
    stmt = insert(vacancies_table).values(**vacancy_data).returning(vacancies_table)
    result = await conn.execute(stmt)
    return await result.first()  


async def create_vacancy_batch(
    conn: SAConnection, vacancies_data: List[Dict[str, str]]) -> List[RowProxy]:
    """Create batch of vacancies in database."""
    stmt = insert(vacancies_table, vacancies_data).returning(vacancies_table)
    results = await conn.execute(stmt)
    return await results.fetchall()


async def filter_vacancies(conn: SAConnection, 
    limit: Optional[int]=None, offset: int=0, **options) -> List[RowProxy]:
    """
    Return list of filtered with options vacancies and count of all filtered items.
    
    :param limit: Number of vacancies to return.
    :param offset: Number of vacancies to skip before to collect.
    :param options: Options to filter vacancies.
    """
    columns = except_tsvector_columns(vacancies_table)
    stmt = select(*columns, func.count().over().label("count"))
    stmt = stmt.filter_by(**options).limit(limit).offset(offset).order_by(
                vacancies_table.c.modified_at, vacancies_table.c.source_name,
            )
    result = await conn.execute(stmt)
    return await result.fetchall()


async def search_vacancies(conn: SAConnection, 
                            date_from: Optional[date]=None, date_to: Optional[date]=None, 
                            search_query: Optional[str]=None, 
                            source_name: Optional[str]=None, published_only: bool=True, 
                            limit: Optional[int]=None, offset: int=0) -> List[RowProxy]:
    """
    Search vacancies by params.

    :param date_from: Collect vacancies with modified_at after this date.
    :param date_to: Collect vacancies with modified_at before this date.
    :param search_query: Search this phrase in indexed fields - name.
    :param published_only: If true, return only published vacancies.
    :param limit: Number of vacancies to return.
    :param offset: Number of vacancies to skip before to collect.

    :return: list of found vacancies and count of all found items.
    """
    columns = except_tsvector_columns(vacancies_table)
    if published_only:
        stmt = select(*columns, func.count().over().label("count")).filter_by(is_published=True)
    else:
        stmt = select(*columns)

    if date_from is not None:
        stmt = stmt.where(vacancies_table.c.modified_at >= date_from)

    if date_to is not None:
        stmt = stmt.where(vacancies_table.c.modified_at <= date_to)

    if search_query is not None:
        stmt = stmt.where(vacancies_table.c.search_index.match(str(search_query)))

    if source_name is not None:
        stmt = stmt.filter_by(source_name=source_name)

    stmt = stmt.limit(limit).offset(offset).order_by(
        vacancies_table.c.modified_at, vacancies_table.c.source_name
    )
    result = await conn.execute(stmt)
    return await result.fetchall()
    