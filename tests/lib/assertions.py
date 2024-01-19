from .constants.constants import CORS_METHODS, CORS_MAX_AGE, CORS_ALLOW_HEADERS, CORS_EXPOSE_HEADERS, CORS_POLICY
from .error_handler import Error_Handler
import json


class Assertions():
    @staticmethod
    def assert_201_response(resp, message_batch_reference, routing_plan_id):
        Error_Handler.handle_retry(resp)

        assert resp.status_code == 201

        response = resp.json().get("data")
        assert response.get("type") == "MessageBatch"
        assert response.get("id") is not None
        assert response.get("id") != ""
        assert response.get("attributes").get("messageBatchReference") is not None
        assert response.get("attributes").get("messageBatchReference") == message_batch_reference
        assert response.get("attributes").get("routingPlan").get("id") is not None
        assert response.get("attributes").get("routingPlan").get("id") == routing_plan_id
        assert response.get("attributes").get("routingPlan").get("version") is not None

        # ensure we have our x-content-type-options set correctly
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"

        # ensure we have our cache-control set correctly
        assert resp.headers.get("Cache-Control") == "no-cache, no-store, must-revalidate"

    @staticmethod
    def assert_200_response_message(resp, environment):
        Error_Handler.handle_retry(resp)

        assert resp.status_code == 200

        response = resp.json().get("data")
        messageStatus = response.get("attributes").get("messageStatus")

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
        if messageStatus != "pending_enrichment":
            assert response.get("attributes").get("metadata") is not None
            assert response.get("attributes").get("metadata") != ""
            assert response.get("attributes").get("metadata")[0].get("queriedAt") is not None
            assert response.get("attributes").get("metadata")[0].get("queriedAt") != ""
            assert response.get("attributes").get("metadata")[0].get("source") is not None
            assert response.get("attributes").get("metadata")[0].get("source") != ""
            # TODO: Uncomment once 4.9.0 is in int
            # assert response.get("attributes").get("metadata")[0].get("version") is not None
            # assert response.get("attributes").get("metadata")[0].get("version") != ""
            assert response.get("attributes").get("metadata")[0].get("labels") != ""
        if messageStatus == "sending" or messageStatus == "delivered":
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

        # temporarily check that links is not sent
        assert "links" not in response

        """
        Disabled this section as we do not want to go live with the links properties.

        hostname = f"{environment}.api.service.nhs.uk"
        prefixes = ["internal-dev", "internal-qa"]

        if environment == 'sandbox':
            for p in prefixes:
                if p in response.get("links").get("self"):
                    hostname = f"{p}-{hostname}"
                    break

        assert response.get("links").get("self").startswith(f"https://{hostname}/comms")
        assert response.get("links").get("self").endswith(f"/v1/messages/{response.get('id')}")
        """

    @staticmethod
    def assert_get_message_status(resp, status, failureReason=None):
        response = resp.json().get("data")
        assert response.get("attributes").get("messageStatus") == status
        if status == "failed":
            assert response.get("attributes").get("messageStatusDescription") == failureReason

    @staticmethod
    def assert_get_message_response_channels(resp, channelType, channelStatus):
        response = resp.json().get("data")
        channels = response.get("attributes").get("channels")
        for c in range(len(channels)):
            assert response.get("attributes").get("channels")[c].get("type") in channelType
            assert response.get("attributes").get("channels")[c].get("retryCount") == 1
            assert response.get("attributes").get("channels")[c].get("channelStatus") in channelStatus
            assert response.get("attributes").get("channels")[c].get("timestamps") is not None
            assert response.get("attributes").get("channels")[c].get("routingPlan") is not None

    @staticmethod
    def assert_201_response_messages(resp, environment):
        Error_Handler.handle_retry(resp)

        assert resp.status_code == 201

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

        # temporarily check that links is not sent
        assert "links" not in response
        assert "Location" not in resp.headers

        """
        Disabled this section as we do not want to go live with the links properties.

        hostname = f"{environment}.api.service.nhs.uk"
        prefixes = ["internal-dev", "internal-qa"]

        if environment == 'sandbox':
            for p in prefixes:
                if p in response.get("links").get("self"):
                    hostname = f"{p}-{hostname}"
                    break

        assert response.get("links").get("self").startswith(f"https://{hostname}/comms")
        assert response.get("links").get("self").endswith(f"/v1/messages/{response.get('id')}")
        assert resp.headers.get("Location") == f"/v1/messages/{response.get('id')}"
        """

    @staticmethod
    def assert_201_routing_plan_and_version(resp, routing_plan):
        Error_Handler.handle_retry(resp)

        assert resp.status_code == 201
        response = resp.json().get("data")

        assert response.get("attributes").get("routingPlan") == routing_plan

    @staticmethod
    def assert_200_valid_message_id_response_body(resp, message_id, url):
        Error_Handler.handle_retry(resp)

        assert resp.status_code == 200

        expected_response_file = open(f"sandbox/messages/{message_id}.json")
        expected = json.load(expected_response_file).get("data")
        expected["links"]["self"] = url
        actual = resp.json().get("data")

        assert actual == expected

    @staticmethod
    def assert_message_batches_idempotency(respOne, respTwo):
        Error_Handler.handle_retry(respOne)
        Error_Handler.handle_retry(respTwo)

        assert respOne.status_code == 201
        assert respTwo.status_code == 201

        responseOne = respOne.json().get("data")
        responseTwo = respTwo.json().get("data")

        assert responseOne.get("id") == responseTwo.get("id")

    @staticmethod
    def assert_messages_idempotency(respOne, respTwo):
        Error_Handler.handle_retry(respOne)
        Error_Handler.handle_retry(respTwo)

        assert respOne.status_code == 201
        assert respTwo.status_code == 201

        responseOne = respOne.json().get("data")
        responseTwo = respTwo.json().get("data")

        assert responseOne.get("id") == responseTwo.get("id")
        assert (responseOne.get("attributes").get("messageStatus") ==
                responseTwo.get("attributes").get("messageStatus"))
        assert (responseOne.get("attributes").get("timestamps").get("created") ==
                responseTwo.get("attributes").get("timestamps").get("created"))
        assert (responseOne.get("attributes").get("routingPlan").get("id") ==
                responseTwo.get("attributes").get("routingPlan").get("id"))
        assert (responseOne.get("attributes").get("routingPlan").get("version") ==
                responseTwo.get("attributes").get("routingPlan").get("version"))

    @staticmethod
    def assert_error_with_optional_correlation_id(resp, code, error, correlation_id):
        if code == 429:
            Error_Handler.handle_504_retry(resp)
        elif code == 504:
            Error_Handler.handle_429_retry(resp)
        else:
            Error_Handler.handle_retry(resp)

        assert resp.status_code == code

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
                assert error == response_errors[0]
            else:
                assert error in response_errors

        assert resp.headers.get("X-Correlation-Id") == correlation_id

        # ensure we have our x-content-type-options set correctly
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"

        # ensure we have our cache-control set correctly
        assert resp.headers.get("Cache-Control") == "no-cache, no-store, must-revalidate"

    @staticmethod
    def assert_cors_response(resp, website):
        Error_Handler.handle_retry(resp)

        assert resp.status_code == 200
        assert resp.headers.get("Access-Control-Allow-Origin") == website
        assert resp.headers.get("Access-Control-Allow-Methods") == CORS_METHODS
        assert resp.headers.get("Access-Control-Max-Age") == CORS_MAX_AGE
        assert resp.headers.get("Access-Control-Allow-Headers") == CORS_ALLOW_HEADERS
        assert resp.headers.get("Cross-Origin-Resource-Policy") == CORS_POLICY

    @staticmethod
    def assert_cors_headers(resp, website):
        Error_Handler.handle_retry(resp)

        assert resp.headers.get("Access-Control-Allow-Origin") == website
        assert resp.headers.get("Access-Control-Expose-Headers") == CORS_EXPOSE_HEADERS
        assert resp.headers.get("Cross-Origin-Resource-Policy") == CORS_POLICY

    @staticmethod
    def assert_no_aws_headers(resp):
        assert "X-Amzn-Trace-Id" not in resp.headers
        assert "x-amzn-RequestId" not in resp.headers
        assert "x-amz-apigw-id" not in resp.headers
