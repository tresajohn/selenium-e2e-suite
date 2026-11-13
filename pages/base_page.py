import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from utils.wait_helper import WaitHelper

_CONSENT_BTN = (By.CSS_SELECTOR, ".fc-cta-consent")


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WaitHelper(driver)

    def _dismiss_consent(self) -> None:
        try:
            btn = WaitHelper(self.driver, timeout=3).until_clickable(_CONSENT_BTN)
            btn.click()
        except Exception:
            pass

    @allure.step("Navigate to {url}")
    def navigate(self, url: str) -> None:
        self.driver.get(url)
        self._dismiss_consent()

    @allure.step("Click element {locator}")
    def click(self, locator: tuple) -> None:
        element = self.wait.until_clickable(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Type '{text}' into {locator}")
    def type_text(self, locator: tuple, text: str) -> None:
        element = self.wait.until_clickable(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        element.clear()
        try:
            element.send_keys(text)
        except Exception:
            self.driver.execute_script(
                "arguments[0].value = arguments[1];", element, text
            )

    def get_text(self, locator: tuple) -> str:
        return self.wait.until_visible(locator).text

    def is_visible(self, locator: tuple) -> bool:
        try:
            self.wait.until_visible(locator)
            return True
        except TimeoutException:
            return False

    def get_title(self) -> str:
        return self.driver.title

    def get_elements(self, locator: tuple) -> list:
        try:
            self.wait.until_visible(locator)
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
