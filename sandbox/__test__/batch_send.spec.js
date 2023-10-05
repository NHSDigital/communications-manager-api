const request = require("supertest");
const assert = require("chai").assert;

const { setup } = require('./helpers')

describe('/api/v1/send', () => {
  let env;

  before(function () {
    env = process.env;
    server = setup()
  });

  after(function () {
      process.env = env;
      server.close();
  });

  it('returns a service ban (403) when the user is banned', (done) => {
    request(server)
        .post('/api/v1/send')
        .set({ Authorization: 'banned' })
        .expect(403, {
            message: 'Request rejected because client service ban is in effect'
        })
        .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when body doesnt exist', (done) => {
      request(server)
          .post('/api/v1/send')
          .expect(400, {
              message: 'Missing request body'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when the sendingGroupId doesnt exist', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({})
          .expect(400, {
              message: 'Missing sendingGroupId'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when the sendingGroupId is null', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: null
          })
          .expect(400, {
              message: 'Missing sendingGroupId'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when the requestRefId doesnt exist', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'sending-group-id'
          })
          .expect(400, {
              message: 'Missing requestRefId'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when the requestRefId is null', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'sending-group-id',
              requestRefId: null
          })
          .expect(400, {
              message: 'Missing requestRefId'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when the data doesnt exist', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'sending-group-id',
              requestRefId: 'request-ref-id'
          })
          .expect(400, {
              message: 'Missing data array'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when the data is null', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'sending-group-id',
              requestRefId: 'request-ref-id',
              data: null
          })
          .expect(400, {
              message: 'Missing data array'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when the data is not an array', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'sending-group-id',
              requestRefId: 'request-ref-id',
              data: 'invalid'
          })
          .expect(400, {
              message: 'Missing data array'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when the data does not contain items with requestItemRefId', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'sending-group-id',
              requestRefId: 'request-ref-id',
              data: [
                  {
                      notARequestItemRefId : '1'
                  }
              ]
          })
          .expect(400, {
              message: 'Missing requestItemRefIds'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when the data contains duplicate requestItemRefIds', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'sending-group-id',
              requestRefId: 'request-ref-id',
              data: [
                  {
                      requestItemRefId : '1'
                  },
                  {
                      requestItemRefId : '1'
                  }
              ]
          })
          .expect(400, {
              message: 'Duplicate requestItemRefIds'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 404 when sendingGroupId is not found', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'sending-group-id',
              requestRefId: 'request-ref-id',
              data: [
                  {
                      requestItemRefId : '1'
                  },
                  {
                      requestItemRefId : '2'
                  }
              ]
          })
          .expect(404, {
              message: 'Routing Config does not exist for clientId "sandbox_client_id" and sendingGroupId "sending-group-id"'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when routing plan is invalid', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: '4ead415a-c033-4b39-9b05-326ac237a3be',
              requestRefId: 'request-ref-id',
              data: [
                  {
                      requestItemRefId : '1'
                  },
                  {
                      requestItemRefId : '2'
                  }
              ]
          })
          .expect(400, {
              message: 'Invalid Routing Config'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 425 when a repeat request is sent too early', (done) => {
    request(server)
         .post('/api/v1/send')
         .send({
             sendingGroupId: 'd895ade5-0029-4fc3-9fb5-86e1e5370854',
             requestRefId: 'request-ref-id',
             data: [
                 {
                     requestItemRefId : '1'
                 },
                 {
                     requestItemRefId : '2'
                 }
             ]
         })
         .expect(425, {
             message: 'Message with this idempotency key is already being processed'
         })
         .expect("Content-Type", /json/, done);
 });

  it('returns a 500 when the sending group has missing templates', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'c8857ccf-06ec-483f-9b3a-7fc732d9ad48',
              requestRefId: 'request-ref-id',
              data: [
                  {
                      requestItemRefId : '1'
                  },
                  {
                      requestItemRefId : '2'
                  }
              ]
          })
          .expect(500, {
              message: 'Templates required in "c8857ccf-06ec-483f-9b3a-7fc732d9ad48" routing config not found'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 500 when the sending group has duplicate templates', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'a3a4e55d-7a21-45a6-9286-8eb595c872a8',
              requestRefId: 'request-ref-id',
              data: [
                  {
                      requestItemRefId : '1'
                  },
                  {
                      requestItemRefId : '2'
                  }
              ]
          })
          .expect(500, {
              message: 'Duplicate templates in routing config: [{"name":"EMAIL_TEMPLATE","type":"EMAIL"},{"name":"SMS_TEMPLATE","type":"SMS"},{"name":"LETTER_TEMPLATE","type":"LETTER"},{"name":"LETTER_PDF_TEMPLATE","type":"LETTER_PDF"},{"name":"NHSAPP_TEMPLATE","type":"NHSAPP"}]'
          })
          .expect("Content-Type", /json/, done);
  });

  it('returns a 500 when the sending group has missing NHS templates', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'aeb16ab8-cb9c-4d23-92e9-87c78119175c',
              requestRefId: 'request-ref-id',
              data: [
                  {
                      requestItemRefId : '1'
                  },
                  {
                      requestItemRefId : '2'
                  }
              ]
          })
          .expect(500, {
              message: 'NHS App Template does not exist with internalTemplateId: invalid-template'
          })
          .expect("Content-Type", /json/, done);
  });

  it('can simulate a 500 error', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: '3bb82e6a-9873-4683-b2b9-fdf33c9ba86f',
              requestRefId: 'simulate-500',
              data: [
                  {
                      requestItemRefId : '1'
                  },
                  {
                      requestItemRefId : '2'
                  }
              ]
          })
          .expect(500, {
              message: 'Error writing request items to DynamoDB'
          })
          .expect("Content-Type", /json/, done);
  });

  it('responds with a 200 when the request is correctly formatted', (done) => {
    request(server)
          .post('/api/v1/send')
          .send({
              sendingGroupId: 'b838b13c-f98c-4def-93f0-515d4e4f4ee1',
              requestRefId: 'request-id',
              data: [
                  {
                      requestItemRefId : '1'
                  },
                  {
                      requestItemRefId : '2'
                  }
              ]
          })
          .expect(200)
          .expect((res) => {
              assert.notEqual(res.body.requestId, undefined);
              assert.notEqual(res.body.requestId, null);
          })
          .expect("Content-Type", /json/, done);
  });

})
