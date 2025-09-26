def assert_message_batch_reference(resp, expected_message_batch_reference):
    actual_message_batch_reference = resp.json().get("data").get("attributes").get("messageBatchReference")
    assert actual_message_batch_reference is not None
    assert expected_message_batch_reference == actual_message_batch_reference


def assert_messages(resp, expected_messages):
    actual_messages = resp.json().get("data").get("attributes").get("messages")
    assert actual_messages is not None
    assert len(actual_messages) > 0

    expected_messages = sorted(expected_messages, key=lambda x: x["messageReference"])
    actual_messages = sorted(actual_messages, key=lambda x: x["messageReference"])
    for i in range(len(actual_messages)):
        assert actual_messages[i].get("messageReference") is not None
        assert actual_messages[i].get("messageReference") == expected_messages[i].get("messageReference")
        assert actual_messages[i].get("id") is not None
        assert actual_messages[i].get("id") != ""
