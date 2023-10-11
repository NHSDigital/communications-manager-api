Scenario: An API consumer submitting a request with too few attributes in the request body receives a 400 'Invalid Value' response
==================================================================================================================================

| **Given** the API consumer provides an message body with too few attributes
| **When** the request is submitted
| **Then** the response returns a 400 too few items error

**Asserts**
- Response returns a 400 'Too Few Items' error
- Response returns the expected error message body with references to the removed attribute
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/request_properties.rst
.. include:: ../../partials/correlation_ids.rst