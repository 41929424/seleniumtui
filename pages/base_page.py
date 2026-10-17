from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def click_and_wait(self, locator, condition):
        """Click normally, using a DOM click only if the expected UI change stalls."""
        self.click(locator)
        try:
            return WebDriverWait(self.driver, 3).until(condition)
        except TimeoutException:
            # Some SauceDemo controls occasionally ignore the native click in headless CI.
            # Retry only while the original control is still present (the state did not change).
            elements = self.driver.find_elements(*locator)
            if elements:
                self.driver.execute_script("arguments[0].click()", elements[0])
            return self.wait.until(condition)

    def text(self, locator) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def visible(self, locator) -> bool:
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
