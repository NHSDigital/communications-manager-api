import { notAllowedContactDetailOverride } from "../config.js";

const invalidPhoneNumber = "07700900002";
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
        field: `${path}/recipient/contactDetails/sms`,
        message: "Input failed format check",
      },
      `Field 'sms': Input failed format check`,
    ]);
  }
  if (typeof sms !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        field: `${path}/recipient/contactDetails/sms`,
        message: "Invalid",
      },
      `Field 'sms': Invalid`,
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
        field: `${path}/recipient/contactDetails/email`,
        message: "Input failed format check",
      },
      `Field 'email': Input failed format check`,
    ]);
  }
  if (typeof email !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        field: `${path}/recipient/contactDetails/email`,
        message: "Invalid",
      },
      `Field 'email': Invalid`,
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
        field: `${path}/recipient/contactDetails/address`,
        message: "Invalid",
      },
      `Field 'address': Invalid`,
    ]);
  }

  if (!address.lines) {
    return validationFailure([
      {
        title: "Missing value",
        field: `${path}/recipient/contactDetails/address`,
        message: "`lines` is missing",
      },
      `Field 'lines': 'lines' is missing`,
    ]);
  }
  if (!Array.isArray(address.lines)) {
    return validationFailure([
      {
        title: "Missing value",
        field: `${path}/recipient/contactDetails/address`,
        message: "`lines` is missing",
      },
      `Field 'lines': 'lines' is missing`,
    ]);
  }

  if (address.lines.some((line) => typeof line !== "string")) {
    return validationFailure([
      {
        title: "Invalid value",
        field: `${path}/recipient/contactDetails/address`,
        message: "Invalid",
      },
      `Field 'lines': Invalid`,
    ]);
  }

  if (address.lines.length < 2) {
    return validationFailure([
      {
        title: "Missing value",
        field: `${path}/recipient/contactDetails/address`,
        message: "Too few address lines were provided",
      },
      `Field 'lines': Too few address lines were provided`,
    ]);
  }
  if (address.lines.length > 5) {
    return validationFailure([
      {
        title: "Invalid value",
        field: `${path}/recipient/contactDetails/address`,
        message: "Invalid",
      },
      `Field 'lines': Invalid`,
    ]);
  }

  if (!address.postcode) {
    return validationFailure([
      {
        title: "Missing value",
        field: `${path}/recipient/contactDetails/address`,
        message: "`postcode` is missing",
      },
      `Field 'postcode': 'postcode' is missing`,
    ]);
  }

  if (typeof address.postcode !== "string") {
    return validationFailure([
      {
        title: "Invalid value",
        field: `${path}/recipient/contactDetails/address/postcode`,
        message: "Invalid",
      },
      `Field 'postcode': Invalid`,
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

  if (validationErrors.length) {
    return [400, validationErrorMessages.join(". "), validationErrors];
  }

  return null;
}
