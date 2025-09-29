import re


def assert_message_batch_reference(resp, expected_message_batch_reference):
    actual_message_batch_reference = resp.json().get("data").get("attributes").get("messageBatchReference")
    assert actual_message_batch_reference is not None
    assert actual_message_batch_reference != ""
    assert isinstance(actual_message_batch_reference, str)
    assert expected_message_batch_reference == actual_message_batch_reference


def assert_messages(resp, expected_messages):
    actual_messages = resp.json().get("data").get("attributes").get("messages")
    assert actual_messages is not None
    assert isinstance(actual_messages, list)
    assert len(actual_messages) > 0
    expected_messages = sorted(expected_messages, key=lambda x: x["messageReference"])
    actual_messages = sorted(actual_messages, key=lambda x: x["messageReference"])
    for i in range(len(actual_messages)):
        assert_message_reference(
            actual_messages[i].get("messageReference"), expected_messages[i].get("messageReference")
        )
        assert_message_id(actual_messages[i].get("id"))


def assert_message_reference(actual_message_reference, expected_message_reference=None):
    assert actual_message_reference is not None
    assert actual_message_reference != ""
    assert isinstance(actual_message_reference, str)
    if expected_message_reference is not None:
        assert actual_message_reference == expected_message_reference


def assert_message_id(actual_message_id):
    assert actual_message_id is not None
    assert actual_message_id != ""
    assert isinstance(actual_message_id, str)
    assert re.match(r"^[a-zA-Z0-9]{27}$", actual_message_id)
