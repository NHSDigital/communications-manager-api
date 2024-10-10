import {
  globalFreeTextEmailSendingGroupId,
  globalFreeTextNhsAppSendingGroupId,
  globalFreeTextSmsSendingGroupId,
} from "../config.js";

const globalFreeTextPersonalisationFields = {
  [globalFreeTextNhsAppSendingGroupId]: ["body"],
  [globalFreeTextEmailSendingGroupId]: ["email_subject", "email_body"],
  [globalFreeTextSmsSendingGroupId]: ["sms_body"],
};

export function getGlobalFreeTextError(personalisation, sendingGroupId) {
  const requiredPersonalisationFields =
    globalFreeTextPersonalisationFields[sendingGroupId];

  if (!requiredPersonalisationFields) {
    return null;
  }

  if (!personalisation) {
    return [
      400,
      `Some personalisation fields are missing: ${requiredPersonalisationFields.join(
        ","
      )}`,
    ];
  }

  const personalisationFields = Object.keys(personalisation);

  const missingPersonalisationFields = [];

  for (const requiredField of requiredPersonalisationFields) {
    if (!personalisationFields.includes(requiredField)) {
      missingPersonalisationFields.push(requiredField);
    }
  }

  if (missingPersonalisationFields.length) {
    return [
      400,
      `Some personalisation fields are missing: ${missingPersonalisationFields.join(
        ","
      )}`,
    ];
  }

  return null;
}
