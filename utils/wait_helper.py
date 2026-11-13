from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WaitHelper:
    def __init__(self, driver, timeout: int = 10):
        self._wait = WebDriverWait(driver, timeout)

    def until_visible(self, locator: tuple):
        return self._wait.until(EC.visibility_of_element_located(locator))

    def until_clickable(self, locator: tuple):
        return self._wait.until(EC.element_to_be_clickable(locator))

    def until_all_visible(self, locator: tuple):
        return self._wait.until(EC.visibility_of_all_elements_located(locator))
