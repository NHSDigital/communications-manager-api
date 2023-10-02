**Methods**

This test makes use of different HTTP methods, if the method is either HEAD or OPTIONS the test will not assert against the body of the response as none is returned.

.. list-table::
    :widths: 50
    :header-rows: 7

    * - Value
    * - GET
    * - POST
    * - PUT
    * - PATCH
    * - DELETE
    * - HEAD
    * - OPTIONS
