# Test cases

All cases assume Chrome is available, the SauceDemo application is reachable, and the driver fixture starts a fresh browser for each test. Tests use `standard_user` / `secret_sauce` unless stated otherwise.

## AUTH-01 · Authentication

### TC-AUTH-001 · Successful login · Positive

**Preconditions:** User is on the login page. **Data:** `standard_user` / `secret_sauce`.

**Steps:** Enter username; enter password; select Login.

**Expected:** Browser opens `/inventory.html`; Products heading and product list are visible.

### TC-AUTH-002 · Invalid password · Negative

**Preconditions:** Login page is open. **Data:** `standard_user` / `wrong_password`.

**Steps:** Enter credentials; select Login.

**Expected:** Login is rejected and an error explains that username and password do not match.

### TC-AUTH-003 · Empty login fields · Negative

**Preconditions:** Login page is open. **Data:** Both fields empty.

**Steps:** Select Login without entering data.

**Expected:** Login is rejected with a username-required validation message.

### TC-AUTH-004 · Locked user · Negative

**Preconditions:** Login page is open. **Data:** `locked_out_user` / `secret_sauce`.

**Steps:** Enter credentials; select Login.

**Expected:** Login is rejected and the message identifies the locked account.

### TC-AUTH-005 · Logout · Positive

**Preconditions:** Logged in as `standard_user` on the inventory page.

**Steps:** Open the menu; select Logout.

**Expected:** Login form is displayed.

## CAT-01 · Product catalog

### TC-CAT-001 · Product list · Positive

**Preconditions:** Logged in. **Steps:** Open inventory.

**Expected:** Products heading and six product cards are visible.

### TC-CAT-002 · Sort by price ascending · Positive

**Preconditions:** Inventory is open. **Steps:** Select Price (low to high).

**Expected:** Product prices appear in ascending numeric order.

### TC-CAT-003 · Sort by price descending · Positive

**Preconditions:** Inventory is open. **Steps:** Select Price (high to low).

**Expected:** Product prices appear in descending numeric order.

### TC-CAT-004 · Sort names A–Z · Positive

**Preconditions:** Inventory is open. **Steps:** Select Name (A to Z).

**Expected:** Product names appear in ascending alphabetical order.

### TC-CAT-005 · Open product details · Positive

**Preconditions:** Inventory is open. **Steps:** Open the first product card.

**Expected:** Product detail page displays the same product name.

## CART-01 · Shopping cart

### TC-CART-001 · Add one item · Positive

**Preconditions:** Logged in. **Steps:** Add Sauce Labs Backpack; open cart.

**Expected:** Cart contains Sauce Labs Backpack.

### TC-CART-002 · Add multiple items · Positive

**Preconditions:** Logged in. **Steps:** Add Backpack and Bike Light; open cart.

**Expected:** Both products appear in the cart.

### TC-CART-003 · Remove item · Positive

**Preconditions:** Cart contains Backpack. **Steps:** Select Remove for Backpack.

**Expected:** Cart is empty.

### TC-CART-004 · Cart quantity · Positive

**Preconditions:** Logged in. **Steps:** Add Backpack and Bike Light.

**Expected:** Header cart badge shows 2.

### TC-CART-005 · Cart persists during navigation · Positive

**Preconditions:** Logged in. **Steps:** Add Backpack; open cart; continue shopping; reopen cart.

**Expected:** Badge remains 1 and Backpack remains in the cart.

## CHK-01 · Checkout

### TC-CHK-001 · Complete order · Positive

**Preconditions:** Cart contains Backpack. **Data:** Alex / Tester / LV-1001.

**Steps:** Start checkout; enter customer details; continue; finish.

**Expected:** Confirmation page says “Thank you for your order!”.

### TC-CHK-002 · Missing first name · Negative

**Preconditions:** Checkout information form is open. **Data:** Empty first name; Tester / LV-1001.

**Steps:** Continue without first name.

**Expected:** Checkout remains on the form and reports that First Name is required.

### TC-CHK-003 · Missing last name · Negative

**Preconditions:** Checkout information form is open. **Data:** Alex / empty last name / LV-1001.

**Steps:** Continue without last name.

**Expected:** Checkout remains on the form and reports that Last Name is required.

### TC-CHK-004 · Missing postal code · Negative

**Preconditions:** Checkout information form is open. **Data:** Alex / Tester / empty postal code.

**Steps:** Continue without postal code.

**Expected:** Checkout remains on the form and reports that Postal Code is required.

### TC-CHK-005 · Order totals · Positive

**Preconditions:** Cart contains Backpack. **Data:** Alex / Tester / LV-1001.

**Steps:** Enter details; continue to order overview.

**Expected:** Item subtotal is $29.99 and grand total includes tax, so exceeds the subtotal.
