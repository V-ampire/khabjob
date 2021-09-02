"""
Command line interface.
"""
from aiohttp import web
import asyncio
import click
import logging
from typing import List

from api.app import init_app
from core.db.utils import create_db, apply_migrations
from jobparser.utils import parse_vacancies_to_db, run_parsers


async def echo_parsers_results(parsers: List[str]=[]):
    results = await run_parsers(parsers)
    click.echo(results)


@click.group()
def cli():
    pass


@click.command(name='init_db')
def initdb():
    create_db()
    apply_migrations()
    asyncio.run(parse_vacancies_to_db())



@click.command(name='update_vacancies')
@click.option('-p', '--parsers', multiple=True, help="Names of parsers to run.")
def updatevacancies(parsers: List[str]):
    asyncio.run(parse_vacancies_to_db(parsers))
    

@click.command(name='run_parsers')
@click.option('-p', '--parsers', multiple=True, help="Names of parsers to run.")
def runparsers(parsers: List[str]):
    asyncio.run(echo_parsers_results(parsers))


@click.command(name='run_app')
def runapp():
    app = init_app({})
    web.run_app(app)


cli.add_command(updatevacancies)
cli.add_command(runparsers)
cli.add_command(initdb)
cli.add_command(runapp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cli()