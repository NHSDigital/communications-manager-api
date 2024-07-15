## Overview

Use this API to send messages to citizens via email, SMS, the NHS App or letter.

NHS Notify provides:

* message templating
* message routing - via SMS, email, letter and NHS App
* enrichment of recipient details
* support for accessible formats and multiple languages

For more information about this service's capabilities, see [NHS Notify](https://digital.nhs.uk/services/nhs-notify).

## Who can use this API

The NHS Notify service is intended for services involved in direct care. This API can only be used where you have a legal basis to issue communications to citizens.

## API status and roadmap

This API is [in production, beta](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#statuses). We are onboarding partners to use it.

You can comment, upvote and view progress on [our roadmap](https://nhs-digital-api-management.featureupvote.com/?order=top&filter=allexceptdone&tag=nhs-notify-api).

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

You need to get your software approved by us before it can go live with this API. You will also need to undertake the NHS Notify onboarding process which is still being defined. Further details will follow.

To understand how our online digital onboarding process works, see [digital onboarding](https://digital.nhs.uk/developer/guides-and-documentation/digital-onboarding).

## Free-text communications

Free-text communications (as opposed to fixed format communications) can be achieved by setting up a generic template and making use of the personalisation fields to provide the content of the message.  In order to make this more convenient the service provides some globally available routing plans that any client can use.

| Global Routing Plan ID               | Channel/Supplier | Read wait time (before failing channel) | Personalisation field name |
|--------------------------------------|------------------|-----------------------------------------|----------------------------|
| 00000000-0000-0000-0000-000000000001 | NHS App          | 24 hours                                | body                       |

Please see the Postman collections in the [environments and testing section](#section/Environments-and-testing) for examples.

## Errors

We use standard HTTP status codes to show whether an API request succeeded or not. They are usually in the range:

* 200 to 299 if it succeeded, including code 202 if it was accepted by an API that needs to wait for further action
* 400 to 499 if it failed because of a client error by your application
* 500 to 599 if it failed because of an error on our server

Errors specific to each API are shown in the Endpoints section, under Response. See our [reference guide for more on errors](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#http-status-codes).

## Receive a callback

You may develop one or many endpoints on your service if you want to receive callbacks from NHS Notify.

We have created an OpenAPI specification detailing the behaviour of the endpoint that consumers should create to subscribe to callbacks.

We will send your API key in the `x-api-key header`. Your service should respond with:

* `401 Unauthorized` if the API key is not received
* `401 Unauthorized` if the API key is invalid

We will send you a HMAC-SHA256 signature in the `x-hmac-sha256-signature` header. You will need to validate the signature to verify the response has come from an authorized sender. Details on this will be provided during the onboarding process. If you receive a request with an invalid signature you should ignore it and respond with a `403 Forbidden`.

Every request includes an `idempotencyKey` field located in the meta collection of the body. This can help ensure your system remains idempotent, capable of managing duplicate delivery of callbacks. It's important to note that requests may be delivered non-sequentially.

If a request fails, our retry policy will make up to three attempts with intervals of five seconds between each attempt.

## Message Statuses

Messages can have the following statuses:

* `created` - the message has been created, but has received no processing
* `pending_enrichment` - the message is currently pending enrichment
* `enriched` - we have queried PDS for this patient's details and now know how to contact this individual
* `sending` - the message is in the process of being sent
* `delivered` - the message has been delivered
* `failed` - we have failed to deliver the message

For certain statuses more information can be found within the `messageStatusDescription` field.

The message status shows an overall aggregate status taken from all of the communication channels that we have attempted to deliver the message using.

## Supplier Statuses

The channels can have the following supplier statuses:

### NHS APP

* `delivered` - the message has been successfully delivered to the user
* `read` - a user has read the message
* `notification_attempted` - a push notification is reported as having been sent to one or more devices, but does not indicate whether the notification was received or displayed
* `unnotified` - it has been determined that a push notification has not been successfully relayed to any devices
* `rejected` - the request to send the communication was rejected by the supplier
* `notified` - a push notification is reported as having been successfully relayed to one or more devices
* `received` - the request has been received by the supplier and is queued to be processed

### GOV.UK Notify (Email/SMS)

* `delivered` - the message has been successfully delivered to the user
* `permanent_failure` - the Email/SMS provider could not deliver the message, this can happen if the phone number was wrong or if the network operator rejects the message
* `temporary_failure` - the Email/SMS provider could not deliver the message, this can happen when the recipient’s phone is off, has no signal, or their text message inbox is full
* `technical_failure` - the message was not sent because there was a problem between GOV.UK Notify and the Email/SMS provider

### GOV.UK Notify (Letters)

* `accepted` - GOV.UK Notify has sent the letter to the provider to be printed
* `received` - the provider has printed and dispatched the letter
* `cancelled` - sending cancelled, the letter will not be printed or dispatched
* `pending_virus_check` - GOV.UK Notify has not completed a virus scan of the precompiled letter file
* `virus_scan_failed` - GOV.UK Notify found a potential virus in the precompiled letter file
* `validation_failed` - content in the precompiled letter file is outside the printable area
* `technical_failure` - GOV.UK Notify had an unexpected error while sending the letter to their printing provider
* `permanent_failure` - the provider cannot print the letter, the letter will not be dispatched

Presently there is no callback integration for HH, MBA, or Synertec.
