const invalidRoutingPlanId = "4ead415a-c033-4b39-9b05-326ac237a3be";
const trigger500SendingGroupId = "3bb82e6a-9873-4683-b2b9-fdf33c9ba86f";
const trigger425SendingGroupId = "d895ade5-0029-4fc3-9fb5-86e1e5370854";
const sendingGroupIdWithMissingTemplates = "c8857ccf-06ec-483f-9b3a-7fc732d9ad48";
const sendingGroupIdWithDuplicateTemplates = "a3a4e55d-7a21-45a6-9286-8eb595c872a8";
const sendingGroupIdWithMissingNHSTemplates = "aeb16ab8-cb9c-4d23-92e9-87c78119175c";
const globalFreeTextNhsAppSendingGroupId = "00000000-0000-0000-0000-000000000001";
const validSendingGroupIds = {
    "b838b13c-f98c-4def-93f0-515d4e4f4ee1": "ztoe2qRAM8M8vS0bqajhyEBcvXacrGPp",
    "49e43b98-70cb-47a9-a55e-fe70c9a6f77c": "G.uwELAFAGMsKEBk2iIeRCBOB6kj6OkE",
    "b402cd20-b62a-4357-8e02-2952959531c8": "J7ZPQIf1yyUB4CiBpUBoy.1ahfOTCCQ7",
    "936e9d45-15de-4a95-bb36-ae163c33ae53": "riOAKoN4ajoVyUf9U2xwHVNRHc5V52A.",
    "9ba00d23-cd6f-4aca-8688-00abc85a7980": "nkz2osS_oc8IZ5GqeN_1yXKSXe9VEUjV",
};
validSendingGroupIds[invalidRoutingPlanId] = "c889ViFFlqtDdgV9E2KH.w58T5I71_x_";
validSendingGroupIds[sendingGroupIdWithMissingTemplates] = "EaSC3Wy4BC8Kuk.hZjI95F1f9mZIkP9l";
validSendingGroupIds[sendingGroupIdWithDuplicateTemplates] = "3t.Ofz4i.NO83.tBDLhRpyClu.sGCxTU";
validSendingGroupIds[trigger500SendingGroupId] = "Jc96S9y4AKjncXndUXiS7M7yIZ3jNtY1";
validSendingGroupIds[trigger425SendingGroupId] = "_oivtOz8fHRXhtZAyFxJmT2j_xpWzq9s";
validSendingGroupIds[sendingGroupIdWithMissingNHSTemplates] = "DjAAu455M2TMq0VKEaD_1WZfwjkspJDL";
validSendingGroupIds[globalFreeTextNhsAppSendingGroupId] = "odbGpMQvYRM7sp7jueU2lRHQiueKujVO";
const invalidEmailAddress = "invalidEmailAddress";

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

const noDefaultOdsClientAuth = "noDefaultOds";
const noOdsChangeClientAuth = "noOdsChange";
const notAllowedContactDetailOverride = "notAllowedContactDetailOverride"

export {
    invalidRoutingPlanId,
    trigger500SendingGroupId,
    trigger425SendingGroupId,
    sendingGroupIdWithMissingTemplates,
    sendingGroupIdWithDuplicateTemplates,
    sendingGroupIdWithMissingNHSTemplates,
    validSendingGroupIds,
    duplicateTemplates,
    globalFreeTextNhsAppSendingGroupId,
    noDefaultOdsClientAuth,
    noOdsChangeClientAuth,
    notAllowedContactDetailOverride,
    invalidEmailAddress
}
