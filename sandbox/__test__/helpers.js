function setup() {
    let app = require("../app");

    let server;
    const version_info = {
        build_label:"1233-shaacdef1",
        releaseId:"1234",
        commitId:"acdef12341ccc"
    };

    app.setup({
        VERSION_INFO: JSON.stringify(version_info),
        LOG_LEVEL: (process.env.NODE_ENV === "test" ? "warn": "debug")
    });
    server = app.start();
    return server;
}

module.exports = {
  setup
}
