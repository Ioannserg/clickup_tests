from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self._endpoint = 'login'

    USERNAME_SELECTOR = 'input[id="login-email-input"]'
    PASSWORD_SELECTOR = 'input[id="login-password-input"]'
    LOGIN_BUTTON_SELECTOR = 'button[data-test="login-submit"]'
    AFTER_LOGIN_URL = 'https://app.clickup.com/90151135180/v/l/2kypu9yc-355'

    def login(self, username, password):
        self.navigate_to()
        self.wait_for_selector_and_type(self.USERNAME_SELECTOR, username, 100)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)
        self.assert_navigate_to_page(self.AFTER_LOGIN_URL)

    def login_negative(self, username, password):
        self.navigate_to()
        self.wait_for_selector_and_type(self.USERNAME_SELECTOR, username, 100)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)
        self.assert_text_present_on_page(' Incorrect password for this email. ')



