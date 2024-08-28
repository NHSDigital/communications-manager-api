const errors = context.getVariable('data.errors');
const messageId = context.getVariable('messageid');
const statusCode = context.getVariable('response.status.code');
const links = {
    about : "{{ ERROR_ABOUT_LINK }}"
};

const enhancedErrors = [];

JSON.parse(errors).forEach((error, index) => {
    var code = 'CM_INVALID_VALUE';
    if (error.title === 'Missing value') {
        code = 'CM_MISSING_VALUE';
    }

    enhancedErrors.push({
        id: messageId + '.' + index,
        code: code,
        links: links,
        status: statusCode,
        title: error.title,
        detail: error.message,
        source: {
            pointer: error.field
        }
    });
});

context.setVariable("data.enhancedErrors", JSON.stringify(enhancedErrors));
