from .constants.constants import CORS_METHODS, CORS_MAX_AGE, CORS_ALLOW_HEADERS, CORS_EXPOSE_HEADERS, CORS_POLICY
from .error_handler import error_handler
import json
from urllib.parse import urlparse, parse_qs


class Assertions():
    @staticmethod
    def assert_201_response(resp, data):
        error_handler.handle_retry(resp)

        assert resp.status_code == 201, f"Response: {resp.status_code}: {resp.text}"

        message_batch_reference = data["data"]["attributes"]["messageBatchReference"]
        routing_plan_id = data["data"]["attributes"]["routingPlanId"]
        messages = data["data"]["attributes"]["messages"]

        response = resp.json().get("data")
        assert response.get("type") == "MessageBatch"
        assert response.get("id") is not None
        assert response.get("id") != ""
        assert response.get("attributes").get("messageBatchReference") is not None
        assert response.get("attributes").get("messageBatchReference") == message_batch_reference
        assert response.get("attributes").get("routingPlan").get("id") is not None
        assert response.get("attributes").get("routingPlan").get("id") == routing_plan_id
        assert response.get("attributes").get("routingPlan").get("version") is not None
        assert response.get("attributes").get("messages") is not None
        assert len(response.get("attributes").get("messages")) > 0
        expected_messages = sorted(messages, key=lambda x: x["messageReference"])
        actual_messages = sorted(response.get("attributes").get("messages"), key=lambda x: x["messageReference"])
        for i in range(len(actual_messages)):
            assert actual_messages[i].get("messageReference") is not None
            assert actual_messages[i].get("messageReference") == expected_messages[i].get("messageReference")
            assert actual_messages[i].get("id") is not None
            assert actual_messages[i].get("id") != ""

        # ensure we have our x-content-type-options set correctly
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"

        # ensure we have our cache-control set correctly
        assert resp.headers.get("Cache-Control") == "no-cache, no-store, must-revalidate"

    @staticmethod
    def assert_200_response_nhsapp_accounts(resp, base_url, ods_code, page):
        error_handler.handle_retry(resp)

        assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"

        response = resp.json()
        data = response.get("data")

        assert data.get("id") is not None
        assert data.get("id") == ods_code
        assert data.get("type") == "NhsAppAccounts"
        assert data.get("attributes").get("accounts") is not None
        assert len(data.get("attributes").get("accounts")) > 0
        for i in range(len(data.get("attributes").get("accounts"))):
            assert data.get("attributes").get("accounts")[i].get("nhsNumber") is not None
            assert data.get("attributes").get("accounts")[i].get("nhsNumber") != ""
            assert data.get("attributes").get("accounts")[i].get("notificationsEnabled") is not None
        assert response.get("links").get("self").startswith(base_url)
        assert response.get("links").get("self") \
            .endswith(f"/channels/nhsapp/accounts?ods-organisation-code={ods_code}&page={page}")

        last_link = response.get("links").get("last")
        parsed_last_link = urlparse(last_link)
        last_link_query_params = parse_qs(parsed_last_link.query)
        last_page_number = int(last_link_query_params["page"][0])

        assert last_link.startswith(base_url)
        assert response.get("links").get("last") \
            .endswith(f"/channels/nhsapp/accounts?ods-organisation-code={ods_code}&page={last_page_number}")

        self_link = response.get("links").get("self")
        parsed_self_link = urlparse(self_link)
        self_link_query_params = parse_qs(parsed_self_link.query)
        self_page_number = int(self_link_query_params["page"][0])

        if self_page_number == last_page_number:
            assert response.get("links").get("next") is None
        else:
            next_page_number = self_page_number + 1
            assert response.get("links").get("next").startswith(base_url)
            assert response.get("links").get("next") \
                .endswith(f"/channels/nhsapp/accounts?ods-organisation-code={ods_code}&page={next_page_number}")

    @staticmethod
    def assert_200_response_message(resp, base_url):
        error_handler.handle_retry(resp)

        assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"

        response = resp.json().get("data")
        message_status = response.get("attributes").get("messageStatus")

        assert response.get("type") == "Message"
        assert response.get("id") is not None
        assert response.get("id") != ""
        assert response.get("attributes").get("messageStatus") is not None
        assert response.get("attributes").get("messageStatus") != ""
        assert response.get("attributes").get("messageReference") is not None
        assert response.get("attributes").get("messageReference") != ""
        assert response.get("attributes").get("routingPlan") is not None
        assert response.get("attributes").get("routingPlan") != ""
        assert response.get("attributes").get("routingPlan").get("id") is not None
        assert response.get("attributes").get("routingPlan").get("id") != ""
        assert response.get("attributes").get("routingPlan").get("version") is not None
        assert response.get("attributes").get("routingPlan").get("version") != ""
        assert response.get("attributes").get("timestamps").get("created")
        assert response.get("attributes").get("timestamps").get("created") is not None
        assert response.get("attributes").get("timestamps").get("created") != ""
        if message_status != "pending_enrichment":
            assert response.get("attributes").get("metadata") is not None
            assert response.get("attributes").get("metadata") != ""
            assert response.get("attributes").get("metadata")[0].get("queriedAt") is not None
            assert response.get("attributes").get("metadata")[0].get("queriedAt") != ""
            assert response.get("attributes").get("metadata")[0].get("source") is not None
            assert response.get("attributes").get("metadata")[0].get("source") != ""
            assert response.get("attributes").get("metadata")[0].get("version") is not None
            assert response.get("attributes").get("metadata")[0].get("version") != ""
            assert response.get("attributes").get("metadata")[0].get("labels") != ""
        if message_status == "sending" or message_status == "delivered":
            assert response.get("attributes").get("channels") is not None
            assert response.get("attributes").get("channels")[0].get("type") is not None
            assert response.get("attributes").get("channels")[0].get("type") != ""
            assert response.get("attributes").get("channels")[0].get("retryCount") is not None
            assert response.get("attributes").get("channels")[0].get("retryCount") != ""
            assert response.get("attributes").get("channels")[0].get("channelStatus") is not None
            assert response.get("attributes").get("channels")[0].get("channelStatus") != ""
            assert response.get("attributes").get("channels")[0].get("timestamps") is not None
            assert response.get("attributes").get("channels")[0].get("timestamps") != ""
            assert response.get("attributes").get("channels")[0].get("routingPlan") is not None
            assert response.get("attributes").get("channels")[0].get("routingPlan") != ""
        assert response.get("links").get("self").startswith(base_url)
        assert response.get("links").get("self").endswith(f"/v1/messages/{response.get('id')}")

    @staticmethod
    def assert_get_message_status(resp, status, failure_reason=None):
        response = resp.json().get("data")
        assert response.get("attributes").get("messageStatus") == status
        if status == "failed":
            assert response.get("attributes").get("messageStatusDescription") == failure_reason

    @staticmethod
    def assert_get_message_response_channels(resp, channel_type, channel_status):
        response = resp.json().get("data")
        channels = response.get("attributes").get("channels")
        for c in range(len(channels)):
            assert response.get("attributes").get("channels")[c].get("type") in channel_type
            assert response.get("attributes").get("channels")[c].get("retryCount") == 1
            assert response.get("attributes").get("channels")[c].get("channelStatus") in channel_status
            assert response.get("attributes").get("channels")[c].get("timestamps") is not None
            assert response.get("attributes").get("channels")[c].get("routingPlan") is not None
            assert response.get("attributes").get("channels")[c].get("cascadeType") in ["primary", "secondary"]
            assert response.get("attributes").get("channels")[c].get("cascadeOrder") is not None

    @staticmethod
    def assert_201_response_messages(resp, environment):
        error_handler.handle_retry(resp)

        assert resp.status_code == 201, f"Response: {resp.status_code}: {resp.text}"

        response = resp.json().get("data")
        assert response.get("type") == "Message"
        assert response.get("id") is not None
        assert response.get("id") != ""
        assert response.get("attributes").get("messageStatus") == "created"
        assert response.get("attributes").get("timestamps").get("created")
        assert response.get("attributes").get("timestamps").get("created") is not None
        assert response.get("attributes").get("timestamps").get("created") != ""
        assert response.get("attributes").get("routingPlan") is not None
        assert response.get("attributes").get("routingPlan").get("id") != ""
        assert response.get("attributes").get("routingPlan").get("version") != ""

        assert response.get("links").get("self").startswith(environment)
        assert response.get("links").get("self").endswith(f"/v1/messages/{response.get('id')}")
        assert resp.headers.get("Location") == f"/v1/messages/{response.get('id')}"

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
        if code == 429:
            # If we are testing a 429 error then only retry on 504 errors
            error_handler.handle_504_retry(resp)
        elif code == 504:
            # If we are testing a 504 error then only retry on 429 errors
            error_handler.handle_429_retry(resp)
        else:
            # We are not testing a 429 or 504, retry if we get either of them
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

        # ensure we have our x-content-type-options set correctly
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"

        # ensure we have our cache-control set correctly
        assert resp.headers.get("Cache-Control") == "no-cache, no-store, must-revalidate"

    @staticmethod
    def assert_correlation_id(res_correlation_id, correlation_id):
        # apigee generates this value if not present with rrt prefix
        if correlation_id:
            assert res_correlation_id == correlation_id
        else:
            assert res_correlation_id.startswith('rrt')

    @staticmethod
    def assert_cors_response(resp, website):
        error_handler.handle_retry(resp)

        assert resp.status_code == 200, f"Response: {resp.status_code}: {resp.text}"
        assert resp.headers.get("Access-Control-Allow-Origin") == website
        assert resp.headers.get("Access-Control-Allow-Methods") == CORS_METHODS
        assert resp.headers.get("Access-Control-Max-Age") == CORS_MAX_AGE
        assert resp.headers.get("Access-Control-Allow-Headers") == CORS_ALLOW_HEADERS
        assert resp.headers.get("Cross-Origin-Resource-Policy") == CORS_POLICY

    @staticmethod
    def assert_cors_headers(resp, website):
        error_handler.handle_retry(resp)

        assert resp.headers.get("Access-Control-Allow-Origin") == website
        assert resp.headers.get("Access-Control-Expose-Headers") == CORS_EXPOSE_HEADERS
        assert resp.headers.get("Cross-Origin-Resource-Policy") == CORS_POLICY

    @staticmethod
    def assert_no_aws_headers(resp):
        assert "X-Amzn-Trace-Id" not in resp.headers
        assert "x-amzn-RequestId" not in resp.headers
        assert "x-amz-apigw-id" not in resp.headers
