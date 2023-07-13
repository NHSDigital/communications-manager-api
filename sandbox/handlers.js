"use strict";

const log = require("loglevel");
const KSUID = require("ksuid")

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
    if (typeof options === "object") {
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
    "9ba00d23-cd6f-4aca-8688-00abc85a7980" : 1,
    "c8857ccf-06ec-483f-9b3a-7fc732d9ad48" : 1,
    "a3a4e55d-7a21-45a6-9286-8eb595c872a8" : 1
};
const sendingGroupIdWithMissingTemplates = "c8857ccf-06ec-483f-9b3a-7fc732d9ad48";
const sendingGroupIdWithDuplicateTemplates = "a3a4e55d-7a21-45a6-9286-8eb595c872a8";
const duplicateTemplates = [
    {
        name: "EMAIL_TEMPLATE",
        type: "EMAIL"
    },
    {
        name: "SMS_TEMPLATE",
        type: "SMS"
    },
    {
        name: "LETTER_TEMPLATE",
        type: "LETTER"
    },
    {
        name: "LETTER_PDF_TEMPLATE",
        type: "LETTER_PDF"
    },
    {
        name: "NHSAPP_TEMPLATE",
        type: "NHSAPP"
    }
];

async function batch_send(req, res, next) {
    if (!req.body) {
        sendError(res, 400, "Missing request body");
        next();
        return;
    }

    if (!req.body.sendingGroupId) {
        sendError(res, 400, "Missing sendingGroupId");
        next();
        return;
    }

    if (!req.body.requestRefId) {
        sendError(res, 400, "Missing requestRefId");
        next();
        return;
    }

    if (!Array.isArray(req.body.data)) {
        sendError(res, 400, "Missing data array");
        next();
        return;
    }

    const requestItemRefIds = req.body.data.map(
        (item) => item.requestItemRefId
    );

    if (requestItemRefIds.includes(undefined)) {
        sendError(res, 400, "Missing requestItemRefIds");
        next();
        return;
    }

    if (new Set(requestItemRefIds).size !== requestItemRefIds.length) {
        sendError(res, 400, "Duplicate requestItemRefIds");
        next();
        return;
    }

    if (!validSendingGroupIds[req.body.sendingGroupId]) {
        sendError(res, 404, `Routing Config does not exist for clientId "sandbox_client_id" and sendingGroupId "${req.body.sendingGroupId}"`);
        next();
        return;
    }

    if (req.body.sendingGroupId === sendingGroupIdWithMissingTemplates) {
        sendError(res, 400, `Templates required in "${req.body.sendingGroupId}" routing config not found`);
        next();
        return;
    }

    if (req.body.sendingGroupId === sendingGroupIdWithDuplicateTemplates) {
        sendError(res, 400, `Duplicate templates found: ${JSON.stringify(duplicateTemplates)}`);
        next();
        return;
    }

    if (req.body.requestRefId === "simulate-500") {
        sendError(res, 500, "Error writing request items to DynamoDB");
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

async function trigger_timeout(req, res, next) {
    let timeoutLength = 3000;

    if (req.query.sleep) {
        timeoutLength = parseInt(req.query.sleep);
    }

    setTimeout(() => {
        res.status(200);
        res.json({});
        next();
    }, timeoutLength);
}

async function backend_408(req, res, next) {
    res.status(408);
    res.send("408 Request Timeout");
    next();
}

async function backend_504(req, res, next) {
    res.status(504);
    res.send("504 Gateway Timeout");
    next();
}

module.exports = {
    status: status,
    batch_send: batch_send,
    trigger_timeout: trigger_timeout,
    backend_408: backend_408,
    backend_504: backend_504
};
