import request from "supertest"
import { setup } from './helpers.js'
import * as uuid from 'uuid';

describe('trigger_timeout can simulate a long request', () => {
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

  it('using a default 3 second delay', (done) => {
    const correlation_id = uuid.v4();
    request(server)
      .get('/_timeout')
      .set('X-Correlation-Id', correlation_id)
      .expect(200)
      .expect("X-Correlation-Id", correlation_id, done);
  }).timeout(4000);

  it('using a custom delay', (done) => {
    request(server)
      .get('/_timeout?sleep=500')
      .expect(200, done);
  }).timeout(1000);

})
