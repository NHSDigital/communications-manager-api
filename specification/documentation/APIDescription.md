## Overview

Use this API to send messages to citizens via email, SMS, the NHS App or letter.

Communications Manager provides:

* message templating
* message routing - via SMS, email, letter and NHS App
* enrichment of recipient details
* support for accessible formats and multiple languages

For more information about this services capabilities, see [Communications Manager Service](https://digital.nhs.uk/services/communications-manager).

## Who can use this API

The Communications Manager service is intended for services involved in direct care. This API can only be used where you have a legal basis to issue communications to citizens.

## API status and roadmap

This API is [in production, beta](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#statuses). We are onboarding partners to use it.

You can comment, upvote and view progress on [our roadmap](https://nhs-digital-api-management.featureupvote.com/?order=popular&filter=allexceptdone&tag=communications-manager-api).

If you have any other queries, [contact us](https://digital.nhs.uk/developer/help-and-support).

## Service level

This service is a [silver](https://digital.nhs.uk/services/reference-guide#service-levels) service, meaning it is available 24 hours a day, 365 days a year and supported from 8am to 6pm, Monday to Friday excluding bank holidays.

For more details, see [service levels](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#service-levels).

## Technology

This API is a [REST-based](https://digital.nhs.uk/developer/guides-and-documentation/our-api-technologies#basic-rest) API.

We follow the [JSON:API](https://jsonapi.org/) standard for our request and response schemas.

### Response content types

This API can generate responses in the following formats:

* `application/vnd.api+json` - see [JSON:API specification](https://jsonapi.org/format/#introduction)
* `application/json`

Both of these formats have the same structure - the API responds with a standard JSON document.

You can control which `Content-Type` is returned by using the `Accept` header.

The `Accept` header can contain the following values:

* `*/*`
* `application/json`
* `application/vnd.api+json`

Where no `Accept` header is present, this will default to `application/vnd.api+json`

### Request Content Types

This API will accept request payloads of the following types:

* `application/vnd.api+json` - see [JSON:API specification](https://jsonapi.org/format/#introduction)
* `application/json`

If you attempt to send a payload without the `Content-Type` header set to either of these values then the API will respond with a `415 Unsupported Media Type` response.

## Network access

This API is available on the internet and, indirectly on the [Health and Social Care Network (HSCN)](https://digital.nhs.uk/services/health-and-social-care-network).

For more details see [Network access for APIs](https://digital.nhs.uk/developer/guides-and-documentation/network-access-for-apis).

## Security and authorisation

This API is [application-restricted](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation#application-restricted-apis), meaning we authenticate the calling application but not the end user.

Authentication and authorisation of end users is the responsibility of your application.

To access this API, use the following security pattern:

* [Application-restricted RESTful API - signed JWT authentication](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/application-restricted-restful-apis-signed-jwt-authentication)

## Environments and testing

| Environment | Base URL |
|------------ | -------- |
| Sandbox     | `https://sandbox.api.service.nhs.uk/comms` |
| Integration test | `https://int.api.service.nhs.uk/comms` |
| Production | `https://api.service.nhs.uk/comms` |

### Sandbox testing

Our [sandbox environment](https://digital.nhs.uk/developer/guides-and-documentation/testing#sandbox-testing):

* is for early developer testing
* only covers a limited set of scenarios
* is stateless, so does not actually persist any updates
* is open access, so does not allow you to test authorisation

For details of sandbox test scenarios, or to try out sandbox using our our 'Try this API' feature, see the documentation for each endpoint.

Alternatively, you can try out the sandbox using our Postman collection:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/28740466-ec078d1e-d4d7-4460-92b9-7d79d51f967a?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D28740466-ec078d1e-d4d7-4460-92b9-7d79d51f967a%26entityType%3Dcollection%26workspaceId%3D3664098f-4f8b-4edf-874d-ed33e1eea8ed)

You can find our postman collection source in our [public repository on github](https://github.com/NHSDigital/communications-manager-api/tree/master/postman).

### Integration testing

Our integration test environment:

* is for formal integration sandbox-testing
* is stateful, so persists updates
* includes authorisation via [signed JWT authentication](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/application-restricted-restful-apis-signed-jwt-authentication)

You can try out our integration environment using our Postman collection. This Postman collection contains the signed JWT authentication mechanism, allowing you to test our integration environment without writing any code:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/28740466-fbe32763-302e-4a0b-b6e9-3a20f1bde923?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D28740466-fbe32763-302e-4a0b-b6e9-3a20f1bde923%26entityType%3Dcollection%26workspaceId%3D3664098f-4f8b-4edf-874d-ed33e1eea8ed#?env%5BIntegration%5D=W3sia2V5IjoiYXBpX2tleSIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6InNlY3JldCIsInNlc3Npb25WYWx1ZSI6IldPekdrM1dFWDBjVU9pbmhsNkdvdVd2N0RXTEhWaUNOIiwic2Vzc2lvbkluZGV4IjowfSx7ImtleSI6InByaXZhdGVfa2V5IiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoic2VjcmV0Iiwic2Vzc2lvblZhbHVlIjoiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tIE1JSUpRZ0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQ1N3d2dna29BZ0VBQW9JQ0FRQ2lPZWtqZlJYTWt0cDguLi4iLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoiYXV0aG9yaXphdGlvbl9oZWFkZXJfdmFsdWUiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJzZWNyZXQiLCJzZXNzaW9uVmFsdWUiOiJCZWFyZXIgTmxrd2Z0S3lQYWNXVjcza3VBZ1FVR2pEdkZlcCIsInNlc3Npb25JbmRleCI6Mn0seyJrZXkiOiJjb3JyZWxhdGlvbl9pZCIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiI1OTMzOGVhOC1iYjQ0LTRhM2EtOTIwYS0xN2ZiMGEzNTVmNTUiLCJzZXNzaW9uSW5kZXgiOjN9LHsia2V5IjoibWltZV90eXBlIiwidmFsdWUiOiJhcHBsaWNhdGlvbi92bmQuYXBpK2pzb24iLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6ImFwcGxpY2F0aW9uL3ZuZC5hcGkranNvbiIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJtZXNzYWdlX2JhdGNoX3JlZmVyZW5jZSIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiJmNjI1Yjc4OS04YTZlLTQ1ODEtOGM1Zi03ZWExMWMyNTRiNmYiLCJzZXNzaW9uSW5kZXgiOjV9XQ==)

Alternatively you can find our postman collection source in our [public repository on github](https://github.com/NHSDigital/communications-manager-api/tree/master/postman).

### Production smoke testing

You must not send communications to real patients for smoke testing in the production environment.

Rather, use the [production test patient for PDS](https://digital.nhs.uk/developer/api-catalogue/personal-demographics-service-fhir/pds-fhir-api-test-data#production-smoke-testing).

## Onboarding

You need to get your software approved by us before it can go live with this API. You will also need to undertake the Communications Manager onboarding process which is still being defined. Further details will follow.

To understand how our online digital onboarding process works, see [digital onboarding](https://digital.nhs.uk/developer/guides-and-documentation/digital-onboarding).

## Errors

We use standard HTTP status codes to show whether an API request succeeded or not. They are usually in the range:

* 200 to 299 if it succeeded, including code 202 if it was accepted by an API that needs to wait for further action
* 400 to 499 if it failed because of a client error by your application
* 500 to 599 if it failed because of an error on our server

Errors specific to each API are shown in the Endpoints section, under Response. See our [reference guide for more on errors](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#http-status-codes).
