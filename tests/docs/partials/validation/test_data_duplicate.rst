Scenario: An API consumer submitting a request with a duplicate attribute in the request body receives a 400 'Duplicate Value' response
=======================================================================================================================================

| **Given** the API consumer provides an message body with duplicate attributes
| **When** the request is submitted
| **Then** the response returns a 400 duplicate value error

**Asserts**
- Response returns a 400 'Duplicate Value' error
- Response returns the expected error message body with references to the duplicate attribute
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/request_properties.rst
.. include:: ../../partials/correlation_ids.rst