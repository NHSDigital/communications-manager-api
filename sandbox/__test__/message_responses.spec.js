import request from "supertest"
import * as uuid from 'uuid';
import { setup } from './helpers.js'

const VALID_MESSAGE_ID = '11111111-1111-4111-8111-111111111111';
const NOT_FOUND_MESSAGE_ID = '00000000-0000-4000-8000-000000000404';
const TOO_MANY_RESPONSES_MESSAGE_ID = '00000000-0000-4000-8000-000000000500';

describe('/api/v1/message-responses/:messageId', () => {
    let env;
    let server;

    beforeEach(() => {
        env = process.env;
        server = setup();
    });

    afterEach(() => {
        process.env = env;
        server.close();
    });

    it('returns a X-Correlation-Id when provided', (done) => {
        const correlationId = uuid.v4();
        request(server)
            .get(`/api/v1/message-responses/${VALID_MESSAGE_ID}`)
            .set('X-Correlation-Id', correlationId)
            .expect(200)
            .expect('X-Correlation-Id', correlationId, done);
    });

    it('returns a service ban (403) when the user is banned', (done) => {
        request(server)
            .get(`/api/v1/message-responses/${VALID_MESSAGE_ID}`)
            .set({ Authorization: 'banned' })
            .expect(403, {
                error: 'Forbidden'
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 400 when messageId is not a UUID', (done) => {
        request(server)
            .get('/api/v1/message-responses/not-a-valid-uuid')
            .expect(400, {
                errors: [
                    {
                        code: 'CM_INVALID_REQUEST',
                        status: '400',
                        title: 'Invalid Request',
                        detail: 'The messageId path parameter is not a valid UUID.',
                        source: { parameter: 'messageId' }
                    }
                ]
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 404 when no responses are found', (done) => {
        request(server)
            .get(`/api/v1/message-responses/${NOT_FOUND_MESSAGE_ID}`)
            .expect(404, {
                errors: [
                    {
                        code: 'CM_NOT_FOUND',
                        status: '404',
                        title: 'Resource not found',
                        detail: 'The resource at the requested URI was not found.'
                    }
                ]
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 500 when too many responses are returned', (done) => {
        request(server)
            .get(`/api/v1/message-responses/${TOO_MANY_RESPONSES_MESSAGE_ID}`)
            .expect(500, {
                errors: [
                    {
                        code: 'CM_TOO_MANY_RESPONSES',
                        status: '500',
                        title: 'Too many responses',
                        detail: 'There are too many responses to return.'
                    }
                ]
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 415 when the content type is not supported', (done) => {
        request(server)
            .get(`/api/v1/message-responses/${VALID_MESSAGE_ID}`)
            .set('Content-Type', 'text/plain')
            .expect(415, {
                message: 'Unsupported media type.'
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 429 when the request is rate limited', (done) => {
        request(server)
            .get(`/api/v1/message-responses/${VALID_MESSAGE_ID}`)
            .set('Prefer', 'code=429')
            .expect(429, {
                errors: [
                    {
                        code: 'CM_QUOTA',
                        status: '429',
                        title: 'Too many requests',
                        detail: 'You have made too many requests. Re-send the request after the time (in seconds) specified `Retry-After` header.'
                    }
                ]
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 200 with correct response structure for a valid messageId', (done) => {
        request(server)
            .get(`/api/v1/message-responses/${VALID_MESSAGE_ID}`)
            .expect(200)
            .expect('Content-Type', /json/)
            .expect((res) => {
                const { body } = res;
                if (!Array.isArray(body.data)) throw new Error('response must contain a data array');
                const first = body.data[0];
                if (!first.id) throw new Error('missing id');
                if (first.type !== 'RecipientResponseSnapshot') throw new Error('incorrect type');
                const { attributes } = first;
                if (attributes.messageId !== VALID_MESSAGE_ID) throw new Error('incorrect messageId');
                if (!attributes.messageReference) throw new Error('missing messageReference');
                if (!attributes.code) throw new Error('missing code');
                if (!attributes.channel) throw new Error('missing channel');
                if (!attributes.channelStatus) throw new Error('missing channelStatus');
                if (!attributes.cascadeType) throw new Error('missing cascadeType');
                if (!attributes.authoredAt) throw new Error('missing authoredAt');
                if (!attributes.timestamp) throw new Error('missing timestamp');
            })
            .end(done);
    });
});
