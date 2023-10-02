import requests
import pytest
import uuid
from lib import Assertions, Generators


CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]
DUPLICATE_ROUTING_PLAN_TEMPLATE_ID = "a3a4e55d-7a21-45a6-9286-8eb595c872a8"
INVALID_ROUTING_CONFIG_ID = "4ead415a-c033-4b39-9b05-326ac237a3be"


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_no_such_routing_plan(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with an unknown routing plan \
        receives a 404 'No Such Routing Plan' response

        | **Given** the API consumer provides a message body with an unknown routing plan
        | **When** the request is submitted
        | **Then** the response returns a 404 no such routing plan error

    **Asserts**
    - Response returns a 404 'No Such Routing Plan' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": f"0{str(uuid.uuid1())[1:]}",
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


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_routing_plan(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request where the \
        routing plan identifier is not a properly formed UUID receives a 400 'No Such Routing Plan' response

        | **Given** the API consumer provides a message body with a routing plan referencing an invalid template
        | **When** the request is submitted
        | **Then** the response returns a 400 invalid value error

    **Asserts**
    - Response returns a 400 'Invalid Value' error
    - Response returns the expected error message body referencing the invalid attribute
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": INVALID_ROUTING_CONFIG_ID,
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
        400,
        Generators.generate_invalid_value_error("/data/attributes/routingPlanId"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_500_duplicate_routing_plan(nhsd_apim_proxy_url, correlation_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a routing plan \
        referencing the same template twice receives a 500 'Duplicate Routing Plan' response

        | **Given** the API consumer provides a message body containing a reference to the same template twice
        | **When** the request is submitted
        | **Then** the response returns a 500 duplicate routing plan error

    **Asserts**
    - Response returns a 500 'Duplicate Routing Plan' error
    - Response returns the expected error message body referencing the duplicate template values
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
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
                "name": "EMAIL_TEMPLATE",
                "type": "EMAIL"
            },
            {
                "name": "SMS_TEMPLATE",
                "type": "SMS"
            },
            {
                "name": "LETTER_TEMPLATE",
                "type": "LETTER"
            },
            {
                "name": "LETTER_PDF_TEMPLATE",
                "type": "LETTER_PDF"
            },
            {
                "name": "NHSAPP_TEMPLATE",
                "type": "NHSAPP"
            }
        ]),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("routing_plan_id", [
    "c8857ccf-06ec-483f-9b3a-7fc732d9ad48",
    "aeb16ab8-cb9c-4d23-92e9-87c78119175c"
])
def test_500_missing_routing_plan(nhsd_apim_proxy_url, correlation_id, routing_plan_id):
    """
    .. py:function:: Scenario: An API consumer submitting a request with a routing plan \
        referencing a missing template receives a 500 'Missing Routing Plan' response

        | **Given** the API consumer provides a message body with a routing plan referencing a missing template
        | **When** the request is submitted
        | **Then** the response returns a 500 missing routing plan template error

    **Asserts**
    - Response returns a 500 'Missing Routing Plan Template' error
    - Response returns the expected error message body
    - Response returns the 'X-Correlation-Id' header if provided

    .. include:: ../../partials/correlation_ids.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
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
