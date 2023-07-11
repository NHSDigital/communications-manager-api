"""
Server response with 404 when invalid routing plan provided

Scenarios:
Invalid Routing Plan
"""
import requests
import pytest
import uuid

# first character is always 0 - ensure we do not have a valid routing plan
# that starts with a 0
routing_plan_id = f"0{str(uuid.uuid1())[1:]}"
x_correlation_id_value = f"0{str(uuid.uuid4())[1:]}"


def __assert_404_error(resp, correlation_id=False, check_body=True):
    assert resp.status_code == 404

    if correlation_id:
        assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value
    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_NO_SUCH_ROUTING_PLAN"
        assert error.get("status") == "404"
        assert error.get("title") == "No such routing plan"
        assert (
            error.get("description") == "The routing plan specified either does not exist or is not in a usable state."
        )
        assert error.get("source").get("pointer") == "/data/attributes/routingPlanId"


@pytest.mark.sandboxtest
def test_404_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": routing_plan_id,
                "messageBatchReference": "da0b1495-c7cb-468c-9d81-07dee089d728",
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
    })
    __assert_404_error(resp)


@pytest.mark.sandboxtest
def test_404_with_correlation_id_post(nhsd_apim_proxy_url):
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        "X-Correlation-Id": x_correlation_id_value},
        json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": routing_plan_id,
                "messageBatchReference": "da0b1495-c7cb-468c-9d81-07dee089d728",
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
    })
    __assert_404_error(resp, correlation_id=True)
