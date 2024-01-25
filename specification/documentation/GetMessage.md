## Overview

Use this endpoint to fetch the status of a single message sent by your account.

### Channels

The [NHS Notify Service](https://digital.nhs.uk/services/nhs-notify) supports multiple channels for delivering a message.

These channels are:

* sms
* email
* letter
* NHS app

The channels used to send your message are configured within the routing plan. These routing plans are configured during your [onboarding process](#overview--onboarding).

The channels configured in your routing plan at the time of sending are returned as part of the message status response. The channels are returned in the order that sending will be attempted.

Key values that are returned for each of these channels are:

* `type` - the channel type
* `channelStatus` - the status of that channel
* `channelStatusDescription` - the channel status description
* `retryCount` - the number of times we have attempted delivery
* `timestamps` - timestamps of key events
* `routingPlan` - the routing plan that was used to generate the channel

Each channel can have one of the following statuses:

* `created` - the channel has been created
* `skipped` - the channel has been skipped
* `sending` - the channel is in the process of sending the message
* `delivered` - the channel has delivered the message
* `failed` - the channel has failed to deliver the message

If your routing plan supports conditional overrides, then in certain situations the routing plan referenced by a channel may be different from the one you initially requested. If this occurs then the `routingPlan.type` field will be set to the value `override`, plus the `id` and `version` fields will reflect the override that was used.

The following CURL request example highlights this interaction and can be replicated using message id `2bBBpsiMl2rnQt99qm6JLZ6w1vq`:
```
curl -X GET 'https://sandbox.api.service.nhs.uk/comms/v1/messages/2bBBpsiMl2rnQt99qm6JLZ6w1vq' \
     --header 'Accept: application/vnd.api+json'
```

### Message Statuses

Messages can have the following statuses:

* `created` - the message has been created, but has received no processing
* `pending_enrichment` - the message is currently pending enrichment
* `enriched` - we have queried PDS for this patients details and now know how to contact this individual
* `sending` - the message is in the process of being sent
* `delivered` - the message has been delivered
* `failed` - we have failed to deliver the message

For certain statuses more information can be found within the `messageStatusDescription` field.

The message status shows an overall aggregate status taken from all of the communication channels that we have attempted to deliver the message using.

### 3rd Party Querying

This system queries 3rd party integrations during the sending process. If this occurs, the `metadata` field will be populated with information about the queries made, including:

* `queriedAt` - the date and time that the query occured at
* `version` - a version of the document returned in the query, if supported by the 3rd party
* `labels` - the channels that the response affected
* `source` - the 3rd party system the query was made to

The 3rd party systems being queried are:

* `pds` - [Personal Demographics Service](https://digital.nhs.uk/services/personal-demographics-service)

### Personalisation & Contact details

Personalisation and contact details are not returned within the messages. This is to ensure that Personally Identifiable Information cannot be extracted from the system.

### Sandbox

When sending this request on sandbox you can use one of these 5 message identifiers:

* single message status of delivered - `2WL3qFTEFM0qMY8xjRbt1LIKCzM`
* single message delivered using multiple channels - `2WL5eYSWGzCHlGmzNxuqVusPxDg`
* single message status of sending - `2WL4GEeFVxXG9S57nRlefBwwKxp`
* single message failed as patient has no exit code - `2WL4mvx6eBva8dcIK60VEGIfcgZ`
* single message routing plan overriden - `2bBBpsiMl2rnQt99qm6JLZ6w1vq`

Here's an example curl command using one of the above message Id's:

```
curl -X GET 'https://sandbox.api.service.nhs.uk/comms/v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM' \
     --header 'Accept: application/vnd.api+json'
```
