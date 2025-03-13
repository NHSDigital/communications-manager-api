import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.constants.constants import INVALID_ROUTING_PLAN


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_no_such_routing_plan(url, bearer_token):
    """
    .. include:: ../partials/invalid_routing_plans/test_no_such_routing_plan.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["routingPlanId"] = f"f{str(uuid.uuid1())[1:]}"

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        None
    )


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
def test_routing_plan_not_belonging_to_client_id(url, bearer_token):
    """
    .. include:: ../partials/invalid_routing_plans/test_routing_plan_not_belonging_to_client_id.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_body("dev")
    data["data"]["attributes"]["routingPlanId"] = INVALID_ROUTING_PLAN

    resp = requests.post(
        f"{url}{MESSAGES_ENDPOINT}",
        headers=headers,
        json=data
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        None
    )
