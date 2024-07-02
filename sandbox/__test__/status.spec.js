import request from "supertest"
import { setup } from './helpers.js'
import * as uuid from 'uuid';

describe('status', () => {
  let env;
  let server;

  const version_info = {
    build_label: "1233-shaacdef1",
    releaseId: "1234",
    commitId: "acdef12341ccc"
  };

  before(function () {
    env = process.env;
    server = setup()
  });

  after(function () {
    process.env = env;
    server.close();
  });

  it("responds to /_ping", (done) => {
    const correlation_id = uuid.v4();
    request(server)
      .get("/_ping")
      .set('X-Correlation-Id', correlation_id)
      .expect(200, {
        status: "pass",
        ping: "pong",
        service: "communications-manager",
        version: version_info
      })
      .expect("X-Correlation-Id", correlation_id)
      .expect("Content-Type", /json/, done)
  });

  it("responds to /_status", (done) => {
    const correlation_id = uuid.v4();
    request(server)
      .get("/_status")
      .set('X-Correlation-Id', correlation_id)
      .expect(200, {
        status: "pass",
        ping: "pong",
        service: "communications-manager",
        version: version_info
      })
      .expect("X-Correlation-Id", correlation_id)
      .expect("Content-Type", /json/, done);
  });

  it("responds to /health", (done) => {
    const correlation_id = uuid.v4();
    request(server)
      .get("/health")
      .set('X-Correlation-Id', correlation_id)
      .expect(200, {
        status: "pass",
        ping: "pong",
        service: "communications-manager",
        version: version_info
      })
      .expect("X-Correlation-Id", correlation_id)
      .expect("Content-Type", /json/, done);
  });
})
