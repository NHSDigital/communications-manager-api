from selenium.webdriver.common.keys import Keys
from utils.locators import LoginPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LandingPage(object):
    def __init__(self, driver):
        # Initialize the LoginPage object with a WebDriver instance.
        self.driver = driver
        # Import the locators for this page.
        self.locator = LoginPageLocators

    def wait_for_element(self, element):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(element)
        )

    def page_title(self):
        self.wait_for_element(self.locator.TITLE)
        return self.driver.find_element(*self.locator.TITLE).text

    def click_continue(self):
        self.wait_for_element(self.locator.CONTINUE)
        self.driver.find_element(*self.locator.CONTINUE).send_keys(Keys.ENTER)
