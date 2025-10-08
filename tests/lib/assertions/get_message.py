from lib.constants.constants import MESSAGE_STATUS, CHANNEL_STATUS, CHANNEL_TYPE, CASCADE_TYPE
from lib.assertions.common import assert_valid_string, assert_valid_list, assert_valid_int
from datetime import datetime


def assert_message_status(resp, expected_status=None):
    message_status = resp.json().get("data").get("attributes").get("messageStatus")
    assert_valid_string(message_status)
    assert message_status in MESSAGE_STATUS
    if expected_status is not None:
        assert expected_status == message_status


def assert_message_reference(resp):
    message_reference = resp.json().get("data").get("attributes").get("messageReference")
    assert_valid_string(message_reference)


def assert_created_timestamp(resp):
    created_timestamp = resp.json().get("data").get("attributes").get("timestamps").get("created")
    assert_valid_string(created_timestamp)
    formatted_date = datetime.fromisoformat(created_timestamp.replace("Z", "+00:00"))
    assert isinstance(formatted_date, datetime)


def assert_metadata(resp):
    metadata = resp.json().get("data").get("attributes").get("metadata")
    assert_valid_list(metadata)
    assert len(metadata) > 0
    assert_metadata_queried(metadata[0].get("queriedAt"))
    assert_metadata_source(metadata[0].get("source"))
    assert_metadata_version(metadata[0].get("version"))
    assert_metadata_labels(metadata[0].get("labels"))


def assert_channels(resp):
    channels = resp.json().get("data").get("attributes").get("channels")
    assert_valid_list(channels)
    assert len(channels) > 0
    for channel in channels:
        assert_channel_type(channel.get("type"))
        assert_cascade_type(channel.get("cascadeType"))
        assert_cascade_order(channel.get("cascadeOrder"))
        assert_channel_status(channel.get("channelStatus"), None)
        assert_channel_created_timestamp(channel.get("timestamps").get("created"))


def assert_self_link(resp, base_url):
    self_link = resp.json().get("data").get("links").get("self")
    request_id = resp.json().get("data").get("id")
    assert_valid_string(self_link)
    assert self_link.startswith(base_url)
    assert self_link.endswith(f"/v1/messages/{request_id}")


def assert_message_status_description(resp, expected_description):
    actual_description = resp.json().get("data").get("attributes").get("messageStatusDescription")
    assert_valid_string(actual_description)
    assert expected_description == actual_description


def assert_failure_reason_code(resp, expected_code):
    failure_reason_code = resp.json().get("data").get("attributes").get("messageFailureReasonCode")
    assert_valid_string(failure_reason_code)
    assert expected_code == failure_reason_code


def assert_channel_status(channel_status, expected_status):
    assert_valid_string(channel_status)
    assert channel_status in CHANNEL_STATUS
    if expected_status is not None:
        assert expected_status == channel_status


def assert_channel_status_description(channel_status_description, expected_description):
    assert_valid_string(channel_status_description)
    assert expected_description == channel_status_description


def assert_channel_failure_reason_code(channel_failure_reason_code, expected_code):
    assert_valid_string(channel_failure_reason_code)
    assert expected_code == channel_failure_reason_code


def assert_metadata_queried(queried_at):
    assert_valid_string(queried_at)
    formatted_date = datetime.fromisoformat(queried_at.replace("Z", "+00:00"))
    assert isinstance(formatted_date, datetime)


def assert_metadata_source(source):
    assert_valid_string(source)


def assert_metadata_version(version):
    assert_valid_string(version)


def assert_metadata_labels(labels):
    assert_valid_list(labels)
    for label in labels:
        assert_valid_string(label)


def assert_channel_type(channel_type):
    assert_valid_string(channel_type)
    assert channel_type in CHANNEL_TYPE


def assert_cascade_type(cascade_type):
    assert_valid_string(cascade_type)
    assert cascade_type in CASCADE_TYPE


def assert_cascade_order(cascade_order):
    assert_valid_int(cascade_order)
    assert cascade_order > 0


def assert_channel_created_timestamp(created_timestamp):
    assert_valid_string(created_timestamp)
    formatted_date = datetime.fromisoformat(created_timestamp.replace("Z", "+00:00"))
    assert isinstance(formatted_date, datetime)
