from urllib.parse import urlparse

def profile_key(pritunl, org_id, usr_id):
    key = pritunl.key.get(org_id=org_id, usr_id=usr_id)
    if key:
        key_uri_url = urlparse(pritunl.BASE_URL)._replace(scheme='pritunl').geturl() + key.json()['uri_url']
        key_view_url =  pritunl.BASE_URL + key.json()['view_url']
        return key_uri_url, key_view_url
    else:
        return None, None
