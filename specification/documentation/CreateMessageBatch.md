## Overview

Use this endpoint to send a batch of messages to 1 or more NHS patients.

### References

You must provide two reference values within the payload to this endpoint:

-   A message batch reference
-   A per message reference

The message batch reference (`messageBatchReference`) is unique for you. This value is used to store your reference for this batch of messages.

The per message reference (`messageReference`) needs to be unique within the message batch. This value is used to store your reference for this specific message within the batch.

### Personalisation

You may be required to send through specific personalisation fields based upon the routing plan (`routingPlanId`). These will have been setup during your [onboarding](#overview--onboarding) process.

These are not validated when we store your message batch, but will be validated when we attempt to send the messages according to the routing plan. If there are values missing from this then the messages will fail to send.

### Sandbox

When sending this request on sandbox you must use one of the 6 preconfigured routing plan identifiers:

-   `b838b13c-f98c-4def-93f0-515d4e4f4ee1`
-   `49e43b98-70cb-47a9-a55e-fe70c9a6f77c`
-   `b402cd20-b62a-4357-8e02-2952959531c8`
-   `936e9d45-15de-4a95-bb36-ae163c33ae53`
-   `9ba00d23-cd6f-4aca-8688-00abc85a7980`
-   `00000000-0000-0000-0000-000000000001`

On other environments these values will be established as part of your [NHS Notify onboarding](#overview--onboarding).

Here is an example curl request which creates a message batch using one of these routing plan identifiers:

```
  curl -X POST \
    --header "Accept: */*" \
    --header "Content-type: application/vnd.api+json" \
    -d '{"data": {"type": "MessageBatch","attributes": {"routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1","messageBatchReference": "da0b1495-c7cb-468c-9d81-07dee089d728","messages": [{"messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575","recipient": {"nhsNumber": "9990548609"},"originator": {"odsCode":"X123"},"personalisation": {}}]}}}' \
    https://sandbox.api.service.nhs.uk/comms/v1/message-batches
```
