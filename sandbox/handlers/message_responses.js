import { sendError } from './utils.js'

const notFoundMessageId = '00000000-0000-4000-8000-000000000404';
const supportedContentTypes = ['application/json', 'application/vnd.api+json'];

export async function messageResponses(req, res, next) {
  if (req.headers.authorization === 'banned') {
    res.status(403).json({ error: 'Forbidden' });
    next();
    return;
  }

  if (req.headers['content-type'] && !supportedContentTypes.includes(req.headers['content-type'])) {
    sendError(res, 415, 'Unsupported media type.');
    next();
    return;
  }

  if (req.headers.prefer === 'code=429') {
    res.status(429).json({
      errors: [
        {
          code: 'CM_QUOTA',
          status: '429',
          title: 'Too many requests',
          detail: 'You have made too many requests. Re-send the request after the time (in seconds) specified `Retry-After` header.'
        }
      ]
    });
    next();
    return;
  }

  const { messageId } = req.params;

  if (messageId === notFoundMessageId) {
    res.status(404).json({
      errors: [
        {
          code: 'CM_NOT_FOUND',
          status: '404',
          title: 'Resource not found',
          detail: 'The resource at the requested URI was not found.'
        }
      ]
    });
    next();
    return;
  }

  res.type('json').status(200).json(getDefaultResponse(messageId));
}

function getDefaultResponse(messageId) {
  return {
    data: [
      {
        type: 'RecipientResponse',
        id: '22222222-2222-4222-8222-222222222222',
        attributes: {
          messageId,
          messageReference: 'msg-ref-1',
          channel: 'nhsapp',
          channelStatus: 'delivered',
          cascadeType: 'primary',
          code: 'YES',
          authoredAt: '2026-01-02T09:00:00.000Z',
          timestamp: '2026-01-02T09:00:02.345Z'
        }
      },
      {
        type: 'RecipientResponse',
        id: '33333333-3333-4333-8333-333333333333',
        attributes: {
          messageId,
          messageReference: 'msg-ref-1',
          channel: 'nhsapp',
          channelStatus: 'delivered',
          cascadeType: 'secondary',
          code: 'NO',
          authoredAt: '2026-01-02T09:05:00.000Z',
          timestamp: '2026-01-02T09:05:01.678Z'
        }
      }
    ]
  };
}
