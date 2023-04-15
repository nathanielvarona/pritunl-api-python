import click

# Pritunl
from .commands import connection
from .commands import users

@click.group()
@click.version_option(package_name='pritunl-api')
@click.pass_context
def run(ctx):
    pass

@run.command()
def status():
    connection.status()

# Get User
@run.command()
@click.option('--org-name')
@click.option('--user-name')
@click.option('--show-advanced-details', is_flag=True)
def get_user(**kwargs):
    users.get_user(**kwargs)

# Create User
@run.command()
@click.option('--org-name')
@click.option('--user-name')
@click.option('--user-email')
@click.option('--pin')
@click.option('--yubikey-id')
@click.option('--from-csv-file', type=click.Path(exists=True))
def create_user(**kwargs):
    users.create_user(**kwargs)

# Update User
@run.command()
@click.option('--org-name')
@click.option('--user-name')
@click.option('--pin')
@click.option('--yubikey-id')
@click.option('--disable/--enable', default=False)
def update_user(**kwargs):
    users.update_user(**kwargs)

# Delete User
@run.command()
@click.option('--org-name')
@click.option('--user-name')
def delete_user(**kwargs):
    users.delete_user(**kwargs)

if __name__ == '__main__':
    run()
