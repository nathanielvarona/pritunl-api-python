import click

# Pritunl
from .commands import user

@click.group()
def run():
    pass

# Get User
@run.command()
@click.option('--org-name')
@click.option('--user-name')
@click.option('--get-profile-key-only', is_flag=True)
def get_user(**kwargs):
    user.get_user(**kwargs)

# Create User
@run.command()
@click.option('--org-name')
@click.option('--user-name')
@click.option('--user-email')
@click.option('--pin')
@click.option('--yubikey-id')
@click.option('--from-csv-file', type=click.Path(exists=True))
def create_user(**kwargs):
    user.create_user(**kwargs)

# Update User
@run.command()
@click.option('--org-name')
@click.option('--user-name')
@click.option('--disable/--enable', default=False)
def update_user(**kwargs):
    user.update_user(**kwargs)

# Delete User
@run.command()
@click.option('--org-name')
@click.option('--user-name')
def delete_user(**kwargs):
    user.delete_user(**kwargs)

if __name__ == '__main__':
    run()
