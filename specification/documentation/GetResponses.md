## Overview

Use this endpoint to query historical NHS App keyword responses associated with a specific message.

Responses are available for retrieval for up to 9 months after the message was sent.

### Authentication

This endpoint requires APIM application identity credentials. You must include a valid `Authorization` header on every request. See the [security and authorisation](#overview--security-and-authorisation) section for details on obtaining credentials.

### Preconditions

* Your application has valid APIM credentials with the appropriate scope.
* The message used the NHS App channel with keyword response options configured.

If no responses exist yet, the `data` array in the response will be empty.

### Request

```
GET /v1/messages/{messageId}/responses
```

#### Path parameters

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `messageId` | KSUID | Yes | The unique identifier of the message for which you are retrieving responses. |

#### Query parameters

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `cursor` | string | No | An opaque cursor value from `links.next` or `links.prev` in a previous response. Omit to retrieve the first page. |

#### Headers

| Header | Required | Description |
| ------ | -------- | ----------- |
| `Authorization` | Yes (except sandbox) | Bearer token from APIM signed JWT authentication. |
| `X-Correlation-ID` | No | An optional ID to track transactions across systems. Returned in the response header. |
| `Accept` | No | `application/vnd.api+json` (default) or `application/json`. |

#### Example request

```
curl -X GET \
  --header "Authorization: Bearer <your-bearer-token>" \
  --header "Accept: application/vnd.api+json" \
  --header "X-Correlation-ID: 11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA" \
  https://api.service.nhs.uk/comms/v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM/responses
```

### Response

A successful `200` response returns a JSON:API collection containing all responses for the given message.

#### Response body

```json
{
  "data": [
    {
      "type": "Response",
      "id": "33333333-3333-4333-8333-333333333333",
      "attributes": {
        "messageId": "2WL3qFTEFM0qMY8xjRbt1LIKCzM",
        "code": "YES",
        "authoredAt": "2026-01-15T10:30:00Z",
        "timestamp": "2026-01-15T10:30:05Z",
        "channel": "nhsapp"
      }
    }
  ],
  "links": {
    "self": "https://api.service.nhs.uk/comms/v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM/responses",
    "next": null,
    "prev": null
  },
  "meta": {
    "totalCount": 1
  }
}
```

#### Response fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `data` | array | Array of response items. Empty if no responses exist. |
| `data[].type` | string | Always `"Response"`. |
| `data[].id` | string (UUID) | The unique identifier for this response. |
| `data[].attributes.messageId` | string (KSUID) | The identifier of the message this response belongs to. |
| `data[].attributes.code` | string | The keyword code selected by the recipient. |
| `data[].attributes.authoredAt` | string (date-time) | The date-time the recipient submitted their response. |
| `data[].attributes.timestamp` | string (date-time) | The date-time the response was processed by NHS Notify. |
| `data[].attributes.channel` | string | The channel through which the response was received. Currently always `nhsapp`. |
| `links.self` | string (URI) | The URL of the current page. |
| `links.next` | string (URI) or null | The URL of the next page. Absent or null if there are no further pages. |
| `links.prev` | string (URI) or null | The URL of the previous page. Absent or null if there is no previous page. |
| `meta.totalCount` | integer | The total number of responses available for this message. |

### Pagination

This endpoint uses cursor-based pagination. The response includes a `links` object containing `next` and `prev` URLs when additional pages are available.

To retrieve all responses for a message:

1. Send an initial request without a `cursor` parameter.
2. If `links.next` is present and non-null, send a subsequent request using the value of `links.next` as your URL (or extract the `cursor` query parameter from it).
3. Continue until `links.next` is null or absent.

The cursor value is opaque — do not attempt to construct or parse it. Always use the full URL from `links.next`.

#### Pagination example

**First page:**

```
GET /v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM/responses
```

Response:

```json
{
  "data": [...],
  "links": {
    "self": "https://api.service.nhs.uk/comms/v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM/responses",
    "next": "https://api.service.nhs.uk/comms/v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM/responses?cursor=eyJsYXN0S2V5IjoidGVzdCJ9",
    "prev": null
  }
}
```

**Second page:**

```
GET /v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM/responses?cursor=eyJsYXN0S2V5IjoidGVzdCJ9
```

### Error responses

#### 400 — Invalid message ID

Returned when the `messageId` path parameter is not a valid KSUID.

```json
{
  "errors": [
    {
      "id": "rrt-1931948104716186917-c-geu2-10664-3111479-3.0",
      "code": "CM_INVALID_VALUE",
      "status": "400",
      "title": "Invalid value",
      "detail": "The message ID provided is not a valid KSUID.",
      "source": {
        "parameter": "messageId"
      }
    }
  ]
}
```

#### 403 — Forbidden

Returned when the request is not authorised.

```json
{
  "errors": [
    {
      "id": "rrt-1931948104716186917-c-geu2-10664-3111479-3.0",
      "code": "CM_FORBIDDEN",
      "status": "403",
      "title": "Forbidden",
      "detail": "Client not recognised or not yet onboarded."
    }
  ]
}
```

#### 503 — Service unavailable

Returned when the datastore is temporarily unavailable. Retry after the number of seconds indicated in the `Retry-After` response header.

```json
{
  "errors": [
    {
      "id": "rrt-1931948104716186917-c-geu2-10664-3111479-3.0",
      "code": "CM_SERVICE_UNAVAILABLE",
      "status": "503",
      "title": "The service is currently unavailable",
      "detail": "The service is currently not able to process this request, try again later."
    }
  ]
}
```

### Security

* **Transport security**: All requests must be made over TLS 1.2 or higher.
* **Authentication**: Every request must include a valid `Authorization` header.
* **Data classification**: Response payloads may contain information about patient interactions. Handle and store this data in accordance with your data processing agreements and applicable data protection obligations.

### Postconditions

* Retrieval is read-only. Calling this endpoint does not modify any message or response state.
* The `X-Correlation-ID` header is returned in every response, for use in end-to-end audit tracing.

### Non-functional requirements

* **Availability**: This endpoint is subject to the same platform SLA as other NHS Notify endpoints. See the [service level](#overview--service-level) section.
* **Rate limiting**: APIM rate limits apply. See the [errors](#overview--errors) section and the `429` response definition.
* **Data retention**: Responses are available for retrieval for up to 9 months after the originating message was sent.

### Sandbox

The sandbox environment does not persist data, so responses will not be returned for messages created in a previous sandbox session.

To test a successful retrieval in the sandbox, first create a message using the `POST /v1/messages` endpoint in the sandbox, then call this endpoint with the returned message ID.

To simulate error responses in the sandbox, use the `Prefer` header:

| `Prefer` value | Simulated response |
| -------------- | ------------------ |
| `code=400` | 400 Invalid message ID |
| `code=403` | 403 Forbidden |
| `code=503` | 503 Service unavailable |

Example:

```
curl -X GET \
  --header "Accept: application/vnd.api+json" \
  --header "Prefer: code=403" \
  https://sandbox.api.service.nhs.uk/comms/v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM/responses
```
