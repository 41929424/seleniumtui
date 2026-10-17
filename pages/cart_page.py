from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CSS_SELECTOR, ".cart_item")
    CONTINUE = (By.ID, "continue-shopping")
    CHECKOUT = (By.ID, "checkout")

    def open(self, base_url: str):
        self.driver.get(f"{base_url.rstrip('/')}/cart.html")
        self.wait.until(lambda driver: driver.current_url.endswith("/cart.html"))
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".title")))
        self.wait.until(lambda _driver: self.item_count() > 0)
        return self

    def names(self) -> list[str]:
        return [e.text for e in self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item_name")]

    def remove(self, name: str):
        slug = name.lower().replace(" ", "-")
        previous_count = self.item_count()
        self.click((By.ID, f"remove-{slug}"))
        self.wait.until(lambda _driver: self.item_count() == previous_count - 1)

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.ITEMS))
