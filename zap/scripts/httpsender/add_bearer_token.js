var HttpSender = Java.type('org.parosproxy.paros.network.HttpSender');
var ScriptVars = Java.type('org.zaproxy.zap.extension.script.ScriptVars');

function sendingRequest(msg, initiator, helper) {
  if (initiator !== HttpSender.AUTHENTICATION_INITIATOR && msg.isInScope()) {
    var token = ScriptVars.getGlobalVar("bearer-token");

    if (token) {
        print("add_bearer_token.js: Adding token to headers...");
        msg.getRequestHeader().setHeader("Authorization", "Bearer " + token);
    }
  }
}

function responseReceived(msg, initiator, helper) {
    //nothing
}