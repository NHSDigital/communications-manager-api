import requests
import pytest
import uuid


POST_PATHS = ["/v1/ignore/i-dont-exist", "/api/fake-endpoint", "/im-a-teapot"]
REQUEST_PATH = POST_PATHS + ["/v1/message-batches"]
x_correlation_id_value = f"0{str(uuid.uuid4())[1:]}"
routing_plan_id = f"0{str(uuid.uuid1())[1:]}"


def __assert_404_not_found_error(resp, correlation_id=False, check_body=True):
    assert resp.status_code == 404

    if correlation_id:
        assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value
    if check_body:
        error = resp.json().get("errors")[0]
        assert error.get("id") == "CM_NOT_FOUND"
        assert error.get("status") == "404"
        assert error.get("title") == "Resource not found"
        assert (
            error.get("description") == "The resource at the requested URI was not found."
        )


def __assert_404_no_such_routing_plan_error(resp, correlation_id=False, check_body=True):
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
@pytest.mark.parametrize("request_path", REQUEST_PATH)
def test_404_get(nhsd_apim_proxy_url, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
    })
    __assert_404_not_found_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize("request_path", REQUEST_PATH)
def test_404_with_correlation_id_get(nhsd_apim_proxy_url, request_path):
    resp = requests.get(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_404_not_found_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', POST_PATHS)
def test_404_post(nhsd_apim_proxy_url, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_not_found_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', POST_PATHS)
def test_404_with_correlation_id_post(nhsd_apim_proxy_url, request_path):
    resp = requests.post(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json",
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_404_not_found_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_put(nhsd_apim_proxy_url, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_not_found_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_with_correlation_id_put(nhsd_apim_proxy_url, request_path):
    resp = requests.put(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json",
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_404_not_found_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_patch(nhsd_apim_proxy_url, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json"
    })
    __assert_404_not_found_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_with_correlation_id_patch(nhsd_apim_proxy_url, request_path):
    resp = requests.patch(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "Content-Type": "application/vnd.api+json",
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_404_not_found_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_delete(nhsd_apim_proxy_url, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*"
    })
    __assert_404_not_found_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_with_correlation_id_delete(nhsd_apim_proxy_url, request_path):
    resp = requests.delete(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_404_not_found_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_head(nhsd_apim_proxy_url, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*"
    })
    __assert_404_not_found_error(resp, check_body=False)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_with_correlation_id_head(nhsd_apim_proxy_url, request_path):
    resp = requests.head(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_404_not_found_error(resp, correlation_id=True, check_body=False)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_options(nhsd_apim_proxy_url, request_path):
    resp = requests.options(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*"
    })
    __assert_404_not_found_error(resp)


@pytest.mark.sandboxtest
@pytest.mark.parametrize('request_path', REQUEST_PATH)
def test_404_with_correlation_id_options(nhsd_apim_proxy_url, request_path):
    resp = requests.options(f"{nhsd_apim_proxy_url}{request_path}", headers={
        "Accept": "*/*",
        "X-Correlation-Id": x_correlation_id_value
    })
    __assert_404_not_found_error(resp, correlation_id=True)


@pytest.mark.sandboxtest
def test_404_no_such_routing_plan_post(nhsd_apim_proxy_url):
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
    __assert_404_no_such_routing_plan_error(resp)


@pytest.mark.sandboxtest
def test_404_no_such_routing_plan_with_correlation_id_post(nhsd_apim_proxy_url):
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
    __assert_404_no_such_routing_plan_error(resp, correlation_id=True)
