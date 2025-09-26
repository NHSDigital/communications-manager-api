from urllib.parse import urlparse, parse_qs


def get_page_number_from_url(url: str) -> int:
    """Extract the 'page' query parameter as an integer from a URL."""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    return int(query_params["page"][0])


def assert_ods_code(resp, expected_ods_code):
    actual_ods_code = resp.json().get("data").get("id")
    assert actual_ods_code is not None
    assert actual_ods_code == expected_ods_code


def assert_accounts(resp):
    accounts = resp.json().get("data").get("attributes").get("accounts")
    assert accounts is not None
    assert len(accounts) > 0
    for i in range(len(accounts)):
        assert accounts[i].get("nhsNumber") is not None
        assert accounts[i].get("nhsNumber") != ""
        assert accounts[i].get("notificationsEnabled") is not None


def assert_self_link(resp, base_url, ods_code, page):
    self_link = resp.json().get("links").get("self")
    assert self_link.startswith(base_url)
    assert self_link.endswith(
        f"/channels/nhsapp/accounts?ods-organisation-code={ods_code}&page={page}"
    )


def assert_last_link(resp, base_url, ods_code, last_page_number):
    last_link = resp.json().get("links").get("last")
    assert last_link.startswith(base_url)
    assert last_link.endswith(
        f"/channels/nhsapp/accounts?ods-organisation-code={ods_code}&page={last_page_number}"
    )


def assert_next_link(resp, base_url, ods_code, self_page_number, last_page_number):
    next_link = resp.json().get("links").get("next")
    if self_page_number == last_page_number:
        assert next_link is None
    else:
        next_page_number = self_page_number + 1
        assert next_link.startswith(base_url)
        assert next_link.endswith(
            f"/channels/nhsapp/accounts?ods-organisation-code={ods_code}&page={next_page_number}"
        )
