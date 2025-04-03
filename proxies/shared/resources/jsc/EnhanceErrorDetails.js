const errors = context.getVariable('data.errors');
const messageId = context.getVariable('messageid');
const links = {
    about: "{{ ERROR_ABOUT_LINK }}"
};

const enhancedErrors = [];

JSON.parse(errors).forEach((error, index) => {
    var translatedError = {
        id: messageId + '.' + index,
        code: error.code,
        links: links,
        status: String(error.statusCode),
        title: error.title,
        detail: error.message
    };
    if (error.field) {
        translatedError.source = {
            pointer: error.field
        };
    }

    enhancedErrors.push(translatedError);
});

context.setVariable("error.content", JSON.stringify({ errors: enhancedErrors }));
