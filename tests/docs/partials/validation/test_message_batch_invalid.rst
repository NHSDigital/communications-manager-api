Scenario: An API consumer submitting a request with an invalid required attribute in the request body receives a 400 'Invalid Value' response
=============================================================================================================================================

| **Given** the API consumer provides an message body with an invalid attribute
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Invalid Value' error
- Response returns the expected error message body with references to the invalid attribute

.. include:: /partials/message_batch_request_properties.rst