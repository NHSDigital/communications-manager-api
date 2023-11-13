const { expect } = require("chai");
const request = require("supertest");
const assert = require("chai").assert;

const { setup } = require('./helpers')

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

    it('responds with a 201 when the request is correctly formatted', (done) => {
        request(server)
            .get('/api/v1/messages/test-id-123')
            .expect(201)
            .expect((res) => {
                const { id, attributes, links, relationships } = res.body.data
                assert.equal(id, "test-id-123");
                assert.equal(attributes.messageStatus, 'created');
                assert.notEqual(attributes.messageReference, undefined);
                assert.notEqual(attributes.routingPlan, undefined);
                assert.notEqual(attributes.channels, undefined);
                assert.notEqual(attributes.log, undefined);
                assert.notEqual(attributes.pdsMeta, undefined);
                assert.notEqual(attributes.timestamps.created, undefined);
                assert.notEqual(links.self, undefined);
                assert.equal(relationships.messageBatch.data.type, 'MessageBatch');
            })
            .expect("Content-Type", /json/, done);
    });
})
