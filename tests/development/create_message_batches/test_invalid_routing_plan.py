import requests
import pytest
import uuid
from lib import Assertions, Generators

CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]
DUPLICATE_ROUTING_PLAN_TEMPLATE_ID = "bb454d66-033b-45c0-bbb6-d9b3420a0bd4"
INVALID_ROUTING_PLAN = "ae0f772e-6660-4829-8f11-1ed8a3fc68c2"


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_no_such_routing_plan(nhsd_apim_proxy_url, correlation_id, nhsd_apim_auth_headers):
    """
    .. py:function:: Test missing routing plan
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
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


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_routing_plan_not_belonging_to_client_id(nhsd_apim_proxy_url, correlation_id, nhsd_apim_auth_headers):
    """
    .. py:function:: Test accessing another users routing plan
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
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


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_500_duplicate_routing_plan(nhsd_apim_proxy_url, correlation_id, nhsd_apim_auth_headers):
    """
    .. py:function:: Test duplicate templates in routing plan
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": DUPLICATE_ROUTING_PLAN_TEMPLATE_ID,
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
        500,
        Generators.generate_duplicate_routing_plan_template_error([
            {
                "communicationType": "NHSAPP",
                "supplier": "NHSAPP",
                "id": "playwright-nhs-app",
                "lettersNotifyNative": False
            }
        ]),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("routing_plan_id", [
    "191b5bf4-1a69-4798-ba8e-fbbd7dc3dea2",
    "d66ace32-20c2-4aff-a1fc-9ffa3f9fa577"
])
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_routing_plan_missing_templates(
    nhsd_apim_proxy_url,
    correlation_id,
    routing_plan_id,
    nhsd_apim_auth_headers
):
    """
    .. py:function:: Test missing routing plan templates
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **nhsd_apim_auth_headers,
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
        500,
        Generators.generate_missing_routing_plan_template_error(),
        correlation_id
    )
