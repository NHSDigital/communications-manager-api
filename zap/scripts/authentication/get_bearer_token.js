const UUID = Java.type("java.util.UUID");
const Base64 = Java.type("java.util.Base64");
const HttpRequestHeader = Java.type("org.parosproxy.paros.network.HttpRequestHeader");
const HttpHeader = Java.type("org.parosproxy.paros.network.HttpHeader");
const URI = Java.type("org.apache.commons.httpclient.URI");
const StandardCharsets = Java.type("java.nio.charset.StandardCharsets");
const PKCS8EncodedKeySpec = Java.type("java.security.spec.PKCS8EncodedKeySpec");
const KeyFactory = Java.type("java.security.KeyFactory");
const ScriptVars = Java.type('org.zaproxy.zap.extension.script.ScriptVars');
const Signature = Java.type("java.security.Signature");

function authenticate(helper, paramsValues, credentials) {
    const existing_token = ScriptVars.getGlobalVar("bearer-token");

    if (existing_token) {
        return;
    }

    const token_endpoint = paramsValues.get("url");
    const api_key = credentials.getParam("api_key");
    const kid = credentials.getParam("kid");

    const api_private_key = Base64.getDecoder().decode(
        credentials.getParam("private_key").replace(/[ \-\n]/g, "").replace("BEGINPRIVATEKEY", "").replace("ENDPRIVATEKEY", "").replace("BEGINRSAPRIVATEKEY", "").replace("ENDRSAPRIVATEKEY", "")
    );
    const spec = new PKCS8EncodedKeySpec(api_private_key);
    const rsaFact = KeyFactory.getInstance("RSA");
    const private_key = rsaFact.generatePrivate(spec);

    const encoder = Base64.getUrlEncoder().withoutPadding();

    // build the token
    const headers = encoder.encodeToString(
        JSON.stringify({
            typ: "JWT",
            alg: "RS512",
            kid
        }).getBytes()
    );
    const token = encoder.encodeToString(
        JSON.stringify({
            sub: api_key,
            iss: api_key,
            jti: UUID.randomUUID().toString(),
            aud: token_endpoint,
            exp: Math.floor(Date.now() / 1000) + 180
        }).getBytes()
    );

    const signer = Signature.getInstance("SHA512withRSA");
    signer.initSign(private_key);
    signer.update([headers, token].join(".").getBytes(StandardCharsets.UTF_8));

    const signature = encoder.encodeToString(signer.sign());
    const jwt = `${headers}.${token}.${signature}`;

    let tokenRequestBody = "grant_type=client_credentials";
    tokenRequestBody+= "&client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer";
    tokenRequestBody+= `&client_assertion=${jwt}`;

    const tokenRequestMainHeader = new HttpRequestHeader(
        HttpRequestHeader.POST, 
        new URI(token_endpoint, false), 
        HttpHeader.HTTP11
    );

    const tokenMsg = helper.prepareMessage();
    tokenMsg.setRequestBody(tokenRequestBody);
    tokenMsg.setRequestHeader(tokenRequestMainHeader);
    tokenMsg.getRequestHeader().setContentLength(tokenMsg.getRequestBody().length());
    helper.sendAndReceive(tokenMsg, false);

    const body = tokenMsg.getResponseBody().toString();
    const json = JSON.parse(body);

    const {access_token} = json;
    
    if (access_token){
        print("get_bearer_token.js: Successfully fetched token!");
        ScriptVars.setGlobalVar("bearer-token", access_token);
    }else{
        print("get_bearer_token.js: Error getting access token");
    }
    
    // return tokenMsg;
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