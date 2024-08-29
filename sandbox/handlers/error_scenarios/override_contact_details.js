import {
    allowedContactDetailOverride,
  } from "../config.js"

const invalidPhoneNumber = '07700900002'
const invalidEmailAddress = 'perm-fail@simulator.notify'

export function getAlternateContactDetailsError(contactDetails, authorizationHeader, path) {
  if (!contactDetails) {
    return null;
  }
  
  if (contactDetails && authorizationHeader !== allowedContactDetailOverride) {
    return [
      400,
      'Client is not allowed to provide alternative contact details'
    ]
  }

  const validationErrorMessages = ['Invalid recipient contact details']
  const validationErrors = []

  if (contactDetails.sms) {
    if (contactDetails.sms === invalidPhoneNumber) {
      validationErrors.push({
          title: 'Invalid value',
          field: `${path}/recipient/contactDetails/sms`,
          message: 'Input failed format check'
      })
      validationErrorMessages.push(`Field 'sms': Input failed format check`)
    }
    else if (typeof contactDetails.sms !== 'string') {
      validationErrors.push({
          title: 'Invalid value',
          field: `${path}/recipient/contactDetails/sms`,
          message: 'Input is not a string'
      })
      validationErrorMessages.push(`Field 'sms': Input is not a string`)
    }
  }

  if (contactDetails.email) {
    if (contactDetails.email === invalidEmailAddress) {
      validationErrors.push({
          title: 'Invalid value',
          field: `${path}/recipient/contactDetails/email`,
          message: 'Input failed format check'
      })
      validationErrorMessages.push(`Field 'email': Input failed format check`)
    }
    if (typeof contactDetails.email !== 'string') {
      validationErrors.push({
          title: 'Invalid value',
          field: `${path}/recipient/contactDetails/email`,
          message: 'Input is not a string'
      })
      validationErrorMessages.push(`Field 'email': Input is not a string`)
    }
  }

  if (contactDetails.address) {
    if (typeof contactDetails.address !== 'object' || Array.isArray(contactDetails.address)) {
      validationErrors.push({
          title: 'Invalid value',
          field: `${path}/recipient/contactDetails/address`,
          message: 'Input is not an object'
      })
      validationErrorMessages.push(`Field 'address': Input is not an object`)
    }
    else {
      if (contactDetails.address.lines) {
        if (Array.isArray(contactDetails.address.lines)) {
          if (contactDetails.address.lines.some((line) => typeof line !== 'string')) {
            validationErrors.push({
                title: 'Invalid value',
                field: `${path}/recipient/contactDetails/address/lines`,
                message: 'Lines contain non-string or empty line' 
            })
            validationErrorMessages.push(`Field 'lines': Lines contain non-string or empty line`)
          }
          if (contactDetails.address.lines.length < 2) {
            validationErrors.push({
                title: 'Invalid value',
                field: `${path}/recipient/contactDetails/address/lines`,
                message: 'Too few address lines were provided' 
            })
            validationErrorMessages.push(`Field 'lines': Too few address lines were provided`)
          }
          if (contactDetails.address.lines.length > 5) {
            validationErrors.push({
                title: 'Invalid value',
                field: `${path}/recipient/contactDetails/address/lines`,
                message: 'Too many address lines were provided' 
            })
            validationErrorMessages.push(`Field 'lines': Too many address lines were provided`)
          }
        }
        else {
          validationErrors.push({
            title: 'Missing value',
            field: `${path}/recipient/contactDetails/address/lines`,
            message: '`lines` is missing' 
          })
          validationErrorMessages.push(`Field 'lines': 'lines' is missing`)
        }
      }
      else {
        validationErrors.push({
          title: 'Missing value',
          field: `${path}/recipient/contactDetails/address/lines`,
          message: '`lines` is missing' 
        })
        validationErrorMessages.push(`Field 'lines': 'lines' is missing`)
      }

      if (contactDetails.address.postcode) {
        if (typeof contactDetails.address.postcode !== 'string') {
          validationErrors.push({
            title: 'Invalid value',
            field: `${path}/recipient/contactDetails/address/postcode`,
            message: `'postcode' is not a string`
          })
          validationErrorMessages.push(`Field 'postcode': 'postcode' is not a string`)
        }
      }
      else {
        validationErrors.push({
          title: 'Missing value',
          field: `${path}/recipient/contactDetails/address/postcode`,
          message: '`postcode` is missing' 
        })
        validationErrorMessages.push(`Field 'postcode': 'postcode' is missing`)
      }
    }
    
  }

  if (validationErrors.length) {
    return [400, validationErrorMessages.join('. '), validationErrors]
  }
  
  return null;
}