## Overview

Use this endpoint to fetch the status of a single message sent by your account.

### Personalisation & Contact details

Personalisation and contact details are not returned within the messages. This is to ensure that Personally Identifiable Information cannot be extracted from the system.

### Sandbox
When sending this request on sandbox you can use one of these 5 message identifiers:
* single message status of delivered - `2WL3qFTEFM0qMY8xjRbt1LIKCzM`
* single message status of sending - `2WL4GEeFVxXG9S57nRlefBwwKxp`
* single message status of failed - `2WL4cPfBRuPKa44JxhyXYf2kr1E`
* message as part of a batch delivered - `2WL5qbEa7TzSWZXU2IAOCCrLXVL`

Here's an example curl command using one of the above message Id's:
```
curl --location 'https://sandbox.api.service.nhs.uk/comms/v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM' \
--header 'Accept: application/vnd.api+json'
```

### Message channels

The [Communications Manager Service](https://digital.nhs.uk/services/communications-manager) supports multiple channels. These channels are configured within the routing plan specified by the messages `routingPlan`. These routing plans are configured during your [onboarding process](#overview--onboarding).

The channels configured in your routing plan at the time of sending are returned as part of the message status response. The channels are returned in the order that sending will be attempted.

Key values that are returned for each of these channels are:

* the channel type - `type`
* the status of that channel - `channelStatus`
* the channel status description - `channelStatusDescription`
* the number of times we have attempted delivery - `retryCount`
* timestamps of key events - `timestamps`
* the routing plan that was used to generate the channel - `routingPlan`

If your routing plan supports conditional overrides then in certain situations the routing plan referenced by a channel may be different from the one you initially requested. If this occurs then the `routingPlan.type` field will be set to the value `override`, plus the `id` and `version` fields will reflect the override that was used.

### Message & Channel statuses

Messages can have the following statuses:

* `created` - the message has been created, but has received no processing
* `pending_enrichment` - the message is currently pending enrichment
* `enriched` - we have queried PDS for this patients details and now know how to contact this individual
* `sending` - the message is in the process of being sent
* `delivered` - the message has been delivered
* `failed` - we have failed to deliver the message

For certain statuses more information can be found within the `messageStatusDescription` field.

This status shows an overall aggregate status taken from all of the communication channels that we have attempted to deliver the message using. For individual channels there is a different set of statuses:

* `created`
* `skipped`
* `sending`
* `delivered`
* `failed`

### PDS Querying

We query PDS in order to extract the NHS patients contact details - these details are utilised for the sending of communications.

In order to aid debugging with changes to a patients PDS record that may occur after you have requested communications to be sent, we return the `versionIdentifier` of the patients PDS record when Communications Manager queried it, aswell as the date and time (`queriedAt`) that the query was made at. Please refer to the [PDS FHIR Get Patientendpoint documentation](https://digital.nhs.uk/developer/api-catalogue/personal-demographics-service-fhir#get-/Patient/-id-) for more information about this `versionIdentifier`.

These values will allow you to reconstruct the state of the PDS record at the time Communications Manager queried PDS - this allows you to confirm why certain channels were or were not used for sending messages. You may need to [contact PDS](https://digital.nhs.uk/services/personal-demographics-service#contact-us) in order to do this reconstruction.
