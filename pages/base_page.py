from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def text(self, locator) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def visible(self, locator) -> bool:
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
