def assert_message_status(resp, expected_status=None):
    message_status = resp.json().get("data").get("attributes").get("messageStatus")
    assert message_status is not None
    assert message_status != ""
    if expected_status is not None:
        assert expected_status == message_status


def assert_message_reference(resp):
    message_reference = resp.json().get("data").get("attributes").get("messageReference")
    assert message_reference is not None
    assert message_reference != ""


def assert_created_timestamp(resp):
    created_timestamp = resp.json().get("data").get("attributes").get("timestamps").get("created")
    assert created_timestamp is not None
    assert created_timestamp != ""


def assert_metadata(resp):
    metadata = resp.json().get("data").get("attributes").get("metadata")
    assert metadata is not None
    assert metadata != ""
    assert metadata[0].get("queriedAt") is not None
    assert metadata[0].get("queriedAt") != ""
    assert metadata[0].get("source") is not None
    assert metadata[0].get("source") != ""
    assert metadata[0].get("version") is not None
    assert metadata[0].get("version") != ""
    assert metadata[0].get("labels") != ""


def assert_channels(resp):
    channels = resp.json().get("data").get("attributes").get("channels")
    assert channels is not None
    assert len(channels) > 0
    for channel in channels:
        assert channel.get("channelType") is not None
        assert channel.get("channelType") != ""
        assert channel.get("to") is not None
        assert channel.get("to") != ""
        assert channel.get("status") is not None
        assert channel.get("status") != ""
        assert channel.get("id") is not None
        assert channel.get("id") != ""
        assert channel.get("timestamps").get("created") is not None


def assert_self_link(resp, base_url):
    self_link = resp.json().get("data").get("links").get("self")
    request_id = resp.json().get("data").get("id")
    assert self_link is not None
    assert self_link != ""
    assert self_link.startswith(base_url)
    assert self_link.endswith(f"/v1/messages/{request_id}")


def assert_message_status_description(resp, expected_description):
    actual_description = resp.json().get("data").get("attributes").get("messageStatusDescription")
    assert actual_description is not None
    assert actual_description != ""
    assert expected_description == actual_description


def assert_failure_reason_code(resp, expected_code):
    failure_reason_code = resp.json().get("data").get("attributes").get("messageFailureReasonCode")
    assert failure_reason_code is not None
    assert failure_reason_code != ""
    assert expected_code == failure_reason_code


def assert_channel_status(channel, expected_status):
    channel_status = channel.get("channelStatus")
    assert channel_status is not None
    assert channel_status != ""
    assert expected_status == channel_status


def assert_channel_status_description(channel, expected_description):
    channel_status_description = channel.get("channelStatusDescription")
    assert channel_status_description is not None
    assert channel_status_description != ""
    assert expected_description == channel_status_description


def assert_channel_failure_reason_code(channel, expected_code):
    channel_failure_reason_code = channel.get("channelFailureReasonCode")
    assert channel_failure_reason_code is not None
    assert channel_failure_reason_code != ""
    assert expected_code == channel_failure_reason_code
