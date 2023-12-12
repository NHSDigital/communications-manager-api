const request = require("supertest");
const assert = require("chai").assert;

const { setup } = require('./helpers')

describe('backend_408', () => {
  let env;

  before(function () {
    env = process.env;
    server = setup()
  });

  after(function () {
      process.env = env;
      server.close();
  });

  it('can mock a 408 response type transformed to a 504', (done) => {
    request(server)
        .get('/_timeout_408')
        .expect(504, '504 Gateway Timeout', done);
  });

})
