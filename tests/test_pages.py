from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from utils.driver_factory import DriverFactory


def test_login_page_elements_accessible():
    """Prove LoginPage locators correctly find and interact with the live form."""
    driver = DriverFactory.create("chrome", headless=True)
    page = LoginPage(driver)
    page.navigate("https://automationexercise.com/login")

    assert not page.is_logged_in()
    assert "Login" in page.get_title() or "Signup" in page.get_title()

    page.type_text(page.EMAIL, "test@example.com")
    page.type_text(page.PASSWORD, "testpass")

    value = driver.find_element(By.CSS_SELECTOR, "[data-qa='login-email']").get_attribute("value")
    assert value == "test@example.com"

    driver.quit()
