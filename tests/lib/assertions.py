import json
from tests.lib.assertion_utils import get_message
from .constants.constants import CORS_METHODS, CORS_MAX_AGE, CORS_ALLOW_HEADERS, CORS_EXPOSE_HEADERS, CORS_POLICY
from .error_handler import error_handler
from lib.assertion_utils import common, message_batches, messages, headers, nhsapp_accounts


class Assertions():
    @staticmethod
    def assert_cors_response(resp, website):
        error_handler.handle_retry(resp)
        assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"

        headers.assert_access_control_allow_origin(resp, website)
        headers.assert_access_control_allow_methods(resp, CORS_METHODS)
        headers.assert_access_control_max_age(resp, CORS_MAX_AGE)
        headers.assert_access_control_allow_headers(resp, CORS_ALLOW_HEADERS)
        headers.assert_access_control_resource_policy(resp, CORS_POLICY)

    @staticmethod
    def assert_cors_headers(resp, website):
        error_handler.handle_retry(resp)

        headers.assert_access_control_allow_origin(resp, website)
        headers.assert_access_control_expose_headers(resp, CORS_EXPOSE_HEADERS)
        headers.assert_access_control_resource_policy(resp, CORS_POLICY)

    @staticmethod
    def assert_no_aws_headers(resp):
        headers.assert_no_aws_headers(resp)

    @staticmethod
    def assert_201_response(resp, data):
        error_handler.handle_retry(resp)
        assert resp.status_code == 201, f"Response: {resp.status_code}: {resp.text}"

        common.assert_message_type(resp, "MessageBatch")
        common.assert_request_id(resp)
        common.assert_routing_plan_id(resp, data["data"]["attributes"]["routingPlanId"])
        common.assert_routing_plan_version(resp)
        common.assert_routing_plan_name(resp)
        common.assert_routing_plan_created_date(resp)
        message_batches.assert_message_batch_reference(resp, data["data"]["attributes"]["messageBatchReference"])
        message_batches.assert_messages(resp, data["data"]["attributes"]["messages"])
        headers.assert_x_content_type_options(resp, "nosniff")
        headers.assert_cache_control(resp, "no-cache, no-store, must-revalidate")

    @staticmethod
    def assert_200_response_nhsapp_accounts(resp, base_url, ods_code, page):
        error_handler.handle_retry(resp)
        assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"
        last_page_number = nhsapp_accounts.get_page_number_from_url(resp.json()["links"]["last"])
        self_page_number = nhsapp_accounts.get_page_number_from_url(resp.json()["links"]["self"])

        common.assert_message_type(resp, "NhsAppAccounts")
        nhsapp_accounts.assert_ods_code(resp, ods_code)
        nhsapp_accounts.assert_accounts(resp)
        nhsapp_accounts.assert_self_link(resp, base_url, ods_code, page)
        nhsapp_accounts.assert_last_link(resp, base_url, ods_code, last_page_number)
        nhsapp_accounts.assert_next_link(resp, base_url, ods_code, self_page_number, last_page_number)

    @staticmethod
    def assert_200_response_message(resp, base_url):
        error_handler.handle_retry(resp)
        assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"
        message_status = resp.json().get("data").get("attributes").get("messageStatus")

        common.assert_request_id(resp)
        common.assert_routing_plan_id(resp)
        common.assert_routing_plan_version(resp)
        common.assert_routing_plan_name(resp)
        common.assert_routing_plan_created_date(resp)
        get_message.assert_message_status(resp)
        get_message.assert_message_reference(resp)
        get_message.assert_created_timestamp(resp)
        get_message.assert_self_link(resp, base_url)
        if message_status != "pending_enrichment":
            get_message.assert_metadata(resp)
        if message_status == "sending" or message_status == "delivered":
            get_message.assert_channels(resp)

    @staticmethod
    def assert_get_message_status(resp, status, failure_reason=None, failure_reason_code=None):
        get_message.assert_message_status(resp, status)
        if status == "failed":
            get_message.assert_message_status_description(resp, failure_reason)
            get_message.assert_failure_reason_code(resp, failure_reason_code)

    @staticmethod
    def assert_get_message_response_channels(resp, status, failure_reason=None, failure_reason_code=None):
        response = resp.json().get("data")
        channels = response.get("attributes").get("channels")
        for channel in channels:
            get_message.assert_channel_status(channel, status)
            if status == "failed":
                get_message.assert_channel_status_description(channel, failure_reason)
                get_message.assert_channel_failure_reason_code(channel, failure_reason_code)

    @staticmethod
    def assert_201_response_messages(resp, base_url):
        error_handler.handle_retry(resp)
        assert resp.status_code == 201, f"Response: {resp.status_code}: {resp.text}"

        common.assert_message_type(resp, "Message")
        common.assert_request_id(resp)
        common.assert_routing_plan_id(resp)
        common.assert_routing_plan_version(resp)
        common.assert_routing_plan_name(resp)
        common.assert_routing_plan_created_date(resp)
        messages.assert_message_status(resp, "created")
        messages.assert_created_timestamp(resp)
        messages.assert_self_link(resp, base_url)

    @staticmethod
    def assert_200_valid_message_id_response_body(resp, message_id, url):
        error_handler.handle_retry(resp)

        assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"

        expected_response_file = open(f"sandbox/messages/{message_id}.json")
        expected = json.load(expected_response_file).get("data")
        expected["links"]["self"] = url
        actual = resp.json().get("data")

        assert actual == expected

    @staticmethod
    def assert_email_gov_uk(response, message_id):
        for message in response:
            if message_id in message.get("reference"):
                assert message.get("status") == "delivered"
                assert message.get("type") == "email"
                assert message.get("body") is not None
                assert message.get("subject") is not None
                assert message.get("email_address") is not None
                break

    @staticmethod
    def assert_sms_gov_uk(response, message_id):
        for message in response:
            if message_id in message.get("reference"):
                assert message.get("status") == "delivered"
                assert message.get("type") == "sms"
                assert message.get("body") is not None
                assert message.get("phone_number") is not None
                break

    @staticmethod
    def assert_letter_gov_uk(response, message_id):
        for message in response:
            if message_id in message.get("reference"):
                assert message.get("status") == "received"
                assert message.get("type") == "letter"
                assert message.get("subject") is not None
                assert message.get("body") is not None
                break

    @staticmethod
    def assert_message_batches_idempotency(resp_one, resp_two):
        error_handler.handle_retry(resp_one)
        error_handler.handle_retry(resp_two)

        assert resp_one.status_code == 201
        assert resp_two.status_code == 201

        response_one = resp_one.json().get("data")
        response_two = resp_two.json().get("data")

        assert response_one.get("id") == response_two.get("id")

    @staticmethod
    def assert_messages_idempotency(resp_one, resp_two):
        error_handler.handle_retry(resp_one)
        error_handler.handle_retry(resp_two)

        assert resp_one.status_code == 201
        assert resp_two.status_code == 201

        response_one = resp_one.json().get("data")
        response_two = resp_two.json().get("data")

        assert response_one.get("id") == response_two.get("id")
        assert (response_one.get("attributes").get("messageStatus") ==
                response_one.get("attributes").get("messageStatus"))
        assert (response_one.get("attributes").get("timestamps").get("created") ==
                response_two.get("attributes").get("timestamps").get("created"))
        assert (response_one.get("attributes").get("routingPlan").get("id") ==
                response_two.get("attributes").get("routingPlan").get("id"))
        assert (response_one.get("attributes").get("routingPlan").get("version") ==
                response_two.get("attributes").get("routingPlan").get("version"))

    @staticmethod
    def assert_error_with_optional_correlation_id(resp, code, error, correlation_id):
        if resp.status_code != code:
            # Unexpected status code, check if the test needs to be retried
            error_handler.handle_retry(resp)

        assert resp.status_code == code, f"Response: {resp.status_code}: {resp.text}"

        if error is not None:
            # ensure that all errors contain an identifier
            response_errors = resp.json().get("errors")
            current_identifier_num = 0
            for e in response_errors:
                assert e.get("id") is not None

                # extract the identifier num
                assert int(e.get("id").split(".")[-1]) == current_identifier_num

                # then remove it as its a unique value that we do not know ahead of time
                e.pop("id")
                current_identifier_num += 1

            # validate the error is present
            if len(response_errors) == 1:
                # this case is for making debugging easier where possible
                assert response_errors[0] == error
            else:
                assert error in response_errors

        Assertions.assert_correlation_id(resp.headers.get("X-Correlation-Id"), correlation_id)
        headers.assert_x_content_type_options(resp, "nosniff")
        headers.assert_cache_control(resp, "no-cache, no-store, must-revalidate")

    @staticmethod
    def assert_correlation_id(res_correlation_id, correlation_id):
        # apigee generates this value if not present with rrt prefix
        if correlation_id:
            assert res_correlation_id == correlation_id
        else:
            assert res_correlation_id.startswith('rrt')
