def org_user(pritunl, org_name, user_name=None):
    """
    Retrieve an organization and optionally a user from Pritunl.

    Args:
        pritunl (object): Pritunl API client
        org_name (str): Name of the organization
        user_name (str, optional): Name of the user. If not provided, returns all users in the organization.

    Returns:
        tuple: (org, user) where org is the organization object and user is the user object or a list of user objects

    Notes:
        If user_name is provided, returns the user object if found, otherwise returns None.
        If user_name is not provided, returns a list of all user objects in the organization.
    """
    def __get_by_name(objs, name):
        for obj in objs:
            if obj['name'] == name:
                return obj
        return None

    org = next((org for org in pritunl.organization.get() if org['name'] == org_name), None)
    if user_name:
        user = next((user for user in pritunl.user.get(org_id=org['id']) if user['name'] == user_name), None)
    else:
        user = pritunl.user.get(org_id=org['id'])  # Return all users
    return org, user
