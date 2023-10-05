const request = require("supertest");

const { setup } = require('./helpers')

describe('backend_504', () => {
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

  it('can mock a 504 response type', (done) => {
    request(server)
        .get('/_timeout_504')
        .expect(504, '504 Gateway Timeout', done);
  });

})
