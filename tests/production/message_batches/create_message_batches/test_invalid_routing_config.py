import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants.constants import PROD_URL, INVALID_ROUTING_PLAN_PROD
from lib.constants.message_batches_paths import MESSAGE_BATCHES_ENDPOINT
from lib.fixtures import *  # NOSONAR


@pytest.mark.prodtest
def test_no_such_routing_plan(bearer_token_prod):
    """
    ..py:function:: test_no_such_routing_plan

    .. include:: ../../partials/invalid_routing_plans/test_no_such_routing_plan.rst
    """
    resp = requests.post(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": bearer_token_prod.value,
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
        None
    )


@pytest.mark.prodtest
def test_routing_plan_not_belonging_to_client_id(bearer_token_prod):
    """
    .. include:: ../../partials/invalid_routing_plans/test_routing_plan_not_belonging_to_client_id.rst
    """
    resp = requests.post(f"{PROD_URL}{MESSAGE_BATCHES_ENDPOINT}", headers={
        "Authorization": bearer_token_prod.value,
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
        None
    )
