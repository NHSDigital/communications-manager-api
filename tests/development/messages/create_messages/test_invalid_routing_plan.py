import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.fixtures import *  # NOSONAR
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib.constants.constants import INVALID_ROUTING_PLAN
from lib.constants.constants import DUPLICATE_ROUTING_PLAN_TEMPLATE_ID
from lib.constants.constants import MISSING_TEMPLATE_ROUTING_PLANS
from lib.constants.constants import CORRELATION_IDS


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_no_such_routing_plan(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_no_such_routing_plan.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "X-Correlation-Id": correlation_id
        },
        json={
            "data": {
                "type": "Message",
                "attributes": {
                    "routingPlanId": f"f{str(uuid.uuid1())[1:]}",
                    "messageReference": str(uuid.uuid1()),
                    "recipient": {
                        "nhsNumber": "9990548609"
                    },
                    "personalisation": {}
                }
            }
        }
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_routing_plan_not_belonging_to_client_id(nhsd_apim_proxy_url, bearer_token_internal_dev, correlation_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_routing_plan_not_belonging_to_client_id.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "X-Correlation-Id": correlation_id
        },
        json={
            "data": {
                "type": "Message",
                "attributes": {
                    "routingPlanId": INVALID_ROUTING_PLAN,
                    "messageReference": str(uuid.uuid1()),
                    "recipient": {
                        "nhsNumber": "9990548609"
                    },
                    "personalisation": {}
                }
            }
        }
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_no_such_routing_plan_error(),
        correlation_id
    )


@pytest.mark.devtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("routing_plan_id", MISSING_TEMPLATE_ROUTING_PLANS)
def test_routing_plan_missing_templates(
    nhsd_apim_proxy_url,
    bearer_token_internal_dev,
    correlation_id,
    routing_plan_id
):
    """
    .. include:: ../../partials/invalid_routing_plans/test_500_missing_routing_plan.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}", headers={
            "Authorization": bearer_token_internal_dev.value,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": routing_plan_id,
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": "9990548609"
                },
                "personalisation": {}
                }
            }
        }
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        500,
        Generators.generate_missing_routing_plan_template_error(),
        correlation_id
    )
