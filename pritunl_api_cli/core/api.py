import json
from rich import print_json

from . import pritunl

def status():
    try:
        status = pritunl.status()
        if status:
            print_json(json.dumps(status))
    except Exception as e:
        raise e
