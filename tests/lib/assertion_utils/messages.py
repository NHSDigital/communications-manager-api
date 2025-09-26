def assert_created_timestamp(resp):
    created_timestamp = resp.json().get("data").get("attributes").get("timestamps").get("created")
    assert created_timestamp is not None
    assert created_timestamp != ""


def assert_message_status(resp, expected_status=None):
    message_status = resp.json().get("data").get("attributes").get("messageStatus")
    assert message_status is not None
    assert message_status != ""
    if expected_status is not None:
        assert expected_status == message_status


def assert_self_link(resp, base_url):
    self_link = resp.json().get("data").get("links").get("self")
    request_id = resp.json().get("data").get("id")
    assert self_link is not None
    assert self_link != ""
    assert self_link.startswith(base_url)
    assert self_link.endswith(f"/v1/messages/{request_id}")
