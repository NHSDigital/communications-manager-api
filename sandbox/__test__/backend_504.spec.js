import request from "supertest"
import { setup } from './helpers.js'

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

})
