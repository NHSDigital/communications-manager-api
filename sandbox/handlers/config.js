const invalidRoutingPlanId = "4ead415a-c033-4b39-9b05-326ac237a3be";
const trigger500SendingGroupId = "3bb82e6a-9873-4683-b2b9-fdf33c9ba86f";
const trigger425SendingGroupId = "d895ade5-0029-4fc3-9fb5-86e1e5370854";
const sendingGroupIdWithMissingTemplates = "c8857ccf-06ec-483f-9b3a-7fc732d9ad48";
const sendingGroupIdWithDuplicateTemplates = "a3a4e55d-7a21-45a6-9286-8eb595c872a8";
const sendingGroupIdWithMissingNHSTemplates = "aeb16ab8-cb9c-4d23-92e9-87c78119175c";
const validSendingGroupIds = {
    "b838b13c-f98c-4def-93f0-515d4e4f4ee1" : 1,
    "49e43b98-70cb-47a9-a55e-fe70c9a6f77c" : 1,
    "b402cd20-b62a-4357-8e02-2952959531c8" : 1,
    "936e9d45-15de-4a95-bb36-ae163c33ae53" : 1,
    "9ba00d23-cd6f-4aca-8688-00abc85a7980" : 1,
};
validSendingGroupIds[invalidRoutingPlanId] = 1;
validSendingGroupIds[sendingGroupIdWithMissingTemplates] = 1;
validSendingGroupIds[sendingGroupIdWithDuplicateTemplates] = 1;
validSendingGroupIds[trigger500SendingGroupId]= 1;
validSendingGroupIds[trigger425SendingGroupId]= 1;
validSendingGroupIds[sendingGroupIdWithMissingNHSTemplates] = 1;

const duplicateTemplates = [
    {
        name: "EMAIL_TEMPLATE",
        type: "EMAIL"
    },
    {
        name: "SMS_TEMPLATE",
        type: "SMS"
    },
    {
        name: "LETTER_TEMPLATE",
        type: "LETTER"
    },
    {
        name: "LETTER_PDF_TEMPLATE",
        type: "LETTER_PDF"
    },
    {
        name: "NHSAPP_TEMPLATE",
        type: "NHSAPP"
    }
];

module.exports = {
  invalidRoutingPlanId,
  trigger500SendingGroupId,
  trigger425SendingGroupId,
  sendingGroupIdWithMissingTemplates,
  sendingGroupIdWithDuplicateTemplates,
  sendingGroupIdWithMissingNHSTemplates,
  validSendingGroupIds,
  duplicateTemplates,
}
