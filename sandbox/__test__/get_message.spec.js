const request = require("supertest");
const assert = require("chai").assert;
const { setup } = require('./helpers')
const { get_message_test_data } = require('./data')

describe('/api/v1/messages/{messageId}', () => {
    let env;

    before(function () {
        env = process.env;
        server = setup()
    });

    after(function () {
        process.env = env;
        server.close();
    });

    it('returns a service ban (403) when the user is banned', (done) => {
        request(server)
            .get('/api/v1/messages/test-id-123')
            .set({ Authorization: 'banned' })
            .expect(403, {
                message: 'Request rejected because client service ban is in effect'
            })
            .expect("Content-Type", /json/, done);
    });
    it('returns a 404 when no message is found', (done) => {
        request(server)
            .get('/api/v1/messages/test-id-123')
            .expect(404, {
                message: `Message with id of test-id-123 not found`
            })
            .expect("Content-Type", /json/, done);
    });

    get_message_test_data.forEach(({ messageId, body }, i) => {
        it(`responds correctly ${i}`, (done) => {
            request(server)
                .get(`/api/v1/messages/${messageId}`)
                .expect(200)
                .expect((res) => {
                    assert.deepEqual(res.body, body);
                })
                .expect("Content-Type", /json/, done);
        });
    })
})
