/*
When a method is used to access an endpoint that doesn't support it, the API responds with a 405
When a GET method is used to access an endpoint that doesn't exist, the API responds with a 404
*/

var is404 = true;
var is405 = false;

const requestMethod = context.getVariable("request.verb").toLowerCase();
const requestPath = context.getVariable("proxy.pathsuffix");
const isSandbox = /sandbox/.test(context.getVariable("request.header.host"));

const validPaths = [
  {
      match: /^\/v1\/message\-batches$/,
      methods: ['post']
  },
  {
      match: /^\/v1\/messages$/,
      methods: ['post']
  },
  {
      match: /^\/v1\/messages\/.*$/,
      methods: ['get', 'head']
  },
  {
    match: /^\/channels\/nhsapp\/accounts$/,
    methods: ['get']
  }
];

if (isSandbox) {
    validPaths.push({
        match: /^\/_timeout_504$/,
        methods: ['get']
    });
    validPaths.push({
        match: /^\/_timeout$/,
        methods: ['get']
    });
    validPaths.push({
        match: /^\/_timeout_408$/,
        methods: ['get']
    });
    validPaths.push({
        match: /^\/_invalid_certificate$/,
        methods: ['get']
    });
}

validPaths.forEach((pathObj) => {
   if (pathObj.match.test(requestPath)) {
        is404 = false;
        is405 = true;
        pathObj.methods.forEach((method) => {
            if (method == requestMethod) {
                is405 = false;
            }
        });
   }
});

context.setVariable("is404", is404);
context.setVariable("is405", is405);
