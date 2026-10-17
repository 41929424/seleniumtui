from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT = (By.ID, "logout_sidebar_link")

    def open(self, url: str):
        self.driver.get(url)
        return self

    def wait_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.TITLE))
        self.wait.until(lambda driver: len(driver.find_elements(*self.ITEMS)) > 0)

    def names(self) -> list[str]:
        return [e.text for e in self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item_name")]

    def prices(self) -> list[float]:
        return [
            float(e.text.replace("$", ""))
            for e in self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item_price")
        ]

    def sort(self, value: str):
        from selenium.webdriver.support.ui import Select

        Select(self.wait.until(EC.element_to_be_clickable(self.SORT))).select_by_value(value)

    def open_product(self, name: str):
        self.click_and_wait(
            (By.LINK_TEXT, name),
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_details_name")),
        )

    def add_product(self, name: str):
        slug = name.lower().replace(" ", "-")
        previous_count = self.cart_count()
        self.click_and_wait(
            (By.ID, f"add-to-cart-{slug}"),
            lambda _driver: self.cart_count() == previous_count + 1,
        )

    def cart_count(self) -> int:
        badges = self.driver.find_elements(By.CSS_SELECTOR, ".shopping_cart_badge")
        return int(badges[0].text) if badges else 0

    def logout(self):
        self.click(self.MENU)
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.LOGOUT))
        except TimeoutException:
            # If the native menu click did not toggle the menu, retry it through the DOM.
            if self.driver.find_elements(*self.MENU):
                self.driver.execute_script(
                    "arguments[0].click()", self.driver.find_element(*self.MENU)
                )
            self.wait.until(EC.visibility_of_element_located(self.LOGOUT))
        self.click_and_wait(
            self.LOGOUT,
            EC.visibility_of_element_located((By.ID, "user-name")),
        )
