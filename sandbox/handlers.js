"use strict";

const log = require("loglevel");
const KSUID = require('ksuid')

const write_log = (res, log_level, options = {}) => {
    if (log.getLevel()>log.levels[log_level.toUpperCase()]) {
        return
    }
    if (typeof options === "function") {
        options = options()
    }
    let log_line = {
        timestamp: Date.now(),
        level: log_level,
        correlation_id: res.locals.correlation_id
    }
    if (typeof options === 'object') {
        options = Object.keys(options).reduce(function(obj, x) {
            let val = options[x]
            if (typeof val === "function") {
                val = val()
            }
            obj[x] = val;
            return obj;
        }, {});
        log_line = Object.assign(log_line, options)
    }
    if (Array.isArray(options)) {
        log_line["log"] = {log: options.map(x=> {return typeof x === "function"? x() : x })}
    }

    log[log_level](JSON.stringify(log_line))
};


async function status(req, res, next) {
    res.json({
        status: "pass",
        ping: "pong",
        service: req.app.locals.app_name,
        version: req.app.locals.version_info
    });
    res.end();
    next();
}

function sendError(res, code, message) {
    res.status(code);
    res.json({
        message: message
    });
}

const validSendingGroupIds = {
    "b838b13c-f98c-4def-93f0-515d4e4f4ee1" : 1,
    "49e43b98-70cb-47a9-a55e-fe70c9a6f77c" : 1,
    "b402cd20-b62a-4357-8e02-2952959531c8" : 1,
    "936e9d45-15de-4a95-bb36-ae163c33ae53" : 1,
    "9ba00d23-cd6f-4aca-8688-00abc85a7980" : 1
};

async function batch_send(req, res, next) {
    if (!req.body) {
        sendError(res, 400, 'Missing request body');
        next();
        return;
    }

    if (!req.body.sendingGroupId) {
        sendError(res, 400, 'Missing sendingGroupId');
        next();
        return;
    }

    if (!req.body.requestRefId) {
        sendError(res, 400, 'Missing requestRefId');
        next();
        return;
    }

    if (!Array.isArray(req.body.data)) {
        sendError(res, 400, 'Missing data array');
        next();
        return;
    }

    const requestItemRefIds = req.body.data.map(
        (item) => item.requestItemRefId
    );

    if (requestItemRefIds.includes(undefined)) {
        sendError(res, 400, 'Missing requestItemRefIds');
        next();
        return;
    }

    if (new Set(requestItemRefIds).size !== requestItemRefIds.length) {
        sendError(res, 400, 'Duplicate requestItemRefIds');
        next();
        return;
    }

    if (!validSendingGroupIds[req.body.sendingGroupId]) {
        sendError(res, 404, `Routing Config does not exist for sendingGroupId "${req.body.sendingGroupId}"`);
        next();
        return;
    }

    if (req.body.requestRefId === 'simulate-500') {
        sendError(res, 500, 'Error writing request items to DynamoDB');
        next();
        return;
    }

    write_log(res, "warn", {
        message: "/api/v1/send",
        req: {
            path: req.path,
            query: req.query,
            headers: req.rawHeaders,
            payload: req.body
        }
    });

    res.json({
        requestId: KSUID.randomSync(new Date()).string
    });
    res.end();
    next();
}

module.exports = {
    status: status,
    batch_send: batch_send
};
