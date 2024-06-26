import pytest
import os
from .authentication import AuthenticationCache
from .app_keys import assert_api_product_in_application, assert_api_product_not_in_application


@pytest.fixture(scope='session')
def proxy_name():
    try:
        return os.environ['API_PROXY']
    except KeyError:
        # fall back to PROXY_NAME
        return os.environ['PROXY_NAME']


# for now this is the same as PROXY_NAME
# this is here to illustrate how these can be decoupled
@pytest.fixture(scope='session')
def api_product_name():
    try:
        return os.environ['API_PROXY']
    except KeyError:
        # fall back to PROXY_NAME
        return os.environ['PROXY_NAME']


# define one of these for each key we have set up and intend to use
@pytest.fixture(scope='session')
def api_product_in_comms_manager_local(developer_app_keys_api, api_product_name):
    if api_product_name.startswith('communications-manager-pr-'):
        yield assert_api_product_in_application(
                developer_app_keys_api,
                'phillip.skinner2@nhs.net',
                'Comms-manager-local',
                os.environ['NON_PROD_API_KEY'],
                api_product_name)
        assert_api_product_not_in_application(
                developer_app_keys_api,
                'phillip.skinner2@nhs.net',
                'Comms-manager-local',
                os.environ['NON_PROD_API_KEY'],
                api_product_name)
    else:
        return None


# By setting the scope to session on the cache but leaving session scope OFF
# the fixtures for each bearer token, we ensure the cache is checked and has a
# chance to refresh before any test which might depend on a bearer token
@pytest.fixture(scope='session')
def authentication_cache():
    return AuthenticationCache()


@pytest.fixture
def bearer_token_internal_dev(authentication_cache, api_product_in_comms_manager_local):
    return authentication_cache.generate_authentication('internal-dev')


@pytest.fixture
def bearer_token_int(authentication_cache):
    return authentication_cache.generate_authentication('int')


@pytest.fixture
def bearer_token_prod(authentication_cache):
    return authentication_cache.generate_authentication('prod')
