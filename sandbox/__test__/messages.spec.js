import request from "supertest"
import { assert } from "chai";
import * as uuid from 'uuid';
import { setup } from './helpers.js'

describe("/api/v1/messages", () => {
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
      .post("/api/v1/messages")
      .set({ Authorization: "banned" })
      .expect(403, {
        message: "Request rejected because client service ban is in effect",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when body doesnt exist", (done) => {
    request(server)
      .post("/api/v1/messages")
      .expect(400, {
        message: "Missing request body",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when body data doesnt exist", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({})
      .expect(400, {
        message: "Missing request body data",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when type is missing", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({ data: {} })
      .expect(400, {
        message: "Missing request body data type",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when type isnt Message", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({ data: { type: "MessageBatch" } })
      .expect(400, {
        message: "Request body data type is not Message",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when attributes dont exist", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({ data: { type: "Message" } })
      .expect(400, {
        message: "Missing request body data attributes",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when the routingPlanId doesnt exist", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({ data: { type: "Message", attributes: {} } })
      .expect(400, {
        message: "Missing routingPlanId",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when the routingPlanId is null", (done) => { 
    request(server)
    .post("/api/v1/messages")
    .send({
      data: {
        type: "Message",
        attributes: {
          routingPlanId: null,
        },
      },
    })
    .expect(400, {
      message: "Missing routingPlanId",
    })
    .expect("Content-Type", /json/, done);
  })

  it("responds with a 201 when the request is correctly formatted", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
            },
            originator: {
              odsCode: "X123"
            },
            personalisation: {},
          },
        },
      })
      .expect(201)
      .expect((res) => {
        const { id, attributes, links } = res.body.data;
        assert.notEqual(id, undefined);
        assert.equal(
          attributes.routingPlan.id,
          "b838b13c-f98c-4def-93f0-515d4e4f4ee1"
        );
        assert.notEqual(attributes.routingPlan.version, undefined);
        assert.equal(
          attributes.messageReference,
          "b5bb84b9-a522-41e9-aa8b-ad1b6a454243"
        );
        assert.equal(attributes.messageStatus, "created");
        assert.notEqual(attributes.timestamps.created, undefined);
        assert.notEqual(links.self, undefined);
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a X-Correlation-Id when provided", (done) => {
    const correlationId = uuid.v4();
    request(server)
      .post("/api/v1/messages")
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
            },
            originator: {
              odsCode: "X123"
            },
            personalisation: {},
          },
        },
      })
      .set('X-Correlation-Id', correlationId)
      .expect(201)
      .expect("X-Correlation-Id", correlationId, done);
  });

  it("responds with a 201 for a valid global NHS app routing plan", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
            },
            originator: {
              odsCode: "X123"
            },
            personalisation: {
              body: "Free text message",
            },
          },
        },
      })
      .expect(201)
      .expect((res) => {
        const { id, attributes, links } = res.body.data;
        assert.notEqual(id, undefined);
        assert.equal(
          attributes.routingPlan.id,
          "00000000-0000-0000-0000-000000000001"
        );
        assert.notEqual(attributes.routingPlan.version, undefined);
        assert.equal(
          attributes.messageReference,
          "b5bb84b9-a522-41e9-aa8b-ad1b6a454243"
        );
        assert.equal(attributes.messageStatus, "created");
        assert.notEqual(attributes.timestamps.created, undefined);
        assert.notEqual(links.self, undefined);
      })
      .expect("Content-Type", /json/, done);
  });

  it("responds with a 400 for missing personalisation for global NHS app routing plan", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
            },
            originator: {
              odsCode: "X123"
            },
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
      .post("/api/v1/messages")
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
            },
            originator: {
              odsCode: "X123"
            },
          },
          personalisation: {
            unknownField: "Free text message",
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
      .post("/api/v1/messages")
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
            },
            originator: {
              odsCode: "X123"
            },
          },
          personalisation: {
            body: "Free text message",
            unknownField: "Free text message",
          },
        },
      })
      .expect(400, {
        message: "Expect single personalisation field of 'body'",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 404 when the sending group is not found or not accessible to the client", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({
        data: {
          type: "Message",
          attributes: {
            routingPlanId: "sending-group-id",
            messageReference: "request-ref-id",
            recipient: {
              nhsNumber: "999999999",
              dateOfBirth: "2000-01-01",
            },
            originator: {
              odsCode: "X123"
            },
            personalisation: {},
          },
        },
      })
      .expect(404, {
        message:
          'Routing Config does not exist for clientId "sandbox_client_id" and routingPlanId "sending-group-id"',
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 500 when the sending group has missing templates", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({
        data: {
          type: "Message",
          attributes: {
            routingPlanId: "c8857ccf-06ec-483f-9b3a-7fc732d9ad48",
            messageReference: "request-ref-id",
            recipient: {
              nhsNumber: "999999999",
              dateOfBirth: "2000-01-01",
            },
            originator: {
              odsCode: "X123"
            },
            personalisation: {},
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
      .post("/api/v1/messages")
      .send({
        data: {
          type: "Message",
          attributes: {
            routingPlanId: "a3a4e55d-7a21-45a6-9286-8eb595c872a8",
            messageReference: "request-ref-id",
            recipient: {
              nhsNumber: "999999999",
              dateOfBirth: "2000-01-01",
            },
            originator: {
              odsCode: "X123"
            },
            personalisation: {},
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
      .post("/api/v1/messages")
      .send({
        data: {
          type: "Message",
          attributes: {
            routingPlanId: "aeb16ab8-cb9c-4d23-92e9-87c78119175c",
            messageReference: "request-ref-id",
            recipient: {
              nhsNumber: "999999999",
              dateOfBirth: "2000-01-01",
            },
            originator: {
              odsCode: "X123"
            },
            personalisation: {},
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
      .post("/api/v1/messages")
      .send({
        data: {
          type: "Message",
          attributes: {
            routingPlanId: "3bb82e6a-9873-4683-b2b9-fdf33c9ba86f",
            messageReference: "request-ref-id",
            recipient: {
              nhsNumber: "999999999",
              dateOfBirth: "2000-01-01",
            },
            originator: {
              odsCode: "X123"
            },
            personalisation: {},
          },
        },
      })
      .expect(500, {
        message: "Error writing request items to DynamoDB",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when there is no odsCode and the client has no default", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "noDefaultOds" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "odsCode must be provided",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when odsCode provided but the client does not allow it", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "noOdsChange" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
            },
            originator: {
              odsCode: "X123"
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "odsCode was provided but ODS code override is not enabled for the client",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 201 when email alternate contact detail is provided and client is allowed to use feature", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                email: 'hello'
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(201)
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when contactDetails provided but client is not permitted to use feature", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "notAllowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                sms: 'hello'
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Client is not allowed to provide alternative contact details",
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 201 when sms alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                sms: 'hello'
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(201)
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid sms alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                sms: '07700900002'
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'sms': Input failed format check",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/sms",
            message: "Input failed format check",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid value for sms alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                sms: {
                  hello: 1
                }
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'sms': Invalid",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/sms",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 201 when valid value for email alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                email: 'hello'
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(201)
      .expect("Content-Type", /json/, done);
  })

  it("returns a 400 when invalid email alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                email: 'invalidEmailAddress'
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'email': Input failed format check",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/email",
            message: "Input failed format check",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid value for email alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                email: {
                  hello: 1
                }
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'email': Invalid",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/email",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 201 when valid value for address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
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
            personalisation: {},
          },
        },
      })
      .expect(201)
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when string for address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                address: 'hello'
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'address': Invalid",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/address",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when array for address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                address: []
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'address': Invalid",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/address",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid value for lines in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
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
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'lines': 'lines' is missing",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/address",
            message: "`lines` is missing",
            title: "Missing value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when too few lines is provided in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
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
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'lines': Too few address lines were provided",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/address",
            message: "Too few address lines were provided",
            title: "Too few items"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when too many lines is provided in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
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
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'lines': Invalid",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/address",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when lines contains non-string value in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
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
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'lines': Invalid",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/address",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when no postcode is provided in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
              contactDetails: {
                address: {
                  lines: ['1', '2'],
                }
              },
            },
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'postcode': 'postcode' is missing",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/address",
            message: "`postcode` is missing",
            title: "Missing value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });

  it("returns a 400 when invalid value is provided for postcode in address alternate contact detail is provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
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
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'postcode': Invalid",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/address/postcode",
            message: "Invalid",
            title: "Invalid value"
          }
        ]
      })
      .expect("Content-Type", /json/, done);
  });
  it('returns a 400 and multiple errors when there are multiple issues in contact details provided', (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send({
        data: {
          type: 'Message',
          attributes: {
            routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
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
            personalisation: {},
          },
        },
      })
      .expect(400, {
        message: "Invalid recipient contact details. Field 'email': Input failed format check. Field 'lines': Too few address lines were provided",
        errors: [
          {
            field: "/data/attributes/recipient/contactDetails/email",
            message: "Input failed format check",
            title: "Invalid value"
          },
          {
            field: "/data/attributes/recipient/contactDetails/address",
            message: "Too few address lines were provided",
            title: "Too few items"
          },
        ]
      })
      .expect("Content-Type", /json/, done);
  })

  it("returns a 201 when all alternate contact details are provided", (done) => {
    request(server)
      .post("/api/v1/messages")
      .set({ Authorization: "allowedContactDetailOverride" })
      .send(
        {
          data: {
            type: "Message",
            attributes: {
              routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
              messageBatchReference: "request-id",
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
                }
              },
            },
          },
        })
      .expect(201)
      .expect("Content-Type", /json/, done);
  });
})