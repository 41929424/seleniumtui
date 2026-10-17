import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    if os.getenv("HEADLESS", "1").lower() not in {"0", "false", "no"}:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)
    yield browser
    browser.quit()


@pytest.fixture
def app_url() -> str:
    return os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com/")
