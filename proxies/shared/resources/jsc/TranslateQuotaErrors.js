
const errorContent = context.getVariable('error.content');
const messageId = context.getVariable('messageid');
const statusCode = context.getVariable('response.status.code');
const links = {
    about : "{{ ERROR_ABOUT_LINK }}"
};

const errorParsed = JSON.parse(errorContent);

const enhancedErrors = [
    {
        id: messageId + '.0',
        code: "CM_QUOTA",
        links: links,
        status: statusCode,
        title: "Too many requests",
        detail: errorParsed.message
    }
];

// If it's a spike arrest then retry after 1 second
let retryAfter = 1;
if (errorParsed.policy == "quota") {
    // If it's a quota limit then retry after 1 minute
    retryAfter = 60;
}

context.setVariable("data.enhancedErrors", JSON.stringify(enhancedErrors));
context.setVariable("data.retryAfter", retryAfter);