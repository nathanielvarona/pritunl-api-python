import os
from pritunl_api import Pritunl

pritunl = Pritunl(
    url=os.environ.get('PRITUNL_BASE_URL'),
    token=os.environ.get('PRITUNL_API_TOKEN'),
    secret=os.environ.get('PRITUNL_API_SECRET')
)
