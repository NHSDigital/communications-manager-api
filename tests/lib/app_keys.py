
def ensure_api_product_in_application(developer_app_keys_api, dev_email, app_name, key_id, api_product_name):
    r = developer_app_keys_api.get_app_key(
            dev_email,
            app_name,
            key_id
            )
    if {'apiproduct': api_product_name, 'status': 'approved'} not in r['apiProducts']:
        print('adding proxy')
        r2 = developer_app_keys_api.post_app_key(
            email=dev_email,
            app_name=app_name,
            key=key_id,
            body={'apiProducts': [api_product_name]}
            )
        return r2
    else:
        return r


def ensure_api_product_not_in_application(
        developer_app_keys_api,
        dev_email,
        app_name,
        key_id,
        api_product_name):
    try:
        return developer_app_keys_api.delete_product_app_key_association(
                email=dev_email,
                app_name=app_name,
                app_key=key_id,
                apiproduct_name=api_product_name
                )
    # we could do with the library giving a more specific error
    #
    # we want this for when the API product already doesn't exist and we have
    # no need to remove anything (i.e. there are more than one test workers)
    except Exception:
        return None
