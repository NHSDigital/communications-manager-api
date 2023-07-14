import requests
import pytest
import string
import random
from lib import Assertions

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
VALID_ROUTING_PLAN_ID_PROD = [
  "0e38317f-1670-480a-9aa9-b711fb136610",
]
VALID_DOB = ["0000-01-01", "2023-01-01", None]
valid_nhs_number = ''.join(random.choices(string.digits, k=10))


@pytest.mark.devtest
@pytest.mark.parametrize('accept_headers', VALID_ACCEPT_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_accept_headers_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, accept_headers):
    resp = requests.post(
      f"{nhsd_apim_proxy_url}{REQUEST_PATH}",
      headers={
          **nhsd_apim_auth_headers,
          "Accept": accept_headers,
          "Content-Type": "application/json"
      },
      json={
        "data": {
          "type": "MessageBatch",
          "attributes": {
            "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
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
    Assertions.assert_201_response(resp)


@pytest.mark.devtest
@pytest.mark.parametrize('content_type', VALID_CONTENT_TYPE_HEADERS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_content_type_headers_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, content_type):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": "application/json",
            "Content-Type": content_type
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
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
    Assertions.assert_201_response(resp)


@pytest.mark.devtest
@pytest.mark.parametrize('routing_plan_id', VALID_ROUTING_PLAN_ID_PROD)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_routing_plan_id_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, routing_plan_id):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
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
    Assertions.assert_201_response(resp)


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_message_batch_reference_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
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
    Assertions.assert_201_response(resp)


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_message_batch_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
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
    Assertions.assert_201_response(resp)


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_nhs_number_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
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
    Assertions.assert_201_response(resp)


@pytest.mark.devtest
@pytest.mark.parametrize('dob', VALID_DOB)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_201_message_batch_valid_dob_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, dob):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            **nhsd_apim_auth_headers,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
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
    Assertions.assert_201_response(resp)


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_request_without_dob_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "0e38317f-1670-480a-9aa9-b711fb136610",
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
    Assertions.assert_201_response(resp)
