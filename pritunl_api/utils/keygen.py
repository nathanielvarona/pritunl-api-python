from urllib.parse import urlparse

def profile_key(pritunl, org_id, usr_id):
    """
    Generate URLs for a profile key in Pritunl.

    Args:
        pritunl (object): Pritunl API client
        org_id (str): Organization ID
        usr_id (str): User ID

    Returns:
        tuple: (key_uri_url, key_view_url) or (None, None) if no key is found
    """
    key = pritunl.key.get(org_id=org_id, usr_id=usr_id)
    if key:
        key_uri_url = urlparse(pritunl.BASE_URL)._replace(scheme='pritunl').geturl() + key['uri_url']
        key_view_url =  pritunl.BASE_URL + key['view_url']
        return key_uri_url, key_view_url
    else:
        return None, None
