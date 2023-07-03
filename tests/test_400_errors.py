import requests
import pytest

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
full_data = {
  "data": {
    "type": "MessageBatch",
    "attributes": {
      "routingPlanId": "2fd7f5c4-802e-4092-bd3d-276bb199df62",
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
}


@pytest.mark.sandboxtest
def test_invalid_body(nhsd_apim_proxy_url):
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": "/"
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        data="{}SF{}NOTVALID",
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.parametrize(
    "property, pointer",
    [
        ("data", "/data"),
        ("type", "/data/type"),
        ("attributes", "/data/attributes"),
        ("routingPlanId", "/data/attributes/routingPlanId"),
        ("messageBatchReference", "/data/attributes/messageBatchReference"),
        ("messages", "/data/attributes/messages"),
        ("messageReference", "/data/attributes/messages/0/messageReference"),
        ("recipient", "/data/attributes/messages/0/recipient"),
        ("nhsNumber", "/data/attributes/messages/0/recipient/nhsNumber"),
        ("dateOfBirth", "/data/attributes/messages/0/recipient/dateOfBirth"),
    ]
)
@pytest.mark.sandboxtest
def test_property_missing(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_without_key(full_data, property)

    expected_error = {
        "id": "CM_MISSING_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Missing property",
        "detail": "The property at the specified location is required, but was not present in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=data,
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.parametrize(
    "property, pointer",
    [
        ("data", "/data"),
        ("attributes", "/data/attributes"),
        ("recipient", "/data/attributes/messages/0/recipient"),
    ]
)
@pytest.mark.sandboxtest
def test_data_null(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_with_null_key(full_data, property)
    expected_error = {
        "id": "CM_NULL_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Property cannot be null",
        "detail": "The property at the specified location is required, but a null value was passed in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.parametrize(
    "property, pointer",
    [
        ("type", "/data/type"),
        ("routingPlanId", "/data/attributes/routingPlanId"),
        ("messageBatchReference", "/data/attributes/messageBatchReference"),
        ("messages", "/data/attributes/messages"),
        ("messageReference", "/data/attributes/messages/0/messageReference"),
        ("recipient", "/data/attributes/messages/0/recipient"),
        ("nhsNumber", "/data/attributes/messages/0/recipient/nhsNumber"),
        ("dateOfBirth", "/data/attributes/messages/0/recipient/dateOfBirth"),
        ("personalisation", "/data/attributes/messages/0/personalisation"),
    ]
)
@pytest.mark.sandboxtest
def test_data_invalid(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_with_new_value(full_data, property, "invalid string")
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.parametrize(
    "property, pointer",
    [
        ("messageReference", "/data/attributes/messages/1/messageReference"),
    ]
)
@pytest.mark.sandboxtest
def test_data_duplicate(nhsd_apim_proxy_url, property, pointer):
    data = full_data
    # Add a duplicate message to the payload to trigger the duplicate error
    data["data"]["attributes"]["messages"].append(
        {
          "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
          "recipient": {
            "nhsNumber": "1234567890",
            "dateOfBirth": "1982-03-17"
          },
          "personalisation": {}
        }
    )
    expected_error = {
        "id": "CM_DUPLICATE_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Duplicate value",
        "detail": "The property at the specified location is a duplicate, duplicated values are not allowed.",
        "source": {
            "pointer": pointer
        }
    }
    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=full_data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.parametrize(
    "property, pointer",
    [
        ("messages", "/data/attributes/messages"),
    ]
)
@pytest.mark.sandboxtest
def test_data_too_few_items(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_with_new_value(full_data, property, [])
    expected_error = {
        "id": "CM_TOO_FEW_ITEMS",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Too few items",
        "detail": "The property at the specified location contains too few items.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


def new_dict_without_key(input_dict, key):
    if isinstance(input_dict, dict):
        return {k: new_dict_without_key(v, key) for k, v in input_dict.items() if k != key}
    elif isinstance(input_dict, list):
        return [new_dict_without_key(element, key) for element in input_dict]
    else:
        return input_dict


def new_dict_with_null_key(input_dict, key):
    if isinstance(input_dict, dict):
        return {k: new_dict_with_null_key(v, key) if k != key else None for k, v in input_dict.items()}
    elif isinstance(input_dict, list):
        return [new_dict_with_null_key(element, key) for element in input_dict]
    else:
        return input_dict


def new_dict_with_new_value(input_dict, key, new_value):
    if isinstance(input_dict, dict):
        return {
            k: new_dict_with_new_value(v, key, new_value) if k != key
            else new_value for k, v in input_dict.items()
        }
    elif isinstance(input_dict, list):
        return [new_dict_with_new_value(element, key, new_value) for element in input_dict]
    else:
        return input_dict
