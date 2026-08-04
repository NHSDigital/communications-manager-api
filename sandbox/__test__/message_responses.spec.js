import request from "supertest"
import * as uuid from 'uuid';
import { setup } from './helpers.js'

const VALID_MESSAGE_ID = '11111111-1111-4111-8111-111111111111';
const NOT_FOUND_MESSAGE_ID = '00000000-0000-4000-8000-000000000404';
const BAD_GATEWAY_MESSAGE_ID = '00000000-0000-4000-8000-000000000502';
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
                message: 'Request rejected because client service ban is in effect.'
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 400 when messageId is not a UUID', (done) => {
        request(server)
            .get('/api/v1/message-responses/not-a-valid-uuid')
            .expect(400, {
                message: 'Invalid message ID format. messageId must be a UUID.'
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 404 when no responses are found', (done) => {
        request(server)
            .get(`/api/v1/message-responses/${NOT_FOUND_MESSAGE_ID}`)
            .expect(404, {
                message: 'No responses found for the given messageId.'
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 500 when too many responses are returned', (done) => {
        request(server)
            .get(`/api/v1/message-responses/${TOO_MANY_RESPONSES_MESSAGE_ID}`)
            .expect(500, {
                message: 'Too many responses returned for this messageId.'
            })
            .expect('Content-Type', /json/, done);
    });

    it('returns a 502 when a bad gateway error occurs', (done) => {
        request(server)
            .get(`/api/v1/message-responses/${BAD_GATEWAY_MESSAGE_ID}`)
            .expect(502, {
                message: 'Bad Gateway'
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
                if (!body.messageId) throw new Error('missing messageId');
                if (body.messageId !== VALID_MESSAGE_ID) throw new Error('incorrect messageId');
                if (!Array.isArray(body.responses)) throw new Error('responses must be an array');
                const first = body.responses[0];
                if (!first.responseId) throw new Error('missing responseId');
                if (!first.code) throw new Error('missing code');
                if (!first.channel) throw new Error('missing channel');
                if (!first.channelStatus) throw new Error('missing channelStatus');
                if (!first.authoredAt) throw new Error('missing authoredAt');
            })
            .end(done);
    });
});
