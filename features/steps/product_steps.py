from behave import given, then, when

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


@given("I am on the home page")
def step_home(context):
    context.home_page = HomePage(context.driver)
    context.home_page.navigate(context.test_config.base_url)


@when('I search for "{keyword}"')
def step_search(context, keyword):
    context.home_page.search(keyword)


@then("I should see at least {count:d} product in the results")
def step_min_results(context, count):
    assert len(context.home_page.get_product_names()) >= count


@then("I should see {count:d} products in the results")
def step_exact_results(context, count):
    assert len(context.home_page.get_product_names()) == count


@when("I add the first visible product to cart")
def step_add_to_cart(context):
    context.home_page.add_first_product_to_cart()


@when("I navigate to the cart page")
def step_nav_cart(context):
    context.cart_page = CartPage(context.driver)
    context.cart_page.navigate(f"{context.test_config.base_url}/view_cart")


@then("I should see at least {count:d} item in the cart")
def step_cart_min_items(context, count):
    assert len(context.cart_page.get_cart_item_names()) >= count


@then("the cart item names list should not be empty")
def step_cart_not_empty(context):
    assert len(context.cart_page.get_cart_item_names()) > 0


@given("I am logged in as a registered user")
def step_logged_in_user(context):
    login = LoginPage(context.driver)
    login.navigate(f"{context.test_config.base_url}/login")
    login.login(context.test_config.test_email, context.test_config.test_password)
    assert login.is_logged_in()


@given("I have a product in my cart")
def step_product_in_cart(context):
    context.home_page = HomePage(context.driver)
    context.home_page.navigate(context.test_config.base_url)
    context.home_page.add_first_product_to_cart()


@when("I proceed to checkout from cart")
def step_proceed_checkout(context):
    context.cart_page = CartPage(context.driver)
    context.cart_page.navigate(f"{context.test_config.base_url}/view_cart")
    context.cart_page.proceed_to_checkout()


@when("I confirm and pay for the order")
def step_confirm_order(context):
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.confirm_order()


@then("I should see the order placed confirmation")
def step_order_confirmed(context):
    msg = context.checkout_page.get_success_message()
    assert len(msg) > 0


@given("I navigate to the contact page")
def step_nav_contact(context):
    context.contact_page = ContactPage(context.driver)
    context.contact_page.navigate(f"{context.test_config.base_url}/contact_us")


@when("I fill in the contact form with valid details")
def step_fill_contact(context):
    context.contact_page.fill_contact_form(
        name="Tresa QA",
        email="tresa.qa@test.com",
        subject="Portfolio Test",
        message="This is an automated test message from Selenium framework.",
    )


@when("I submit the contact form")
def step_submit_contact(context):
    context.contact_page.submit()


@then("I should see the contact success message")
def step_contact_success(context):
    msg = context.contact_page.get_success_message()
    assert "success" in msg.lower()
