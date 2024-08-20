const errors = context.getVariable('data.errors');
const messageId = context.getVariable('messageid');
const statusCode = context.getVariable('response.status.code');
const links = {
    about : "{{ ERROR_ABOUT_LINK }}"
};

errors.forEach((error, index) => {
    let code = 'CM_INVALID_VALUE';
    if (error.title === 'Missing value') {
        code = 'CM_MISSING_VALUE';
    }
    
    Object.defineProperty(error, "id", {value: messageId});
    Object.defineProperty(error, "code", {value: code});
    Object.defineProperty(error, "links", {value: links});
    Object.defineProperty(error, "status", {value: statusCode});
    Object.defineProperty(error, "title", {value: error.title});
    Object.defineProperty(error, "detail", {value: error.message});
});
