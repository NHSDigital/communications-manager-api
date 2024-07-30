import express from "express";
import log from "loglevel";
import * as handlers from "./handlers/index.js";

const app = express();
app.disable("x-powered-by");

function setup(options = {}) {
    app.locals.app_name = options.APP_NAME || 'communications-manager';
    app.locals.version_info = JSON.parse(options.VERSION_INFO || '{}');
    log.setLevel(options.LOG_LEVEL || "info");


    log.info(JSON.stringify({
        timestamp: Date.now(),
        level: "info",
        app: app.locals.app_name,
        msg: "setup",
        version: app.locals.version_info
    }));
}

function start(options = {}) {
    const server = app.listen(options.PORT || 9000, () => {
        log.info(JSON.stringify({
            timestamp: Date.now(),
            level: "info",
            app: app.locals.app_name,
            msg: "startup",
            server_port: server.address().port,
            version: app.locals.version_info
        }))
    });
    return server;
}

function beforeRequest(req, res, next) {
    res.locals.started_at = Date.now();
    res.locals.correlation_id = (
        req.header('X-Correlation-ID')
        || req.header('Correlation-ID')
        || req.header('CorrelationID')
        || undefined
    );
    if (res.locals.correlation_id) {
        res.setHeader('X-Correlation-Id', res.locals.correlation_id);
    }
    next();
}

const _healthEndpoints = ["/_ping", "/health"];

function afterRequest(req, res, next) {
    if (_healthEndpoints.includes(req.path) && !('log' in { ...req.query })) {
        // don't log ping / health by default
        return next();
    }
    const finishedAt = Date.now();
    const logEntry = {
        timestamp: finishedAt,
        level: "info",
        app: app.locals.app_name,
        msg: "request",
        correlation_id: res.locals.correlation_id,
        started: res.locals.started_at,
        finished: finishedAt,
        duration: finishedAt - res.locals.started_at,
        req: {
            url: req.url,
            method: req.method,
            query: req.query,
            path: req.path,
        },
        res: {
            status: res.statusCode,
            message: res.message
        },
        version: app.locals.version_info
    };

    if (log.getLevel() < 2) {
        // debug
        logEntry.req.headers = req.rawHeaders;
        logEntry.res.headers = res.rawHeaders;
    }
    log.info(JSON.stringify(logEntry));
    
    next();
    return undefined;
}

function onError(err, req, res, next) {
    let logErr = err;
    if (logErr instanceof Error) {
        logErr = {
            name: err.name,
            message: err.message,
            stack: err.stack
        }
    }
    const finishedAt = Date.now();
    log.error(JSON.stringify({
        timestamp: finishedAt,
        level: "error",
        app: app.locals.app_name,
        msg: "error",
        correlation_id: res.locals.correlation_id,
        started: res.locals.started_at,
        finished: finishedAt,
        duration: finishedAt - res.locals.started_at,
        err: logErr,
        version: app.locals.version_info
    }));
    if (res.headersSent) {
        next();
        return;
    }
    res.status(500);
    res.json({ error: "something went wrong" });
    next();
}

app.use(beforeRequest);
app.use(express.json({ limit: '10mb' }));
app.get("/_ping", handlers.status);
app.get("/_status", handlers.status);
app.get("/health", handlers.status);
app.post("/api/v1/send", handlers.batchSend);
app.post("/api/v1/messages", handlers.messages);
app.get("/api/v1/messages/:messageId", handlers.getMessage);
app.get("/api/channels/nhsapp/accounts", handlers.nhsappAccounts);
app.get("/_timeout", handlers.triggerTimeout);
app.get("/_invalid_certificate", handlers.backend403);
app.get("/_timeout_408", handlers.backend408);
app.get("/_timeout_504", handlers.backend504);
app.use(onError)
app.use(afterRequest);

export { start, setup };
