import * as  fs from 'fs'
import { sendError } from './utils.js'

const paginationOdsCode = 'T00001';
const odsCodeRegex = new RegExp('^[A-Za-z]\\d{5}$|^[A-Za-z]\\d[A-Za-z]\\d[A-Za-z]$')

export async function user_details(req, res, next) {
  if (req.headers["authorization"] === "banned") {
    sendError(
      res,
      403,
      "Request rejected because client service ban is in effect."
    );
    next();
    return;
  }

  if (!req.query['ods-organisation-code']) {
    sendError(res, 400, 'ods-organisation-code not provided.')
    next()
    return;
  }

  const odsCode = req.query['ods-organisation-code'].toUpperCase()

  if (!odsCodeRegex.test(odsCode) && odsCode !== 'X26') {
    sendError(res, 400, 'Invalid ods-organisation-code value.')
    next()
    return;
  }

  const page = req.query?.page ?? '1'

  if (odsCode === paginationOdsCode) {
    fs.readFile(`./user-details/${page}.json`, 'utf-8', (err, fileContent) => {
      if (err) {
        sendError(res, 404, `Report not found.`);
        next();
        return
      }
      res.type('json').status(200).send(fileContent)
    })
    return;
  }

  if (page !== '1') {
    sendError(res, 404, `Report not found.`);
    next()
    return;
  }

  res.type('json').status(200).send(getDefaultResponse(odsCode))
}

function getDefaultResponse(odsCode) {
  return {
    data: {
      id: odsCode,
      type: "NHSAppAccounts",
      attributes: {
        accounts: [
          {
            nhsNumber: "9074662803",
            notificationsEnabled: true
          },
          {
            nhsNumber: "9903002157",
            notificationsEnabled: false
          }
        ]
      }
    },
    links: {
      last: `https://sandbox.api.service.nhs.uk/comms/v1/ods-organisation-codes/${odsCode}/nhs-app-accounts?page=1`,
      next: null,
      self: `https://sandbox.api.service.nhs.uk/comms/v1/ods-organisation-codes/${odsCode}/nhs-app-accounts?page=1`
    }
  }
}