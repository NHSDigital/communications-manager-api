import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.constants.constants import DUPLICATE_ROUTING_PLAN_TEMPLATE_ID
from lib.constants.constants import MISSING_TEMPLATE_ROUTING_PLANS
from lib.constants.constants import INVALID_ROUTING_PLAN
from lib.constants.constants import CORRELATION_IDS
from lib.constants.constants import INT_URL
from lib.fixtures import *

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_no_such_routing_plan(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_no_such_routing_plan.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": bearer_token_int
        },
        json={
            "data": {
                "type": "Message",
                "attributes": {
                    "routingPlanId": f"f{str(uuid.uuid1())[1:]}",
                    "messageReference": str(uuid.uuid1()),
                    "recipient": {
                        "nhsNumber": "9990548609",
                        "dateOfBirth": "1982-03-17"
                    },
                    "personalisation": {}
                }
            }
        }
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_routing_plan_not_belonging_to_client_id(bearer_token_int, correlation_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_routing_plan_not_belonging_to_client_id.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": bearer_token_int
        },
        json={
            "data": {
                "type": "Message",
                "attributes": {
                    "routingPlanId": INVALID_ROUTING_PLAN,
                    "messageReference": str(uuid.uuid1()),
                    "recipient": {
                        "nhsNumber": "9990548609",
                        "dateOfBirth": "1982-03-17"
                    },
                    "personalisation": {}
                }
            }
        }
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("routing_plan_id", MISSING_TEMPLATE_ROUTING_PLANS)
def test_routing_plan_missing_templates(bearer_token_int, correlation_id, routing_plan_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_500_missing_routing_plan.rst
    """
    resp = requests.post(f"{INT_URL}{MESSAGES_ENDPOINT}", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": bearer_token_int
        }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": routing_plan_id,
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "1982-03-17"
                },
                "personalisation": {}
                }
            }
        }
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        500,
        Generators.generate_missing_routing_plan_template_error(),
        correlation_id
    )
