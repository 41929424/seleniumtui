from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CSS_SELECTOR, ".cart_item")
    CONTINUE = (By.ID, "continue-shopping")
    CHECKOUT = (By.ID, "checkout")

    def open(self, base_url: str):
        self.driver.get(f"{base_url.rstrip('/')}/cart.html")
        return self

    def names(self) -> list[str]:
        return [e.text for e in self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item_name")]

    def remove(self, name: str):
        slug = name.lower().replace(" ", "-")
        self.click((By.ID, f"remove-{slug}"))

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.ITEMS))
