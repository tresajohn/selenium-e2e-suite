from utils.driver_factory import DriverFactory


def test_creates_headless_chrome_driver():
    driver = DriverFactory.create("chrome", headless=True)
    assert driver is not None
    driver.quit()


def test_driver_reaches_target_site():
    driver = DriverFactory.create("chrome", headless=True)
    driver.get("https://automationexercise.com")
    assert "Automation Exercise" in driver.title
    driver.quit()
