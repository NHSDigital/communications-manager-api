import requests
import pytest
import uuid
from lib import Assertions, Generators, Authentication
from lib.constants.constants import PROD_URL, CORRELATION_IDS, INVALID_ROUTING_PLAN_PROD
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_no_such_routing_plan(correlation_id):
    """
    ..py:function:: test_no_such_routing_plan

    .. include:: ../../partials/invalid_routing_plans/test_no_such_routing_plan.rst
    """
    resp = requests.post(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        "X-Correlation-Id": correlation_id
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
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "1982-03-17"
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


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_routing_plan_not_belonging_to_client_id(correlation_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_routing_plan_not_belonging_to_client_id.rst
    """
    resp = requests.post(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": f"{Authentication.generate_authentication('prod')}",
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": INVALID_ROUTING_PLAN_PROD,
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "1982-03-17"
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
