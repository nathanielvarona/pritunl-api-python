import click

from pritunl_api_cli.core import api

@click.group(help='Pritunl API Utilities')
def cli():
    pass

@cli.command('status')
def status():
    """Pritunl API Connection"""
    api.status()
