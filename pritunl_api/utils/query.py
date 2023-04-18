def org_user(pritunl, org_name, user_name=None):
    def __get_org_by_name(orgs_obj, org_name):
        for org in orgs_obj:
            if org['name'] == org_name:
                return org
        return None

    def __get_user_by_name(users_obj, user_name):
        for user in users_obj:
            if user["name"] == user_name:
                return user
        return None

    org = __get_org_by_name(pritunl.organization.get(), org_name)
    user = pritunl.user.get(org_id=org['id'])

    if user_name:
        user = __get_user_by_name(pritunl.user.get(org_id=org['id']), user_name)
        return org, user

    return org, user
