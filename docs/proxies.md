# Proxy Configuration

The proxy is constructed of two main parts:

* proxy definition
* communications manager target definition

## Proxy definition

The proxy definition contains the configuration that is to be applied on all incoming requests.

The following diagram details the proxy flow:

```mermaid
flowchart
    S[Request] --> QSA["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#quotas--spike-arrests'>Quotas & Spike Arrests</a>"]
    QSA --> E1{Exception thrown?}
    QSA --> OPF["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#options-preflight'>Options PreFlight</a>"]
    OPF --> E1
    OPF --> APTP["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#add-payload-to-ping-ping-endpoint'>Add Payload to Ping</a>"]
    APTP --> E1
    APTP --> SE["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#status-endpoint'>Status Endpoint</a>"]
    SE --> E1
    SE --> RT["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#request-routing'>Follow endpoint routing config</a>"]
    RT --> E1
    RT --> SRD["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#set-response-defaults'>Set Response Defaults</a>"]
    RT --> CALL["Callout to <a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#target-definition'>communications-manager-target</a>"]
    SRD --> E1
    E1 --> |Yes| PRF["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#proxy-fault-rules'>Proxy Fault Rules</a>"]
    PRF --> E2{Exception handled?}
    SRD --> R[Response]
    E2 --> |Yes| R
    E2 --> |No| PDFR["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#proxy-default-fault-rule'>Proxy Default Fault Rule</a>"]
    PDFR --> R
    R --> PCF["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#post-client-flow'>Post Client Flow</a>"]
    PCF --> E[End]
```

## Target definition

The target definition contains configuration thats specific for calling the backend communications manager API service.

This configuration is called via the proxy definition as part of the request routing configuration.

This diagram details the target definition flow:

```mermaid
flowchart
    S[Request] --> TPFR["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#target-preflow-request'>Target PreFlow Request</a>"]
    TPFR --> E1{Exception thrown?}
    TPFR --> CMB["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#create-message-batch'>Create Message Batch</a>"]
    CMB --> E1
    CMB --> CM["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#create-message'>Create Message</a>"]
    CM --> E1
    CM --> TPFRESP["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#target-preflow-response'>Target PreFlow Response</a>"]
    TPFRESP --> E1
    TPFRESP --> TPOSTF["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#target-post-flow'>Target Post Flow</a>"]
    TPOSTF --> E1
    TPOSTF --> E[End]
    E1 --> |Yes| TFR["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#target-fault-rules'>Target Fault Rules</a>"]
    TFR --> E
```

## Components

### Quotas & Spike Arrests

There are two sets of quotas and spike arrests, one set is global and the other is applied on a per app basis.

Source: [proxies/shared/partials/Partial.Proxy.PreFlow.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Proxy.PreFlow.xml).

```mermaid
flowchart LR
    S[Start] --> Env{Is sandbox?}
    Env --> |No| PASA["Apply per app spike arrest

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/SpikeArrest.PerApp.xml'>SpikeArrest.PerApp</a></em>"]
    PASA --> PAQ["Apply per app quotas

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/Quota.PerApp.xml'>Quota.PerApp</a></em>"]
    Env --> |Yes| GSA["Apply global spike arrest

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/SpikeArrest.Global.xml'>SpikeArrest.Global</a></em>"]
    GSA --> GQ["Apply global quotas

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/Quota.Global.xml'>Quota.Global</a></em>"]
    PAQ --> GSA
    GQ --> E[End]
```

### Options PreFlight

This determines if we need to add CORS headers into the response, allowing the API to be used with cross origin requests.

Source: [proxies/shared/partials/Partial.Flows.OptionsPreFlight.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Flows.OptionsPreFlight.xml)

```mermaid
flowchart LR
    S[Start] --> Q1{Is <code>OPTIONS</code> request?}
    Q1 --> |No| E[End]
    Q1 --> |Yes| Q2{Is <code>Origin</code> set?}
    Q2 --> |No| E
    Q2 --> |Yes| Q3{"Is
    <code>Access-Control-Request-Method</code>
    set?"}
    Q3 --> |No| E
    Q3 --> |Yes| AC["Set CORS response

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.AddCors.xml'>AssignMessage.AddCors</a></em>"]
    AC --> E
```

### Add Payload to Ping (ping endpoint)

This component determines if we should add the ping payload into the response.

Source: [proxies/shared/partials/Partial.Flows.AddPayloadToPing.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Flows.AddPayloadToPing.xml)

```mermaid
flowchart LR
    S[Start] --> Q1{Is path /_ping?}
    Q1 --> |No| E[End]
    Q1 --> |Yes| Q2{GET or HEAD request?}
    Q2 --> |No| E
    Q2 --> |Yes| APTP["Add payload to ping response

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.AddPayloadToPing.xml'>AssignMessage.AddPayloadToPing</a></em>"]
    APTP --> E
```

### Status Endpoint

Determines if the service callout to the status response endpoint should be made - if so the response body is then output using the data returned from the service callout.

Source: [proxies/shared/partials/Partial.Flows.StatusEndpoint.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Flows.StatusEndpoint.xml)


```mermaid
flowchart LR
    S[Start] --> Q1{Is path /_status?}
    Q1 --> |No| E[End]
    Q1 --> |Yes| Q2{GET or HEAD request?}
    Q2 --> |No| E
    Q2 --> |Yes| Q3{API key is valid?}
    Q3 --> |No| RF[Raise Fault]
    Q3 --> |Yes| CHE["Check backend service health

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/ServiceCallout.CallHealthcheckEndpoint.xml'>ServiceCallout.CallHealthcheckEndpoint</a></em>"]
    CHE --> SSR["Set status response

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/javascript.SetStatusResponse.xml'>javascript.SetStatusResponse</a></em>"]
    SSR --> E
```

### Set response defaults

This component is used to set default values on outgoing responses, including:

* Response content type
* Correlation identifier
* CORS headers

Source: [proxies/shared/partials/Partial.Component.SetResponseDefaults.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Component.SetResponseDefaults.xml)

```mermaid
flowchart LR
    S[Start] --> SRCT["Set response headers

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/JavaScript.SetResponseHeaders.xml'>JavaScript.SetResponseHeaders</a></em>"]
    SRCT --> Q1{Correlation id present?}
    Q1 --> |Yes| SCI["Set correlation id

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.SetCorrelationId.xml'>AssignMessage.SetCorrelationId</a></em>"]
    Q1 --> |No| Q2{Origin is set?}
    SCI --> Q2
    Q2 --> |No| E[End]
    Q2 --> |Yes| Q3{OPTIONS request?}
    Q3 --> |Yes| E
    Q3 --> |No| ACR["Add CORS response

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.AddCorsResponse.xml'>AssignMessage.AddCorsResponse</a></em>"]
    ACR --> E
```

### Proxy Fault Rules

This component handles faults that occur at the proxy level.

Source: [proxies/shared/partials/Partial.Proxy.FaultRules.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Proxy.FaultRules.xml)

```mermaid
flowchart LR
    S[Start] --> SRD["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#set-response-defaults'>Set response defaults</a>"]
    SRD --> Q1{Is SpikeArrestViolation?}
    Q1 --> |Yes| 429["Throw 429

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.429TooManyRequests.xml'>RaiseFault.429TooManyRequests</a></em>"]
    Q1 --> |No| Q2{Is QuotaViolation?}
    Q2 --> |Yes| 429
    Q2 --> |No| E[End]
    429 --> E
```

### Proxy Default Fault Rule

This is the default fault handler for the proxy.

Source: [proxies/shared/partials/Partial.Faults.DefaultFaultRule.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Faults.DefaultFaultRule.xml)

```mermaid
flowchart LR
    S[Start] --> SRD["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#set-response-defaults'>Set response defaults</a>"]
    SRD --> CAM["Error message catch all

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.Errors.CatchAllMessage.xml'>AssignMessage.Errors.CatchAllMessage</a></em>"]
    CAM --> E[End]
```

### Post Client Flow

This flow executes after the response has been sent.

Source: [proxies/shared/partials/Partial.Proxy.PostClientFlow.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Proxy.PostClientFlow.xml)

```mermaid
flowchart LR
    S[Start] --> LTS["Send logs to splunk

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/FlowCallout.LogToSplunk.xml'>FlowCallout.LogToSplunk</a></em>"]
    LTS --> E[End]
```

### Request Routing

This defines how incoming requests are routed to target servers.

Source: [proxies/shared/partials/Partial.Proxy.Routes.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Proxy.Routes.xml)

```mermaid
flowchart LR
    S[Start] --> Q1{Is CORs request?}
    Q1 --> |Yes| NR[Route no-op]
    Q1 --> |No| Q2{Is ping endpoint?}
    Q2 --> |Yes| NR
    Q2 --> |No| Q3{Is status endpoint?}
    Q3 --> |Yes| NR
    Q3 --> |No| TS[Call <a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#target-definition'>communications-manager-target</a>]
    NR --> E[End]
    TS --> E[End]
```

### Content Negotiation

This flow ensures that the incoming request contains a payload that is understandable, and that the service can respond with a payload that the client finds acceptable.

Source: [proxies/shared/partials/Partial.PreFlow.ContentNegotiation.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.PreFlow.ContentNegotiation.xml)

```mermaid
flowchart LR
    S[Start] --> Q1{Is acceptable?}
    Q1 --> |Yes| Q2{Is supported media?}
    Q1 --> |No| 406["Raise 406 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.406NotAcceptable.xml'>RaiseFault.406NotAcceptable</a></em>"]
    406 --> E[End]
    Q2 --> |No| 415["Raise 415 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.415UnsupportedMedia.xml'>RaiseFault.415UnsupportedMedia</a></em>"]
    415 --> E
    Q2 --> |Yes| E
```

### Target PreFlow Request

This defines the actions carried out on all incoming requests to the communications manager target.

Source: [proxies/shared/partials/Partial.Target.PreFlowRequest.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Target.PreFlowRequest.xml)

```mermaid
flowchart
    S[Start] --> SRD["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#set-response-defaults'>Set response defaults</a>"]
    SRD --> SBCI["Set the backend request correlation id

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/JavaScript.SetBackendCorrelationId.xml'>JavaScript.SetBackendCorrelationId</a></em>"]
    SBCI --> ADRP["Sets a default request path

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.AddDefaultRequestPath.xml'>AssignMessage.AddDefaultRequestPath</a></em>"]
    ADRP --> Q1{Is sandbox environment?}
    Q1 --> |Yes| Q2{Prefer code 408?}
    Q2 --> |Yes| 408["Raise 408 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.408RequestTimeout.xml'>RaiseFault.408RequestTimeout</a></em>"]
    408 --> E[End]
    Q2 --> |No| Q3{Prefer code 504?}
    Q3 --> |Yes| 504["Raise 504 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.504GatewayTimeout.xml'>RaiseFault.504GatewayTimeout</a></em>"]
    504 --> E
    Q3 --> |No| Q4{Prefer 503 error?}
    Q4 --> |Yes| 503["Raise 503 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.503ServiceUnavailable.xml'>RaiseFault.503ServiceUnavailable</a></em>"]
    503 --> E
    Q4 --> |No| Q5{Prefer 401 error?}
    Q5 --> |Yes| 401["Raise 401 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.401Unauthorized.xml'>RaiseFault.401Unauthorized</a></em>"]
    401 --> E
    Q5 --> |No| Q6{Prefer 403 error?}
    Q6 --> |Yes| 403["Raise 403 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.403Forbidden.xml'>RaiseFault.403Forbidden</a></em>"]
    403 --> E
    Q6 --> |No| Q6.1{Prefer 403.1 error?}
    Q6.1 --> |Yes| 403.1["Raise 403 service ban error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.403ServiceBan.xml'>RaiseFault.403ServiceBan</a></em>"]
    403.1 --> E
    Q6.1 --> |No| Q7{Prefer 425 error?}
    Q7 --> |Yes| 425["Raise 425 Retry Too Early

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.425RetryTooEarly.xml'>RaiseFault.425RetryTooEarly</a></em>"]
    425 --> E
    Q7 --> |No| CN["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#content-negotiation'>Content Negotiation</a>"]
    Q1 --> |No| VAT["Verify access token

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/OauthV2.VerifyAccessToken.xml'>OauthV2.VerifyAccessToken</a></em>"]
    VAT --> Q8{Is client credentials?}
    Q8 --> |No| 403
    Q8 --> |Yes| CN
    CN --> Q9{Is sandbox environment?}
    Q9 --> |Yes| Q10{Prefer 429 error?}
    Q10 --> |Yes| 429["Raise 429 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.429TooManyRequests.xml'>RaiseFault.429TooManyRequests</a></em>"]
    429 --> E
    Q10 --> |No| E
    Q9 --> |No| Q11{Is request on a known resource?}
    Q11 --> |Yes| E
    Q11 --> |No| 404["Raise 404 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.404NotFound.xml'>RaiseFault.404NotFound</a></em>"]
    404 --> E
```

### Target PreFlow Response

This defines the actions carried out on all outgoing responses from the communications manager target.

Source: [proxies/shared/partials/Partial.Target.PreFlowResponse.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Target.PreFlowResponse.xml)

```mermaid
flowchart LR
    S[Start] --> AD["Add CORS headers

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.AddCors.xml'>AssignMessage.AddCors</a></em>"]
    AD --> E[End]
```

### Create Message Batch

This flow manages the validating of incoming create message batches requests, plus mapping the incoming request and outgoing response so they match the schemas set out in the specification.

Source: [proxies/shared/partials/Partial.Flows.CreateMessageBatchEndpoint.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Flows.CreateMessageBatchEndpoint.xml)

```mermaid
flowchart
    S[Start] --> Q1{Matches create message batch endpoint?}
    Q1 --> |No| E[End]
    Q1 --> |Yes| V["Validate incoming request payload

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/JavaScript.MessageBatches.Create.Validate.xml'>JavaScript.MessageBatches.Create.Validate</a></em>"]
    V --> Q2{Validation errors found?}
    Q2 --> |Yes| 400["Raise 400 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.400BadRequest.xml'>RaiseFault.400BadRequest</a></em>"]
    400 --> E
    Q2 --> |No| MREQ["Convert request payload

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/JavaScript.MessageBatches.Create.Request.xml'>JavaScript.MessageBatches.Create.Request</a></em>"]
    MREQ --> CR["Create backend request

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.MessageBatches.Create.Request.xml'>AssignMessage.MessageBatches.Create.Request</a></em>"]
    CR --> AD["Assign authentication credentials

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.AuthenticationDetails.xml'>AssignMessage.AuthenticationDetails</a></em>"]
    AD --> SEND["Send request to backend"]
    SEND --> ERES["Extract variables from response

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/ExtractVariables.MessageBatches.Create.Response.xml'>ExtractVariables.MessageBatches.Create.Response</a></em>"]
    ERES --> MRESP["Convert response

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.MessageBatches.Create.Response.xml'>AssignMessage.MessageBatches.Create.Response</a></em>"]
    MRESP --> E
```

### Create Message

This flow manages the validating of incoming create message requests, plus mapping the incoming request and outgoing response so they match the schemas set out in the specification.

Source: [proxies/shared/partials/Partial.Flows.CreateMessageEndpoint.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Flows.CreateMessageEndpoint.xml)

```mermaid
flowchart
    S[Start] --> Q1{Matches create message endpoint?}
    Q1 --> |No| E[End]
    Q1 --> |Yes| V["Validate incoming request payload

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/JavaScript.Messages.Create.Validate.xml'>JavaScript.Messages.Create.Validate</a></em>"]
    V --> Q2{Validation errors found?}
    Q2 --> |Yes| 400["Raise 400 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.400BadRequest.xml'>RaiseFault.400BadRequest</a></em>"]
    400 --> E
    Q2 --> |No| MREQ["Convert request payload

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/JavaScript.Messages.Create.Request.xml'>JavaScript.Messages.Create.Request</a></em>"]
    MREQ --> CR["Create backend request

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.Messages.Create.Request.xml'>AssignMessage.Messages.Create.Request</a></em>"]
    CR --> AD["Assign authentication credentials

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.AuthenticationDetails.xml'>AssignMessage.AuthenticationDetails</a></em>"]
    AD --> SEND["Send request to backend"]
    SEND --> ERES["Extract variables from response

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/JavaScript.Messages.Create.Response.xml'>JavaScript.Messages.Create.Response</a></em>"]
    ERES --> MRESP["Convert response

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/AssignMessage.MessageBatches.Create.Response.xml'>AssignMessage.Messages.Create.Response</a></em>"]
    MRESP --> E
```

### Target Post Flow

This flow runs on all outgoing responses from the target.

Source: [proxies/shared/partials/Partial.Target.PostFlow.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Target.PostFlow.xml)

```mermaid
flowchart LR
    S[Start] --> SRD["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#set-response-defaults'>Set response defaults</a>"]
    SRD --> E[End]
```

### Target Fault Rules

This flow handles all of the fault rules being understood and output from the backend service.

Source: [proxies/shared/partials/Partial.Target.FaultRules.xml](https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/partials/Partial.Target.FaultRules.xml)

```mermaid
flowchart
    S[Start] --> SRD["<a href='https://github.com/NHSDigital/communications-manager-api/blob/release/docs/proxies.md#set-response-defaults'>Set response defaults</a>"]
    SRD --> Q1{Is sandbox environment?}
    Q1 --> |No| Q2{Token verification failure?}
    Q2 --> |Yes| 401["Raise 401 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.401Unauthorized.xml'>RaiseFault.401Unauthorized</a></em>"]
    401 --> E1[End]
    Q2 --> |No| Q3{Backend 403 response?}
    Q3 --> |Yes| Q3.1{Service ban?}
    Q3.1 --> |Yes| 403ServiceBan["Raise 403 service ban error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.403ServiceBan.xml'>RaiseFault.403ServiceBan</a></em>"]
    403ServiceBan --> E2[End]
    Q3.1 --> |No| 403["Raise 403 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.403Forbidden.xml'>RaiseFault.403Forbidden</a></em>"]
    403 --> E2[End]
    Q3 --> |No| Q4{Backend 404 & invalid routing plan?}
    Q1 --> |Yes| Q3
    Q4 --> |Yes| 404Invalid["Raise 404 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.404InvalidRoutingPlan.xml'>RaiseFault.404InvalidRoutingPlan</a></em>"]
    404Invalid --> E3[End]
    Q4 --> |No| Q5{Backend 404 response?}
    Q5 --> |Yes| 404["Raise 404 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.404NotFound.xml'>RaiseFault.404NotFound</a></em>"]
    404 --> E4[End]
    Q5 --> |No| Q6{Backend 400 & invalid routing config?}
    Q6 --> |Yes| 400InvalidRoutingPlan["Raise 400 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.400BackendException.InvalidRoutingConfig.xml'>RaiseFault.400BackendException.InvalidRoutingConfig</a></em>"]
    400InvalidRoutingPlan --> E5[End]
    Q6 --> |No| Q7{Backend 400 & duplicate requestItemRefIds?}
    Q7 --> |Yes| 400Duplicates["Raise 400 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.400BackendException.DuplicateRequestItemRefIds.xml'>RaiseFault.400BackendException.DuplicateRequestItemRefIds</a></em>"]
    400Duplicates --> E6[End]
    Q7 --> |No| Q8{Backend 400 & missing sendingGroupId?}
    Q8 --> |Yes| 400MissingSendingGroupId["Raise 400 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.400BackendException.MissingSendingGroupId.xml'>RaiseFault.400BackendException.MissingSendingGroupId</a></em>"]
    400MissingSendingGroupId --> E7[End]
    Q8 --> |No| Q9{Backend 400 & missing requestRefId?}
    Q9 --> |Yes| 400MissingRequestRefId["Raise 400 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.400BackendException.MissingRequestRefId.xml'>RaiseFault.400BackendException.MissingRequestRefId</a></em>"]
    400MissingRequestRefId --> E8[End]
    Q9 --> |No| Q10{Backend 400 & missing data?}
    Q10 --> |Yes| 400MissingData["Raise 400 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.400BackendException.MissingDataArray.xml'>RaiseFault.400BackendException.MissingDataArray</a></em>"]
    400MissingData --> E9[End]
    Q10 --> |No| Q11{Backend 425 response?}
    Q11 --> |Yes| 425RetryTooEarly["Raise 425 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.400BackendException.MissingDataArray.xml'>RaiseFault.425RetryTooEarly</a></em>"]
    425RetryTooEarly --> E10[End]
    Q11 --> |No| Q12{Backend 500 & duplicate templates?}
    Q12 --> |Yes| 500DuplicatesExtract["Extract duplicate templates

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/JavaScript.500DuplicateTemplates.ExtractDuplicates.xml'>JavaScript.500DuplicateTemplates.ExtractDuplicates</a></em>"]
    500DuplicatesExtract --> 500DuplicatesError["Raise 500 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.500DuplicateTemplates.xml'>RaiseFault.500DuplicateTemplates</a></em>"]
    500DuplicatesError --> E11[End]
    Q12 --> |No| Q13{Backend 500 & templates missing?}
    Q13 --> |Yes| 500MissingTemplates["Raise 500 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.500MissingTemplates.xml'>RaiseFault.500MissingTemplates</a></em>"]
    500MissingTemplates --> E12[End]
    Q13 --> |No| Q14{Other 500 exception?}
    Q14 --> |Yes| 500["Raise 500 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.500Generic.xml'>RaiseFault.500Generic</a></em>"]
    500 --> E13[End]
    Q14 --> |No| Q15{Backend service unavailable?}
    Q15 --> |Yes| 503["Raise 503 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.503ServiceUnavailable.xml'>RaiseFault.503ServiceUnavailable</a></em>"]
    503 --> E14[End]
    Q15 --> |No| Q16{Backend 504 or gateway timeout?}
    Q16 --> |Yes| 504["Raise 504 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.504GatewayTimeout.xml'>RaiseFault.504GatewayTimeout</a></em>"]
    504 --> E15[End]
    Q16 --> |No| Q17{Backend 408 or request timeout?}
    Q17 --> |Yes| 408["Raise 408 error

    <em><a href='https://github.com/NHSDigital/communications-manager-api/blob/release/proxies/shared/policies/RaiseFault.408RequestTimeout.xml'>RaiseFault.408RequestTimeout</a></em>"]
    408 --> E16[End]
    Q17 --> |No| E16
```