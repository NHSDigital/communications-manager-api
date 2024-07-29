const fs = require("fs");
const sinon = require("sinon");
const uuid = require("uuid");

const validationScripts = [
    fs.readFileSync("../../shared/resources/jsc/helpers/validationChecks.js").toString("utf8"),
    fs.readFileSync("../../shared/resources/jsc/helpers/validationErrors.js").toString("utf8"),
    fs.readFileSync("../../shared/resources/jsc/MessageBatches.Create.Validate.js").toString("utf8")
];
const validateScript = validationScripts.join("\n");
const context = {
    getVariable: () => {},
    setVariable: () => {},
};

const duplicateRef = uuid.v4();
const genDuplicateMessage = () => ({
        messageReference: duplicateRef,
        recipient: { nhsNumber: "9990548609" },
        personalisation: {}
    });

let flipFlopRef = null;
let flip = 0;
const genDuplicateFlipFlopMessage = () => {
    if (flip === 0) {
        flipFlopRef = uuid.v4();
    }

    const ret = {
        messageReference: `${flipFlopRef  }`,
        recipient: { nhsNumber: "9990548609" },
        personalisation: {}
    };

    if (flip === 0) {
        flip = 1;
    } else {
        flip = 0;
    }

    return ret;
};

const genMessage = () => ({
        messageReference: uuid.v4(),
        recipient: { nhsNumber: "9990548609" },
        personalisation: {}
    });

const generateBigMessage = (size, genFunction) => JSON.stringify({
      data: {
        type: "MessageBatch",
        attributes: {
          routingPlanId: "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
          messageBatchReference: "5450539c-3bfd-40bc-9c79-a19040797554",
          messages: Array.from(Array(size).keys()).map(genFunction)
        }
      }
    })

const testValidationPerformance = (runs) => {
    console.log("Generating big message....");
    console.time("message");
    const message = generateBigMessage(50000, genMessage);
    console.timeEnd("message");

    console.time("total");
    for (let i = 0; i < runs; i++) {
        const contextMock = sinon.mock(context);
        contextMock.expects("getVariable").once().withArgs("messageid").returns("apigee-message-id");
        contextMock.expects("getVariable").once().withArgs("request.content").returns(message);
        contextMock.expects("setVariable").once().withArgs("errors", null);

        console.time("validation");
        // this makes me just as sad as you
        eval(validateScript);
        console.timeEnd("validation");

        contextMock.verify();
    }
    console.timeEnd("total");
};

const testValidationDuplicatePerformance = (runs) => {
    console.log("Generating big message....");
    console.time("message");
    const message = generateBigMessage(50000, genDuplicateMessage);
    console.timeEnd("message");

    console.time("total");
    for (let i = 0; i < runs; i++) {
        const contextMock = sinon.mock(context);
        contextMock.expects("getVariable").once().withArgs("messageid").returns("apigee-message-id");
        contextMock.expects("getVariable").once().withArgs("request.content").returns(message);
        contextMock.expects("setVariable").once().withArgs("errors");

        console.time("validation");
        // this makes me just as sad as you
        eval(validateScript);
        console.timeEnd("validation");

        contextMock.verify();
    }
    console.timeEnd("total");
};

const testValidationDuplicateWorstCasePerformance = (runs) => {
    console.log("Generating big message....");
    console.time("message");
    const message = generateBigMessage(50000, genDuplicateFlipFlopMessage);
    console.timeEnd("message");

    console.time("total");
    for (let i = 0; i < runs; i++) {
        const contextMock = sinon.mock(context);
        contextMock.expects("getVariable").once().withArgs("messageid").returns("apigee-message-id");
        contextMock.expects("getVariable").once().withArgs("request.content").returns(message);
        contextMock.expects("setVariable").once().withArgs("errors");

        console.time("validation");
        // this makes me just as sad as you
        eval(validateScript);
        console.timeEnd("validation");

        contextMock.verify();
    }
    console.timeEnd("total");
};

testValidationPerformance(10);
testValidationDuplicatePerformance(10);
testValidationDuplicateWorstCasePerformance(10);
