# Validation Tests


## Scenario: An API consumer submitting a message with an invalid required attribute in the request body receives a 400 ‘Invalid Value’ response

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

| Attribute        | Location                             |
|------------------|--------------------------------------|
| data             | /data                                |
| type             | /data/type                           |
| attributes       | /data/attributes                     |
| routingPlanId    | /data/attributes/routingPlanId       |
| messageReference | /data/attributes/messageReference    |
| recipient        | /data/attributes/recipient           |
| nhsNumber        | /data/attributes/recipient/nhsNumber |


## Scenario: An API consumer submitting a message with an empty required attribute in the request body receives a 400 ‘Null Value’ response

**Given** the API consumer provides an message body with a null attribute
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 null value error
<br/>

**Asserts**
- Response returns a 400 ‘Null Value’ error
- Response returns the expected error message body with references to the null attribute

**Request Properties**

This test uses a method to replace the values in the response body, it sets the new value, and sets the value of the location of where the attribute has been changed.

Below is a table showing the required attributes and their locations as seen in the response body.

| Attribute        | Location                             |
|------------------|--------------------------------------|
| data             | /data                                |
| type             | /data/type                           |
| attributes       | /data/attributes                     |
| routingPlanId    | /data/attributes/routingPlanId       |
| messageReference | /data/attributes/messageReference    |
| recipient        | /data/attributes/recipient           |
| nhsNumber        | /data/attributes/recipient/nhsNumber |


## Scenario: An API consumer submitting a request with invalid address lines (too many) receives a 400 ‘Invalid Value’ response

A valid contact detail must be structured in this format: { address: { lines: [ Value1, Value2 ], postcode: value } }

**Given** the API consumer provides an message body with with too many address lines
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid value’ error
- Response returns the expected error message body with references to the invalid attribute

| Value                            | Description                                               |
|----------------------------------|-----------------------------------------------------------|
| [ “1”, “2”, “3”, “4”, “5”, “6” ] | Used to ensure list of more than 5 values is not accepted |


## Scenario: An API consumer submitting a request without a request body receives a 400 ‘Invalid Value’ response

**Given** the API consumer provides an empty message body
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body


## Scenario: An API consumer submitting a request with an invalid email receives a 400 ‘Invalid Value’ response

A valid contact detail must be structured in this format: { email: Value }

**Given** the API consumer provides an message body with an invalid email address
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute

| Value               | Description                                          |
|---------------------|------------------------------------------------------|
| invalidEmailAddress | Used to ensure invalid email address is not accepted |


## Scenario: An API consumer submitting a request with an invalid message reference receives a 400 ‘Invalid Value’ response

The message reference must be in a UUID format, for more information on UUID, look [here](https://en.wikipedia.org/wiki/Universally_unique_identifier)

**Given** the API consumer provides an message body with an invalid message reference
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute


## Scenario: An API consumer submitting a request with an invalid NHS number receives a 400 ‘Invalid NHS Number’ response

An NHS Number is a 10 digit number used to identify patients, for more information on the structure of NHS numbers look [here](https://www.datadictionary.nhs.uk/attributes/nhs_number.html)

**Given** the API consumer provides an message body with an invalid NHS number
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid nhs number error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid NHS Number’ error
- Response returns the expected error message body with references to the invalid attribute


## Scenario: An API consumer submitting a request with an invalid personalisation receives a 400 ‘Invalid value’ response

A valid personalisation must be structured in this format: { parameter: value }

**Given** the API consumer provides a message body with an invalid personalisation
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid value’ error
- Response returns the expected error message body with references to the invalid attribute

| Value                    | Description                                                               |
|--------------------------|---------------------------------------------------------------------------|
| None                     | Are tested to ensure that null personalisation values are not accepted    |
| 5, “”, “some-string”, [] | Are tested to ensure that invalid personalisation values are not accepted |


## Scenario: An API consumer submitting a request with an invalid routing plan receives a 400 ‘Invalid Value’ response

The routing plan must be in a UUID format, for more information on UUID, look [here](https://en.wikipedia.org/wiki/Universally_unique_identifier)

**Given** the API consumer provides an message body with an invalid routing plan
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute


## Scenario: An API consumer submitting a request with an invalid sms receives a 400 ‘Invalid Value’ response

A valid sms contact detail must be structured in this format: { sms: value }

**Given** the API consumer provides an message body with an invalid sms
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid Value’ error
- Response returns the expected error message body with references to the invalid attribute

|        Value | Description                                         |
|--------------|-----------------------------------------------------|
| 077009000021 | Used to ensure invalid phone number is not accepted |


## Scenario: An API consumer submitting a request with an contact details when not allowed receives a 400 ‘Cannot set contact details’ response

**Given** the API consumer provides a message body with contact details
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 Cannot set contact details error
<br/>

**Asserts**
- Response returns a 400 ‘Cannot set contact details’ error
- Response returns the expected error message body with references to the invalid attribute


## Scenario: An API consumer submitting a request with an invalid personalisation receives a 400 ‘Invalid value’ response

A valid personalisation must be structured in this format: { parameter: value }

**Given** the API consumer provides a message body with an invalid personalisation
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 invalid value error
<br/>

**Asserts**
- Response returns a 400 ‘Invalid value’ error
- Response returns the expected error message body with references to the invalid attribute

| Value                    | Description                                                               |
|--------------------------|---------------------------------------------------------------------------|
| None                     | Are tested to ensure that null personalisation values are not accepted    |
| 5, “”, “some-string”, [] | Are tested to ensure that invalid personalisation values are not accepted |


## Scenario: An API consumer submitting a message without a required attribute in the request body receives a 400 ‘Missing Value’ response

**Given** the API consumer provides an message body with a missing required attribute
<br/>
**When** the request is submitted
<br/>
**Then** the response returns a 400 missing value error
<br/>

**Asserts**
- Response returns a 400 ‘Missing Value’ error
- Response returns the expected error message body with references to the missing attribute

**Request Properties**

This test uses a method to replace the values in the response body, it sets the new value, and sets the value of the location of where the attribute has been changed.

Below is a table showing the required attributes and their locations as seen in the response body.

| Attribute        | Location                             |
|------------------|--------------------------------------|
| data             | /data                                |
| type             | /data/type                           |
| attributes       | /data/attributes                     |
| routingPlanId    | /data/attributes/routingPlanId       |
| messageReference | /data/attributes/messageReference    |
| recipient        | /data/attributes/recipient           |
| nhsNumber        | /data/attributes/recipient/nhsNumber |
