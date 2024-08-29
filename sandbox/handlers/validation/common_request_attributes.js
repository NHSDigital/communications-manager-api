export function commonMandatoryRequestFieldValidation(body, expectedRequestType) {
    if (!body) {
        return [400, "Missing request body"]
      }
    
    const { data } = body;
    if (!data) {
        return [400, "Missing request body data"]
    }

    const { type, attributes } = data;
    if (!type) {
        return [400, "Missing request body data type"]
    }

    if (type !== expectedRequestType) {
        return [400, `Request body data type is not ${expectedRequestType}`]
    }

    if (!attributes) {
        return [400, "Missing request body data attributes"]
    }

    if (!attributes.routingPlanId) {
        return [400, "Missing routingPlanId"]
    }

    return null
}