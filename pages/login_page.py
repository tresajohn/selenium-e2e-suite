from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL = (By.CSS_SELECTOR, "[data-qa='login-email']")
    PASSWORD = (By.CSS_SELECTOR, "[data-qa='login-password']")
    SUBMIT = (By.CSS_SELECTOR, "[data-qa='login-button']")
    ERROR_MSG = (By.XPATH, "//p[contains(text(),'Your email or password is incorrect')]")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")

    SIGNUP_NAME = (By.CSS_SELECTOR, "[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "[data-qa='signup-email']")
    SIGNUP_SUBMIT = (By.CSS_SELECTOR, "[data-qa='signup-button']")
    SIGNUP_ERROR = (By.XPATH, "//p[contains(text(),'Email Address already exist')]")

    def login(self, email: str, password: str) -> None:
        self.type_text(self.EMAIL, email)
        self.type_text(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MSG)

    def is_logged_in(self) -> bool:
        return self.is_visible(self.LOGOUT_LINK)

    def fill_signup(self, name: str, email: str) -> None:
        self.type_text(self.SIGNUP_NAME, name)
        self.type_text(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_SUBMIT)

    def get_signup_error(self) -> str:
        return self.get_text(self.SIGNUP_ERROR)
