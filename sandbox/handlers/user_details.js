import * as  fs from 'fs'
import { sendError } from './utils.js'

const paginationOdsCode = 'T00001';
const odsCodeRegex = new RegExp('^[A-Za-z]\\d{5}$|^[A-Za-z]\\d[A-Za-z]\\d[A-Za-z]$')

export async function user_details(req, res, next) {
  if (req.headers["authorization"] === "banned") {
    sendError(
      res,
      403,
      "Request rejected because client service ban is in effect"
    );
    next();
    return;
  }

  if (req.headers["authorization"] === "server_error") {
    sendError(
      res,
      500,
      "Something went wrong"
    );
    next();
    return;
  }

  if (req.headers["authorization"] === "rate_limit") {
    sendError(
      res,
      429,
      "Too many requests"
    );
    next();
    return;
  }

  const odsCode = req.params.odsCode.toUpperCase()

  if (!odsCodeRegex.test(odsCode) && odsCode !== 'X26') {
    sendError(res, 400, 'Invalid ODS Code')
    next()
    return;
  }

  const page = req.query?.page ?? '1'

  if (odsCode === paginationOdsCode) {
    fs.readFile(`./user-details/${page}.json`, 'utf-8', (err, fileContent) => {
      if (err) {
        sendError(res, 404, `Report not found`);
        next();
        return
      }
      res.type('json').status(200).send(fileContent)
    })
    return;
  }

  if (page !== '1') {
    sendError(res, 404, `Report not found`);
    next()
    return;
  }

  res.type('json').status(200).send(getDefaultResponse(odsCode))
}

function getDefaultResponse(odsCode) {
  return {
    data: [
      {
        id: "9074662803",
        type: "NhsAppAccount",
        attributes: {
          notificationsEnabled: true
        }
      },
      {
        id: "9903002157",
        type: "NhsAppAccount",
        attributes: {
          notificationsEnabled: false
        }
      }
    ],
    links: {
      last: `https://sandbox.api.service.nhs.uk/comms/v1/ods-organisation-codes/${odsCode}/nhs-app-accounts?page=1`,
      next: null,
      prev: null,
      self: `https://sandbox.api.service.nhs.uk/comms/v1/ods-organisation-codes/${odsCode}/nhs-app-accounts?page=1`
    },
    relationships: {
      "ods-organisation-code": {
        data: {
          id: odsCode,
          type: "OdsOrganisationCode"
        }
      }
    }
  }
}