from utils.locators import NhsAppMessagesHomePageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NhsAppMessagesHomePage(object):
    def __init__(self, driver):
        # Initialize the LoginPage object with a WebDriver instance.
        self.driver = driver
        # Import the locators for this page.
        self.locator = NhsAppMessagesHomePageLocators

    def wait_for_element(self, element):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(element)
        )

    def page_title(self):
        self.wait_for_element(self.locator.TITLE)
        return self.driver.find_element(*self.locator.TITLE).text
    
    def click_messages_link(self):
        self.wait_for_element(self.locator.MESSAGES_LINK)
        self.driver.find_element(*self.locator.MESSAGES_LINK).click()

