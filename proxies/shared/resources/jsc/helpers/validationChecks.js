// Regex to validate the id is a valid UUID
const uuidRegex = /^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$/i
const nhsNumberRegex = /^\d{10}$/i
const messageId = context.getVariable("messageid");

const isUndefined = (val) => {
    return typeof val === "undefined";
}

const isValidNhsNumber = (nhsNumber, nhsNumberRegex) => {
    if (!nhsNumberRegex.test(nhsNumber)) {
        return false;
    }

    const checkDigit = nhsNumber.substring(9);

    var total = 0;
    for (var i = 0; i <= 8; i++) {
        var digit = (parseInt(nhsNumber.substring(i, i + 1)))
        total += (digit * (10 - i))
    }

    const remainder = total % 11;
    return (11 - remainder) % 11 === parseInt(checkDigit);
}

// validate field value and push any errors
const validateObject = (errors, fieldValue, fieldPointer) => {
    if (isUndefined(fieldValue)) {
        errors.push(missingError(fieldPointer));
        return false
    }
    if (fieldValue === null) {
        errors.push(nullError(fieldPointer));
        return false
    }
    if (typeof fieldValue !== "object" || Array.isArray(fieldValue)) {
        errors.push(invalidError(fieldPointer));
        return false
    }
    return true
}

const validateUuid = (errors, fieldValue, fieldPointer) => {
    if (isUndefined(fieldValue)) {
        errors.push(missingError(fieldPointer));
        return false
    }
    if (fieldValue === null) {
        errors.push(nullError(fieldPointer));
        return false
    }
    if (typeof fieldValue !== "string" || !uuidRegex.test(fieldValue)) {
        errors.push(invalidError(fieldPointer));
        return false
    }
    return true
}

const validateConstantString = (errors, fieldValue, fieldPointer, requiredValue) => {
    if (isUndefined(fieldValue)) {
        errors.push(missingError(fieldPointer));
        return false
    }
    if (fieldValue === null) {
        errors.push(nullError(fieldPointer));
        return false
    }
    if (fieldValue !== requiredValue) {
        errors.push(invalidError(fieldPointer));
        return false
    }
    return true
}

const validateNhsNumber = (errors, fieldValue, fieldPointer) => {
    if (!isUndefined(fieldValue)) {
        if (fieldValue === null) {
            errors.push(nullError(fieldPointer));
            return false
        }
        if (typeof fieldValue !== "string" || !isValidNhsNumber(fieldValue, nhsNumberRegex)) {
            errors.push(invalidNhsNumberError(fieldPointer));
            return false
        }
    }
    return true
}

const validateArray = (errors, fieldValue, fieldPointer, minElements) => {
    if (isUndefined(fieldValue)) {
        errors.push(missingError(fieldPointer));
        return false
    } else if (fieldValue === null) {
        errors.push(nullError(fieldPointer));
        return false
    } else if (!Array.isArray(fieldValue)) {
        errors.push(invalidError(fieldPointer));
        return false
    } else if (fieldValue.length < minElements) {
        errors.push(tooFewItemsError(fieldPointer));
        return false
    }
    return true
}

const validateString = (errors, fieldValue, fieldPointer) => {
    if (isUndefined(fieldValue)) {
        errors.push(missingError(fieldPointer));
        return false
    }
    if (fieldValue === null) {
        errors.push(nullError(fieldPointer));
        return false
    }
    if (typeof fieldValue !== "string") {
        errors.push(invalidError(fieldPointer));
        return false;
    }
    if (fieldValue.trim().length === 0) {
        errors.push(invalidError(fieldPointer));
        return false;
    }
    return true
}

const validateOdsCode = (errors, fieldValue, fieldPointer) => {
    if (
        !isUndefined(fieldValue)
        && (
            fieldValue === null
            || typeof fieldValue !== "string"
        )
    ) {
        errors.push(invalidError(fieldPointer));
        return false
    }
    return true
}
