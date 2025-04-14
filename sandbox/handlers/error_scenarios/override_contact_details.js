import { notAllowedContactDetailOverride } from "../config.js";

const invalidPhoneNumber = "11111111111";
const invalidEmailAddress = "invalidEmailAddress";

function validationSuccess() {
  return {
    valid: true,
  };
}

function validationFailure(result) {
  return {
    valid: false,
    result,
  };
}

function smsValidation(sms, path) {
  if (!sms) {
    return validationSuccess();
  }
  if (sms === invalidPhoneNumber) {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/sms`,
        message: "Input failed format check",
        statusCode: 400,
      },
      `Field 'sms': Input failed format check`,
    ]);
  }
  if (typeof sms !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/sms`,
        message: "Input is not a string",
        statusCode: 400,
      },
      `Field 'sms': Input is not a string`,
    ]);
  }
  return validationSuccess();
}

function emailValidation(email, path) {
  if (!email) {
    return validationSuccess();
  }
  if (email === invalidEmailAddress) {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/email`,
        message: "Input failed format check",
        statusCode: 400,
      },
      `Field 'email': Input failed format check`,
    ]);
  }
  if (typeof email !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/email`,
        message: "Input is not a string",
        statusCode: 400,
      },
      `Field 'email': Input is not a string`,
    ]);
  }
  return validationSuccess();
}

function addressValidation(address, path) {
  if (!address) {
    return validationSuccess();
  }

  if (typeof address !== "object" || Array.isArray(address)) {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/address`,
        message: "Invalid",
        statusCode: 400,
      },
      `Field 'address': Invalid`,
    ]);
  }

  if (!address.lines) {
    return validationFailure([
      {
        title: "Missing value",
        code: 'CM_MISSING_VALUE',
        field: `${path}/recipient/contactDetails/address`,
        message: "`lines` is missing",
        statusCode: 400,
      },
      `Field 'address': 'lines' is missing`,
    ]);
  }
  if (!Array.isArray(address.lines)) {
    return validationFailure([
      {
        title: "Missing value",
        code: 'CM_MISSING_VALUE',
        field: `${path}/recipient/contactDetails/address`,
        message: "`lines` is missing",
        statusCode: 400,
      },
      `Field 'address': 'lines' is missing`,
    ]);
  }

  if (address.lines.some((line) => typeof line !== "string")) {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/address`,
        message: "Lines contain non-string or empty line",
        statusCode: 400,
      },
      `Field 'address': Lines contain non-string or empty line`,
    ]);
  }

  if (address.lines.length < 2) {
    return validationFailure([
      {
        code: 'CM_TOO_FEW_ITEMS',
        title: "Too few items",
        field: `${path}/recipient/contactDetails/address`,
        message: "Too few address lines were provided",
        statusCode: 400,
      },
      `Field 'address': Too few address lines were provided`,
    ]);
  }
  if (address.lines.length > 5) {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/address`,
        message: "Too many address lines were provided",
        statusCode: 400,
      },
      `Field 'address': Too many address lines were provided`,
    ]);
  }

  if (!address.postcode) {
    return validationFailure([
      {
        title: "Missing value",
        code: 'CM_MISSING_VALUE',
        field: `${path}/recipient/contactDetails/address`,
        message: "`postcode` is missing",
        statusCode: 400,
      },
      `Field 'address': 'postcode' is missing`,
    ]);
  }

  if (typeof address.postcode !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/address`,
        message: "'postcode' is not a string",
        statusCode: 400,
      },
      `Field 'address': 'postcode' is not a string`,
    ]);
  }
  return validationSuccess();
}

function nameValidation(name, path) {

  if (!name) {
    return validationSuccess();
  }

  if (typeof name !== "object" || Array.isArray(name)) {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/name`,
        message: "Invalid",
        statusCode: 400,
      },
      `Field 'name': Invalid`,
    ]);
  }

  if (typeof name.prefix !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/name`,
        message: "'prefix' is not a string",
        statusCode: 400,
      },
      `Field 'name': 'prefix' is not a string`,
    ]);
  }

  if (typeof name.firstName !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/name`,
        message: "'firstName' is not a string",
        statusCode: 400,
      },
      `Field 'name': 'firstName' is not a string`,
    ]);
  }

  if (typeof name.middleNames !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/name`,
        message: "'middleNames' is not a string",
        statusCode: 400,
      },
      `Field 'name': 'middleNames' is not a string`,
    ]);
  }

  if (typeof name.lastName === "undefined") {
    return validationFailure([
      {
        title: "Missing value",
        code: 'CM_MISSING_VALUE',
        field: `${path}/recipient/contactDetails/name`,
        message: "`lastName` is missing",
        statusCode: 400,
      },
      `Field 'name': 'lastName' is missing`,
    ]);
  }

  if (typeof name.lastName !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/name`,
        message: "'lastName' must be a non-empty string",
        statusCode: 400,
      },
      `Field 'name': 'lastName' must be a non-empty string`,
    ]);
  }

  if (typeof name.suffix !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/name`,
        message: "'suffix' is not a string",
        statusCode: 400,
      },
      `Field 'name': 'suffix' is not a string`,
    ]);
  }
  return validationSuccess();
}

export function getAlternateContactDetailsError(
  contactDetails,
  authorizationHeader,
  path
) {
  if (!contactDetails) {
    return null;
  }

  if (contactDetails && authorizationHeader === notAllowedContactDetailOverride) {
    return [
      400,
      "Client is not allowed to provide alternative contact details",
      [
        {
          code: "CM_CANNOT_SET_CONTACT_DETAILS",
          title: "Cannot set contact details",
          field: `${path}/recipient/contactDetails`,
          message: "Client is not allowed to provide alternative contact details.",
          statusCode: 400,
        },
      ]
    ];
  }

  const validationErrorMessages = ["Invalid recipient contact details"];
  const validationErrors = [];

  const { valid: smsValid, result: smsErrors } = smsValidation(
    contactDetails.sms,
    path
  );

  if (!smsValid) {
    const [errors, errorMessage] = smsErrors;
    validationErrors.push(errors);
    validationErrorMessages.push(errorMessage);
  }

  const { valid: emailValid, result: emailErrors } = emailValidation(
    contactDetails.email,
    path
  );

  if (!emailValid) {
    const [errors, errorMessage] = emailErrors;
    validationErrors.push(errors);
    validationErrorMessages.push(errorMessage);
  }

  const { valid: addressValid, result: addressErrors } = addressValidation(
    contactDetails.address,
    path
  );

  if (!addressValid) {
    const [errors, errorMessage] = addressErrors;
    validationErrors.push(errors);
    validationErrorMessages.push(errorMessage);
  }

  const { valid: nameValid, result: nameErrors } = nameValidation(
    contactDetails.name,
    path
  );

  if (!nameValid) {
    const [errors, errorMessage] = nameErrors;
    validationErrors.push(errors);
    validationErrorMessages.push(errorMessage);
  }

  if (validationErrors.length) {
    return [400, validationErrorMessages.join(". "), validationErrors];
  }

  return null;
}
