"""
Server returns a 201 when a valid request is raised against /v1/message-batches
"""
import requests
import pytest
import string
import random

VALID_ACCEPT_HEADERS = ["*/*", "application/json", "application/vnd.api+json"]
VALID_CONTENT_TYPE_HEADERS = ["application/json", "application/vnd.api+json"]
REQUEST_PATH = "/v1/message-batches"
VALID_ROUTING_PLAN_ID = [
    "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
    "49e43b98-70cb-47a9-a55e-fe70c9a6f77c",
    "b402cd20-b62a-4357-8e02-2952959531c8",
    "936e9d45-15de-4a95-bb36-ae163c33ae53",
    "9ba00d23-cd6f-4aca-8688-00abc85a7980"
]
VALID_DOB = ["0000-01-01", "2023-01-01", None]
valid_nhs_number = ''.join(random.choices(string.digits, k=10))


def __assert_201_response(resp):
    assert resp.status_code == 201

    response = resp.json().get("data")
    assert response.get("type") == "MessageBatch"
    assert response.get("id") is not None
    assert response.get("id") != ""
    assert response.get("attributes").get("messageBatchReference") == "0f58f589-db44-423c-85f7-0c0f0b5a3f77"


@pytest.mark.sandboxtest
@pytest.mark.parametrize('accept_headers', VALID_ACCEPT_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_accept_headers(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    # import pdb; pdb.set_trace()
    resp = requests.post(
        f"{nhsd_apim_proxy_url}{REQUEST_PATH}",
        headers={
            "Accept": accept_headers,
            "Content-Type": "application/json"
        } | nhsd_apim_auth_headers,
        json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                    "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": "1234567890",
                                "dateOfBirth": "1982-03-17"
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        }
    )
    __assert_201_response(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
def test_201_message_batch_valid_content_type_headers(nhsd_apim_proxy_url, content_type):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            "Accept": "application/json",
            "Content-Type": content_type
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                    "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": "1234567890",
                                "dateOfBirth": "1982-03-17"
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        }
    )
    __assert_201_response(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('routing_plan_id', VALID_ROUTING_PLAN_ID)
def test_201_message_batch_valid_routing_plan_id(nhsd_apim_proxy_url, routing_plan_id):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": routing_plan_id,
                    "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": "1234567890",
                                "dateOfBirth": "1982-03-17"
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        }
    )
    __assert_201_response(resp)


@pytest.mark.sandboxtest
def test_201_message_batch_valid_message_batch_reference(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                    "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": "1234567890",
                                "dateOfBirth": "1982-03-17"
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        }
    )
    __assert_201_response(resp)


@pytest.mark.sandboxtest
def test_201_message_batch_valid_message_batch(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                    "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                    "messages": [
                        {
                            "messageReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f78",
                            "recipient": {
                                "nhsNumber": "1234567890",
                                "dateOfBirth": "1982-03-17"
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        }
    )
    __assert_201_response(resp)


@pytest.mark.sandboxtest
def test_201_message_batch_valid_nhs_number(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                    "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": valid_nhs_number,
                                "dateOfBirth": "1982-03-17"
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        }
    )
    __assert_201_response(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('dob', VALID_DOB)
def test_201_message_batch_valid_dob(nhsd_apim_proxy_url, dob):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                    "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": "0123456789",
                                "dateOfBirth": dob
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        }
    )
    __assert_201_response(resp)


@pytest.mark.sandboxtest
def test_request_without_dob(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                    "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                    "messages": [
                        {
                            "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
                            "recipient": {
                                "nhsNumber": "1234567890",
                            },
                            "personalisation": {}
                        }
                    ]
                }
            }
        })
    __assert_201_response(resp)
