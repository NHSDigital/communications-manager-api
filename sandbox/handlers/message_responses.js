import { sendError } from './utils.js'

const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

const notFoundMessageId = '00000000-0000-4000-8000-000000000404';
const tooManyResponsesMessageId = '00000000-0000-4000-8000-000000000422';

export async function messageResponses(req, res, next) {
  if (req.headers.authorization === 'banned') {
    res.status(403).json({ error: 'Forbidden' });
    next();
    return;
  }

  if (req.headers['content-type'] && req.headers['content-type'] !== 'application/json') {
    sendError(res, 415, 'Unsupported media type.');
    next();
    return;
  }

  if (req.headers.prefer === 'code=429') {
    sendError(res, 429, 'Too many requests.');
    next();
    return;
  }

  const { messageId } = req.params;

  if (!uuidRegex.test(messageId)) {
    res.status(400).json({ error: 'Invalid messageId format' });
    next();
    return;
  }

  if (messageId === notFoundMessageId) {
    res.status(404).json({ error: 'No responses found for the specified messageId' });
    next();
    return;
  }

  if (messageId === tooManyResponsesMessageId) {
    res.status(422).json({
      error: 'response_too_large',
      message: 'There are too many responses to return.'
    });
    next();
    return;
  }

  res.type('json').status(200).json(getDefaultResponse(messageId));
}

function getDefaultResponse(messageId) {
  return [
    {
      responseId: '22222222-2222-4222-8222-222222222222',
      messageId,
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
      messageId,
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
