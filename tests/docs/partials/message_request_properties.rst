**Request Properties**

This test uses a method to replace the values in the response body, it sets the new value, and sets the value of the location of where the attribute has been changed.

Below is a table showing the required attributes and their locations as seen in the response body.

.. list-table::
    :widths: 50 50

    * - Attribute
      - Location
    * - data
      - /data
    * - type
      - /data/type
    * - attributes
      - /data/attributes
    * - routingPlanId
      - /data/attributes/routingPlanId
    * - messageReference
      - /data/attributes/messageReference
    * - recipient
      - /data/attributes/recipient
    * - nhsNumber
      - /data/attributes/recipient/nhsNumber
