"""
Server responds with a 400 response when invalid information is provided in the body of the request

NHS Number must be 10 digits long
DOB must be in the format of YYYY-MM-DD
"""
import requests
import pytest


NHS_NUMBER = ["012345678", "01234567890", "abcdefghij"]
DOB = ["1990-10-1", "1990-1-10", "90-10-10", "10-12-1990", "1-MAY-2000", "1990/01/01"]


@pytest.mark.smoketest
@pytest.mark.parametrize("nhs_number", NHS_NUMBER)
def test_invalid_nhs_number(nhsd_apim_proxy_url, nhs_number):
    resp = requests.post(nhsd_apim_proxy_url, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": nhs_number,
                            "dateOfBirth": "1982-1-11"
                            },
                        "personalisation": {}
                        }
                    ]
                }
            }
        })

    assert resp.status_code == 400
    error = resp.json().get("errors")[0]
    assert error.get("id") == "CM_INVALID_VALUE"
    assert error.get("status") == "400"
    assert error.get("title") == "Invalid value"
    assert (error.get("description") == "The property at the specified location does not allow this value.")
    assert error.get("source").get("pointer") == "/data/attributes/messages/0/recipient/dateOfBirth"


@pytest.mark.smoketest
@pytest.mark.parametrize("dob", DOB)
def test_invalid_dob(nhsd_apim_proxy_url, dob):
    resp = requests.post(nhsd_apim_proxy_url, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": "0f58f589-db44-423c-85f7-0c0f0b5a3f77",
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": "0123456789",
                            "dateOfBirth": dob
                            },
                        "personalisation": {}
                        }
                    ]
                }
            }
        })

    assert resp.status_code == 400
    error = resp.json().get("errors")[0]
    assert error.get("id") == "CM_INVALID_VALUE"
    assert error.get("status") == "400"
    assert error.get("title") == "Invalid value"
    assert (error.get("description") == "The property at the specified location does not allow this value.")
    assert error.get("source").get("pointer") == "/data/attributes/messages/0/recipient/nhsNumber"
