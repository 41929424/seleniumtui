import pytest
from selenium.webdriver.common.by import By

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


def test_auth_01_valid_login(driver, app_url):
    LoginPage(driver).open(app_url).login()
    page = InventoryPage(driver)
    page.wait_loaded()
    assert driver.current_url.endswith("/inventory.html")
    assert page.text(page.TITLE) == "Products"


def test_auth_02_invalid_password(driver, app_url):
    page = LoginPage(driver).open(app_url)
    page.login(password="wrong_password")
    assert "Username and password do not match" in page.error_message()


def test_auth_03_empty_fields(driver, app_url):
    page = LoginPage(driver).open(app_url)
    page.click(page.LOGIN_BUTTON)
    assert "Username is required" in page.error_message()


def test_auth_04_locked_user(driver, app_url):
    page = LoginPage(driver).open(app_url)
    page.login(username="locked_out_user")
    assert "locked out" in page.error_message().lower()


def test_auth_05_logout(driver, app_url):
    LoginPage(driver).open(app_url).login()
    inventory = InventoryPage(driver)
    inventory.wait_loaded()
    inventory.logout()
    assert driver.find_element(By.ID, "user-name").is_displayed()
