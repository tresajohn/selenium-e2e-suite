from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class HomePage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "#search_product")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#submit_search")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-image-wrapper")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".product-overlay .add-to-cart")
    MODAL_CONTINUE = (By.CSS_SELECTOR, ".modal-footer .btn-success")
    VIEW_CART_MODAL = (By.CSS_SELECTOR, "u")

    def search(self, keyword: str) -> None:
        if "/products" not in self.driver.current_url:
            origin = self.driver.execute_script("return window.location.origin")
            self.navigate(f"{origin}/products")
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        # wait for results to reload
        try:
            self.wait.until_visible(self.PRODUCT_NAMES)
        except TimeoutException:
            pass

    def get_product_names(self) -> list[str]:
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [
            tc for el in elements
            if (tc := el.get_attribute("textContent") or "").strip()
        ]

    def add_first_product_to_cart(self) -> None:
        products = self.get_elements(self.PRODUCT_ITEMS)
        if not products:
            raise RuntimeError("No products found on home page")
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", products[0])
        ActionChains(self.driver).move_to_element(products[0]).perform()
        add_btns = self.driver.find_elements(*self.ADD_TO_CART_BTN)
        if add_btns:
            self.driver.execute_script("arguments[0].click();", add_btns[0])
        # dismiss modal if shown
        try:
            self.wait.until_clickable(self.MODAL_CONTINUE)
            self.click(self.MODAL_CONTINUE)
        except TimeoutException:
            pass
