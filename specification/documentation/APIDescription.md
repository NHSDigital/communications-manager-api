## Overview

Use this API to send messages to citizens via NHS App, email, text message or letter.

[NHS Notify](https://digital.nhs.uk/services/nhs-notify) provides:

* message templating
* message routing
* enrichment of recipient details
* support for accessible formats and multiple languages

Learn more about [NHS Notify's features](https://notify.nhs.uk/features/).

## Who can use this API

The NHS Notify service is intended for services involved in direct care. This API can only be used where you have a legal basis to issue communications to citizens.

## API status and roadmap

This API is [in production, beta](https://digital.nhs.uk/developer/guides-and-documentation/reference-guide#statuses). We are onboarding partners to use it.

We may make additive non-breaking changes to the API without notice, for example the addition of fields to a response or callback, or new optional fields to a request.

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

You can use the `Accept` header to control which `Content-Type` is returned in the response.

The `Accept` header can contain the following values:

* `*/*`
* `application/json`
* `application/vnd.api+json`

The `Accept` header may optionally include a `charset` attribute. If included, it **must** be set to `charset=utf-8` Any other `charset` value will result in a `415` error response. If omitted then `utf-8` is assumed. 

Where no `Accept` header is present, this will default to `application/vnd.api+json`

### Request content types

This API will accept request payloads of the following types:

* `application/vnd.api+json` - see [JSON:API specification](https://jsonapi.org/format/#introduction)
* `application/json`

The `Content-Type` header may optionally include a `charset` attribute. If included, it **must** be set to `charset=utf-8` Any other `charset` value will result in a `406` error response. If omitted then `utf-8` is assumed. 

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

[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.postman.com/nhs-communications-manager/communications-manager/collection/41628342-33dcc9d0-8ccc-4756-8ccb-237fd78337f5/?action=share&creator=41628342)

You can find our postman collection source in our [public repository on github](https://github.com/NHSDigital/communications-manager-api/tree/master/postman).

### Integration testing

Our integration test environment:

* is for formal integration sandbox-testing
* is stateful, so persists updates
* includes authorisation via [signed JWT authentication](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/application-restricted-restful-apis-signed-jwt-authentication)

You can try out our integration environment using our Postman collection. This Postman collection contains the signed JWT authentication mechanism, allowing you to test our integration environment without writing any code:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.postman.com/nhs-communications-manager/communications-manager/collection/cna2c8u/nhs-notify-integration?action=share&creator=41628342)

Alternatively you can find our postman collection source in our [public repository on github](https://github.com/NHSDigital/communications-manager-api/tree/master/postman).

### Production smoke testing

You must not send communications to real patients for smoke testing in the production environment.

Smoke testing is permitted only using the NHS Notify production test patients. When you onboard to NHS Notify, our onboarding team will get in touch to put together a smoke test plan. Smoke testing will be done one day prior to go live.

## Onboarding

You need to get your software approved by us before it can go live with this API.

You will also need to follow our steps to [onboard with NHS Notify](https://notify.nhs.uk/get-started/onboard-with-nhs-notify).

## Enable users to write and send messages from your software

NHS Notify can deliver NHS App messages, emails and text messages that your users write in your software's free-text inputs.

This is also useful if you:

* do not need to set up reusable templates for multiple recipients
* want to send individual messages

### Setting up your free-text inputs
You'll need to configure your free-text inputs to populate one of our personalisation fields. Each personalisation field is specific to a message channel and will contain the entire message content that your user will enter in your software.

You'll then need to include this personalisation field in your request.

###	Making your request to send messages from your software
Use the following routing plan IDs and personalisation fields that match the message channel your user will send their message with.

| Message channel                          | Personalisation field                  | Routing plan ID                      | 
|------------------------------------------|----------------------------------------|--------------------------------------|
| NHS App message                          | body                                   | 00000000-0000-0000-0000-000000000001 |
| Email                                    | email_subject, email_body              | 00000000-0000-0000-0000-000000000002 |
| Text message                             | sms_body                               | 00000000-0000-0000-0000-000000000003 |
| NHS App message with a fallback to email | nhsapp_body, email_subject, email_body | 00000000-0000-0000-0000-000000000004 |
| NHS App message with a 4hr fallback to email | nhsapp_body, email_subject, email_body | 00000000-0000-0000-0000-000000000005 |
| NHS App message with a 24hr fallback to Text message | nhsapp_body, sms_body | 00000000-0000-0000-0000-000000000006 |
| NHS App message with a 4hr fallback to Text message | nhsapp_body, sms_body | 00000000-0000-0000-0000-000000000007 |

For email, use the personalisation field `email_subject` to allow your user to add the email subject line.

Complete your request in the same way you [send a single message](#post-/v1/messages) or [send a batch of messages](#post-/v1/message-batches).

When you make your request, we'll aim to deliver the message within:
* 24 hours for NHS App messages 
* 72 hours for emails
* 72 hours for text messages

Your message will have a 'failed' status if it's not delivered within this time. Find out more about [message, channel and supplier statuses](https://notify.nhs.uk/using-nhs-notify/message-channel-supplier-status).

You can try out example requests in the sandbox environment in our [Postman collection](#overview--environments-and-testing).

### Formatting messages written in your software
You can use Markdown to add formatting that your users apply to NHS App messages and emails they write in your software.

For NHS App messages, follow the <a href="https://digital.nhs.uk/developer/api-catalogue/nhs-app#post-/communication/in-app/FHIR/R4/CommunicationRequest" target="new">Markdown guidance in the 'contentString' section of the schema (opens in a new tab)</a>.

For emails, follow the Markdown guidance for:
* <a href="https://www.notifications.service.gov.uk/using-notify/links-and-URLs" target="_new">links and URLs (opens in a new tab)</a>
* <a href="https://www.notifications.service.gov.uk/using-notify/formatting" target="_new">bullet points, headings, horizontal lines, inset text and numbered steps (opens in a new tab)</a>

Your users will not be able to use <a href="https://notify.nhs.uk/using-nhs-notify/personalisation" target="_new">personalisation offered by NHS Notify (opens in a new tab)</a> in messages they write from your software.

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

We will send you a HMAC-SHA256 signature in the `x-hmac-sha256-signature` header. You will need to validate the signature to verify the response has come from NHS Notify.
This can be achieved by hashing the request body using the HMAC-SHA256 algorithm with a secret value that is comprised of a concatenation of your APIM application ID and the API key that we provide you. The secret takes the following form `[APPLICATION_ID].[API_KEY]`. If you receive a request with an invalid signature you should ignore it and respond with a `403 Forbidden`.

Every request includes an `idempotencyKey` field located in the meta collection of the body. This can help ensure your system remains idempotent, capable of managing duplicate delivery of callbacks. It's important to note that requests may be delivered non-sequentially.

If a request fails, our retry policy will continue to attempt to deliver the callback for a period of 2 hours.

## Message character limits
Different character limits apply to each of the communication channels as listed below. NHS Notify will validate that any personalisation fields submitted in the send message request do not exceed these limits but it is the client's responsibility to ensure that when personalisation is combined with any templated text, the channel character limit is not exceeded.

| Channel            | Character Limit |
|--------------------|-----------------|
| Email              | 100,000         |
| Letter             | 15,000          |
| NHS App            | 5,000           |
| Text message (SMS) | 918             |