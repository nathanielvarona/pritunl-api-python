import csv
import json
from urllib.parse import urlparse

from . import pritunl

from pritunl_api.utils.query import org_user
from pritunl_api.utils.genkey import profile_key

import click

from rich import print_json
from rich.console import Console
from rich.table import Table

console = Console()


def get_user(**kwargs):
    table = Table(
        title=f"User Profile and Key Information:",
        title_style="bold green",
        title_justify="left"
        )

    table.add_column("User Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Organization", justify="left", style="magenta")
    table.add_column("Profile URL [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")
    table.add_column("Profile URI [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")

    org, user = org_user(pritunl_obj=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])

    if user:
        key_uri_url, key_view_url = profile_key(pritunl_obj=pritunl, org_id=org['id'], usr_id=user['id'])

        table.add_row(f"{user['name']}", f"{org['name']}", f"{key_view_url}", f"{key_uri_url}")
        console.print(table)

        if kwargs['show_advanced_details']:
            console.print(
                f"Advanced Details:",
                style="blue bold"
            )
            print_json(json.dumps(user))
    else:
        console.print(f"[bold red]No user profile found![/bold red]")


def create_user(**kwargs):
    table = Table(
        title=f"User Profile Created and Key Information:",
        title_style="bold green",
        title_justify="left",
        show_lines=True
        )

    table.add_column("Action", justify="left", style="green", no_wrap=True)
    table.add_column("User Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("User Email", justify="left", style="cyan", no_wrap=True)
    table.add_column("Organization", justify="left", style="magenta")
    table.add_column("Profile URL [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")
    table.add_column("Profile URI [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")

    def __create_user(org_id, user_name, user_email):
        user_data = {
            'name': user_name,
            'email': user_email
        }

        if kwargs['pin']:
            user_data["pin"] = kwargs['pin']

        if kwargs['yubikey_id']:
            user_data["auth_type"] = "yubico"
            user_data["yubico_id"] = kwargs['yubikey_id'][:12]

        create_user = pritunl.user.post(org_id=org_id, data=user_data)

        for user in create_user:
            key_uri_url, key_view_url = profile_key(pritunl_obj=pritunl, org_id=org['id'], usr_id=user['id'])

            table.add_row(f"[green]Created[/green]", f"{user['name']}", f"{user['email']}", f"{user['organization_name']}", f"{key_view_url}", f"{key_uri_url}")

    if kwargs['org_name'] and kwargs['user_name'] and kwargs['user_email'] and not kwargs['from_csv_file']:
        org, user = org_user(pritunl_obj=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])

        if not user:
            __create_user(org_id=org['id'], user_name=kwargs['user_name'], user_email=kwargs['user_email'])
        else:
            key_uri_url, key_view_url = profile_key(pritunl_obj=pritunl, org_id=org['id'], usr_id=user['id'])
            table.add_row(f"[yellow]Skipped[/yellow]", f"{user['name']}", f"{user['email']}", f"{user['organization_name']}", f"{key_view_url}", f"{key_uri_url}")

        console.print(table)

    elif kwargs['from_csv_file'] and not kwargs['org_name'] and not kwargs['user_name'] and not kwargs['user_email']:
        csv_list = []
        with open(kwargs['from_csv_file']) as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                csv_list.append(row)

        for row in csv_list:
            org, user = org_user(pritunl_obj=pritunl, org_name=row['Organization'], user_name=row['Username'])
            if not user:
                __create_user(org_id=org['id'], user_name=row['Username'], user_email=row['Email'])
            else:
                key_uri_url, key_view_url = profile_key(pritunl_obj=pritunl, org_id=org['id'], usr_id=user['id'])
                table.add_row(f"[yellow]Skipped[/yellow]", f"{user['name']}", f"{user['email']}", f"{user['organization_name']}", f"{key_view_url}", f"{key_uri_url}")

        console.print(table)

    else:
        if not kwargs['org_name'] and not kwargs['user_name'] and not kwargs['user_email'] and not kwargs['from_csv_file']:
            raise click.UsageError('Error: You entered with empty options.')
        else:
            raise click.UsageError('Error: You entered an invalid combination of options.')


def update_user(**kwargs):

    table = Table(
        title=f"User Profile Update and Key Information:",
        title_style="bold green",
        title_justify="left",
        )

    table.add_column("Action", justify="left", style="green", no_wrap=True)
    table.add_column("User Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Organization", justify="left", style="magenta")
    table.add_column("Profile URL [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")
    table.add_column("Profile URI [italic red](Expires after 24 hours)[/italic red]", justify="left", style="green")

    org, user = org_user(pritunl_obj=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])

    if user:
        user_data = {
            'name': user['name'],
            'email': user['email'],
            'disabled': False,
        }

        if kwargs['pin']:
            user_data["pin"] = kwargs['pin']

        if kwargs['disable']:
            user_data.update({'disabled': True})

        response = pritunl.user.put(org_id=org['id'], usr_id=user['id'], data=user_data)

        if response:
            key_uri_url, key_view_url = profile_key(pritunl_obj=pritunl, org_id=org['id'], usr_id=user['id'])
            table.add_row(f"[yellow]Updated[/yellow]", f"{user['name']}", f"{user['organization_name']}", f"{key_view_url}", f"{key_uri_url}")
            console.print(table)

    else:
        console.print(f"[bold red]No user profile to update![/bold red]")


def delete_user(**kwargs):

    table = Table(
        title=f"User Profile Delete:",
        title_style="bold green",
        title_justify="left",
        )

    table.add_column("Action", justify="left", style="green", no_wrap=True)
    table.add_column("User Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Organization", justify="left", style="magenta")

    org, user = org_user(pritunl_obj=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])

    if user:
        response = pritunl.user.delete(org_id=org['id'], usr_id=user['id'])

        if response:
            table.add_row(f"[red]Deleted[/red]", f"{user['name']}", f"{user['organization_name']}")
            console.print(table)

    else:
        console.print(f"[bold red]No user profile to delete![/bold red]")
