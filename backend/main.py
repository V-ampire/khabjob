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
from typing import List

from api.app import init_app
from api.validation.auth import validate_password_format

from core.db.utils import create_db, apply_migrations, get_postgres_dsn
from core.services.auth import create_user

from jobparser.utils import parse_vacancies_to_db, run_parsers


async def echo_parsers_results(parsers: List[str]=[]):
    results = await run_parsers(parsers)
    click.echo(results)


async def add_user(username: str, password: str):
    async with create_engine(get_postgres_dsn()) as aio_engine:
        async with aio_engine.acquire() as conn:
            await create_user(conn, username, password)

    click.echo(click.style('User successfully created!', fg='green'))


class UserCredentials(BaseModel):
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
    pass


@click.command(name='init_db')
def initdb():
    """Create databse and apply migrations."""
    create_db()
    apply_migrations()
    asyncio.run(parse_vacancies_to_db())


@click.command(name='update_vacancies')
@click.option('-p', '--parsers', multiple=True, help="Names of parsers to run.")
def updatevacancies(parsers: List[str]):
    """Parse vacancies and save it yo database."""
    asyncio.run(parse_vacancies_to_db(parsers))
    

@click.command(name='run_parsers')
@click.option('-p', '--parsers', multiple=True, help="Names of parsers to run.")
def runparsers(parsers: List[str]):
    """Run parsers."""
    asyncio.run(echo_parsers_results(parsers))


@click.command(name='run_app')
def runapp():
    """Start API server."""
    app = init_app({})
    web.run_app(app)


@click.command(name='create_user')
def createuser():
    """Create user."""
    username = click.prompt('Username', type=str)
    password1 = click.prompt('Password', type=str, hide_input=True)
    password2 = click.prompt('Confirm passwrod', type=str, hide_input=True)

    user_credentials = UserCredentials(
        username=username,
        password1=password1,
        password2=password2
    )

    asyncio.run(add_user(user_credentials.username, user_credentials.password1))


cli.add_command(updatevacancies)
cli.add_command(runparsers)
cli.add_command(initdb)
cli.add_command(runapp)
cli.add_command(createuser)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cli()