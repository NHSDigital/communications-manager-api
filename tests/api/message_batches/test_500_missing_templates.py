import requests
import pytest
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT
from lib.constants.constants import MISSING_TEMPLATE_ROUTING_PLANS


@pytest.mark.test
@pytest.mark.devtest
@pytest.mark.inttest
@pytest.mark.prodtest
@pytest.mark.parametrize("routing_plan_id", MISSING_TEMPLATE_ROUTING_PLANS)
def test_routing_plan_missing_templates(url, bearer_token, routing_plan_id):
    """
    .. include:: ../partials/invalid_routing_plans/test_500_missing_routing_plan.rst
    """
    headers = Generators.generate_valid_headers(bearer_token.value)
    data = Generators.generate_valid_create_message_batch_body("dev")
    data["data"]["attributes"]["routingPlanId"] = routing_plan_id

    resp = requests.post(
        f"{url}{MESSAGE_BATCHES_ENDPOINT}",
        headers=headers,
        json=data
        )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        500,
        Generators.generate_missing_routing_plan_template_error(),
        None
    )
