import log from "loglevel"

export const writeLog = (res, logLevel, options = {}) => {
  if (log.getLevel() > log.levels[logLevel.toUpperCase()]) {
    return
  }
  let processedOptions;
  if (typeof options === "function") {
    processedOptions = options()
  } else {
    processedOptions = options
  }
  let logLine = {
    timestamp: Date.now(),
    level: logLevel,
    correlation_id: res.locals.correlation_id
  }
  if (typeof options === "object") {
    processedOptions = Object.keys(processedOptions).reduce((obj, x) => {
      const val = processedOptions[x];
      const returnedObj = obj;
      if (typeof val === "function") {
        returnedObj[x] = val()
      } else {
        returnedObj[x] = val
      }

      return returnedObj
    }, {});
    logLine = Object.assign(logLine, processedOptions)
  }
  if (Array.isArray(processedOptions)) {
    logLine.log = { log: processedOptions.map(x => typeof x === "function" ? x() : x ) }
  }

  log[logLevel](JSON.stringify(logLine))
};

export function sendError(res, code, message) {
  res.status(code);
  res.json({
    message
  });
}

export function hasValidGlobalTemplatePersonalisation(personalisation) {
  if (!personalisation) {
    return false;
  }

  const personalisationFields = Object.keys(personalisation);
  if (personalisationFields.length !== 1) {
    return false;
  }

  if (personalisationFields[0] !== "body") {
    return false;
  }
  return true;
}
