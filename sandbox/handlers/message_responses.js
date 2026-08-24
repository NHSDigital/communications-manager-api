const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

const notFoundMessageId = '00000000-0000-4000-8000-000000000404';
const tooManyResponsesMessageId = '00000000-0000-4000-8000-000000000500';
const supportedContentTypes = ['application/json', 'application/vnd.api+json'];

export async function messageResponses(req, res, next) {
  if (req.headers.authorization === 'banned') {
    res.status(403).json({
      errors: [
        {
          code: 'CM_FORBIDDEN',
          status: '403',
          title: 'Forbidden',
          detail: 'Client not recognised or not yet onboarded.'
        }
      ]
    });
    next();
    return;
  }

  if (req.headers['content-type'] && !supportedContentTypes.includes(req.headers['content-type'])) {
    res.status(415).json({
      errors: [
        {
          code: 'CM_UNSUPPORTED_MEDIA',
          status: '415',
          title: 'Unsupported media',
          detail: 'Invalid content-type, this API only supports application/vnd.api+json or application/json.',
          source: { header: 'Content-Type' }
        }
      ]
    });
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

  if (!uuidRegex.test(messageId)) {
    res.status(400).json({
      errors: [
        {
          code: 'CM_INVALID_REQUEST',
          status: '400',
          title: 'Invalid Request',
          detail: 'The messageId path parameter is not a valid UUID.',
          source: { parameter: 'messageId' }
        }
      ]
    });
    next();
    return;
  }

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

  if (messageId === tooManyResponsesMessageId) {
    res.status(500).json({
      errors: [
        {
          code: 'CM_TOO_MANY_RESPONSES',
          status: '500',
          title: 'Too many responses',
          detail: 'There are too many responses to return.'
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
        type: 'RecipientResponseSnapshot',
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
        type: 'RecipientResponseSnapshot',
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
