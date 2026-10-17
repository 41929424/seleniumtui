from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def wait_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))

    def fill_information(self, first: str, last: str, postal: str):
        for locator, value in (
            (self.FIRST_NAME, first),
            (self.LAST_NAME, last),
            (self.POSTAL_CODE, postal),
        ):
            field = self.wait.until(EC.visibility_of_element_located(locator))
            if value:
                # Focus each control and wait until the typed value is present.
                field.click()
                field.send_keys(value)
                self.wait.until(
                    lambda _driver, field=field, value=value: field.get_property("value") == value
                )

    def error_message(self) -> str:
        return self.text(self.ERROR)

    def item_total(self) -> float:
        return float(self.text((By.CSS_SELECTOR, ".summary_subtotal_label")).split("$")[-1])
