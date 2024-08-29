import request from "supertest"
import * as uuid from 'uuid';
import { setup } from '../helpers.js'

describe('backend_504', () => {
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

  it('can mock a 504 response type', (done) => {
    request(server)
      .get('/_timeout_504')
      .expect(504, '504 Gateway Timeout', done);
  });

  it("returns a X-Correlation-Id when provided", (done) => {
    const correlationId = uuid.v4();
    request(server)
      .get('/_timeout_504')
      .set('X-Correlation-Id', correlationId)
      .expect(504, '504 Gateway Timeout')
      .expect("X-Correlation-Id", correlationId, done);
  });
})
