from core.db.schema import vacancies_table

from aiopg.sa import SAConnection
from datetime import datetime
from sqlalchemy import select, insert

from typing import List, Dict


async def create_vacancy(conn: SAConnection, **vacancy_data):
    """Create new vacancy in database."""
    stmt = insert(vacancies_table).values(**vacancy_data)
    await conn.execute(stmt)


async def create_vacancy_batch(conn: SAConnection, vacancies_data: List[Dict[str, str]]):
    """Create batch of vacancies in database."""
    stmt = insert(vacancies_table, vacancies_data)
    await conn.execute(stmt)
    

async def get_vacancies_for_date(conn: SAConnection, date: datetime):
    """Return vacancies for date."""
    vacancies = await conn.execute(
        select(vacancies_table).where(vacancies_table.c.modified_at == date)
    )
