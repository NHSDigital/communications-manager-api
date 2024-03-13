import request from "supertest"
import { setup } from './helpers.js'

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
    request(server)
      .get("/_ping")
      .expect(200, {
        status: "pass",
        ping: "pong",
        service: "communications-manager",
        version: version_info
      })
      .expect("Content-Type", /json/, done)
  });

  it("responds to /_status", (done) => {
    request(server)
      .get("/_status")
      .expect(200, {
        status: "pass",
        ping: "pong",
        service: "communications-manager",
        version: version_info
      })
      .expect("Content-Type", /json/, done);
  });

  it("responds to /health", (done) => {
    request(server)
      .get("/health")
      .expect(200, {
        status: "pass",
        ping: "pong",
        service: "communications-manager",
        version: version_info
      })
      .expect("Content-Type", /json/, done);
  });
})
