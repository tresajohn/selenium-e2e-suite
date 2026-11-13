from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.driver_factory import DriverFactory


def test_navigate_and_title():
    driver = DriverFactory.create("chrome", headless=True)
    page = BasePage(driver)
    page.navigate("https://automationexercise.com")
    assert "Automation Exercise" in page.get_title()
    driver.quit()


def test_is_visible_true_for_present_element():
    driver = DriverFactory.create("chrome", headless=True)
    page = BasePage(driver)
    page.navigate("https://automationexercise.com")
    assert page.is_visible((By.CSS_SELECTOR, "a[href='/login']")) is True
    driver.quit()


def test_is_visible_false_for_absent_element():
    driver = DriverFactory.create("chrome", headless=True)
    page = BasePage(driver)
    page.navigate("https://automationexercise.com")
    assert page.is_visible((By.CSS_SELECTOR, "#nonexistent_xyz_abc")) is False
    driver.quit()
