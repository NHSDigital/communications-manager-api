import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators, Authentication
import lib.constants.constants as constants
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.constants.constants import INVALID_ROUTING_PLAN_PROD, CORRELATION_IDS


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_no_such_routing_plan(correlation_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_no_such_routing_plan.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "routingPlanId",
            f"f{str(uuid.uuid1())[1:]}"
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        correlation_id
    )


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_routing_plan_not_belonging_to_client_id(correlation_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_routing_plan_not_belonging_to_client_id.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": f"{Authentication.generate_authentication('prod')}"
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_body("prod"),
            "routingPlanId",
            INVALID_ROUTING_PLAN_PROD
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        correlation_id
    )
