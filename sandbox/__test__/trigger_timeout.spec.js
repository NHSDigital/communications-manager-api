import request from "supertest"
import { setup } from './helpers.js'

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
    request(server)
      .get('/_timeout')
      .expect(200, done);
  }).timeout(4000);

  it('using a custom delay', (done) => {
    request(server)
      .get('/_timeout?sleep=500')
      .expect(200, done);
  }).timeout(1000);

})
