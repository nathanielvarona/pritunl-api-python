import csv
import json
from urllib.parse import urlparse

from . import pritunl
from .utils.query import org_user

import click

from rich import print_json
from rich.console import Console
console = Console(width=160)


def get_user(**kwargs):
    org, user = org_user(pritunl_obj=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])
    key = pritunl.key.get(org_id=org['id'], usr_id=user['id'])

    if kwargs['get_profile_key_only']:
        console.print(
            f"USER KEY INFORMATION FOR `{user['name']}` FROM `{org['name']}` ORGANIZATION",
            f"TEMPORARY PROFILE KEY (Expires after 24 hours)",
            style="green bold", sep='\n'
        )
        console.print(
            f"PROFILE URI (PRITUNNL CLIENT IMPORT PROFILE): '{urlparse(pritunl.BASE_URL)._replace(scheme='pritunl').geturl() + key.json()['uri_url']}'",
            f"PROFILE URL (WEB VIEW PROFILE): '{pritunl.BASE_URL + key.json()['view_url']}'",
            style="blue", sep='\n', end='\n \n', new_line_start=True
        )
    else:
        console.print(
            f"USER INFORMATION FOR `{user['name']}` FROM `{org['name']}` ORGANIZATION",
            style="green bold", end='\n \n'
        )
        print_json(json.dumps(user))


def create_user(**kwargs):
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
            key = pritunl.key.get(org_id=user['organization'], usr_id=user['id'])
            context = {
                'key_urls': {
                    'uri_url': urlparse(pritunl.BASE_URL)._replace(scheme='pritunl').geturl() + key.json()['uri_url'],
                    'view_url': pritunl.BASE_URL + key.json()['view_url'],
                }
            }
            console.print(
                f"USER `{user['name']}` WITH AN EMAIL `{user['email']}` FOR `{user['organization_name']}` ORGANIZATION IS SUCCESSFULLY CREATED!",
                f"TEMPORARY PROFILE KEY (Expires after 24 hours)",
                style="green bold", sep='\n', new_line_start=True
            )

            console.print(
                f"PROFILE URI (PRITUNNL CLIENT IMPORT PROFILE): '{context['key_urls']['uri_url']}'",
                f"PROFILE URL (WEB VIEW PROFILE): '{context['key_urls']['view_url']}'",
                style="blue", sep='\n', end='\n \n', new_line_start=True
            )

    if kwargs['org_name'] and kwargs['user_name'] and kwargs['user_email'] and not kwargs['from_csv_file']:
        org, user = org_user(pritunl_obj=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])
        if not user:
            __create_user(org_id=org['id'], user_name=kwargs['user_name'], user_email=kwargs['user_email'])
        else:
            console.print(
                f"User `{kwargs['user_name']}` already exist for organization `{kwargs['org_name']}`, escaping user creation!",
                style="red bold", new_line_start=True, end='\n \n'
            )

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
                console.print(
                    f"User `{row['Username']}` already exist for organization `{row['Organization']}`, escaping user creation!",
                    style="red bold"
                )
            console.rule()

    else:
        if not kwargs['org_name'] and not kwargs['user_name'] and not kwargs['user_email'] and not kwargs['from_csv_file']:
            raise click.UsageError('Error: You entered with empty options.')
        else:
            raise click.UsageError('Error: You entered an invalid combination of options.')



def update_user(**kwargs):
    org, user = org_user(pritunl_obj=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])
    user_data = {
        'name': user['name'],
        'email': user['email'],
        'disabled': False,
    }

    if kwargs['disable']:
        user_data.update({'disabled': True})

    response = pritunl.user.put(org_id=org['id'], usr_id=user['id'], data=user_data)
    if response:
        console.print(
            f"USER `{user['name']}` FROM `{org['name']}` ORGANIZATION WAS SUCCESSFULLY `{'DISABLED' if response['disabled']==True else 'ENABLED'}`",
            style="green bold", sep='\n', new_line_start=True
        )

def delete_user(**kwargs):
    org, user = org_user(pritunl_obj=pritunl, org_name=kwargs['org_name'], user_name=kwargs['user_name'])
    response = pritunl.user.delete(org_id=org['id'], usr_id=user['id'])

    if response:
        console.print(
            f"USER `{user['name']}` FROM `{org['name']}` ORGANIZATION WAS SUCCESSFULLY DELETED",
            style="green bold", sep='\n', new_line_start=True
        )
