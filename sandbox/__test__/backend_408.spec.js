import request from "supertest";
import { setup } from './helpers.js';
import * as uuid from 'uuid';

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

  it("returns a X-Correlation-Id when provided", (done) => {
    const correlation_id = uuid.v4();
    request(server)
      .get('/_timeout_408')
      .set('X-Correlation-Id', correlation_id)
      .expect(408, '408 Request Timeout')
      .expect("X-Correlation-Id", correlation_id, done);
  });
})
