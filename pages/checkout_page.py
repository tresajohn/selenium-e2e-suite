from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    PLACE_ORDER = (By.CSS_SELECTOR, "a[href='/payment']")
    CARD_NAME = (By.CSS_SELECTOR, "[data-qa='name-on-card']")
    CARD_NUMBER = (By.CSS_SELECTOR, "[data-qa='card-number']")
    CVC = (By.CSS_SELECTOR, "[data-qa='cvc']")
    EXPIRY_MONTH = (By.CSS_SELECTOR, "[data-qa='expiry-month']")
    EXPIRY_YEAR = (By.CSS_SELECTOR, "[data-qa='expiry-year']")
    PAY_BUTTON = (By.CSS_SELECTOR, "[data-qa='pay-button']")
    SUCCESS_MSG = (By.CSS_SELECTOR, "[data-qa='order-placed']")

    def confirm_order(self) -> None:
        self.click(self.PLACE_ORDER)
        self.type_text(self.CARD_NAME, "Test User QA")
        self.type_text(self.CARD_NUMBER, "4111111111111111")
        self.type_text(self.CVC, "111")
        self.type_text(self.EXPIRY_MONTH, "12")
        self.type_text(self.EXPIRY_YEAR, "2027")
        self.click(self.PAY_BUTTON)

    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_MSG)
