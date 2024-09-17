const errors = context.getVariable('data.errors');
const messageId = context.getVariable('messageid');
const statusCode = context.getVariable('response.status.code');
const links = {
    about: "{{ ERROR_ABOUT_LINK }}"
};

const enhancedErrors = [];

const errorCodes = {
    'Property cannot be null': 'CM_NULL_VALUE',
    'Duplicate value': 'CM_DUPLICATE_VALUE',
    'Missing value': 'CM_MISSING_VALUE',
    'Too few items': 'CM_TOO_FEW_ITEMS'
};

JSON.parse(errors).forEach((error, index) => {
    const code = errorCodes[error.title] || 'CM_INVALID_VALUE';

    enhancedErrors.push({
        id: messageId + '.' + index,
        code: code,
        links: links,
        status: String(statusCode),
        title: error.title,
        detail: error.message,
        source: {
            pointer: error.field
        }
    });
});

context.setVariable("error.content", JSON.stringify({ errors: enhancedErrors }));
