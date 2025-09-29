from datetime import datetime
from lib.constants.constants import MESSAGE_TYPES
import re


def assert_message_type(resp, type):
    message_type = resp.json().get("data").get("type")
    assert message_type is not None
    assert message_type != ""
    assert isinstance(message_type, str)
    assert message_type in MESSAGE_TYPES
    assert message_type == type


def assert_request_id(resp):
    request_id = resp.json().get("data").get("id")
    assert request_id is not None
    assert request_id != ""
    assert isinstance(request_id, str)
    assert re.match(r"^[a-zA-Z0-9]{27}$", request_id)


def assert_routing_plan_id(resp, expected_routing_plan_id=None):
    actual_routing_plan_id = resp.json().get("data").get("attributes").get("routingPlan").get("id")
    assert actual_routing_plan_id is not None
    assert actual_routing_plan_id != ""
    assert isinstance(actual_routing_plan_id, str)
    if expected_routing_plan_id is not None:
        assert expected_routing_plan_id == actual_routing_plan_id


def assert_routing_plan_version(resp):
    actual_routing_plan_version = resp.json().get("data").get("attributes").get("routingPlan").get("version")
    assert actual_routing_plan_version is not None
    assert actual_routing_plan_version != ""
    assert isinstance(actual_routing_plan_version, str)


def assert_routing_plan_name(resp):
    actual_routing_plan_name = resp.json().get("data").get("attributes").get("routingPlan").get("name")
    assert actual_routing_plan_name is not None
    assert isinstance(actual_routing_plan_name, str)


def assert_routing_plan_created_date(resp):
    actual_routing_plan_created_date = resp.json().get("data").get("attributes").get("routingPlan").get("createdDate")
    assert actual_routing_plan_created_date is not None
    assert actual_routing_plan_created_date != ""
    assert isinstance(actual_routing_plan_created_date, str)
    formatted_date = datetime.fromisoformat(actual_routing_plan_created_date.replace("Z", "+00:00"))
    assert formatted_date is not None
