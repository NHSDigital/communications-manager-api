import request from "supertest"
import * as uuid from 'uuid';
import { setup } from './helpers.js'

describe('triggerTimeout can simulate a long request', () => {
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

  it('using a default 3 second delay', (done) => {
    const correlationId = uuid.v4();
    request(server)
      .get('/_timeout')
      .set('X-Correlation-Id', correlationId)
      .expect(200)
      .expect("X-Correlation-Id", correlationId, done);
  }).timeout(4000);

  it('using a custom delay', (done) => {
    request(server)
      .get('/_timeout?sleep=500')
      .expect(200, done);
  }).timeout(1000);

})
