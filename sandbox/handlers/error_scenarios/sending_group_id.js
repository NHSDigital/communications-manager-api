import {
  validSendingGroupIds,
  sendingGroupIdWithMissingNHSTemplates,
  sendingGroupIdWithMissingTemplates,
  sendingGroupIdWithDuplicateTemplates,
  duplicateTemplates,
  trigger500SendingGroupId,
  invalidRoutingPlanId,
  trigger425SendingGroupId
} from "../config.js"

export function getSendingGroupIdError(sendingGroupId) {
  if (!validSendingGroupIds[sendingGroupId]) {
    return [
      404,
      `Routing Config does not exist for clientId "sandbox_client_id" and routingPlanId "${sendingGroupId}"`
    ]
  }

  if (sendingGroupId === sendingGroupIdWithMissingNHSTemplates) {
    return [
      500,
      `NHS App Template does not exist with internalTemplateId: invalid-template`
    ]
  }

  if (sendingGroupId === sendingGroupIdWithMissingTemplates) {
    return [
      500,
      `Templates required in "${sendingGroupIdWithMissingTemplates}" routing config not found`
    ]
  }

  if (sendingGroupId === sendingGroupIdWithDuplicateTemplates) {
    return [
      500,
      `Duplicate templates in routing config: ${JSON.stringify(
        duplicateTemplates
      )}`
    ]
  }

  if (sendingGroupId === invalidRoutingPlanId) {
    return [400, "Invalid Routing Config"]
  }

  if (sendingGroupId === trigger500SendingGroupId) {
    return [500, "Error writing request items to DynamoDB"]
  }

  if (sendingGroupId === trigger425SendingGroupId) {
    return [
      425,
      "Message with this idempotency key is already being processed"
    ]
  }

  return null;
}


