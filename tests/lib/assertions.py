from .constants.constants import CORS_METHODS, CORS_MAX_AGE, CORS_ALLOW_HEADERS, CORS_EXPOSE_HEADERS, CORS_POLICY
from .error_handler import Error_Handler


class Assertions():
    @staticmethod
    def assert_201_response(resp, message_batch_reference):
        Error_Handler.handle_retry(resp)

        Assertions.assertStatusCode(resp.status_code, 201)

        response = resp.json().get("data")
        Assertions.assertEquals(response.get("type"), "MessageBatch")
        Assertions.assertNotNull(response.get("id"))
        Assertions.assertNotBlank(response.get("id"))
        Assertions.assertNotNull(response.get("attributes").get("messageBatchReference"))
        Assertions.assertEquals(response.get("attributes").get("messageBatchReference"), message_batch_reference)

        # ensure we have our x-content-type-options set correctly
        Assertions.assertEquals(resp.headers.get("X-Content-Type-Options"), "nosniff")

        # ensure we have our cache-control set correctly
        Assertions.assertEquals(resp.headers.get("Cache-Control"), "no-cache, no-store, must-revalidate")

    @staticmethod
    def assert_201_response_messages(resp):
        Error_Handler.handle_retry(resp)

        Assertions.assertStatusCode(resp.status_code, 201)

        response = resp.json().get("data")
        Assertions.assertEquals(response.get("type"), "Message")
        Assertions.assertNotNull(response.get("id"))
        Assertions.assertNotBlank(response.get("id"))
        Assertions.assertEquals(response.get("attributes").get("messageStatus"), "created")
        Assertions.assertNotNull(response.get("attributes").get("timestamps").get("created"))
        Assertions.assertNotBlank(response.get("attributes").get("timestamps").get("created"))

    @staticmethod
    def assert_error_with_optional_correlation_id(resp, code, error, correlation_id):
        if code == 429:
            Error_Handler.handle_504_retry(resp)
        elif code == 504:
            Error_Handler.handle_429_retry(resp)
        else:
            Error_Handler.handle_retry(resp)

        Assertions.assertStatusCode(resp.status_code, code)

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

        Assertions.assertEquals(resp.headers.get("X-Correlation-Id"), correlation_id)
        Assertions.assertEquals(resp.headers.get("X-Content-Type-Options"), "nosniff")
        Assertions.assertEquals(resp.headers.get("Cache-Control"), "no-cache, no-store, must-revalidate")

    @staticmethod
    def assert_cors_response(resp, website):
        Error_Handler.handle_retry(resp)

        Assertions.assertStatusCode(resp.status_code, 200)
        Assertions.assertEquals(resp.headers.get("Access-Control-Allow-Origin"), website)
        Assertions.assertEquals(resp.headers.get("Access-Control-Allow-Methods"), CORS_METHODS)
        Assertions.assertEquals(resp.headers.get("Access-Control-Max-Age"), CORS_MAX_AGE)
        Assertions.assertEquals(resp.headers.get("Access-Control-Allow-Headers"), CORS_ALLOW_HEADERS)
        Assertions.assertEquals(resp.headers.get("Cross-Origin-Resource-Policy"), CORS_POLICY)

    @staticmethod
    def assert_cors_headers(resp, website):
        Error_Handler.handle_retry(resp)

        Assertions.assertEquals(resp.headers.get("Access-Control-Allow-Origin"), website)
        Assertions.assertEquals(resp.headers.get("Access-Control-Expose-Headers"), CORS_EXPOSE_HEADERS)
        Assertions.assertEquals(resp.headers.get("Cross-Origin-Resource-Policy"), CORS_POLICY)

    @staticmethod
    def assertStatusCode(actual, expected):
        try:
            assert actual == expected
        except AssertionError:
            raise AssertionError(f"Expected status code to be '{expected}', but was '{actual}'")

    @staticmethod
    def assertEquals(actual, expected):
        try:
            assert expected == actual
        except AssertionError:
            raise AssertionError(f"Expected '{expected}', but got '{actual}'")

    @staticmethod
    def assertNotNull(attribute):
        try:
            assert attribute is not None
        except AssertionError:
            raise AssertionError(f"Expected attribute to be null, but was '{attribute}'")

    @staticmethod
    def assertNotBlank(attribute):
        try:
            assert attribute != ""
        except AssertionError:
            raise AssertionError(f"Expected attribute to be blank, but was '{attribute}'")

    @staticmethod
    def assertContains(value, attribute):
        try:
            assert value in attribute
        except AssertionError:
            raise AssertionError(f"Expected value '{value}' in attribute, but got '{attribute}'")
