import click

from pritunl_api_cli.core import user

@click.group(help='Pritunl User')
def cli():
    pass

# Get User
@cli.command('get', no_args_is_help=True)
@click.option('--org-name')
@click.option('--user-name')
@click.option('--all-users', is_flag=True)
@click.option('--show-advanced-details', is_flag=True)
def user_get(**kwargs):
    """Pritunl Get User"""
    user.get(**kwargs)

# Create User
@cli.command('create', no_args_is_help=True)
@click.option('--org-name')
@click.option('--user-name')
@click.option('--user-email')
@click.option('--pin')
@click.option('--yubikey-id')
@click.option('--from-csv', type=click.Path(exists=True))
def create(**kwargs):
    """Pritunl Create User"""
    user.create(**kwargs)

# Update User
@cli.command('update', no_args_is_help=True)
@click.option('--org-name')
@click.option('--user-name')
@click.option('--pin')
@click.option('--yubikey-id')
@click.option('--disable/--enable', default=False)
def update(**kwargs):
    """Pritunl Update User"""
    user.update(**kwargs)

# Delete User
@cli.command('delete', no_args_is_help=True)
@click.option('--org-name')
@click.option('--user-name')
def delete(**kwargs):
    """Pritunl Delete User"""
    user.delete(**kwargs)
