from .constants import *


class Assertions():
    @staticmethod
    def assert_201_response(resp, messageBatchReference):
        if (resp.status_code == 429):
            raise AssertionError('Unexpected 429')

        assert resp.status_code == 201

        response = resp.json().get("data")
        assert response.get("type") == "MessageBatch"
        assert response.get("id") is not None
        assert response.get("id") != ""
        assert response.get("attributes").get("messageBatchReference") is not None
        assert response.get("attributes").get("messageBatchReference") == messageBatchReference

    @staticmethod
    def assert_error_with_optional_correlation_id(resp, code, error, correlation_id):
        if (code != 429 and resp.status_code == 429):
            raise AssertionError('Unexpected 429')

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
            assert error in response_errors

        assert resp.headers.get("X-Correlation-Id") == correlation_id

    @staticmethod
    def assert_cors_response(resp, website):
        if resp.status_code == 429:
            raise AssertionError('Unexpected 429')

        assert resp.status_code == 200
        assert resp.headers.get("Access-Control-Allow-Origin") == website
        assert resp.headers.get("Access-Control-Allow-Methods") == CORS_METHODS
        assert resp.headers.get("Access-Control-Max-Age") == CORS_MAX_AGE
        assert resp.headers.get("Access-Control-Allow-Headers") == CORS_ALLOW_HEADERS

    @staticmethod
    def assert_cors_headers(resp, website):
        assert resp.headers.get("Access-Control-Allow-Origin") == website
        assert resp.headers.get("Access-Control-Expose-Headers") == CORS_EXPOSE_HEADERS
