

const get_message_response_data = [
  // Enrichment failures
  // ======================================================
  {
    messageId: "2WL4QcKGjNHvHFQeKgYbapZJGHK",
    body: {
      "data": {
        "type": "Message",
        "id": "2WL4QcKGjNHvHFQeKgYbapZJGHK",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "4fbc5f73-0f7c-4304-b848-5c6ccb781c84",
          "messageStatus": "failed",
          "messageStatusDescription": "Patient does not exist in PDS",
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:31:59Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4QcKGjNHvHFQeKgYbapZJGHK"
        }
      }
    }
  },
  {
    messageId: "2WL4cPfBRuPKa44JxhyXYf2kr1E",
    body: {
      "data": {
        "type": "Message",
        "id": "2WL4cPfBRuPKa44JxhyXYf2kr1E",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "d85be1f0-1593-41b0-94d2-beae6ee7dcc0",
          "messageStatus": "failed",
          "messageStatusDescription": "Patient record invalidated",
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:31:59Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4cPfBRuPKa44JxhyXYf2kr1E"
        }
      }
    }
  },
  {
    messageId: "2WL4g2f7GQ2F9HZmgonIFiXAPku", body: {
      "data": {
        "type": "Message",
        "id": "2WL4g2f7GQ2F9HZmgonIFiXAPku",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "b801d925-70aa-49d6-a045-28cec9893de3",
          "messageStatus": "failed",
          "messageStatusDescription": "PDS response date of birth does not match given date of birth",
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:31:59Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:31:59Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4g2f7GQ2F9HZmgonIFiXAPku"
        }
      }
    }
  },
  {
    messageId: "2WL4ibGoigirgbH4yQwqbPaJXyQ", body: {
      "data": {
        "type": "Message",
        "id": "2WL4ibGoigirgbH4yQwqbPaJXyQ",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "2f2e071c-9fba-4dde-bf8d-8dd0c8060300",
          "messageStatus": "failed",
          "messageStatusDescription": "Patient is formally dead",
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:31:59Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:31:59Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4ibGoigirgbH4yQwqbPaJXyQ"
        }
      }
    }
  },
  {
    messageId: "2WL4khXn32dOOj4bB4bi8Tkllrq", body: {
      "data": {
        "type": "Message",
        "id": "2WL4khXn32dOOj4bB4bi8Tkllrq",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "68cc8e05-c404-405a-a41d-92cdb8afd9e3",
          "messageStatus": "failed",
          "messageStatusDescription": "Patient is informally dead",
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:31:59Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:31:59Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4khXn32dOOj4bB4bi8Tkllrq"
        }
      }
    }
  },
  {
    messageId: "2WL4mvx6eBva8dcIK60VEGIfcgZ", body: {
      "data": {
        "type": "Message",
        "id": "2WL4mvx6eBva8dcIK60VEGIfcgZ",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "1791d23b-6f5d-4153-ab45-637bd7711d41",
          "messageStatus": "failed",
          "messageStatusDescription": "Patient has exit code",
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:31:59Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:31:59Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4mvx6eBva8dcIK60VEGIfcgZ"
        }
      }
    }
  },
  {
    messageId: "2WL4pcpmKxYYblm3PSKVEqcmEPX", body: {
      "data": {
        "type": "Message",
        "id": "2WL4pcpmKxYYblm3PSKVEqcmEPX",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "2c98d875-3843-4919-9c79-2034e957e251",
          "messageStatus": "failed",
          "messageStatusDescription": "Name response is invalid: Contact detail is malformed",
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:31:59Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:31:59Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4pcpmKxYYblm3PSKVEqcmEPX"
        }
      }
    }
  },
  // NHS app only
  // ==============================================================

  {
    messageId: "2WL4vHFZzInmaYwq6HRNDqTX8dH", body: {
      "data": {
        "type": "Message",
        "id": "2WL4vHFZzInmaYwq6HRNDqTX8dH",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "d1cc6082-729e-4e31-8842-ac3279d3f72d",
          "messageStatus": "failed",
          "messageStatusDescription": "Contact detail is missing",
          "channels": [
            {
              "type": "nhsapp",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "Contact detail is missing",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:31:59Z",
                "failed": "2023-10-09T10:31:59Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:31:59Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:31:59Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4vHFZzInmaYwq6HRNDqTX8dH"
        }
      }
    }
  },
  {
    messageId: "2WL3qFTEFM0qMY8xjRbt1LIKCzM", body: {
      "data": {
        "type": "Message",
        "id": "2WL3qFTEFM0qMY8xjRbt1LIKCzM",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "7a94bc7c-5d55-4816-bea0-8449eb81d65f",
          "messageStatus": "delivered",
          "channels": [
            {
              "type": "nhsapp",
              "retryCount": 0,
              "channelStatus": "delivered",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "delivered": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "delivered": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL3qFTEFM0qMY8xjRbt1LIKCzM"
        }
      }
    }
  },

  {
    messageId: "2WL44QP7vrKxKKBZdTtUQoB2bWl", body: {
      "data": {
        "type": "Message",
        "id": "2WL44QP7vrKxKKBZdTtUQoB2bWl",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "6495d48e-919a-4350-aa43-0f209731d118",
          "messageStatus": "sending",
          "channels": [
            {
              "type": "nhsapp",
              "retryCount": 0,
              "channelStatus": "sending",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:31:59Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "enriched": "2023-10-09T10:31:59Z",
            "updated": "2023-10-09T10:31:59Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL44QP7vrKxKKBZdTtUQoB2bWl"
        }
      }
    }
  },

  {
    messageId: "2WL45YuHOLATvC3GspEu0oSioux", body: {
      "data": {
        "type": "Message",
        "id": "2WL4vHFZzInmaYwq6HRNDqTX8dH",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "d1cc6082-729e-4e31-8842-ac3279d3f72d",
          "messageStatus": "failed",
          "messageStatusDescription": "NHS number not found",
          "channels": [
            {
              "type": "nhsapp",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "NHS number not found",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4vHFZzInmaYwq6HRNDqTX8dH"
        }
      }
    }
  },

  // Email only
  // ================================================================

  {
    messageId: "2WL4xcWKvz4F32g0htBEl8DINzn", body: {
      "data": {
        "type": "Message",
        "id": "2WL4xcWKvz4F32g0htBEl8DINzn",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "0b88296d-b7e3-4697-be86-7424444a205c",
          "messageStatus": "failed",
          "messageStatusDescription": "Contact detail is missing",
          "channels": [
            {
              "type": "email",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "Contact detail is missing",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4xcWKvz4F32g0htBEl8DINzn"
        }
      }
    }
  },
  {
    messageId: "2WL3wwFhpZ6blJNIoh747bDEFNv", body: {
      "data": {
        "type": "Message",
        "id": "2WL3wwFhpZ6blJNIoh747bDEFNv",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "7cf26e8d-9a12-44c3-8186-d9c2f2e03631",
          "messageStatus": "delivered",
          "channels": [
            {
              "type": "email",
              "retryCount": 0,
              "channelStatus": "delivered",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "delivered": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "delivered": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL3wwFhpZ6blJNIoh747bDEFNv"
        }
      }
    }
  },
  {
    messageId: "2WL4GEeFVxXG9S57nRlefBwwKxp", body: {
      "data": {
        "type": "Message",
        "id": "2WL4GEeFVxXG9S57nRlefBwwKxp",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "500710db-9e51-4fcf-830b-166fca7fb18f",
          "messageStatus": "sending",
          "channels": [
            {
              "type": "email",
              "retryCount": 0,
              "channelStatus": "sending",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "enriched": "2023-10-09T10:31:59Z",
            "updated": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4GEeFVxXG9S57nRlefBwwKxp"
        }
      }
    }
  },
  {
    messageId: "2WL4W9RgbuLLByXdR77H8vjKSDd", body: {
      "data": {
        "type": "Message",
        "id": "2WL4W9RgbuLLByXdR77H8vjKSDd",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "0397b134-e30d-4fb1-9060-0d204b0ac340",
          "messageStatus": "failed",
          "messageStatusDescription": "The provider could not deliver the message. This can happen when the recipient’s inbox is full or their anti-spam filter rejects your email. Check your content does not look like spam before you try to send the message again.",
          "channels": [
            {
              "type": "email",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "The provider could not deliver the message. This can happen when the recipient’s inbox is full or their anti-spam filter rejects your email. Check your content does not look like spam before you try to send the message again.",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4GEeFVxXG9S57nRlefBwwKxp"
        }
      }
    }
  },


  // SMS only
  // ==========================================================================

  {
    messageId: "2WL50w41YaZXcyFCNT346LY8rlz", body: {
      "data": {
        "type": "Message",
        "id": "2WL50w41YaZXcyFCNT346LY8rlz",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "7b2be2cf-7e59-4b15-b199-fd4ba0cb9f19",
          "messageStatus": "failed",
          "messageStatusDescription": "Contact detail is missing",
          "channels": [
            {
              "type": "sms",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "Contact detail is missing",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL50w41YaZXcyFCNT346LY8rlz"
        }
      }
    }
  },
  {
    messageId: "2WL3ydEEk37IzREoWRhuAdolFCE", body: {
      "data": {
        "type": "Message",
        "id": "2WL3ydEEk37IzREoWRhuAdolFCE",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "ef2d84fa-5dc0-4de5-959e-30f2e2e6f4b5",
          "messageStatus": "delivered",
          "channels": [
            {
              "type": "sms",
              "retryCount": 0,
              "channelStatus": "delivered",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "delivered": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "delivered": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL3ydEEk37IzREoWRhuAdolFCE"
        }
      }
    }
  },
  {
    messageId: "2WL4JXrfauCaQnSFbAujoImSKwo", body: {
      "data": {
        "type": "Message",
        "id": "2WL4JXrfauCaQnSFbAujoImSKwo",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "9de1821a-058d-499b-ab8e-5c127278284e",
          "messageStatus": "sending",
          "channels": [
            {
              "type": "sms",
              "retryCount": 0,
              "channelStatus": "sending",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "enriched": "2023-10-09T10:31:59Z",
            "updated": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4JXrfauCaQnSFbAujoImSKwo"
        }
      }
    }
  },
  {
    messageId: "2WL4JtCiOe7l2TT4szwPjNJah3z", body: {
      "data": {
        "type": "Message",
        "id": "2WL4JtCiOe7l2TT4szwPjNJah3z",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "e21cd9c0-75af-4596-9e9a-57fa7581fe59",
          "messageStatus": "failed",
          "messageStatusDescription": "The provider could not deliver the message. This can happen when the recipient’s phone is off, has no signal, or their text message inbox is full. You can try to send the message again. You’ll still be charged for text messages to phones that are not accepting messages.",
          "channels": [
            {
              "type": "sms",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "The provider could not deliver the message. This can happen when the recipient’s phone is off, has no signal, or their text message inbox is full. You can try to send the message again. You’ll still be charged for text messages to phones that are not accepting messages.",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4JtCiOe7l2TT4szwPjNJah3z"
        }
      }
    }
  },

  // Letter only
  // ==========================================================================

  {
    messageId: "2WL54x0XQjCbWeE5lN0DKQZcokU", body: {
      "data": {
        "type": "Message",
        "id": "2WL54x0XQjCbWeE5lN0DKQZcokU",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "1226417c-f683-4d68-afe8-2d52321a6b70",
          "messageStatus": "failed",
          "messageStatusDescription": "Contact detail is missing",
          "channels": [
            {
              "type": "letter",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "Contact detail is missing",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL54x0XQjCbWeE5lN0DKQZcokU"
        }
      }
    }
  },
  {
    messageId: "2WL3zxCY9e5vm2VP1ZfYMb53WPF", body: {
      "data": {
        "type": "Message",
        "id": "2WL3zxCY9e5vm2VP1ZfYMb53WPF",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "78c55f88-c2fd-42cc-aa0f-5f1273babd66",
          "messageStatus": "delivered",
          "channels": [
            {
              "type": "letter",
              "retryCount": 0,
              "channelStatus": "delivered",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "delivered": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "delivered": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL3zxCY9e5vm2VP1ZfYMb53WPF"
        }
      }
    }
  },
  {
    messageId: "2WL4LuyNMtoGAsJQIpTxZLl8e3e", body: {
      "data": {
        "type": "Message",
        "id": "2WL4LuyNMtoGAsJQIpTxZLl8e3e",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "25642d81-a76b-45da-b633-0d192ba15638",
          "messageStatus": "sending",
          "channels": [
            {
              "type": "letter",
              "retryCount": 0,
              "channelStatus": "sending",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "enriched": "2023-10-09T10:31:59Z",
            "updated": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4LuyNMtoGAsJQIpTxZLl8e3e"
        }
      }
    }
  },
  {
    messageId: "2WL4MOuSeCTODDAScFG7KIq9a5r", body: {
      "data": {
        "type": "Message",
        "id": "2WL4MOuSeCTODDAScFG7KIq9a5r",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "b9603694-5542-4043-b905-1e570b26d4c2",
          "messageStatus": "failed",
          "messageStatusDescription": "We had an unexpected error while sending the letter to our printing provider.",
          "channels": [
            {
              "type": "letter",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "We had an unexpected error while sending the letter to our printing provider.",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "failed": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL4MOuSeCTODDAScFG7KIq9a5r"
        }
      }
    }
  },

  // Multi-channel
  // ==========================================================================

  {
    messageId: "2WL5TWl7F7PondWbZ1vctlEtOZ3", body: {
      "data": {
        "type": "Message",
        "id": "2WL5TWl7F7PondWbZ1vctlEtOZ3",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "d0612714-59e2-4377-86f4-6d0c114ab83d",
          "messageStatus": "delivered",
          "channels": [
            {
              "type": "nhsapp",
              "retryCount": 0,
              "channelStatus": "delivered",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "delivered": "2023-10-09T10:52:12Z"
              }
            },
            {
              "type": "email",
              "retryCount": 0,
              "channelStatus": "created",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z"
              }
            },
            {
              "type": "sms",
              "retryCount": 0,
              "channelStatus": "created",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z"
              }
            },
            {
              "type": "letter",
              "retryCount": 0,
              "channelStatus": "created",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:39:37Z",
            "delivered": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL5TWl7F7PondWbZ1vctlEtOZ3"
        }
      }
    }
  },
  {
    messageId: "2WL5eDefrbW31uw1il84WdF8ndH", body: {
      "data": {
        "type": "Message",
        "id": "2WL5eDefrbW31uw1il84WdF8ndH",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "adcbc45a-a867-4798-8c61-7c02d132e1e6",
          "messageStatus": "delivered",
          "channels": [
            {
              "type": "nhsapp",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "NHS number not found",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            },
            {
              "type": "email",
              "retryCount": 0,
              "channelStatus": "delivered",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T11:25:23Z",
                "delivered": "2023-10-09T11:25:23Z"
              }
            },
            {
              "type": "sms",
              "retryCount": 0,
              "channelStatus": "created",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z"
              }
            },
            {
              "type": "letter",
              "retryCount": 0,
              "channelStatus": "created",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T11:25:23Z",
            "enriched": "2023-10-09T10:39:37Z",
            "delivered": "2023-10-09T11:25:23Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL5eDefrbW31uw1il84WdF8ndH"
        }
      }
    }
  },
  {
    messageId: "2WL5eYSWGzCHlGmzNxuqVusPxDg", body: {
      "data": {
        "type": "Message",
        "id": "2WL5eYSWGzCHlGmzNxuqVusPxDg",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "ac8e4b6c-b0bc-480f-976c-a601fda36351",
          "messageStatus": "delivered",
          "channels": [
            {
              "type": "nhsapp",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "NHS number not found",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            },
            {
              "type": "email",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "The provider could not deliver the message. This can happen when the recipient’s inbox is full or their anti-spam filter rejects your email. Check your content does not look like spam before you try to send the message again.",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T11:25:23Z",
                "failed": "2023-10-09T11:25:23Z"
              }
            },
            {
              "type": "sms",
              "retryCount": 0,
              "channelStatus": "delivered",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T11:48:52Z",
                "delivered": "2023-10-09T11:48:52Z"
              }
            },
            {
              "type": "letter",
              "retryCount": 0,
              "channelStatus": "created",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T11:48:52Z",
            "enriched": "2023-10-09T10:39:37Z",
            "delivered": "2023-10-09T11:48:52Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL5eYSWGzCHlGmzNxuqVusPxDg"
        }
      }
    }
  },
  {
    messageId: "2WL5f8j4XVxUPgd3OOqXVYvVFIW", body: {
      "data": {
        "type": "Message",
        "id": "2WL5f8j4XVxUPgd3OOqXVYvVFIW",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "eb9a3342-afb2-4977-9536-65fab370376c",
          "messageStatus": "delivered",
          "channels": [
            {
              "type": "nhsapp",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "NHS number not found",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "failed": "2023-10-09T10:52:12Z"
              }
            },
            {
              "type": "email",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "The provider could not deliver the message. This can happen when the recipient’s inbox is full or their anti-spam filter rejects your email. Check your content does not look like spam before you try to send the message again.",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T11:25:23Z",
                "failed": "2023-10-09T11:25:23Z"
              }
            },
            {
              "type": "sms",
              "retryCount": 0,
              "channelStatus": "failed",
              "channelStatusDescription": "The provider could not deliver the message. This can happen when the recipient’s phone is off, has no signal, or their text message inbox is full. You can try to send the message again. You’ll still be charged for text messages to phones that are not accepting messages.",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T11:48:52Z",
                "failed": "2023-10-09T11:48:52Z"
              }
            },
            {
              "type": "letter",
              "retryCount": 0,
              "channelStatus": "delivered",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-12T08:23:41Z",
                "delivered": "2023-10-12T08:23:41Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-12T08:23:41Z",
            "enriched": "2023-10-09T10:39:37Z",
            "delivered": "2023-10-12T08:23:41Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL5f8j4XVxUPgd3OOqXVYvVFIW"
        }
      }
    }
  },

  // Batched messages
  // ==========================================================================

  {
    messageId: "2WL5qbEa7TzSWZXU2IAOCCrLXVL", body: {
      "data": {
        "type": "Message",
        "id": "2WL5qbEa7TzSWZXU2IAOCCrLXVL",
        "attributes": {
          "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          "messageReference": "dcaf64cc-2afa-42ff-9797-1b9a948e0d10",
          "messageStatus": "delivered",
          "channels": [
            {
              "type": "nhsapp",
              "retryCount": 0,
              "channelStatus": "delivered",
              "timestamps": {
                "created": "2023-10-09T10:31:59Z",
                "updated": "2023-10-09T10:52:12Z",
                "delivered": "2023-10-09T10:52:12Z"
              }
            }
          ],
          "timestamps": {
            "created": "2023-10-09T10:31:37Z",
            "updated": "2023-10-09T10:52:12Z",
            "enriched": "2023-10-09T10:31:59Z",
            "delivered": "2023-10-09T10:52:12Z"
          },
          "pdsMeta": {
            "queriedAt": "2023-10-09T10:31:59Z",
            "versionId": "23"
          }
        },
        "links": {
          "self": "%PATH_ROOT%/2WL5qbEa7TzSWZXU2IAOCCrLXVL"
        },
        "relationships": {
          "messageBatch": {
            "data": {
              "type": "MessageBatch",
              "id": "2WWq0oqcx5pdoNnh8hJuYLonZMy"
            }
          }
        }
      }
    }
  }]



module.exports = {
  get_message_response_data
}
