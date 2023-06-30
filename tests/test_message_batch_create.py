"""
Server returns a 201 when a valid request is raised against /v1/message-batches
"""
import requests
import pytest

VALID_ROUTING_PLAN_ID = [
    "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
    "49e43b98-70cb-47a9-a55e-fe70c9a6f77c",
    "b402cd20-b62a-4357-8e02-2952959531c8",
    "936e9d45-15de-4a95-bb36-ae163c33ae53",
    "9ba00d23-cd6f-4aca-8688-00abc85a7980"
]

REQUEST_PATH = "/v1/message-batches"


def __assert_201_response(resp):
    assert resp.status_code == 201

    response = resp.json().get("data")
    assert response.get("type") == "MessageBatch"
    assert response.get("id") is not None
    assert response.get("id") != ""
    assert response.get("attributes").get("messageBatchReference") == "0f58f589-db44-423c-85f7-0c0f0b5a3f77"


@pytest.mark.sandboxtest
@pytest.mark.parametrize('routingPlan', VALID_ROUTING_PLAN_ID)
def test_201_message_batch(nhsd_apim_proxy_url, routingPlan):
    resp = requests.post(f"{nhsd_apim_proxy_url}{REQUEST_PATH}", headers={
            "Accept": "*/*",
            "Content-Type": "application/vnd.api+json"
        }, json={
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": routingPlan,
                    "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                    "messages": [
                        {
                            "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
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
