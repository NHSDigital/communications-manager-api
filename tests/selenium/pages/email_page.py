from selenium.webdriver.common.keys import Keys
from utils.locators import EmailPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EmailPage(object):
    def __init__(self, driver):
        # Initialize the LoginPage object with a WebDriver instance.
        self.driver = driver
        # Import the locators for this page.
        self.locator = EmailPageLocators

    def wait_for_element(self, element):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(element)
        )

    def page_title(self):
        self.wait_for_element(self.locator.TITLE)
        return self.driver.find_element(*self.locator.TITLE).text

    def enter_email(self, email):
        self.wait_for_element(self.locator.EMAIL_TEXT_BOX)
        self.driver.find_element(*self.locator.EMAIL_TEXT_BOX).send_keys(email)

    def click_continue(self):
        self.wait_for_element(self.locator.CONTINUE)
        self.driver.find_element(*self.locator.CONTINUE).send_keys(Keys.ENTER)
