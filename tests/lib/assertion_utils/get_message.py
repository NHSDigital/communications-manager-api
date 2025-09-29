from lib.constants.constants import MESSAGE_STATUS, CHANNEL_STATUS, CHANNEL_TYPE, CASCADE_TYPE, SUPPLIER_STATUS
from datetime import datetime


def assert_message_status(resp, expected_status=None):
    message_status = resp.json().get("data").get("attributes").get("messageStatus")
    assert message_status is not None
    assert message_status != ""
    assert isinstance(message_status, str)
    assert message_status in MESSAGE_STATUS
    if expected_status is not None:
        assert expected_status == message_status


def assert_message_reference(resp):
    message_reference = resp.json().get("data").get("attributes").get("messageReference")
    assert message_reference is not None
    assert message_reference != ""
    assert isinstance(message_reference, str)


def assert_created_timestamp(resp):
    created_timestamp = resp.json().get("data").get("attributes").get("timestamps").get("created")
    assert created_timestamp is not None
    assert created_timestamp != ""
    assert isinstance(created_timestamp, str)
    formatted_date = datetime.fromisoformat(created_timestamp.replace("Z", "+00:00"))
    assert formatted_date is not None


def assert_metadata(resp):
    metadata = resp.json().get("data").get("attributes").get("metadata")
    assert metadata is not None
    assert metadata != ""
    assert isinstance(metadata, list)
    assert len(metadata) > 0
    assert_metadata_queried(metadata[0].get("queriedAt"))
    assert_metadata_source(metadata[0].get("source"))
    assert_metadata_version(metadata[0].get("version"))
    assert_metadata_labels(metadata[0].get("labels"))


def assert_channels(resp):
    channels = resp.json().get("data").get("attributes").get("channels")
    assert channels is not None
    assert isinstance(channels, list)
    assert len(channels) > 0
    for channel in channels:
        assert_channel_type(channel.get("channelType"))
        assert_cascade_type(channel.get("cascadeType"))
        assert_cascade_order(channel.get("cascadeOrder"))
        assert_channel_status(channel.get("channelStatus"), None)
        assert_supplier_status(channel.get("supplierStatus"))
        assert_channel_created_timestamp(channel.get("timestamps").get("created"))
        assert_channel_enriched_timestamp(channel.get("timestamps").get("enriched"))


def assert_self_link(resp, base_url):
    self_link = resp.json().get("data").get("links").get("self")
    request_id = resp.json().get("data").get("id")
    assert self_link is not None
    assert self_link != ""
    assert isinstance(self_link, str)
    assert self_link.startswith(base_url)
    assert self_link.endswith(f"/v1/messages/{request_id}")


def assert_message_status_description(resp, expected_description):
    actual_description = resp.json().get("data").get("attributes").get("messageStatusDescription")
    assert actual_description is not None
    assert actual_description != ""
    assert isinstance(actual_description, str)
    assert expected_description == actual_description


def assert_failure_reason_code(resp, expected_code):
    failure_reason_code = resp.json().get("data").get("attributes").get("messageFailureReasonCode")
    assert failure_reason_code is not None
    assert failure_reason_code != ""
    assert isinstance(failure_reason_code, str)
    assert expected_code == failure_reason_code


def assert_channel_status(channel_status, expected_status):
    assert channel_status is not None
    assert channel_status != ""
    assert isinstance(channel_status, str)
    assert channel_status in CHANNEL_STATUS
    assert expected_status == channel_status


def assert_channel_status_description(channel_status_description, expected_description):
    assert channel_status_description is not None
    assert channel_status_description != ""
    assert isinstance(channel_status_description, str)
    assert expected_description == channel_status_description


def assert_channel_failure_reason_code(channel_failure_reason_code, expected_code):
    assert channel_failure_reason_code is not None
    assert channel_failure_reason_code != ""
    assert isinstance(channel_failure_reason_code, str)
    assert expected_code == channel_failure_reason_code


def assert_metadata_queried(queried_at):
    assert queried_at is not None
    assert queried_at != ""
    assert isinstance(queried_at, str)
    formatted_date = datetime.fromisoformat(queried_at.replace("Z", "+00:00"))
    assert formatted_date is not None


def assert_metadata_source(source):
    assert source is not None
    assert source != ""
    assert isinstance(source, str)


def assert_metadata_version(version):
    assert version is not None
    assert version != ""
    assert isinstance(version, str)


def assert_metadata_labels(labels):
    assert labels is not None
    assert isinstance(labels, list)
    for label in labels:
        assert label is not None
        assert label != ""
        assert isinstance(label, str)


def assert_channel_type(channel_type):
    assert channel_type is not None
    assert channel_type != ""
    assert isinstance(channel_type, str)
    assert channel_type in CHANNEL_TYPE


def assert_cascade_type(cascade_type):
    assert cascade_type is not None
    assert cascade_type != ""
    assert isinstance(cascade_type, str)
    assert cascade_type in CASCADE_TYPE


def assert_cascade_order(cascade_order):
    assert cascade_order is not None
    assert isinstance(cascade_order, int)
    assert cascade_order > 0


def assert_supplier_status(supplier_status):
    assert supplier_status is not None
    assert supplier_status != ""
    assert isinstance(supplier_status, str)
    assert supplier_status in SUPPLIER_STATUS


def assert_channel_created_timestamp(created_timestamp):
    assert created_timestamp is not None
    assert created_timestamp != ""
    assert isinstance(created_timestamp, str)
    formatted_date = datetime.fromisoformat(created_timestamp.replace("Z", "+00:00"))
    assert formatted_date is not None


def assert_channel_enriched_timestamp(enriched_timestamp):
    assert enriched_timestamp is not None
    assert enriched_timestamp != ""
    assert isinstance(enriched_timestamp, str)
    formatted_date = datetime.fromisoformat(enriched_timestamp.replace("Z", "+00:00"))
    assert formatted_date is not None