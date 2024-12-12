import requests
import pytest
import uuid
from lib import Assertions, Generators
import lib.constants.constants as constants
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT
from lib.fixtures import *  # NOSONAR

CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]

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
    resp = requests.post(f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": bearer_token_int.value
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": f"f{str(uuid.uuid1())[1:]}",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                        "recipient": {
                            "nhsNumber": "9990548609"
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

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
    resp = requests.post(f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
            **headers,
            "X-Correlation-Id": correlation_id,
            "Authorization": bearer_token_int.value
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": constants.INVALID_ROUTING_PLAN,
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                        "recipient": {
                            "nhsNumber": "9990548609"
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        correlation_id
    )


@pytest.mark.inttest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("routing_plan_id", constants.MISSING_TEMPLATE_ROUTING_PLANS)
def test_routing_plan_missing_templates(bearer_token_int, correlation_id, routing_plan_id,):
    """
    .. include:: ../../partials/invalid_routing_plans/test_500_missing_routing_plan.rst
    """
    resp = requests.post(f"{constants.INT_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
            **headers,
            "Authorization": bearer_token_int.value,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": routing_plan_id,
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                        "recipient": {
                            "nhsNumber": "9990548609"
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        500,
        Generators.generate_missing_routing_plan_template_error(),
        correlation_id
    )
