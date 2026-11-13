from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ContactPage(BasePage):
    NAME = (By.CSS_SELECTOR, "[data-qa='name']")
    EMAIL = (By.CSS_SELECTOR, "[data-qa='email']")
    SUBJECT = (By.CSS_SELECTOR, "[data-qa='subject']")
    MESSAGE = (By.CSS_SELECTOR, "[data-qa='message']")
    SUBMIT = (By.CSS_SELECTOR, "[data-qa='submit-button']")
    SUCCESS_MSG = (By.CSS_SELECTOR, ".contact-form .alert-success")

    def fill_contact_form(self, name: str, email: str, subject: str, message: str) -> None:
        self.type_text(self.NAME, name)
        self.type_text(self.EMAIL, email)
        self.type_text(self.SUBJECT, subject)
        self.type_text(self.MESSAGE, message)

    def submit(self) -> None:
        self.click(self.SUBMIT)
        # Accept the alert that appears on submit
        try:
            self.driver.switch_to.alert.accept()
        except Exception:
            pass

    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_MSG)
