Scenario: An API consumer submitting a message with an invalid required attribute in the request body receives a 400 'Invalid Value' response
=============================================================================================================================================

| **Given** the API consumer provides an message body with an invalid attribute
| **When** the request is submitted
| **Then** the response returns a 400 invalid value error

**Asserts**
- Response returns a 400 'Invalid Value' error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/message_request_properties.rst
.. include:: ../../partials/correlation_ids.rst