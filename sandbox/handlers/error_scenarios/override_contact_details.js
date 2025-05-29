import { notAllowedContactDetailOverride } from "../config.js";

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
  if (typeof sms !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/sms`,
        message: "'sms' is not a string",
        statusCode: 400,
      },
      `Field 'sms': 'sms' is not a string`,
    ]);
  }
  return validationSuccess();
}

function emailValidation(email, path) {
  if (!email) {
    return validationSuccess();
  }
  if (typeof email !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/email`,
        message: "'email' is not a string",
        statusCode: 400,
      },
      `Field 'email': 'email' is not a string`,
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

  if ("lines" in address) {
    if (!Array.isArray(address.lines)) {
      return validationFailure([
        {
          title: "Invalid value",
          code: 'CM_INVALID_VALUE',
          field: `${path}/recipient/contactDetails/address`,
          message: "'lines' is not a string array",
          statusCode: 400,
        },
        `Field 'address': 'lines' is not a string array`,
      ]);
    }

    if (address.lines.some((line) => typeof line !== "string")) {
      return validationFailure([
        {
          title: "Invalid value",
          code: 'CM_INVALID_VALUE',
          field: `${path}/recipient/contactDetails/address`,
          message: "'lines' is not a string array",
          statusCode: 400,
        },
        `Field 'address': 'lines' is not a string array`,
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
  }

  if ("postcode" in address && typeof address.postcode !== "string") {
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

  if ("prefix" in name && typeof name.prefix !== "string") {
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

  if ("firstName" in name && typeof name.firstName !== "string") {
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

  if ("middleNames" in name && typeof name.middleNames !== "string") {
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

  if ("lastName" in name && typeof name.lastName !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        code: 'CM_INVALID_VALUE',
        field: `${path}/recipient/contactDetails/name`,
        message: "'lastName' is not a string",
        statusCode: 400,
      },
      `Field 'name': 'lastName' is not a string`,
    ]);
  }

  if ("suffix" in name && typeof name.suffix !== "string") {
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
