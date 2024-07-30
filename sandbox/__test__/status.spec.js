import request from "supertest"
import * as uuid from 'uuid';
import { setup } from './helpers.js'

describe('status', () => {
  let env;
  let server;

  const versionInfo = {
    build_label: "1233-shaacdef1",
    releaseId: "1234",
    commitId: "acdef12341ccc"
  };

  beforeEach(() => {
    env = process.env;
    server = setup()
  });

  afterEach(() => {
    process.env = env;
    server.close();
  });

  it("responds to /_ping", (done) => {
    const correlationId = uuid.v4();
    request(server)
      .get("/_ping")
      .set('X-Correlation-Id', correlationId)
      .expect(200, {
        status: "pass",
        ping: "pong",
        service: "communications-manager",
        version: versionInfo
      })
      .expect("X-Correlation-Id", correlationId)
      .expect("Content-Type", /json/, done)
  });

  it("responds to /_status", (done) => {
    const correlationId = uuid.v4();
    request(server)
      .get("/_status")
      .set('X-Correlation-Id', correlationId)
      .expect(200, {
        status: "pass",
        ping: "pong",
        service: "communications-manager",
        version: versionInfo
      })
      .expect("X-Correlation-Id", correlationId)
      .expect("Content-Type", /json/, done);
  });

  it("responds to /health", (done) => {
    const correlationId = uuid.v4();
    request(server)
      .get("/health")
      .set('X-Correlation-Id', correlationId)
      .expect(200, {
        status: "pass",
        ping: "pong",
        service: "communications-manager",
        version: versionInfo
      })
      .expect("X-Correlation-Id", correlationId)
      .expect("Content-Type", /json/, done);
  });
})
