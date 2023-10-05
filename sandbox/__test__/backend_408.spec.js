const request = require("supertest");
const assert = require("chai").assert;

const { setup } = require('./helpers')

describe('backend_408', () => {
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

  it('can mock a 408 response type', (done) => {
    request(server)
        .get('/_timeout_408')
        .expect(408, '408 Request Timeout', done);
  });

})
