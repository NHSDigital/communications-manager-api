# Validation Tests


### Scenario: An API consumer submitting a request with an invalid         message value receives a 400 'Invalid Value' response

**Given** the API consumer provides an message body with an invalid message value
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with a duplicate attribute         in the request body receives a 400 'Duplicate Value' response

**Given** the API consumer provides an message body with duplicate attributes
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 duplicate value error
<br/>

**Asserts**
- Response returns a 400 ‘Duplicate Value’ error
- Response returns the expected error message body with references to the duplicate attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Request Properties**

This test uses a method to replace the values in the response body, it sets the new value, and sets the value of the location of where the attribute has been changed.

Below is a table showing the required attributes and their locations as seen in the response body.

| Attribute             | Location                                        |
|-----------------------|-------------------------------------------------|
| data                  | /data                                           |
| type                  | /data/type                                      |
| attributes            | /data/attributes                                |
| routingPlanId         | /data/attributes/routingPlanId                  |
| messageBatchReference | /data/attributes/messageBatchReference          |
| messages              | /data/attributes/messages                       |
| messageReference      | /data/attributes/messages/0/messageReference    |
| recipient             | /data/attributes/messages/0/recipient           |
| nhsNumber             | /data/attributes/messages/0/recipient/nhsNumber |

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with an invalid required attribute         in the request body receives a 400 'Invalid Value' response

**Given** the API consumer provides an message body with an invalid attribute
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Request Properties**

This test uses a method to replace the values in the response body, it sets the new value, and sets the value of the location of where the attribute has been changed.

Below is a table showing the required attributes and their locations as seen in the response body.

| Attribute             | Location                                        |
|-----------------------|-------------------------------------------------|
| data                  | /data                                           |
| type                  | /data/type                                      |
| attributes            | /data/attributes                                |
| routingPlanId         | /data/attributes/routingPlanId                  |
| messageBatchReference | /data/attributes/messageBatchReference          |
| messages              | /data/attributes/messages                       |
| messageReference      | /data/attributes/messages/0/messageReference    |
| recipient             | /data/attributes/messages/0/recipient           |
| nhsNumber             | /data/attributes/messages/0/recipient/nhsNumber |

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with an empty required attribute         in the request body receives a 400 'Null Value' response

**Given** the API consumer provides an message body with a null attribute
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 null value error
<br/>

**Asserts**
- Response returns a 400 ‘Null Value’ error
- Response returns the expected error message body with references to the null attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Request Properties**

This test uses a method to replace the values in the response body, it sets the new value, and sets the value of the location of where the attribute has been changed.

Below is a table showing the required attributes and their locations as seen in the response body.

| Attribute             | Location                                        |
|-----------------------|-------------------------------------------------|
| data                  | /data                                           |
| type                  | /data/type                                      |
| attributes            | /data/attributes                                |
| routingPlanId         | /data/attributes/routingPlanId                  |
| messageBatchReference | /data/attributes/messageBatchReference          |
| messages              | /data/attributes/messages                       |
| messageReference      | /data/attributes/messages/0/messageReference    |
| recipient             | /data/attributes/messages/0/recipient           |
| nhsNumber             | /data/attributes/messages/0/recipient/nhsNumber |

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with too few attributes         in the request body receives a 400 'Invalid Value' response

**Given** the API consumer provides an message body with too few attributes
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 too few items error
<br/>

**Asserts**
- Response returns a 400 ‘Too Few Items’ error
- Response returns the expected error message body with references to the removed attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Request Properties**

This test uses a method to replace the values in the response body, it sets the new value, and sets the value of the location of where the attribute has been changed.

Below is a table showing the required attributes and their locations as seen in the response body.

| Attribute             | Location                                        |
|-----------------------|-------------------------------------------------|
| data                  | /data                                           |
| type                  | /data/type                                      |
| attributes            | /data/attributes                                |
| routingPlanId         | /data/attributes/routingPlanId                  |
| messageBatchReference | /data/attributes/messageBatchReference          |
| messages              | /data/attributes/messages                       |
| messageReference      | /data/attributes/messages/0/messageReference    |
| recipient             | /data/attributes/messages/0/recipient           |
| nhsNumber             | /data/attributes/messages/0/recipient/nhsNumber |

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request without a request body         receives a 400 'Invalid Value' response

**Given** the API consumer provides an empty message body
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with an invalid         date of birth receives a 400 'Invalid Value' response

A valid date of birth must be structured in this format: YYYY-MM-dd

**Given** the API consumer provides an message body with an invalid date of birth
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with an invalid         message batch reference receives a 400 'Invalid Value' response

The message batch reference must be in a UUID format, for more information on UUID,             look [here](https://en.wikipedia.org/wiki/Universally_unique_identifier)

**Given** the API consumer provides an message body with an invalid message batch reference
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with an invalid         message reference receives a 400 'Invalid Value' response

The message reference must be in a UUID format, for more information on UUID,             look [here](https://en.wikipedia.org/wiki/Universally_unique_identifier)

**Given** the API consumer provides an message body with an invalid message reference
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with an invalid         NHS number receives a 400 'Invalid NHS Number' response

An NHS Number is a 10 digit number used to identify patients, for more             information on the structure of NHS numbers look                 [here](https://www.datadictionary.nhs.uk/attributes/nhs_number.html)

**Given** the API consumer provides an message body with an invalid NHS number
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid nhs number error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid NHS Number’ error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with an invalid        routing plan receives a 400 'Invalid Value' response

The routing plan must be in a UUID format, for more information on UUID,             look [here](https://en.wikipedia.org/wiki/Universally_unique_identifier)

**Given** the API consumer provides an message body with an invalid routing plan
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request with a null         message value receives a 400 'Null Value' response

**Given** the API consumer provides an message body with a null message value
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 null value error
<br/>

**Asserts**
- Response returns a 400 ‘Null Value’ error
- Response returns the expected error message body with references to the null attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |


### Scenario: An API consumer submitting a request without a required attribute         in the request body receives a 400 'Missing Value' response

**Given** the API consumer provides an message body with a missing required attribute
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 missing value error
<br/>

**Asserts**
- Response returns a 400 ‘Missing Value’ error
- Response returns the expected error message body with references to the missing attribute
- Response returns the ‘X-Correlation-Id’ header if provided

**Request Properties**

This test uses a method to replace the values in the response body, it sets the new value, and sets the value of the location of where the attribute has been changed.

Below is a table showing the required attributes and their locations as seen in the response body.

| Attribute             | Location                                        |
|-----------------------|-------------------------------------------------|
| data                  | /data                                           |
| type                  | /data/type                                      |
| attributes            | /data/attributes                                |
| routingPlanId         | /data/attributes/routingPlanId                  |
| messageBatchReference | /data/attributes/messageBatchReference          |
| messages              | /data/attributes/messages                       |
| messageReference      | /data/attributes/messages/0/messageReference    |
| recipient             | /data/attributes/messages/0/recipient           |
| nhsNumber             | /data/attributes/messages/0/recipient/nhsNumber |

**Correlation IDs**

This test uses the ‘X-Correlation-Id’ header, when provided in a request it is returned in the response.

| Value                                | Description                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------|
| None                                 | Is tested to ensure that we do not send back a correlation identifier if one was not provided in the request. |
| 76491414-d0cf-4655-ae20-a4d1368472f3 | Is tested to ensure that when a correlation identifier is sent, we respond with the same value.               |
