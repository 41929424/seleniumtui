import pytest
from selenium.webdriver.common.by import By

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.fixture
def checkout(driver, app_url):
    LoginPage(driver).open(app_url).login()
    InventoryPage(driver).add_product("Sauce Labs Backpack")
    cart = CartPage(driver).open(app_url)
    cart.click(cart.CHECKOUT)
    return CheckoutPage(driver), app_url


def test_chk_01_successful_order(checkout, driver):
    page, _ = checkout
    page.fill_information("Alex", "Tester", "LV-1001")
    page.click(page.CONTINUE)
    page.click(page.FINISH)
    assert driver.find_element(By.CSS_SELECTOR, ".complete-header").text == "Thank you for your order!"


def test_chk_02_missing_first_name(checkout):
    page, _ = checkout
    page.fill_information("", "Tester", "LV-1001")
    page.click(page.CONTINUE)
    assert "First Name is required" in page.error_message()


def test_chk_03_missing_last_name(checkout):
    page, _ = checkout
    page.fill_information("Alex", "", "LV-1001")
    page.click(page.CONTINUE)
    assert "Last Name is required" in page.error_message()


def test_chk_04_missing_postal_code(checkout):
    page, _ = checkout
    page.fill_information("Alex", "Tester", "")
    page.click(page.CONTINUE)
    assert "Postal Code is required" in page.error_message()


def test_chk_05_order_total(checkout):
    page, _ = checkout
    page.fill_information("Alex", "Tester", "LV-1001")
    page.click(page.CONTINUE)
    assert page.item_total() == pytest.approx(29.99)
    total = float(page.text((By.CSS_SELECTOR, ".summary_total_label")).split("$")[-1])
    assert total > page.item_total()
