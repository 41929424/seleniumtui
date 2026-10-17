import pytest
from selenium.webdriver.common.by import By

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.fixture
def inventory(driver, app_url):
    LoginPage(driver).open(app_url).login()
    page = InventoryPage(driver)
    page.wait_loaded()
    return page


def test_cat_01_product_list_is_displayed(inventory):
    assert inventory.text(inventory.TITLE) == "Products"
    assert len(inventory.names()) == 6


def test_cat_02_sort_price_ascending(inventory):
    inventory.sort("lohi")
    assert inventory.prices() == sorted(inventory.prices())


def test_cat_03_sort_price_descending(inventory):
    inventory.sort("hilo")
    assert inventory.prices() == sorted(inventory.prices(), reverse=True)


def test_cat_04_sort_name_a_to_z(inventory):
    inventory.sort("az")
    assert inventory.names() == sorted(inventory.names())


def test_cat_05_open_product_card(inventory, driver):
    name = inventory.names()[0]
    inventory.open_product(name)
    assert inventory.text((By.CSS_SELECTOR, ".inventory_details_name")) == name
