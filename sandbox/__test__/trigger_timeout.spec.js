const request = require("supertest");

const { setup } = require('./helpers')

describe('trigger_timeout can simulate a long request', () => {
  let env;

  before(function () {
    env = process.env;
    server = setup()
  });

  beforeEach(function () {
  });

  afterEach(function () {
  });

  after(function () {
      process.env = env;
      server.close();
  });

  it('using a default 3 second delay', (done) => {
    request(server)
        .get('/_timeout')
        .expect(200, done);
  }).timeout(4000);

  it('using a custom delay', (done) => {
      request(server)
          .get('/_timeout?sleep=500')
          .expect(200, done);
  }).timeout(1000);

})
