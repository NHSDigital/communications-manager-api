import request from "supertest"
import { setup } from './helpers.js'
import * as uuid from 'uuid';

describe('backend_504', () => {
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

  it('can mock a 504 response type', (done) => {
    request(server)
      .get('/_timeout_504')
      .expect(504, '504 Gateway Timeout', done);
  });

  it("returns a X-Correlation-Id when provided", (done) => {
    const correlation_id = uuid.v4();
    request(server)
      .get('/_timeout_504')
      .set('X-Correlation-Id', correlation_id)
      .expect(504, '504 Gateway Timeout')
      .expect("X-Correlation-Id", correlation_id, done);
  });
})
