def org_user(pritunl_obj, org_name, user_name=None):
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

    org = __get_org_by_name(pritunl_obj.organization.get(), org_name)

    if user_name:
        user = __get_user_by_name(pritunl_obj.user.get(org_id=org['id']), user_name)
        return org, user
    return org
