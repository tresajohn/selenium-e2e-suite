from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    PASSWORD = (By.CSS_SELECTOR, "[data-qa='password']")
    DAY = (By.CSS_SELECTOR, "[data-qa='days']")
    MONTH = (By.CSS_SELECTOR, "[data-qa='months']")
    YEAR = (By.CSS_SELECTOR, "[data-qa='years']")
    FIRST_NAME = (By.CSS_SELECTOR, "[data-qa='first_name']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-qa='last_name']")
    ADDRESS = (By.CSS_SELECTOR, "[data-qa='address']")
    COUNTRY = (By.CSS_SELECTOR, "[data-qa='country']")
    STATE = (By.CSS_SELECTOR, "[data-qa='state']")
    CITY = (By.CSS_SELECTOR, "[data-qa='city']")
    ZIPCODE = (By.CSS_SELECTOR, "[data-qa='zipcode']")
    MOBILE = (By.CSS_SELECTOR, "[data-qa='mobile_number']")
    CREATE_ACCOUNT = (By.CSS_SELECTOR, "[data-qa='create-account']")
    ACCOUNT_CREATED = (By.CSS_SELECTOR, "[data-qa='account-created'] b")

    def complete_registration(self, password: str = "Test@1234") -> None:
        self.type_text(self.PASSWORD, password)
        self.type_text(self.FIRST_NAME, "Test")
        self.type_text(self.LAST_NAME, "User")
        self.type_text(self.ADDRESS, "123 Test Street")
        self.type_text(self.STATE, "TestState")
        self.type_text(self.CITY, "TestCity")
        self.type_text(self.ZIPCODE, "12345")
        self.type_text(self.MOBILE, "1234567890")
        self.click(self.CREATE_ACCOUNT)
        self.wait.until_visible(self.ACCOUNT_CREATED)

    def is_registered(self) -> bool:
        return self.is_visible(self.ACCOUNT_CREATED)
