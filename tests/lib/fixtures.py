import pytest
import os
import re
from .authentication import AuthenticationCache
from .app_keys import ensure_api_product_in_application, ensure_api_product_not_in_application
from .rate_limiting import RateLimiting
from lib.constants.constants import PROD_URL


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
        yield ensure_api_product_in_application(
                developer_app_keys_api,
                'phillip.skinner2@nhs.net',
                'Comms-manager-local',
                os.environ['NON_PROD_API_KEY'],
                api_product_name)
        ensure_api_product_not_in_application(
                developer_app_keys_api,
                'phillip.skinner2@nhs.net',
                'Comms-manager-local',
                os.environ['NON_PROD_API_KEY'],
                api_product_name)
    else:
        yield None


@pytest.fixture(scope='session')
def api_product_in_nhs_notify_test_client_1(developer_app_keys_api, api_product_name):
    if api_product_name.startswith('communications-manager-pr-'):
        yield ensure_api_product_in_application(
                developer_app_keys_api,
                'ian.hodges1@nhs.net',
                'NHS Notify Test Client 1',
                os.environ['NON_PROD_API_KEY_TEST_1'],
                api_product_name)
        ensure_api_product_not_in_application(
                developer_app_keys_api,
                'ian.hodges1@nhs.net',
                'NHS Notify Test Client 1',
                os.environ['NON_PROD_API_KEY_TEST_1'],
                api_product_name)
    else:
        yield None


# By setting the scope to session on the cache but leaving session scope OFF
# the fixtures for each bearer token, we ensure the cache is checked and has a
# chance to refresh before any test which might depend on a bearer token
@pytest.fixture(scope='session')
def authentication_cache():
    return AuthenticationCache()


@pytest.fixture
def bearer_token_internal_dev_test_1(authentication_cache,
                                     api_product_in_nhs_notify_test_client_1,
                                     nhsd_apim_proxy_url):
    return authentication_cache.generate_authentication('internal-dev-test-1', nhsd_apim_proxy_url)


@pytest.fixture(scope='session')
def rate_limiting(products_api, api_product_name, developer_apps_api):
    rate_limiting = RateLimiting(products_api, developer_apps_api, api_product_name, 5)
    yield rate_limiting
    rate_limiting.set_default_rate_limit()
    rate_limiting.remove_app_ratelimit('ian.hodges1@nhs.net', 'NHS Notify Test Client 1')


@pytest.fixture(scope='session')
def url(api_product_name):
    if api_product_name is not None and api_product_name.startswith('communications-manager-pr-'):
        pr_number = re.search(r'\d+', api_product_name).group()
        suffix = f"comms-pr-{pr_number}"
    else:
        suffix = "comms"

    environment = os.environ['API_ENVIRONMENT']
    if environment == "prod":
        return "https://api.service.nhs.uk/comms"
    # authentication for ref and ref2 is shared with internal-dev
    elif environment in ["ref", "ref2"]:
        return "https://internal-dev.api.service.nhs.uk/comms"
    else:
        return f"https://{environment}.api.service.nhs.uk/{suffix}"


@pytest.fixture()
def bearer_token(authentication_cache, api_product_in_comms_manager_local):
    environment = os.environ['API_ENVIRONMENT']
    if environment == "prod":
        url = PROD_URL
    # the ref2 url is structured slightly differently so it needs to be explicitly called out here
    elif environment == "ref2":
        url = "https://ref.api.service.nhs.uk/comms-2"
    else:
        url = f"https://{environment}.api.service.nhs.uk/comms"
    return authentication_cache.generate_authentication(environment, url)
