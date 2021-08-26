"""
Command line interface.
"""
import asyncio
import click
from typing import List

from core.db.utils import setup_db
from jobparser.utils import parse_vacancies_to_db, run_parsers
# run app


async def echo_parsers_results(parsers: List[str]=[]):
    results = await run_parsers(parsers)
    click.echo(results)


@click.group()
def cli():
    pass


@click.command(name='init_db')
def initdb():
    setup_db()


@click.command(name='update_vacancies')
@click.option('-p', '--parsers', multiple=True, help="Names of parsers to run.")
def updatevacancies(parsers: List[str]):
    asyncio.run(parse_vacancies_to_db(parsers))
    

@click.command(name='run_parsers')
@click.option('-p', '--parsers', multiple=True, help="Names of parsers to run.")
def runparsers(parsers: List[str]):
    asyncio.run(echo_parsers_results(parsers))


cli.add_command(updatevacancies)
cli.add_command(runparsers)
cli.add_command(initdb)


if __name__ == '__main__':
    cli()