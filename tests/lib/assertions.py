from .constants.constants import CORS_METHODS, CORS_MAX_AGE, CORS_ALLOW_HEADERS, CORS_EXPOSE_HEADERS, CORS_POLICY
from .error_handler import Error_Handler
from datetime import datetime


class Assertions():
    @staticmethod
    def assert_201_response(resp, message_batch_reference):
        Error_Handler.handle_retry(resp)

        assert resp.status_code == 201

        response = resp.json().get("data")
        assert response.get("type") == "MessageBatch"
        assert response.get("id") is not None
        assert response.get("id") != ""
        assert response.get("attributes").get("messageBatchReference") is not None
        assert response.get("attributes").get("messageBatchReference") == message_batch_reference

        # ensure we have our x-content-type-options set correctly
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"

        # ensure we have our cache-control set correctly
        assert resp.headers.get("Cache-Control") == "no-cache, no-store, must-revalidate"

    @staticmethod
    def assert_200_response_message(resp, environment):
        Error_Handler.handle_retry(resp)

        assert resp.status_code == 200

        response = resp.json().get("data")
        assert response.get("type") == "Message"
        assert response.get("id") is not None
        assert response.get("id") != ""
        assert response.get("attributes").get("messageStatus") == "created"
        assert response.get("attributes").get("timestamps").get("created")
        assert response.get("attributes").get("timestamps").get("created") is not None
        assert response.get("attributes").get("timestamps").get("created") != ""

        hostname = f"{environment}.api.service.nhs.uk"
        prefixes = ["internal-dev", "internal-qa"]

        for p in prefixes:
            if p in response.get("links").get("self"):
                hostname = f"{p}-{hostname}"
                break

        assert response.get("links").get("self").startswith(f"https://{hostname}/comms")
        assert response.get("links").get("self").endswith(response.get("id"))

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

        hostname = f"{environment}.api.service.nhs.uk"
        prefixes = ["internal-dev", "internal-qa"]

        for p in prefixes:
            if p in response.get("links").get("self"):
                hostname = f"{p}-{hostname}"
                break

        assert response.get("links").get("self").startswith(f"https://{hostname}/comms")
        assert response.get("links").get("self").endswith(response.get("id"))

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
