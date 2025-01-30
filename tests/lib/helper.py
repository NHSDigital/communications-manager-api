import requests
import time
import os
import re
from install_playwright import install
from playwright.sync_api import expect, sync_playwright
from lib.constants.messages_paths import MESSAGES_ENDPOINT
from lib import error_handler

DEFAULT_CONTENT_TYPE = "application/vnd.api+json"


class Helper():
    @staticmethod
    def send_single_message(url, auth, body):
        resp = requests.post(f"{url}{MESSAGES_ENDPOINT}", headers={
                **auth,
                "Accept": DEFAULT_CONTENT_TYPE,
                "Content-Type": DEFAULT_CONTENT_TYPE
            }, json=body
        )
        error_handler.handle_retry(resp)
        assert resp.status_code == 201
        return resp

    @staticmethod
    def get_message(url, auth, message_id):
        resp = requests.get(f"{url}{MESSAGES_ENDPOINT}/{message_id}", headers={
            **auth,
            "Accept": DEFAULT_CONTENT_TYPE
        })
        error_handler.handle_retry(resp)
        assert resp.status_code == 200
        return resp

    @staticmethod
    def poll_get_message(url, auth, message_id, end_state="delivered", poll_time=300):
        message_status = None
        end_time = int(time.time()) + poll_time

        while message_status != end_state and int(time.time()) < end_time:
            get_message_response = requests.get(
                f"{url}{MESSAGES_ENDPOINT}/{message_id}",
                headers={
                    **auth,
                    "Accept": DEFAULT_CONTENT_TYPE
                },
            )

            if get_message_response.status_code == 200:
                message_status = get_message_response.json().get("data").get("attributes").get("messageStatus")
            time.sleep(10)

            if message_status == "failed":
                raise ValueError(f"Request ended up in an unexpected state. \
                                 Message status: {message_status}, Message ID: {message_id}")

        if message_status != end_state:
            raise TimeoutError(f"Request took too long to be processed. \
                               Message status: {message_status}, Message ID: {message_id}")

    @staticmethod
    def nhs_app_login_and_view_message(personalisation):
        email = os.environ.get("UAT_NHS_APP_USERNAME")
        password = os.environ.get("UAT_NHS_APP_PASSWORD")
        otp = os.environ.get("UAT_NHS_APP_OTP")

        with sync_playwright() as playwright:
            install(playwright.chromium)
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.set_default_timeout(15000)
            expect.set_options(timeout=15000)

            page.goto("https://www-onboardingaos.nhsapp.service.nhs.uk/login")

            expect(page.get_by_role("heading", name="Access your NHS services")).to_be_visible()
            page.get_by_role("button", name="Continue").click()

            expect(page.get_by_role("heading", name="Enter your email address")).to_be_visible()
            page.get_by_label("Email address", exact=True).fill(email)
            page.get_by_role("button", name="Continue").click()

            expect(page.get_by_role("heading", name="Enter your password")).to_be_visible()
            page.get_by_label("Password", exact=True).fill(password)
            page.get_by_role("button", name="Continue").click()

            expect(page.get_by_role("heading", name="Enter the security code")).to_be_visible()
            page.get_by_label("Security code", exact=True).fill(otp)
            page.get_by_role("button", name="Continue").click()

            page.wait_for_url('**/patient/')

            expect(page.get_by_text('NHS number: 973 061')).to_be_visible()
            link_text = re.compile(r"You have \d+ unread messages")
            page.get_by_role("link", name=link_text).click()

            expect(page.get_by_role("heading", name="Messages")).to_be_visible()
            page.get_by_role("link", name="Your NHS healthcare services").click()

            expect(page.get_by_role("heading", name="Your messages")).to_be_visible()

            # There might several unread messages, we need to select the right one
            page.locator(f'text="APIM end to end test: {personalisation} "').locator("..") \
                .locator("..").get_by_label("Unread message from NHS").click()

            page.wait_for_url("**/patient/messages/app-messaging/app-message?messageId=**")
            expect(page.get_by_role("heading", name="NHS ENGLAND - X26")).to_be_visible()
            expect(page.get_by_text(f"APIM end to end test: {personalisation}")).to_be_visible()
