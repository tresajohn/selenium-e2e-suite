from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM_NAMES = (By.CSS_SELECTOR, ".cart_description h4 a")
    PROCEED_CHECKOUT = (By.CSS_SELECTOR, "a.btn.check_out")

    def get_cart_item_names(self) -> list[str]:
        elements = self.get_elements(self.CART_ITEM_NAMES)
        return [el.text for el in elements if el.text]

    def proceed_to_checkout(self) -> None:
        self.click(self.PROCEED_CHECKOUT)
