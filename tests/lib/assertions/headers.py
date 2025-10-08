def assert_x_content_type_options(resp, expected_options):
    # ensure we have our x-content-type-options set correctly
    content_type_options = resp.headers.get("X-Content-Type-Options")
    assert content_type_options == expected_options


def assert_cache_control(resp, expected_cache_control):
    # ensure we have our cache-control set correctly
    cache_control = resp.headers.get("Cache-Control")
    assert cache_control == expected_cache_control


def assert_access_control_allow_origin(resp, expected_origin):
    # ensure we have our access-control-allow-origin set correctly
    allow_origin = resp.headers.get("Access-Control-Allow-Origin")
    assert allow_origin == expected_origin


def assert_access_control_allow_methods(resp, expected_methods):
    # ensure we have our access-control-allow-methods set correctly
    allow_methods = resp.headers.get("Access-Control-Allow-Methods")
    assert allow_methods == expected_methods


def assert_access_control_max_age(resp, expected_max_age):
    # ensure we have our access-control-max-age set correctly
    max_age = resp.headers.get("Access-Control-Max-Age")
    assert max_age == expected_max_age


def assert_access_control_allow_headers(resp, expected_headers):
    # ensure we have our access-control-allow-headers set correctly
    allow_headers = resp.headers.get("Access-Control-Allow-Headers")
    assert allow_headers == expected_headers


def assert_access_control_expose_headers(resp, expected_expose_headers):
    # ensure we have our access-control-expose-headers set correctly
    expose_headers = resp.headers.get("Access-Control-Expose-Headers")
    assert expose_headers == expected_expose_headers


def assert_access_control_resource_policy(resp, expected_policy):
    # ensure we have our access-control-resource-policy set correctly
    resource_policy = resp.headers.get("Cross-Origin-Resource-Policy")
    assert resource_policy == expected_policy


def assert_no_aws_headers(resp):
    # ensure we do not have any AWS headers leaking through
    assert "X-Amzn-Trace-Id" not in resp.headers
    assert "x-amzn-RequestId" not in resp.headers
    assert "x-amz-apigw-id" not in resp.headers


def assert_location_header(resp):
    location_header = resp.headers.get("Location")
    expected_value = f"/v1/messages/{resp.json().get('data').get('id')}"
    assert location_header == expected_value
