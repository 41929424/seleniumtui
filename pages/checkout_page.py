from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
                field.click()
                field.send_keys(value)
                try:
                    WebDriverWait(self.driver, 2).until(
                        lambda driver, locator=locator, value=value: (
                            driver.find_element(*locator).get_property("value") == value
                        )
                    )
                except TimeoutException:
                    # Fall back to the native input setter when headless Chrome
                    # drops keyboard input on the controlled checkout form.
                    self.driver.execute_script(
                        """
                        const [input, value] = arguments;
                        const setter = Object.getOwnPropertyDescriptor(
                            window.HTMLInputElement.prototype, "value"
                        ).set;
                        setter.call(input, value);
                        input.dispatchEvent(new Event("input", { bubbles: true }));
                        input.dispatchEvent(new Event("change", { bubbles: true }));
                        """,
                        self.driver.find_element(*locator),
                        value,
                    )
                    self.wait.until(
                        lambda driver, locator=locator, value=value: (
                            driver.find_element(*locator).get_property("value") == value
                        )
                    )

    def error_message(self) -> str:
        return self.text(self.ERROR)

    def item_total(self) -> float:
        return float(self.text((By.CSS_SELECTOR, ".summary_subtotal_label")).split("$")[-1])
