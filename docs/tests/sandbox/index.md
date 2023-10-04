# Sandbox test suite

The Sandbox Test Suite is a collection of tests ran against the internal-dev-sandbox environment. These tests are ran as part of the [pull request pipeline](https://dev.azure.com/NHSD-APIM/API%20Platform/_build?definitionId=619), [release pipeline](https://dev.azure.com/NHSD-APIM/API%20Platform/_build?definitionId=620) and the [nightly sandbox integration test run](https://dev.azure.com/NHSD-APIM/API%20Platform/_build?definitionId=627)

* [Generic Tests](generic/index.md)
  * [Authentication Tests](generic/authentication.md)
  * [Content Types](generic/content_types.md)
  * [Header Tests](generic/headers.md)
  * [Not Found Tests](generic/not_found.md)
  * [Quota Tests](generic/quotas.md)
  * [Timeout Tests](generic/timeouts.md)
* [POST /v1/message-batches](post_v1_message-batches/index.md)
  * [Validation Tests](post_v1_message-batches/validation.md)
  * [Invalid Routing Plans](post_v1_message-batches/invalid_routing_plans.md)
  * [Performance Tests](post_v1_message-batches/performance.md)
  * [Happy Path Tests](post_v1_message-batches/happy_path.md)
  * [Service Ban](post_v1_message-batches/service_ban.md)
