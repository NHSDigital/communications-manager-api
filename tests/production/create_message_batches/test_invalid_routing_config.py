import requests
import pytest
import uuid
from lib import Assertions, Generators, Authentication
from lib.constants import PROD_URL

CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]
INVALID_ROUTING_PLAN = "acd3d4b9-de96-49ef-9ab9-8ce03e678082"


@pytest.mark.prodtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_no_such_routing_plan(correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a routing plan \
        not belonging to the associated client ID receives a 404 'No Such Routing Plan' response

        | **Given** the API consumer provides a routing plan not associated to a client ID
        | **When** the request is submitted
        | **Then** the response returns a 404 no such routing plan error

    **Asserts**
    - Response returns a 404 'No Such Routing Plan' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided
    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{PROD_URL}/v1/message-batches", headers={
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
    .. py:function:: Test using someone elses routing plan
    """
    resp = requests.post(f"{PROD_URL}/v1/message-batches", headers={
            "Authorization": f"{Authentication.generate_authentication('prod')}",
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": INVALID_ROUTING_PLAN,
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
