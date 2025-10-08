from datetime import datetime
from lib.assertions.common import assert_valid_string


def assert_created_timestamp(resp):
    created_timestamp = resp.json().get("data").get("attributes").get("timestamps").get("created")
    assert_valid_string(created_timestamp)
    formatted_date = datetime.fromisoformat(created_timestamp.replace("Z", "+00:00"))
    assert isinstance(formatted_date, datetime)


def assert_message_status(resp, expected_status=None):
    message_status = resp.json().get("data").get("attributes").get("messageStatus")
    assert_valid_string(message_status)
    if expected_status is not None:
        assert expected_status == message_status


def assert_self_link(resp, base_url):
    self_link = resp.json().get("data").get("links").get("self")
    request_id = resp.json().get("data").get("id")
    assert_valid_string(self_link)
    assert self_link.startswith(base_url)
    assert self_link.endswith(f"/v1/messages/{request_id}")
