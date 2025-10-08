from datetime import datetime
from lib.constants.constants import MESSAGE_TYPES
import re


def assert_valid_string(string):
    assert string is not None
    assert string != ""
    assert isinstance(string, str)


def assert_valid_list(lst):
    assert lst is not None
    assert isinstance(lst, list)


def assert_valid_int(integer):
    assert integer is not None
    assert isinstance(integer, int)


def assert_valid_bool(value):
    assert value is not None
    assert isinstance(value, bool)


def assert_message_type(resp, type):
    message_type = resp.json().get("data").get("type")
    assert_valid_string(message_type)
    assert message_type in MESSAGE_TYPES
    assert message_type == type


def assert_request_id(resp):
    request_id = resp.json().get("data").get("id")
    assert_valid_string(request_id)
    assert re.match(r"^[a-zA-Z0-9]{27}$", request_id)


def assert_routing_plan_id(resp, expected_routing_plan_id=None):
    actual_routing_plan_id = resp.json().get("data").get("attributes").get("routingPlan").get("id")
    assert_valid_string(actual_routing_plan_id)
    if expected_routing_plan_id is not None:
        assert expected_routing_plan_id == actual_routing_plan_id


def assert_routing_plan_version(resp):
    actual_routing_plan_version = resp.json().get("data").get("attributes").get("routingPlan").get("version")
    assert_valid_string(actual_routing_plan_version)


def assert_routing_plan_name(resp):
    actual_routing_plan_name = resp.json().get("data").get("attributes").get("routingPlan").get("name")
    # If routing plan name is not present on the routing plan, it will return an empty string
    assert actual_routing_plan_name is not None
    assert isinstance(actual_routing_plan_name, str)


def assert_routing_plan_created_date(resp):
    actual_routing_plan_created_date = resp.json().get("data").get("attributes").get("routingPlan").get("createdDate")
    assert_valid_string(actual_routing_plan_created_date)
    formatted_date = datetime.fromisoformat(actual_routing_plan_created_date.replace("Z", "+00:00"))
    assert formatted_date is not None
