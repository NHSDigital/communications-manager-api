const request = require("supertest");
const assert = require("chai").assert;

const { setup } = require('./helpers')

describe('/api/v1/messages', () => {
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
        .post('/api/v1/messages')
        .set({ Authorization: 'banned' })
        .expect(403, {
            message: 'Request rejected because client service ban is in effect'
        })
        .expect("Content-Type", /json/, done);
  });

  it('returns a 400 when body doesnt exist', (done) => {
      request(server)
          .post('/api/v1/messages')
          .expect(400, {
              message: 'Missing request body'
          })
          .expect("Content-Type", /json/, done);
  });

  it('responds with a 201 when the request is correctly formatted', (done) => {
    request(server)
          .post('/api/v1/messages')
          .send({
              data: {
                attributes: {
                  routingPlanId: 'b838b13c-f98c-4def-93f0-515d4e4f4ee1',
                  messageReference: 'b5bb84b9-a522-41e9-aa8b-ad1b6a454243',
                  recipient: {
                    nhsNumber: '1',
                    dateOfBirth: '1',
                  },
                  personalisation: {}
                }
              }
          })
          .expect(201)
          .expect((res) => {
            const { id, attributes, links } = res.body.data
            assert.notEqual(id, undefined);
            assert.equal(attributes.routingPlanId, 'b838b13c-f98c-4def-93f0-515d4e4f4ee1');
            assert.equal(attributes.messageReference, 'b5bb84b9-a522-41e9-aa8b-ad1b6a454243');
            assert.equal(attributes.messageStatus, 'created');
            assert.notEqual(attributes.timestamps.created, undefined);
            assert.notEqual(links.self, undefined);
          })
          .expect("Content-Type", /json/, done);
  });

})
