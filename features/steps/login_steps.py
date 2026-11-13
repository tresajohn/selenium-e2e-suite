import time

from behave import given, then, when
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


@given("I navigate to the login page")
def step_nav_login(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate(f"{context.test_config.base_url}/login")


@when('I login with email "{email}" and password "{password}"')
def step_login(context, email, password):
    actual_email = context.test_config.test_email if email == "valid" else email
    actual_pw = context.test_config.test_password if password == "valid" else password
    context.login_page.login(actual_email, actual_pw)


@when("I submit login with empty email and password")
def step_login_empty(context):
    # HTML5 required attribute prevents submission — just click the button
    context.login_page.click(context.login_page.SUBMIT)


@then("I should be logged in successfully")
def step_logged_in(context):
    assert context.login_page.is_logged_in() is True, "Expected to be logged in"


@then('I should see the login error "{message}"')
def step_login_error(context, message):
    actual = context.login_page.get_error_message()
    assert message in actual, f"Expected '{message}' in '{actual}'"


@then("I should remain on the login page")
def step_on_login_page(context):
    assert "/login" in context.driver.current_url


@when('I sign up with a unique email and name "{name}"')
def step_signup_unique(context, name):
    unique_email = f"qaauto{int(time.time())}@mailinator.com"
    context.login_page.fill_signup(name, unique_email)
    context.reg_page = RegistrationPage(context.driver)
    context.reg_page.complete_registration("Test@1234")


@when('I sign up with email "{email}" and name "{name}"')
def step_signup_existing(context, email, name):
    context.login_page.fill_signup(name, email)


@then("I should see the account created confirmation")
def step_account_created(context):
    assert context.reg_page.is_registered() is True, "Expected account created page"


@then('I should see the signup error "{message}"')
def step_signup_error(context, message):
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    locator = (By.XPATH, f"//p[contains(text(),'{message}')]")
    try:
        error_el = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        assert error_el.is_displayed(), f"Expected signup error: {message}"
    except Exception:
        assert False, f"Expected signup error: {message}"
