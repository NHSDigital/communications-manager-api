# Integration test suite

The Integration test suite is a collection of tests ran against the integration environment. These tests are ran as part of the [release pipeline](https://dev.azure.com/NHSD-APIM/API%20Platform/_build?definitionId=620) and the [nightly integration integration test run](https://dev.azure.com/NHSD-APIM/API%20Platform/_build?definitionId=628)

* [Generic Tests](generic/index.md)
  * [Authentication Tests](generic/authentication.md)
  * [Content Types](generic/content_types.md)
  * [Header Tests](generic/headers.md)
  * [Not Found Tests](generic/not_found.md)
* [POST /v1/message-batches](post_v1_message-batches/index.md)
  * [Validation Tests](post_v1_message-batches/validation.md)
  * [Invalid Routing Plans](post_v1_message-batches/invalid_routing_plans.md)
  * [Performance Tests](post_v1_message-batches/performance.md)
  * [Happy Path Tests](post_v1_message-batches/happy_path.md)
