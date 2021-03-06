"""Entrypoint."""
from aiohttp import web

from aiopg.sa import create_engine

from pydantic import (
    BaseModel, 
    validator,
)

import asyncio
import click
import logging
from logging.config import dictConfig
from typing import List, Optional

from api.app import init_app
from api.validation.auth import validate_password_format

from core.db.utils import create_db, apply_migrations, get_postgres_dsn
from core.services.auth import create_user
from core.services.vacancies import delete_expired_vacancies

from jobparser.utils import parse_vacancies_to_db, run_parsers

from config import LOG_CONFIG, DEBUG, VACANCY_EXPIRED


async def echo_parsers_results(parsers: Optional[List[str]] = None):
    """Output parses results."""
    if parsers is None:
        parsers = []
    results = await run_parsers(parsers)
    click.echo(results)


async def add_user(username: str, password: str):
    """Create new user and output message."""
    async with create_engine(get_postgres_dsn()) as aio_engine:
        async with aio_engine.acquire() as conn:
            await create_user(conn, username, password)

    click.echo(click.style('User successfully created!', fg='green'))


async def clean_up_expired_vacancies():
    """Clean up dtatabase and output message."""
    async with create_engine(get_postgres_dsn()) as aio_engine:
        async with aio_engine.acquire() as conn:
            deleted_count = await delete_expired_vacancies(conn, VACANCY_EXPIRED)

    click.echo(
        click.style('{0} vacancies were deleted!'.format(deleted_count), fg='green'),
    )


class UserCredentials(BaseModel):
    """Validate user credentials to create user."""

    username: str
    password1: str
    password2: str

    @validator('password1')
    def validate_password_strength(cls, password):
        validate_password_format(password)
        return password

    @validator('password2')
    def validate_passwords_match(cls, password2, values):
        password1 = values.get('password1')
        if password1 != password2:
            raise ValueError('Passwords mismatch.')  


@click.group()
def cli():
    """Initialize CLI."""


@click.command(name='init_db')
def initdb():
    """Create databse and apply migrations."""
    create_db()
    apply_migrations()
    asyncio.run(parse_vacancies_to_db())


@click.command(name='update_vacancies')
@click.option('-p', '--parsers', multiple=True, help='Names of parsers to run.')
def updatevacancies(parsers: List[str]):
    """Parse vacancies and save it yo database."""
    asyncio.run(parse_vacancies_to_db(parsers))
    

@click.command(name='run_parsers')
@click.option('-p', '--parsers', multiple=True, help='Names of parsers to run.')
def runparsers(parsers: List[str]):
    """Run parsers."""
    asyncio.run(echo_parsers_results(parsers))


@click.command(name='run_app')
@click.option('-h', '--host', type=str)
@click.option('-p', '--port', type=str)
@click.option('--path', type=str)
def runapp(host, port, path):
    """Start API server."""
    app = init_app()
    web.run_app(app, host=host, port=port, path=path)


@click.command(name='create_user')
def createuser():
    """Create user."""
    username = click.prompt('Username', type=str)
    password1 = click.prompt('Password', type=str, hide_input=True)
    password2 = click.prompt('Confirm passwrod', type=str, hide_input=True)

    user_credentials = UserCredentials(
        username=username,
        password1=password1,
        password2=password2,
    )

    asyncio.run(add_user(user_credentials.username, user_credentials.password1))


@click.command(name='drop_expired_vacancies')
def dropexpired():
    """Drop expired vacancies."""
    asyncio.run(clean_up_expired_vacancies())


cli.add_command(updatevacancies)
cli.add_command(runparsers)
cli.add_command(initdb)
cli.add_command(runapp)
cli.add_command(createuser)
cli.add_command(dropexpired)


if __name__ == '__main__':
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        dictConfig(LOG_CONFIG)
    cli()
