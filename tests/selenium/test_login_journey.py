from base_test import BaseTest
from pages import LandingPage, EmailPage, PasswordPage, OtpPage, NhsAppHomePage
import os
email = os.environ.get("UAT_NHS_APP_USERNAME")
password = os.environ.get("UAT_NHS_APP_PASSWORD")
otp = os.environ.get("UAT_NHS_APP_OTP")
# Define a test class named TestLogin that inherits from BaseTest.
class TestLogin(BaseTest):
    
    def setUp(self):
        super().setUp()

    # Define the first test method, which tests login with valid user credentials.
    def test_login_with_valid_user(self):
        self.setUp()

        landing_page = LandingPage(self.driver)
        self.assertEqual("Access your NHS services", landing_page.page_title())
        landing_page.click_continue()

        email_page = EmailPage(self.driver)
        self.assertEqual("Enter your email address", email_page.page_title())
        email_page.enter_email(email)
        email_page.click_continue()

        password_page = PasswordPage(self.driver)
        self.assertEqual("Enter your password", password_page.page_title())
        password_page.enter_password(password)
        password_page.click_continue()


        otp_page = OtpPage(self.driver)
        self.assertEqual("Enter the security code", otp_page.page_title())
        otp_page.enter_otp(otp)
        otp_page.click_continue()

        nhsapp_home_page = NhsAppHomePage(self.driver)
        self.assertEqual("Access your NHS services any time, day or night", nhsapp_home_page.page_title())
