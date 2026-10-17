import pytest
from selenium.webdriver.common.by import By

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.fixture
def inventory(driver, app_url):
    LoginPage(driver).open(app_url).login()
    page = InventoryPage(driver)
    page.wait_loaded()
    return page


def test_cart_01_add_one_item(inventory, driver, app_url):
    inventory.add_product("Sauce Labs Backpack")
    CartPage(driver).open(app_url)
    assert CartPage(driver).names() == ["Sauce Labs Backpack"]


def test_cart_02_add_multiple_items(inventory, driver, app_url):
    inventory.add_product("Sauce Labs Backpack")
    inventory.add_product("Sauce Labs Bike Light")
    cart = CartPage(driver).open(app_url)
    assert set(cart.names()) == {"Sauce Labs Backpack", "Sauce Labs Bike Light"}


def test_cart_03_remove_item(inventory, driver, app_url):
    inventory.add_product("Sauce Labs Backpack")
    cart = CartPage(driver).open(app_url)
    cart.remove("Sauce Labs Backpack")
    assert cart.item_count() == 0


def test_cart_04_item_quantity(inventory, driver):
    inventory.add_product("Sauce Labs Backpack")
    inventory.add_product("Sauce Labs Bike Light")
    assert inventory.cart_count() == 2


def test_cart_05_cart_persists_during_navigation(inventory, driver, app_url):
    inventory.add_product("Sauce Labs Backpack")
    cart = CartPage(driver).open(app_url)
    cart.click_and_wait(
        cart.CONTINUE,
        lambda _driver: driver.current_url.endswith("/inventory.html"),
    )
    inventory = InventoryPage(driver)
    assert inventory.cart_count() == 1
    CartPage(driver).open(app_url)
    assert "Sauce Labs Backpack" in CartPage(driver).names()
