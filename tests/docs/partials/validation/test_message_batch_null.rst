Scenario: An API consumer submitting a request with an empty required attribute in the request body receives a 400 'Null Value' response
========================================================================================================================================

| **Given** the API consumer provides an message body with a null attribute
| **When** the request is submitted
| **Then** the response returns a 400 null value error

**Asserts**
- Response returns a 400 'Null Value' error
- Response returns the expected error message body with references to the null attribute

.. include:: /partials/message_batch_request_properties.rst