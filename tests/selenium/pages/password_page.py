from selenium.webdriver.common.keys import Keys
from utils.locators import PasswordPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PasswordPage(object):
    def __init__(self, driver):
        # Initialize the LoginPage object with a WebDriver instance.
        self.driver = driver
        # Import the locators for this page.
        self.locator = PasswordPageLocators

    def wait_for_element(self, element):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(element)
        )
    
    def page_title(self):
        self.wait_for_element(self.locator.TITLE)
        return self.driver.find_element(*self.locator.TITLE).text

    def enter_password(self, password):
        self.wait_for_element(self.locator.PASSWORD_TEXT_BOX)
        self.driver.find_element(*self.locator.PASSWORD_TEXT_BOX).send_keys(password)

    def click_continue(self):
        self.wait_for_element(self.locator.CONTINUE)
        self.driver.find_element(*self.locator.CONTINUE).click()
