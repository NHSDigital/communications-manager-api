# Integration test suite

The Integration test suite is a collection of tests ran against the integration environment. These tests are ran as part of the [release pipeline](https://dev.azure.com/NHSD-APIM/API%20Platform/_build?definitionId=620) and the [nightly integration integration test run](https://dev.azure.com/NHSD-APIM/API%20Platform/_build?definitionId=628)

* [Generic Tests](generic/index.md)
  * [Authentication Tests](generic/authentication.md)
  * [Not Found Tests](generic/not_found.md)
* [GET /channels/nhsapp/accounts](get_channels_nhsapp_accounts/index.md)
  * [Happy Path Tests](get_channels_nhsapp_accounts/happy_path.md)
  * [404 Tests](get_channels_nhsapp_accounts/404.md)
  * [400 Tests](get_channels_nhsapp_accounts/400.md)
