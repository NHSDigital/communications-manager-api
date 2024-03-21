import request from "supertest"
import * as fs from "fs"
import * as path from "path"
import { fileURLToPath } from 'url';
import { assert } from "chai";
import { setup } from './helpers.js'

function getMessageData() {
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = path.dirname(__filename);
    const directoryPath = path.join(__dirname, '../messages');
    let messagesArray = []; // Array to hold the result

    const files = fs.readdirSync(directoryPath)

    files.forEach(file => {
        let messageId = path.basename(file, '.json');

        const fileContent = fs.readFileSync(path.join(directoryPath, file), 'utf8')

        messagesArray.push({ messageId, response: JSON.parse(fileContent) });

    })
    return messagesArray
}
describe('/api/v1/messages/{messageId}', () => {
    let env;
    let server;

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

    getMessageData().forEach(({ messageId, response }, i) => {
        it(`responds correctly ${i}`, (done) => {
            request(server)
                .get(`/api/v1/messages/${messageId}`)
                .expect(200)
                .expect((res) => {
                    assert.deepEqual(res.body, response);
                })
                .expect("Content-Type", /json/, done);
        });
    })
})
