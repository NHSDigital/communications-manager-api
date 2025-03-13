Scenario: An API consumer submitting a request without a required attribute in the request body receives a 400 'Missing Value' response
=======================================================================================================================================

| **Given** the API consumer provides an message body with a missing required attribute
| **When** the request is submitted
| **Then** the response returns a 400 missing value error

**Asserts**
- Response returns a 400 'Missing Value' error
- Response returns the expected error message body with references to the missing attribute

.. include:: /partials/message_request_properties.rst