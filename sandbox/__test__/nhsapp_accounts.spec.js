import request from "supertest"
import * as  fs from 'fs'
import { setup } from './helpers.js'

describe("/api/channels/nhsapp/accounts", () => {
    let env;
    let server;

    before(function () {
        env = process.env;
        server = setup();
    });

    after(function () {
        process.env = env;
        server.close();
    });

    it("returns a service ban (403) when the user is banned", (done) => {
        request(server)
            .get("/api/channels/nhsapp/accounts")
            .query({
                "ods-organisation-code": "X26"
            })
            .set({ Authorization: "banned" })
            .expect(403, {
                message: "Request rejected because client service ban is in effect.",
            })
            .expect("Content-Type", /json/, done);
    });

    it("returns a bad gateway (502) when unable to connect to the NHS App API", (done) => {
        request(server)
            .get("/api/channels/nhsapp/accounts")
            .query({
                "ods-organisation-code": "T00502"
            })
            .expect(502, {
                message: "bad gateway",
            })
            .expect("Content-Type", /json/, done);
    });

    describe('returns a 400 when given invalid ODS code', () => {
        const tests = [
            'X27',
            'R323',
            'Z000000',
            'TT000',
            '23414'
        ]

        tests.forEach((odsCode) => {
            it(`ODS code: ${odsCode}`, (done) => {
                request(server)
                    .get('/api/channels/nhsapp/accounts')
                    .query({
                        "ods-organisation-code": odsCode
                    })
                    .expect(400, {
                        message: "Invalid ODS Code"
                    })
                    .expect("Content-Type", /json/, done);
            });
        })
    })

    describe('returns a 400 when given invalid page number', () => {
        const tests = [
            0,
            -1,
            -20,
            'page1'
        ]

        tests.forEach((page) => {
            it(`Page: ${page}`, (done) => {
                request(server)
                    .get('/api/channels/nhsapp/accounts')
                    .query({
                        "ods-organisation-code": "X26",
                        "page": page
                    })
                    .expect(400, {
                        message: "page must be a positive non-zero integer"
                    })
                    .expect("Content-Type", /json/, done);
            });
        })
    })

    it('returns a 400 when ODS code not provided', (done) => {
        request(server)
            .get('/api/channels/nhsapp/accounts')
            .expect(400, {
                message: "Missing ODS Code"
            })
            .expect("Content-Type", /json/, done);
    })

    describe("returns a 200 and default response for valid ODS codes other than T00001", (done) => {
        const testCases = ['X26', 'T00002', 'X23201', 'A90001']

        testCases.forEach((odsCode) => {
            it(`ODS code: ${odsCode}`, (done) => {
                request(server)
                    .get('/api/channels/nhsapp/accounts')
                    .query({
                        "ods-organisation-code": odsCode
                    }).expect(200, {
                        data: {
                            id: odsCode,
                            type: 'NhsAppAccounts',
                            attributes: {
                                accounts: [
                                    {
                                        nhsNumber: "9074662803",
                                        notificationsEnabled: true

                                    },
                                    {
                                        nhsNumber: "9903002157",
                                        notificationsEnabled: false

                                    }
                                ]
                            }

                        },
                        links: {
                            last: `%PATH_ROOT%?ods-organisation-code=${odsCode}&page=1`,
                            self: `%PATH_ROOT%?ods-organisation-code=${odsCode}&page=1`,
                        },
                    })
                    .expect("Content-Type", /json/, done);
            })
        })
    })

    describe("returns a 200 and default response for valid ODS codes other than T00001 with page 1 for query param", (done) => {
        const testCases = ['X26', 'T00002', 'X23201', 'A90001']

        testCases.forEach((odsCode) => {
            it(`ODS code: ${odsCode}`, (done) => {
                request(server)
                    .get('/api/channels/nhsapp/accounts')
                    .query({
                        "ods-organisation-code": odsCode,
                        page: 1
                    })
                    .expect(200, {
                        data: {
                            id: odsCode,
                            type: 'NhsAppAccounts',
                            attributes: {
                                accounts: [
                                    {
                                        nhsNumber: "9074662803",
                                        notificationsEnabled: true

                                    },
                                    {
                                        nhsNumber: "9903002157",
                                        notificationsEnabled: false

                                    }
                                ]
                            }

                        },
                        links: {
                            last: `%PATH_ROOT%?ods-organisation-code=${odsCode}&page=1`,
                            self: `%PATH_ROOT%?ods-organisation-code=${odsCode}&page=1`,                        },
                    })
                    .expect("Content-Type", /json/, done);
            })
        })
    })

    describe("returns a 404 for valid ODS code other than T00001 when providing page query param", () => {
        const testCases = [7, 2, 4]

        testCases.forEach((pageNumber) => {
            it(`?page=${pageNumber}`, (done) => {
                request(server)
                    .get('/api/channels/nhsapp/accounts')
                    .query({
                        "ods-organisation-code": 'X26',
                        page: pageNumber
                    })
                    .expect(404, { message: 'Report not found' })
                    .expect("Content-Type", /json/, done);
            })
        })
    })

    it("returns 200 with first page result for T00001 ODS code when no page query provided", (done) => {
        request(server)
            .get('/api/channels/nhsapp/accounts')
            .query({
                "ods-organisation-code": 'T00001'
            })
            .expect(200, getResponse(1))
            .expect("Content-Type", /json/, done);
    })

    describe("returns 200 for T00001 ODS Code when providing valid page in query param", () => {
        const pageNumbers = [1, 2, 3, 4, 5, 6, 7, 8]

        pageNumbers.forEach((pageNumber) => {
            it(`?page=${pageNumber}`, (done) => {
                request(server)
                    .get('/api/channels/nhsapp/accounts')
                    .query({
                        "ods-organisation-code": 'T00001',
                        page: pageNumber
                    })
                    .expect(200, getResponse(pageNumber))
                    .expect("Content-Type", /json/, done);
            })
        })

    })

    describe("returns 404 for T00001 ODS code when providing page in query param does not exist ", () => {
        const pageNumbers = [9, 200]

        pageNumbers.forEach((pageNumber) => {
            it(`?page=${pageNumber}`, (done) => {
                request(server)
                    .get('/api/channels/nhsapp/accounts')
                    .query({
                        "ods-organisation-code": 'T00001',
                        page: pageNumber
                    })
                    .expect(404, { message: 'Report not found' })
                    .expect("Content-Type", /json/, done);
            })
        })
    })
})

function getResponse(page) {
    return fs.readFileSync(`./nhsapp-accounts/${page}.json`, 'utf-8', (err, fileContent) => {
        if (err) {
            throw err;
        }
        return fileContent
    })
}