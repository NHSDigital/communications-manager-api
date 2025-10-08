from lib.assertions.common import assert_valid_string, assert_valid_list
import re


def assert_message_batch_reference(resp, expected_message_batch_reference):
    actual_message_batch_reference = resp.json().get("data").get("attributes").get("messageBatchReference")
    assert_valid_string(actual_message_batch_reference)
    assert expected_message_batch_reference == actual_message_batch_reference


def assert_messages(resp, expected_messages):
    actual_messages = resp.json().get("data").get("attributes").get("messages")
    assert_valid_list(actual_messages)
    expected_messages = sorted(expected_messages, key=lambda x: x["messageReference"])
    actual_messages = sorted(actual_messages, key=lambda x: x["messageReference"])
    for i in range(len(actual_messages)):
        assert_message_reference(
            actual_messages[i].get("messageReference"), expected_messages[i].get("messageReference")
        )
        assert_message_id(actual_messages[i].get("id"))


def assert_message_reference(actual_message_reference, expected_message_reference=None):
    assert_valid_string(actual_message_reference)
    if expected_message_reference is not None:
        assert actual_message_reference == expected_message_reference


def assert_message_id(actual_message_id):
    assert_valid_string(actual_message_id)
    assert re.match(r"^[a-zA-Z0-9]{27}$", actual_message_id)
