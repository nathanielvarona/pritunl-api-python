import json

from . import pritunl

def status():
    try:
        status = pritunl.status()
        if status:
            print(json.dumps(status))
    except Exception as e:
        raise e
