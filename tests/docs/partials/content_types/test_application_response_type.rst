Scenario: An API consumer submitting a request with a valid accept header receives a response containing the expected accept header
===================================================================================================================================

| **Given** the API consumer provides a valid accept header
| **When** the request is submitted
| **Then** the response returned is in the format requested

**Asserts**
- Response returns the expected accept header

.. include:: /partials/valid_accept_headers.rst
.. include:: /partials/methods.rst