import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators
import lib.constants.constants as constants
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.constants.constants import INVALID_ROUTING_PLAN_PROD
from lib.fixtures import *  # NOSONAR


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


@pytest.mark.prodtest
def test_no_such_routing_plan(bearer_token_prod):
    """
    .. include:: ../../partials/invalid_routing_plans/test_no_such_routing_plan.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        None
    )


@pytest.mark.prodtest
def test_routing_plan_not_belonging_to_client_id(bearer_token_prod):
    """
    .. include:: ../../partials/invalid_routing_plans/test_routing_plan_not_belonging_to_client_id.rst
    """
    resp = requests.post(
        f"{constants.PROD_URL}{MESSAGES_ENDPOINT}",
        headers={
            **headers,
            "Authorization": bearer_token_prod.value
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
        None
    )
