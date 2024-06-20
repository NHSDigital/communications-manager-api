NHSAPP_ACCOUNTS_ENDPOINT = "/channels/nhsapp/accounts"
ODS_CODE_PARAM_NAME = "ods-organisation-code"
PAGE_PARAM_NAME = "page"

SINGLE_PAGE_ODS_CODES = [
    "X26",
    "Y00001",
    "X12345"
]

MULTIPLE_PAGES_ODS_CODES = [
    "T00001"
]

INVALID_ODS_CODES = [
    "NOT_A_VALID_CODE",
    "X25",
    "Y123456"
]

INVALID_PAGES = [
    "page1",
    0,
    -1,
    -20
]

LIVE_ODS_CODES = [
    "X26"
]

VALID_MULTI_PAGE_NUMBERS = [None, 1, 2, 3, 4, 5, 6, 7, 8]
MULTI_LAST_PAGE = 8
VALID_SINGLE_PAGE_NUMBERS = [None, 1]

CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
