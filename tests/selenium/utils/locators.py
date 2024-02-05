from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    TITLE = (By.ID, 'title')
    CONTINUE = (By.ID, 'viewInstructionsButton')

class EmailPageLocators(object):
    TITLE = (By.TAG_NAME, 'h1')
    EMAIL_TEXT_BOX = (By.XPATH, '//*[@id="user-email"]')
    CONTINUE = (By.XPATH, '//*[@id="continue-button"]/button')
    ERROR_HEADING = (By.ID, 'error-summary-heading')

class PasswordPageLocators(object):
    TITLE = (By.TAG_NAME, 'h1')
    PASSWORD_TEXT_BOX = (By.XPATH, '//*[@id="password-input"]')
    CONTINUE = (By.XPATH, '//*[@id="main-content"]/ng-component/div/div/form/button')

class OtpPageLocators(object):
    TITLE = (By.TAG_NAME, 'h1')
    OTP_TEXT_BOX = (By.ID, 'otp-input')
    CONTINUE = (By.XPATH, '//*[@id="main-content"]/ng-component/div/div/form/spinner-button-full-width/button')

class NhsAppHomePageLocators(object):
    TITLE = (By.TAG_NAME, 'h1')
    MESSAGES_LINK = (By.LINK_TEXT, 'View your messages')

class NhsAppMessagesHomePageLocators(object):
    TITLE = (By.TAG_NAME, 'h1')
    MESSAGES_LINK = (By.LINK_TEXT, 'Your NHS healthcare services')

class NhsAppAppMessagesPage(object):
    TITLE = (By.TAG_NAME, 'h1')
