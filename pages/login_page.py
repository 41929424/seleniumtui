from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self, url: str):
        self.driver.get(url)
        self.wait.until(lambda driver: driver.find_element(*self.USERNAME))
        return self

    def login(self, username: str = "standard_user", password: str = "secret_sauce"):
        self.driver.find_element(*self.USERNAME).clear()
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.click(self.LOGIN_BUTTON)

    def error_message(self) -> str:
        return self.text(self.ERROR)
