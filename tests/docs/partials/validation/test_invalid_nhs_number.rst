Scenario: An API consumer submitting a request with an invalid NHS number receives a 400 'Invalid NHS Number' response
======================================================================================================================

An NHS Number is a 10 digit number used to identify patients, for more information on the structure of NHS numbers look `here <https://www.datadictionary.nhs.uk/attributes/nhs_number.html>`__

| **Given** the API consumer provides an message body with an invalid NHS number
| **When** the request is submitted
| **Then** the response returns a 400 invalid nhs number error

**Asserts**
- Response returns a 400 'Invalid NHS Number' error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the 'X-Correlation-Id' header if provided

.. include:: ../../partials/correlation_ids.rst