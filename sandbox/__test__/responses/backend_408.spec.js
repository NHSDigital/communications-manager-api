import request from "supertest";
import * as uuid from 'uuid';
import { setup } from '../helpers.js';

describe('backend_408', () => {
  let env;
  let server;

  beforeEach(() => {
    env = process.env;
    server = setup()
  });

  afterEach(() => {
    process.env = env;
    server.close();
  });

  it('can mock a 408 response type', (done) => {
    request(server)
      .get('/_timeout_408')
      .expect(408, '408 Request Timeout', done);
  });

  it("returns a X-Correlation-Id when provided", (done) => {
    const correlationId = uuid.v4();
    request(server)
      .get('/_timeout_408')
      .set('X-Correlation-Id', correlationId)
      .expect(408, '408 Request Timeout')
      .expect("X-Correlation-Id", correlationId, done);
  });
})
