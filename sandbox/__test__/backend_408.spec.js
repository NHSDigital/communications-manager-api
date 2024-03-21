import request from "supertest";
import { setup } from './helpers.js';

describe('backend_408', () => {
  let env;
  let server;

  before(function () {
    env = process.env;
    server = setup()
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
