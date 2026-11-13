import allure
from dotenv import load_dotenv

from config.config import get_config
from utils.driver_factory import DriverFactory
from utils.jira_helper import JiraHelper
from utils.screenshot_helper import take_screenshot


def _handle_cleanup_error(context, cleanup_func, exception):
    pass


def before_all(context):
    load_dotenv()
    context.test_config = get_config()
    context.fail_on_cleanup_errors = False
    context.on_cleanup_error = _handle_cleanup_error


def before_scenario(context, scenario):
    if "needs_credentials" in scenario.tags:
        if not context.test_config.test_email or not context.test_config.test_password:
            scenario.skip("TEST_EMAIL and TEST_PASSWORD not set — skipping credential scenario")
            return
    context.driver = DriverFactory.create(context.test_config.browser, context.test_config.headless)
    if context.test_config.headless:
        context.driver.set_window_size(1920, 3000)
    else:
        context.driver.maximize_window()


def after_scenario(context, scenario):
    if not hasattr(context, "driver"):
        return
    try:
        if scenario.status in ("failed", "error"):
            path = None
            try:
                path = take_screenshot(context.driver, scenario.name)
                allure.attach.file(
                    str(path),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
            try:
                JiraHelper(context.test_config).create_bug(
                    summary=f"[Auto] {scenario.name}",
                    description=f"Feature: {scenario.feature.name}\nScenario: {scenario.name}",
                    screenshot_path=path,
                )
            except Exception:
                pass
        context.driver.delete_all_cookies()
    except Exception:
        pass
    try:
        context.driver.quit()
    except Exception:
        pass
