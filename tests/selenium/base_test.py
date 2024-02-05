import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Define a test class named BaseTest that inherits from unittest.TestCase.
class BaseTest(unittest.TestCase):

    # This method is called before each test case.
    def setUp(self):
        chrome_driver_path = "drivers/chromedriver-linux64/chromedriver"
        chrome_options = Options()
        chrome_options.binary_location = "drivers/chrome-linux64/chrome"
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        service = Service(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Create a Chrome WebDriver instance.
        self.driver.get("https://www-onboardingaos.nhsapp.service.nhs.uk/login")

    # This method is called after each test case.
    def tearDown(self):
        # Close the WebDriver, terminating the browser session.
        self.driver.close()

# Check if this script is the main module to be executed.
if __name__ == "__main__":
   # Run the test cases defined in this module
   unittest.main(verbosity=1)