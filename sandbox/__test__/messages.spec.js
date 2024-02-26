const { expect } = require("chai");
const request = require("supertest");
const assert = require("chai").assert;

const { setup } = require("./helpers");

describe("/api/v1/messages", () => {
  let env;

  before(function () {
    env = process.env;
    server = setup();
  });

  after(function () {
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

  it("responds with a 201 when the request is correctly formatted", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({
        data: {
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

  it("responds with a 201 for a valid global NHS app routing plan", (done) => {
    request(server)
      .post("/api/v1/messages")
      .send({
        data: {
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
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
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
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
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
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
          attributes: {
            routingPlanId: "00000000-0000-0000-0000-000000000001",
            messageReference: "b5bb84b9-a522-41e9-aa8b-ad1b6a454243",
            recipient: {
              nhsNumber: "1",
              dateOfBirth: "1",
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
            personalisation: {},
          },
        },
      })
      .expect(404, {
        message:
          'Routing Config does not exist for clientId "sandbox_client_id" and sendingGroupId "sending-group-id"',
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
            personalisation: {},
          },
        },
      })
      .expect(500, {
        message: "Error writing request items to DynamoDB",
      })
      .expect("Content-Type", /json/, done);
  });
});
