function createErrorObject(code, status_code, title, detail, pointer, links) {
    return {
        "id": messageId + "." + errors.length,
        "code": code,
        "links": Object.assign({}, { "about": "https://digital.nhs.uk/developer/api-catalogue/nhs-notify" }, links),  // NOSONAR
        "status": status_code,
        "title": title,
        "detail": detail,
        "source": {
            "pointer": pointer
        }
    };
}

function missingError(pointer) {
    return createErrorObject(
        "CM_MISSING_VALUE",
        "400",
        "Missing property",
        "The property at the specified location is required, but was not present in the request.",
        pointer,
        {}
    );
}

function nullError(pointer) {
    return createErrorObject(
        "CM_NULL_VALUE",
        "400",
        "Property cannot be null",
        "The property at the specified location is required, but a null value was passed in the request.",
        pointer,
        {}
    );
}

function invalidError(pointer) {
    return createErrorObject(
        "CM_INVALID_VALUE",
        "400",
        "Invalid value",
        "The property at the specified location does not allow this value.",
        pointer,
        {}
    );
}

function duplicateError(pointer) {
    return createErrorObject(
        "CM_DUPLICATE_VALUE",
        "400",
        "Duplicate value",
        "The property at the specified location is a duplicate, duplicated values are not allowed.",
        pointer,
        {}
    );
}

function tooFewItemsError(pointer) {
    return createErrorObject(
        "CM_TOO_FEW_ITEMS",
        "400",
        "Too few items",
        "The property at the specified location contains too few items.",
        pointer,
        {}
    )
}

function tooManyItemsError(pointer) {
    return createErrorObject(
        "CM_TOO_MANY_ITEMS",
        "413",
        "Too many items",
        "The property at the specified location contains too many items.",
        pointer,
        {}
    )
}

function invalidNhsNumberError(pointer) {
    return createErrorObject(
        "CM_INVALID_NHS_NUMBER",
        "400",
        "Invalid nhs number",
        "The value provided in this nhsNumber field is not a valid NHS number.",
        pointer,
        { "nhsNumbers": "https://www.datadictionary.nhs.uk/attributes/nhs_number.html" }
    );
}
