var UUID = Java.type("java.util.UUID");
var Base64 = Java.type("java.util.Base64");
var HttpRequestHeader = Java.type("org.parosproxy.paros.network.HttpRequestHeader");
var HttpHeader = Java.type("org.parosproxy.paros.network.HttpHeader");
var URI = Java.type("org.apache.commons.httpclient.URI");
var StandardCharsets = Java.type("java.nio.charset.StandardCharsets");
var PKCS8EncodedKeySpec = Java.type("java.security.spec.PKCS8EncodedKeySpec");
var KeyFactory = Java.type("java.security.KeyFactory");
var ScriptVars = Java.type('org.zaproxy.zap.extension.script.ScriptVars');
var Signature = Java.type("java.security.Signature");

function authenticate(helper, paramsValues, credentials) {
    var existing_token = ScriptVars.getGlobalVar("bearer-token");

    if (existing_token) {
        print("get_bearer_token.js: Returning existing token...");
        return;
    }

    var token_endpoint = paramsValues.get("url");
    var api_key = credentials.getParam("api_key");

    var api_private_key = Base64.getDecoder().decode(
        credentials.getParam("private_key").replace(/[ \-\n]/g, "").replace("BEGINPRIVATEKEY", "").replace("ENDPRIVATEKEY", "")
    );
    var spec = new PKCS8EncodedKeySpec(api_private_key);
    var rsaFact = KeyFactory.getInstance("RSA");
    var private_key = rsaFact.generatePrivate(spec);

    var encoder = Base64.getUrlEncoder().withoutPadding();

    //build the token
    var headers = encoder.encodeToString(
        JSON.stringify({
            typ: "JWT",
            alg: "RS512",
            kid: "local"
        }).getBytes()
    );
    var token = encoder.encodeToString(
        JSON.stringify({
            sub: api_key,
            iss: api_key,
            jti: UUID.randomUUID().toString(),
            aud: token_endpoint,
            exp: Math.floor(Date.now() / 1000) + 180
        }).getBytes()
    );

    var signer = Signature.getInstance("SHA512withRSA");
    signer.initSign(private_key);
    signer.update([headers, token].join(".").getBytes(StandardCharsets.UTF_8));

    var signature = encoder.encodeToString(signer.sign());
    var jwt = headers + "." + token + "." + signature;

    var tokenRequestBody = "grant_type=client_credentials";
    tokenRequestBody+= "&client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer";
    tokenRequestBody+= "&client_assertion=" + jwt;

    var tokenRequestMainHeader = new HttpRequestHeader(
        HttpRequestHeader.POST, 
        new URI(token_endpoint, false), 
        HttpHeader.HTTP11
    );

    var tokenMsg = helper.prepareMessage();
    tokenMsg.setRequestBody(tokenRequestBody);
    tokenMsg.setRequestHeader(tokenRequestMainHeader);
    tokenMsg.getRequestHeader().setContentLength(tokenMsg.getRequestBody().length());
    helper.sendAndReceive(tokenMsg, false);

    var body = tokenMsg.getResponseBody().toString();
    var json = JSON.parse(body);

    var access_token = json['access_token'];
    
    if (access_token){
        print("get_bearer_token.js: Successfully fetched token!");
        ScriptVars.setGlobalVar("bearer-token", access_token);
    }else{
        print("get_bearer_token.js: Error getting access token");
    }
    
    return tokenMsg;
}

function getRequiredParamsNames(){
    return ["url"];
}

function getOptionalParamsNames(){
    return [];
}

function getCredentialsParamsNames(){
    return ["api_key", "private_key"];
}