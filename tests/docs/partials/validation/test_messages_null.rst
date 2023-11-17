Scenario: An API consumer submitting a message with an empty required attribute in the request body receives a 400 'Null Value' response
========================================================================================================================================

| **Given** the API consumer provides an message body with a null attribute
| **When** the request is submitted
| **Then** the response returns a 400 null value error

**Asserts**
- Response returns a 400 'Null Value' error
- Response returns the expected error message body with references to the null attribute
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/message_request_properties.rst
.. include:: ../../partials/correlation_ids.rst