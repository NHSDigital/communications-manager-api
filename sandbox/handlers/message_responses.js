import { sendError } from './utils.js'

const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

const notFoundMessageId = '00000000-0000-4000-8000-000000000404';
const badGatewayMessageId = '00000000-0000-4000-8000-000000000502';
const tooManyResponsesMessageId = '00000000-0000-4000-8000-000000000500';

export async function messageResponses(req, res, next) {
  if (req.headers.authorization === 'banned') {
    sendError(res, 403, 'Request rejected because client service ban is in effect.');
    next();
    return;
  }

  const { messageId } = req.params;

  if (!uuidRegex.test(messageId)) {
    sendError(res, 400, 'Invalid message ID format. messageId must be a UUID.');
    next();
    return;
  }

  if (messageId === badGatewayMessageId) {
    sendError(res, 502, 'Bad Gateway');
    next();
    return;
  }

  if (messageId === notFoundMessageId) {
    sendError(res, 404, 'No responses found for the given messageId.');
    next();
    return;
  }

  if (messageId === tooManyResponsesMessageId) {
    sendError(res, 500, 'Too many responses returned for this messageId.');
    next();
    return;
  }

  res.type('json').status(200).json(getDefaultResponse());
}

function getDefaultResponse() {
  return [
    {
      responseId: '22222222-2222-4222-8222-222222222222',
      messageId: '2WL3qFTEFM0qMY8xjRbt1LIKCzM',
      messageReference: 'msg-ref-1',
      channel: 'nhsapp',
      channelStatus: 'delivered',
      cascadeType: 'primary',
      code: 'YES',
      authoredAt: '2026-01-02T09:00:00.000Z',
      timestamp: '2026-01-02T09:00:02.345Z'
    },
    {
      responseId: '33333333-3333-4333-8333-333333333333',
      messageId: '2WL3qFTEFM0qMY8xjRbt1LIKCzM',
      messageReference: 'msg-ref-1',
      channel: 'nhsapp',
      channelStatus: 'delivered',
      cascadeType: 'secondary',
      code: 'NO',
      authoredAt: '2026-01-02T09:05:00.000Z',
      timestamp: '2026-01-02T09:05:01.678Z'
    }
  ];
}
