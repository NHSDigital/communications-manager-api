import * as app from "../app.js"

export function setup() {
    const versionInfo = {
        build_label: "1233-shaacdef1",
        releaseId: "1234",
        commitId: "acdef12341ccc"
    };

    app.setup({
        VERSION_INFO: JSON.stringify(versionInfo),
        LOG_LEVEL: (process.env.NODE_ENV === "test" ? "warn" : "debug")
    });
    const server = app.start();
    return server;
}
