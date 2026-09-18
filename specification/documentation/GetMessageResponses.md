## Overview

Use this endpoint to retrieve recipient responses associated with a specific message.

Recipient responses are the keyword answers selected by a recipient for a message sent through the NHS App. For more information, see the [recipient response callback](#post-/-client-provided-recipient-response-URI-).

Responses are available for retrieval for up to 9 months after the message was sent.

### Response structure

A successful response returns a JSON:API document containing an array of recipient response resources, for example:

```json
{
  "data": [
    {
      "type": "RecipientResponse",
      "id": "33333333-3333-4333-8333-333333333333",
      "attributes": {
        "messageId": "11111111-1111-4111-8111-111111111111",
        "messageReference": "da0b1495-c7cb-468c-9d81-07dee089d728",
        "channel": "nhsapp",
        "channelStatus": "delivered",
        "cascadeType": "primary",
        "code": "YES",
        "authoredAt": "2026-06-15T14:30:00.000Z",
        "timestamp": "2026-06-15T14:30:05.123Z"
      }
    }
  ]
}
```

Each resource has:

* `type` - the resource type, always `RecipientResponse`
* `id` - the unique identifier for this response

Each resource's `attributes` include:

* `messageId` - the identifier of the message this response relates to
* `messageReference` - the reference you provided when the message was created
* `channel` - the channel through which the response was received
* `channelStatus` - the status of the channel at the time the response was received
* `channelFailureReasonCode` - the reason code for the channel failure (only present when `channelStatus` is `failed`)
* `cascadeType` - whether this is a `primary` or `secondary` cascade response
* `code` - the keyword code selected by the recipient
* `authoredAt` - the date-time the recipient submitted their response
* `timestamp` - the date-time the response was recorded by NHS Notify

If no responses exist for the given message, a `404` response is returned.

### Sandbox

When sending this request on sandbox you can use any valid UUID v4 message ID.

To simulate error responses in the sandbox, use the following message IDs:

* not found - `00000000-0000-4000-8000-000000000404`

Here's an example curl command:

```
curl -X GET 'https://sandbox.api.service.nhs.uk/comms/v1/message-responses/11111111-1111-4111-8111-111111111111' \
     --header 'Accept: application/vnd.api+json'
```
