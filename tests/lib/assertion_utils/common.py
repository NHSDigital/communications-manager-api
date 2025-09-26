def assert_message_type(resp, type):
    message_type = resp.json().get("data").get("type")
    assert message_type == type


def assert_request_id(resp):
    request_id = resp.json().get("data").get("id")
    assert request_id is not None
    assert request_id != ""


def assert_routing_plan_id(resp, expected_routing_plan_id=None):
    actual_routing_plan_id = resp.json().get("data").get("attributes").get("routingPlan").get("id")
    assert actual_routing_plan_id is not None
    if expected_routing_plan_id is not None:
        assert expected_routing_plan_id == actual_routing_plan_id


def assert_routing_plan_version(resp):
    actual_routing_plan_version = resp.json().get("data").get("attributes").get("routingPlan").get("version")
    assert actual_routing_plan_version is not None


def assert_routing_plan_name(resp):
    actual_routing_plan_name = resp.json().get("data").get("attributes").get("routingPlan").get("name")
    assert actual_routing_plan_name is not None


def assert_routing_plan_created_date(resp):
    actual_routing_plan_created_date = resp.json().get("data").get("attributes").get("routingPlan").get("createdDate")
    assert actual_routing_plan_created_date is not None
