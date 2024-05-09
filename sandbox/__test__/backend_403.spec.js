import request from "supertest";
import { setup } from './helpers.js';

describe('backend_403', () => {
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

  it('can mock a 403 response type for invalid certificates', (done) => {
    request(server)
      .get('/_invalid_certificate')
      .expect(403, '{"message":"Forbidden"}', done);
  });
})
