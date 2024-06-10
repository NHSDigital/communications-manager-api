import * as  fs from 'fs'
import { sendError } from './utils.js'

const paginationOdsCode = 'T00001';
const odsCodeRegex = new RegExp('^[A-Za-z]\\d{5}$|^[A-Za-z]\\d[A-Za-z]\\d[A-Za-z]$')
const badGatewayOdsCode = 'T00502'; // simulates something going wrong between the BE and the NHS APP API'
const notFoundOdsCode = 'T00404'; // valid format but no data stored against it

export async function nhsapp_accounts(req, res, next) {
  if (req.headers["authorization"] === "banned") {
    sendError(
      res,
      403,
      "Request rejected because client service ban is in effect."
    );
    next();
    return;
  }

  if (!req.query || !req.query['ods-organisation-code']) {
    sendError(res, 400, 'Missing ODS Code')
    next()
    return;
  }

  const odsCode = req.query['ods-organisation-code'].toUpperCase()

  if (odsCode === badGatewayOdsCode) {
    sendError(res, 502, 'bad gateway')
    next()
    return;
  }

  if (odsCode === notFoundOdsCode) {
    sendError(res, 404, 'Report not found')
    next()
    return;
  }

  if (!odsCodeRegex.test(odsCode) && odsCode !== 'X26') {
    sendError(res, 400, 'Invalid ODS Code')
    next()
    return;
  }

  let page = '1'

  if (req.query.page) {
    const pageNumber = Number(req.query.page)

    if (isNaN(pageNumber) || pageNumber <= 0) {
      sendError(res, 400, 'page must be a positive non-zero integer')
      next()
      return;
    }

    page = req.query.page
  }

  if (odsCode === paginationOdsCode) {
    fs.readFile(`./nhsapp-accounts/${page}.json`, 'utf-8', (err, fileContent) => {
      if (err) {
        sendError(res, 404, 'Report not found');
        next();
        return
      }
      res.type('json').status(200).send(fileContent)
    })
    return;
  }

  if (page !== '1') {
    sendError(res, 404, 'Report not found');
    next()
    return;
  }

  res.type('json').status(200).send(getDefaultResponse(odsCode))
}

function getDefaultResponse(odsCode) {
  return {
    data: {
      id: odsCode,
      type: "NhsAppAccounts",
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
      last: `%PATH_ROOT%?ods-organisation-code=${odsCode}&page=1`,
      self: `%PATH_ROOT%?ods-organisation-code=${odsCode}&page=1`
    }
  }
}