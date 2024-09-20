import request from "supertest"
import { assert } from "chai";
import * as uuid from 'uuid';
import { setup } from './helpers.js'


describe("/api/v1/send", () => {
  let env;
  let server;

  beforeEach(() => {
    env = process.env;
    server = setup();
  });

  afterEach(() => {
    process.env = env;
    server.close();
  });

  it("returns a service ban (403) when the user is banned", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "banned" })
      .expect(403, {
        message: "Request rejected because client service ban is in effect",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when body doesnt exist", (done) => {
    request(server)
      .post("/api/v1/send")
      .expect(400, {
        message: "Missing request body",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when body data doesnt exist", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({})
      .expect(400, {
        message: "Missing request body data",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when type is missing", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({ data: {} })
      .expect(400, {
        message: "Missing request body data type",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when type isnt MessageBatch", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({ data: { type: "Message" } })
      .expect(400, {
        message: "Request body data type is not MessageBatch",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when attributes dont exist", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({ data: { type: "MessageBatch" } })
      .expect(400, {
        message: "Missing request body data attributes",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when the routingPlanId doesnt exist", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({ data: { type: "MessageBatch", attributes: {} } })
      .expect(400, {
        message: "Missing routingPlanId",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when the routingPlanId is null", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: null,
          },
        },
      })
      .expect(400, {
        message: "Missing routingPlanId",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when the messageBatchReference doesnt exist", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "sending-group-id",
          },
        },
      })
      .expect(400, {
        message: "Missing messageBatchReference",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when the messageBatchReference is null", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "sending-group-id",
            messageBatchReference: null,
          },
        },
      })
      .expect(400, {
        message: "Missing messageBatchReference",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when messages doesnt exist", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "sending-group-id",
            messageBatchReference: "request-ref-id",
          },
        },
      })
      .expect(400, {
        message: "Missing messages array",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when messages is null", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "sending-group-id",
            messageBatchReference: "request-ref-id",
            messages: null,
          },
        },
      })
      .expect(400, {
        message: "Missing messages array",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when messages is not an array", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "sending-group-id",
            messageBatchReference: "request-ref-id",
            messages: "invalid",
          },
        },
      })
      .expect(400, {
        message: "Missing messages array",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when the data does not contain items with messageReference", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "sending-group-id",
            messageBatchReference: "request-ref-id",
            messages: [
              {
                notAMessageReference: "1",
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Missing messageReferences",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when the data contains duplicate messageReferences", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "sending-group-id",
            messageBatchReference: "request-ref-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "1",
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Duplicate messageReferences",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 404 when routingPlanId is not found", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "sending-group-id",
            messageBatchReference: "request-ref-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
              },
            ],
          },
        },
      })
      .expect(404, {
        message:
          'Routing Config does not exist for clientId "sandbox_client_id" and routingPlanId "sending-group-id"',
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when routing plan is invalid", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "4ead415a-c033-4b39-9b05-326ac237a3be",
            messageBatchReference: "request-ref-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid Routing Config",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 425 when a repeat request is sent too early", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "d895ade5-0029-4fc3-9fb5-86e1e5370854",
            messageBatchReference: "request-ref-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
              },
            ],
          },
        },
      })
      .expect(425, {
        message: "Message with this idempotency key is already being processed",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 500 when the sending group has missing templates", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "c8857ccf-06ec-483f-9b3a-7fc732d9ad48",
            messageBatchReference: "request-ref-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
              },
            ],
          },
        },
      })
      .expect(500, {
        message:
          'Templates required in "c8857ccf-06ec-483f-9b3a-7fc732d9ad48" routing config not found',
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 500 when the sending group has duplicate templates", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "a3a4e55d-7a21-45a6-9286-8eb595c872a8",
            messageBatchReference: "request-ref-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
              },
            ],
          },
        },
      })
      .expect(500, {
        message:
          'Duplicate templates in routing config: [{"name":"EMAIL_TEMPLATE","type":"EMAIL"},{"name":"SMS_TEMPLATE","type":"SMS"},{"name":"LETTER_TEMPLATE","type":"LETTER"},{"name":"LETTER_PDF_TEMPLATE","type":"LETTER_PDF"},{"name":"NHSAPP_TEMPLATE","type":"NHSAPP"}]',
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 500 when the sending group has missing NHS templates", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "aeb16ab8-cb9c-4d23-92e9-87c78119175c",
            messageBatchReference: "request-ref-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
              },
            ],
          },
        },
      })
      .expect(500, {
        message:
          "NHS App Template does not exist with internalTemplateId: invalid-template",
      })
      .expect("Content-Type", /json/, done);
  });

  it("can simulate a 500 error", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "3bb82e6a-9873-4683-b2b9-fdf33c9ba86f",
            messageBatchReference: "simulate-500",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
              },
            ],
          },
        },
      })
      .expect(500, {
        message: "Error writing request items to DynamoDB",
      })
      .expect("Content-Type", /json/, done);
  });

  it("responds with a 200 when the request is correctly formatted", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
              },
            ],
          },
        },
      })
      .expect(200)
      .expect((res) => {
        assert.notEqual(res.body.requestId, undefined);
        assert.notEqual(res.body.requestId, null);
        assert.notEqual(res.body.routingPlan.id, undefined);
        assert.notEqual(res.body.routingPlan.id, null);
        assert.notEqual(res.body.routingPlan.version, undefined);
        assert.notEqual(res.body.routingPlan.version, null);
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a X-Correlation-Id when provided", (done) => {
    const correlationId = uuid.v4();
    request(server)
      .post("/api/v1/send")
      .set('X-Correlation-Id', correlationId)
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                },
                personalisation: {
                  body: "Free text message 1",
                },
              },
              {
                messageReference: "2",
                recipient: {
                  nhsNumber: "2",
                  dateOfBirth: "2",
                },
                personalisation: {
                  body: "Free text message 2",
                },
              },
            ],
          },
        },
      })
      .expect(200)
      .expect("X-Correlation-Id", correlationId, done);
  });

  it("responds with a 200 for a valid global NHS app routing plan", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                },
                personalisation: {
                  body: "Free text message 1",
                },
              },
              {
                messageReference: "2",
                recipient: {
                  nhsNumber: "2",
                  dateOfBirth: "2",
                },
                personalisation: {
                  body: "Free text message 2",
                },
              },
            ],
          },
        },
      })
      .expect(200)
      .expect((res) => {
        assert.notEqual(res.body.requestId, undefined);
        assert.notEqual(res.body.requestId, null);
        assert.notEqual(res.body.routingPlan.id, undefined);
        assert.notEqual(res.body.routingPlan.id, null);
        assert.notEqual(res.body.routingPlan.version, undefined);
        assert.notEqual(res.body.routingPlan.version, null);
      })
      .expect("Content-Type", /json/, done);
  });

  it("responds with a 400 for missing personalisation for global NHS app routing plan", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                },
              },
              {
                messageReference: "2",
                recipient: {
                  nhsNumber: "2",
                  dateOfBirth: "2",
                },
                personalisation: {
                  body: "Free text message 2",
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Expect single personalisation field of 'body'",
      })
      .expect("Content-Type", /json/, done);
  });

  it("responds with a 400 for missing body for global NHS app routing plan", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                },
                personalisation: {
                  body: "Free text message 1",
                },
              },
              {
                messageReference: "2",
                recipient: {
                  nhsNumber: "2",
                  dateOfBirth: "2",
                },
                personalisation: {
                  unknownField: "Free text message 2",
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Expect single personalisation field of 'body'",
      })
      .expect("Content-Type", /json/, done);
  });

  it("responds with a 400 for redundant personalisation for global NHS app routing plan", (done) => {
    request(server)
      .post("/api/v1/send")
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                },
                personalisation: {
                  body: "Free text message 1",
                },
              },
              {
                messageReference: "2",
                recipient: {
                  nhsNumber: "2",
                  dateOfBirth: "2",
                },
                personalisation: {
                  body: "Free text message 2",
                  unknownField: "Unknown field",
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Expect single personalisation field of 'body'",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when a message has no odsCode and the client has no default", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "noDefaultOds" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
                originator: {
                  odsCode: "X26"
                }
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "odsCode must be provided",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when a message has an odsCode but the client does not allow it", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "noOdsChange" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
              },
              {
                messageReference: "2",
                originator: {
                  odsCode: "X26"
                }
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "odsCode was provided but ODS code override is not enabled for the client",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 200 when email alternate contact detail is provided and client is allowed to use feature", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "MessageBatch",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
              messages: [
                {
                  messageReference: "1",
                  recipient: {
                    nhsNumber: "1",
                    dateOfBirth: "1",
                    contactDetails: {
                      email: 'hello'
                    },
                  },
                },
              ],
            },
          },
        }
      )
      .expect(200)
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when contactDetails provided but client is not permitted to use feature", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "notAllowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "MessageBatch",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
              messages: [
                {
                  messageReference: "1",
                  recipient: {
                    nhsNumber: "1",
                    dateOfBirth: "1",
                    contactDetails: {
                      sms: 'hello'
                    },
                  },
                },
              ],
            },
          },
        }
      )
      .expect(400, {
        message: "Client is not allowed to provide alternative contact details",
        errors: [
          {
            code: "CM_CANNOT_SET_CONTACT_DETAILS",
            title: 'Cannot set contact details',
            field: `/data/attributes/messages/0/recipient/contactDetails`,
            message:
              'Client is not allowed to provide alternative contact details.',
          },
        ],
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 200 when sms alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "MessageBatch",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
              messages: [
                {
                  messageReference: "1",
                  recipient: {
                    nhsNumber: "1",
                    dateOfBirth: "1",
                    contactDetails: {
                      sms: 'hello'
                    },
                  },
                },
              ],
            },
          },
        })
      .expect(200)
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid sms alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "MessageBatch",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
              messages: [
                {
                  messageReference: "1",
                  recipient: {
                    nhsNumber: "1",
                    dateOfBirth: "1",
                    contactDetails: {
                      sms: '07700900002'
                    },
                  },
                },
              ],
            },
          },
        })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'sms': Input failed format check",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/sms",
            message: "Input failed format check",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid value for sms alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "MessageBatch",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
              messages: [
                {
                  messageReference: "1",
                  recipient: {
                    nhsNumber: "1",
                    dateOfBirth: "1",
                    contactDetails: {
                      sms: {
                        hello: 1
                      }
                    },
                  },
                },
              ],
            },
          },
        })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'sms': Invalid",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/sms",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 200 when sms alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "MessageBatch",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
              messages: [
                {
                  messageReference: "1",
                  recipient: {
                    nhsNumber: "1",
                    dateOfBirth: "1",
                    contactDetails: {
                      email: 'hello'
                    },
                  },
                },
              ],
            },
          },
        })
      .expect(200)
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid email alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "MessageBatch",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
              messages: [
                {
                  messageReference: "1",
                  recipient: {
                    nhsNumber: "1",
                    dateOfBirth: "1",
                    contactDetails: {
                      email: 'invalidEmailAddress'
                    },
                  },
                },
              ],
            },
          },
        })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'email': Input failed format check",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/email",
            message: "Input failed format check",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid value for email alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    email: {
                      hello: 1
                    }
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'email': Invalid",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/email",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 200 when address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "MessageBatch",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
              messages: [
                {
                  messageReference: "1",
                  recipient: {
                    nhsNumber: "1",
                    dateOfBirth: "1",
                    contactDetails: {
                      address: {
                        lines: ['1', '2'],
                        postcode: 'hello'
                      }
                    },
                  },
                },
              ],
            },
          },
        })
      .expect(200)
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when string for address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    address: 'hello'
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'address': Invalid",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/address",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when array for address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    address: []
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'address': Invalid",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/address",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid value for lines in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    address: {
                      lines: 'test',
                      postcode: 'test'
                    }
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'lines': 'lines' is missing",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/address",
            message: "`lines` is missing",
            title: "Missing value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when too few lines is provided in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    address: {
                      lines: ['1'],
                      postcode: 'hello'
                    }
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'lines': Too few address lines were provided",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/address",
            message: "Too few address lines were provided",
            title: "Missing value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when too many lines is provided in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    address: {
                      lines: ['1', '2', '3', '4', '5', '6'],
                      postcode: 'hello'
                    }
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'lines': Invalid",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/address",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when lines contains non-string value in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    address: {
                      lines: ['1', '2', 3, '4', '5'],
                      postcode: 'hello'
                    }
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'lines': Invalid",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/address",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when no postcode is provided in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    address: {
                      lines: ['1', '2'],
                    }
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'postcode': 'postcode' is missing",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/address",
            message: "`postcode` is missing",
            title: "Missing value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid value is provided for postcode in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    address: {
                      lines: ['1', '2'],
                      postcode: []
                    }
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'postcode': Invalid",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/address/postcode",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });
  it('returns a 400 and multiple errors when there are multiple issues in contact details provided', (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: "MessageBatch",
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageBatchReference: "request-id",
            messages: [
              {
                messageReference: "1",
                recipient: {
                  nhsNumber: "1",
                  dateOfBirth: "1",
                  contactDetails: {
                    address: {
                      lines: ['1'],
                      postcode: []
                    },
                    email: 'invalidEmailAddress'
                  },
                },
              },
            ],
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'email': Input failed format check. Field 'lines': Too few address lines were provided",
        errors: [
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/email",
            message: "Input failed format check",
            title: "Invalid value"
          },
          {
            field: "/data/attributes/messages/0/recipient/contactDetails/address",
            message: "Too few address lines were provided",
            title: "Missing value"
          },
        ]
      })
      .expect("Content-Type", /json/, done);
  })

  it("returns a 200 when all alternate contact details are provided", (done) => {
    request(server)
      .post("/api/v1/send")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "MessageBatch",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
              messages: [
                {
                  messageReference: "1",
                  recipient: {
                    nhsNumber: "1",
                    dateOfBirth: "1",
                    contactDetails: {
                      email: 'hello',
                      sms: 'hello',
                      address: {
                        lines: ['1', '2'],
                        postcode: 'hello'
                      }
                    },
                  },
                },
              ],
            },
          },
        })
      .expect(200)
      .expect("Content-Type", /json/, done);
  });
});
