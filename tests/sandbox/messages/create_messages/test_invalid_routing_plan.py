import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants.messages_paths import MESSAGES_ENDPOINT


CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_no_such_routing_plan(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_no_such_routing_plan.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": f"0{str(uuid.uuid1())[1:]}",
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "1982-03-17"
                },
                "personalisation": {}
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("routing_plan_id", [
    "c8857ccf-06ec-483f-9b3a-7fc732d9ad48",
    "aeb16ab8-cb9c-4d23-92e9-87c78119175c"
])
def test_500_routing_plan_with_missing_template(nhsd_apim_proxy_url, correlation_id, routing_plan_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_500_missing_routing_plan.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
        "X-Correlation-Id": correlation_id
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
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        500,
        Generators.generate_missing_routing_plan_template_error(),
        correlation_id
    )
