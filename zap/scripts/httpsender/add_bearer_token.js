const HttpSender = Java.type('org.parosproxy.paros.network.HttpSender');
const ScriptVars = Java.type('org.zaproxy.zap.extension.script.ScriptVars');

function sendingRequest(msg, initiator, helper) {
  if (initiator !== HttpSender.AUTHENTICATION_INITIATOR && msg.isInScope()) {
    const token = ScriptVars.getGlobalVar("bearer-token");

    if (token) {
        msg.getRequestHeader().setHeader("Authorization", "Bearer " + token);
    }
  }
}

function responseReceived(msg, initiator, helper) {
    //nothing
}