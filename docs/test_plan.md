# SauceDemo UI regression test plan

## Objective and scope

Validate the core customer journey on the public SauceDemo demo: authentication, product catalog, cart, and checkout. The suite uses Selenium WebDriver, pytest, and Page Objects. It is intended for Chrome/Chromium and can run locally or in GitHub Actions.

## Test data

- Valid account: `standard_user` / `secret_sauce`
- Locked account: `locked_out_user` / `secret_sauce`
- Invalid password: `standard_user` / `wrong_password`
- Cart item used for checkout: Sauce Labs Backpack ($29.99)
- Additional cart item: Sauce Labs Bike Light ($9.99)

These are public demo credentials and should only be used on SauceDemo.

## Execution and evidence

Run `uv run pytest tests/ui -v`. Set `SAUCEDEMO_URL` to override the base URL and `HEADLESS=0` to show Chrome. Allure JSON can be written with `--alluredir=allure-results`. CI runs the suite on pushes and pull requests and stores the raw Allure result files as an artifact.

## Coverage

| Module | Scenarios | Coverage |
| --- | ---: | --- |
| AUTH-01 Authentication | 5 | Login success, invalid password, empty credentials, locked user, logout |
| CAT-01 Catalog | 5 | Product list, price ascending/descending, name A–Z, product details |
| CART-01 Cart | 5 | Add one, add multiple, remove, quantity badge, persistence on navigation |
| CHK-01 Checkout | 5 | Successful order, required first/last name and postal code, totals |
| **Total** | **20** | |

## Entry and exit criteria

Entry: dependencies installed, browser available, SauceDemo reachable. Exit: all 20 scenarios have completed; failures are triaged and documented in `bug_reports/` before a release candidate is considered ready. A test count in documentation is not evidence of a passing run.
