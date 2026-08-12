## Overview

Use this endpoint to retrieve recipient responses associated with a specific message.

Responses are available for retrieval for up to 9 months after the message was sent.

### Response structure

A successful response returns a flat JSON array of response items.

Each item includes:

* `responseId` - the unique identifier for this response
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

When sending this request on sandbox you can use any valid message ID format.

To simulate error responses in the sandbox, use the following message IDs:

* not found - `00000000-0000-4000-8000-000000000404`
* bad gateway - `00000000-0000-4000-8000-000000000502`
* too many responses - `00000000-0000-4000-8000-000000000500`

Here's an example curl command:

```
curl -X GET 'https://sandbox.api.service.nhs.uk/comms/v1/message-responses/2WL3qFTEFM0qMY8xjRbt1LIKCzM' \
     --header 'Accept: application/vnd.api+json'
```
