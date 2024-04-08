import request from "supertest"
import * as  fs from 'fs'
import { setup } from './helpers.js'

describe("/api/v1/ods-organisation-code/{odsCode}/nhsapp-user-details", () => {
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
            .get("/api/v1/ods-organisation-code/X26/nhsapp-user-details")
            .set({ Authorization: "banned" })
            .expect(403, {
                message: "Request rejected because client service ban is in effect",
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
                    .get(`/api/v1/ods-organisation-code/${odsCode}/nhsapp-user-details`)
                    .expect(400, {
                        message: "Invalid ODS Code"
                    })
                    .expect("Content-Type", /json/, done);
            });
        })
    })

    describe("returns a 200 and default response for valid ODS codes other than T00001", (done) => {
        const testCases = ['X26', 'T00002', 'X23201', 'A90001']

        testCases.forEach((odsCode) => {
            it(`ODS code: ${odsCode}`, (done) => {
                request(server)
                    .get(`/api/v1/ods-organisation-code/${odsCode}/nhsapp-user-details`)
                    .expect(200, {
                        data: [
                            {
                                id: "9074662803",
                                type: "NhsAppAccount",
                                attributes: {
                                    notificationsEnabled: true
                                }
                            },
                            {
                                id: "9903002157",
                                type: "NhsAppAccount",
                                attributes: {
                                    notificationsEnabled: false
                                }
                            }
                        ],
                        links: {
                            last: `https://sandbox.api.service.nhs.uk/comms/v1/ods-organisation-codes/${odsCode}/nhs-app-accounts?page=1`,
                            next: null,
                            prev: null,
                            self: `https://sandbox.api.service.nhs.uk/comms/v1/ods-organisation-codes/${odsCode}/nhs-app-accounts?page=1`
                        },
                        relationships: {
                            "ods-organisation-code": {
                                data: {
                                    id: `${odsCode}`,
                                    type: "OdsOrganisationCode"
                                }
                            }
                        }
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
                    .get(`/api/v1/ods-organisation-code/${odsCode}/nhsapp-user-details?page=1`)
                    .expect(200, {
                        data: [
                            {
                                id: "9074662803",
                                type: "NhsAppAccount",
                                attributes: {
                                    notificationsEnabled: true
                                }
                            },
                            {
                                id: "9903002157",
                                type: "NhsAppAccount",
                                attributes: {
                                    notificationsEnabled: false
                                }
                            }
                        ],
                        links: {
                            last: `https://sandbox.api.service.nhs.uk/comms/v1/ods-organisation-codes/${odsCode}/nhs-app-accounts?page=1`,
                            next: null,
                            prev: null,
                            self: `https://sandbox.api.service.nhs.uk/comms/v1/ods-organisation-codes/${odsCode}/nhs-app-accounts?page=1`
                        },
                        relationships: {
                            "ods-organisation-code": {
                                data: {
                                    id: `${odsCode}`,
                                    type: "OdsOrganisationCode"
                                }
                            }
                        }
                    })
                    .expect("Content-Type", /json/, done);
            })
        })
    })

    describe("returns a 404 for valid ODS code other than T00001 when providing page query param", () => {
        const testCases = [7, 2, 4, 0, 'page1']

        testCases.forEach((pageNumber) => {
            it(`?page=${pageNumber}`, (done) => {
                request(server)
                    .get(`/api/v1/ods-organisation-code/X26/nhsapp-user-details?page=${pageNumber}`)
                    .expect(404, { message: 'Report not found' })
                    .expect("Content-Type", /json/, done);
            })
        })
    })

    it("returns 200 with first page result for T00001 ODS code when no page query provided", (done) => {
        request(server)
            .get("/api/v1/ods-organisation-code/T00001/nhsapp-user-details")
            .expect(200, getResponse(1))
            .expect("Content-Type", /json/, done);
    })

    describe("returns 200 for T00001 ODS Code when providing valid page in query param", () => {
        const pageNumbers = [1, 2, 3, 4, 5, 6, 7, 8]

        pageNumbers.forEach((pageNumber) => {
            it(`?page=${pageNumber}`, (done) => {
                request(server)
                    .get(`/api/v1/ods-organisation-code/T00001/nhsapp-user-details?page=${pageNumber}`)
                    .expect(200, getResponse(pageNumber))
                    .expect("Content-Type", /json/, done);
            })
        })

    })

    describe("returns 404 for T00001 ODS code when providing page in query param does not exist ", () => {
        const pageNumbers = [0, 9, 'page1']

        pageNumbers.forEach((pageNumber) => {
            it(`?page=${pageNumber}`, (done) => {
                request(server)
                    .get(`/api/v1/ods-organisation-code/T00001/nhsapp-user-details?page=${pageNumber}`)
                    .expect(404, { message: 'Report not found' })
                    .expect("Content-Type", /json/, done);
            })
        })
    })
})

function getResponse(page) {
    return fs.readFileSync(`./user-details/${page}.json`, 'utf-8', (err, fileContent) => {
        if (err) {
            throw err;
        }
        return fileContent
    })
}