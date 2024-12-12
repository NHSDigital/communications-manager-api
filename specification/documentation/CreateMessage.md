## Overview

Use this endpoint to send a single message to an NHS patient.

### References

You must provide a single reference value within the payload to this endpoint that is a message reference.

This reference must be a [Universal Unique Identifier (UUID)](https://en.wikipedia.org/wiki/Universally_unique_identifier).

The message reference (`messageReference`) needs to be unique across all single messages you have sent. This value is used to store your reference for this specific message and can be used if you lose (or do not recieve) our unique identifier in the response.

### Personalisation

You may be required to send through specific personalisation fields based upon the routing plan (`routingPlanId`). These will have been setup during your onboarding process.

These are not validated when we store your message, but will be validated when we attempt to send the message according to the routing plan. If there are values missing from this then the message will fail to send.

### Sandbox

When sending this request on sandbox you must use one of the 6 preconfigured routing plan identifiers:

-   `b838b13c-f98c-4def-93f0-515d4e4f4ee1`
-   `49e43b98-70cb-47a9-a55e-fe70c9a6f77c`
-   `b402cd20-b62a-4357-8e02-2952959531c8`
-   `936e9d45-15de-4a95-bb36-ae163c33ae53`
-   `9ba00d23-cd6f-4aca-8688-00abc85a7980`
-   `00000000-0000-0000-0000-000000000001`

On other environments these values will be established as part of your [NHS Notify onboarding](#overview--onboarding).

Here is an example curl request which creates a message using one of these routing plan identifiers:

```
  curl -X POST \
    --header "Accept: */*" \
    --header "Content-type: application/vnd.api+json" \
    -d '{"data": {"type": "Message","attributes": {"routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1","messageReference": "da0b1495-c7cb-468c-9d81-07dee089d728","recipient": {"nhsNumber": "9990548609"},"originator": {"odsCode":"X123"},"personalisation": {}}}}' \
    https://sandbox.api.service.nhs.uk/comms/v1/messages
```
