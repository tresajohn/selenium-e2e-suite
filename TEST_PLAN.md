# Test Plan — selenium-e2e-suite (automationexercise.com)

**Project:** selenium-e2e-suite  
**Target Site:** https://automationexercise.com  
**Framework:** Python 3.12 · Selenium 4 · Behave (BDD) · Allure Reports  
**Author:** Tresa John  
**Last Updated:** 2026-11-12

---

## Coverage Summary

| Priority | Total TCs | Automated | Gap |
|----------|-----------|-----------|-----|
| P0 — Smoke / critical path | 11 | 11 | 0 |
| P1 — Core functionality | 15 | 0 | 15 |
| P2 — Standard regression | 12 | 0 | 12 |
| **Total** | **38** | **11** | **27** |

> All P0 scenarios are automated and run headless in CI on every push to `main`.

---

## Feature 1: User Login

### Acceptance Criteria
1. Valid credentials redirect to logged-in home page (username visible in nav)
2. Invalid credentials show "Your email or password is incorrect!"
3. Empty form submission stays on login page (HTML5 validation)
4. Login page is accessible at `/login`

### Equivalence Classes

| Parameter | Valid Class | Invalid Class | Boundary |
|-----------|-------------|---------------|----------|
| Email | registered@email.com | notanemail / unregistered@x.com | 1 char / 254 chars |
| Password | correct password | wrong string | 1 char / 128 chars |
| Both fields | populated | empty | one filled, one empty |

### Test Cases

| TC ID | Title | Preconditions | Steps | Expected Result | Priority | Type |
|-------|-------|---------------|-------|-----------------|----------|------|
| TC-LOGIN-001 | Login with valid credentials redirects to home | Registered account; on `/login` | Enter valid email + password → click Login | Nav shows "Logged in as \<name\>" | P0 | Functional |
| TC-LOGIN-002 | Login with wrong password shows error | On `/login` | Enter registered email + wrong password → click Login | Error: "Your email or password is incorrect!" | P0 | Negative |
| TC-LOGIN-003 | Login with unregistered email shows error | On `/login` | Enter unregistered email + any password → click Login | Error: "Your email or password is incorrect!" | P1 | Negative |
| TC-LOGIN-004 | Submit empty form stays on login page | On `/login` | Leave both fields empty → click Login | URL remains `/login` | P1 | Negative |
| TC-LOGIN-005 | Submit with email only stays on login page | On `/login` | Enter email, leave password empty → click Login | URL remains `/login` | P2 | Boundary |
| TC-LOGIN-006 | Submit with password only stays on login page | On `/login` | Leave email empty, enter password → click Login | URL remains `/login` | P2 | Boundary |
| TC-LOGIN-007 | XSS payload in email field | On `/login` | Enter `<script>alert(1)</script>` as email | No script executes; error message shown | P1 | Security |
| TC-LOGIN-008 | SQL injection in password field | On `/login` | Enter `' OR '1'='1` as password | No bypass; error message shown | P1 | Security |
| TC-LOGIN-009 | Logout redirects to login page | Logged in | Click Logout in nav | Redirected to `/login`; nav shows no username | P0 | Functional |

### Gherkin Scenarios

```gherkin
@needs_credentials
Scenario: Login with valid credentials
  Given I navigate to the login page
  When I login with email "valid" and password "valid"
  Then I should be logged in successfully

Scenario: Login with invalid credentials shows error
  Given I navigate to the login page
  When I login with email "wrong@example.com" and password "differentwrongpass999"
  Then I should see the login error "Your email or password is incorrect!"

Scenario: Login with empty credentials stays on login page
  Given I navigate to the login page
  When I submit login with empty email and password
  Then I should remain on the login page
```

### Automation Status

| TC ID | Automated | Feature File / Scenario |
|-------|-----------|------------------------|
| TC-LOGIN-001 | ✅ | `features/login.feature` — "Login with valid credentials" |
| TC-LOGIN-002 | ✅ | `features/login.feature` — "Login with invalid credentials" |
| TC-LOGIN-004 | ✅ | `features/login.feature` — "Login with empty credentials stays on login page" |
| TC-LOGIN-003, 005–009 | ❌ | Not yet automated |

---

## Feature 2: User Registration

### Acceptance Criteria
1. New email completes registration and shows "Account Created!" confirmation
2. Duplicate email shows "Email Address already exist!"
3. All mandatory fields (name, email) must be filled to reach registration form

### Equivalence Classes

| Parameter | Valid Class | Invalid Class | Boundary |
|-----------|-------------|---------------|----------|
| Signup name | "Tresa QA" | "" (empty) | 1 char / 50 chars |
| Signup email | unique@test.com | duplicate / malformed | — |
| Registration fields | all filled | any mandatory empty | — |

### Test Cases

| TC ID | Title | Preconditions | Steps | Expected Result | Priority | Type |
|-------|-------|---------------|-------|-----------------|----------|------|
| TC-REG-001 | Register new account with unique email shows confirmation | On `/login` | Fill signup name + unique email → click Signup → complete form → click Create Account | "Account Created!" page shown | P0 | Functional |
| TC-REG-002 | Register with existing email shows error | On `/login` | Fill signup name + existing email → click Signup | "Email Address already exist!" shown | P0 | Negative |
| TC-REG-003 | Register with empty name field | On `/login` | Leave name empty, fill email → click Signup | Stays on login page or shows validation | P1 | Negative |
| TC-REG-004 | Register with malformed email | On `/login` | Enter "notanemail" as email → click Signup | HTML5 validation prevents submission | P2 | Negative |
| TC-REG-005 | XSS in signup name | On `/login` | Enter `<img src=x onerror=alert(1)>` as name | No script executes | P1 | Security |

### Gherkin Scenarios

```gherkin
Scenario: Register a new account with unique email
  Given I navigate to the login page
  When I sign up with a unique email and name "Portfolio QA"
  Then I should see the account created confirmation

Scenario: Register with an already-used email shows error
  Given I navigate to the login page
  When I sign up with email "wrong@example.com" and name "Any Name"
  Then I should see the signup error "Email Address already exist!"
```

### Automation Status

| TC ID | Automated | Feature File / Scenario |
|-------|-----------|------------------------|
| TC-REG-001 | ✅ | `features/registration.feature` — "Register a new account with unique email" |
| TC-REG-002 | ✅ | `features/registration.feature` — "Register with an already-used email shows error" |
| TC-REG-003–005 | ❌ | Not yet automated |

---

## Feature 3: Product Search

### Acceptance Criteria
1. Search for a known keyword returns matching products
2. Search for an unknown keyword returns 0 results
3. Search is accessible from `/products` page

### Equivalence Classes

| Parameter | Valid Class | Invalid Class | Boundary |
|-----------|-------------|---------------|----------|
| Keyword | "Top", "Dress" | "xyznonexistent999" | 1 char / special chars |
| Results | ≥1 product card | 0 cards | exactly 1 result |

### Test Cases

| TC ID | Title | Preconditions | Steps | Expected Result | Priority | Type |
|-------|-------|---------------|-------|-----------------|----------|------|
| TC-SRCH-001 | Search for valid keyword returns results | On `/products` | Enter "Top" → click Search | ≥1 product card displayed | P0 | Functional |
| TC-SRCH-002 | Search for unknown keyword returns 0 results | On `/products` | Enter "xyznonexistent999" → click Search | 0 product cards; no crash | P0 | Negative |
| TC-SRCH-003 | Search is case-insensitive | On `/products` | Enter "top" (lowercase) → click Search | Same results as "Top" | P2 | Functional |
| TC-SRCH-004 | Search with empty input | On `/products` | Leave search empty → click Search | All products shown or stays on page | P2 | Boundary |
| TC-SRCH-005 | Search with special characters | On `/products` | Enter `<script>` → click Search | 0 results; no script executes | P1 | Security |
| TC-SRCH-006 | Search result count matches displayed cards | On `/products` | Enter "Dress" → count product cards | Card count ≥1; correct products visible | P1 | Functional |

### Gherkin Scenarios

```gherkin
Scenario: Search returns results for valid keyword
  Given I am on the home page
  When I search for "Top"
  Then I should see at least 1 product in the results

Scenario: Search returns no results for unknown keyword
  Given I am on the home page
  When I search for "xyznonexistent999"
  Then I should see 0 products in the results
```

### Automation Status

| TC ID | Automated | Feature File / Scenario |
|-------|-----------|------------------------|
| TC-SRCH-001 | ✅ | `features/product_search.feature` — "Search returns results for valid keyword" |
| TC-SRCH-002 | ✅ | `features/product_search.feature` — "Search returns no results for unknown keyword" |
| TC-SRCH-003–006 | ❌ | Not yet automated |

---

## Feature 4: Shopping Cart

### Acceptance Criteria
1. Adding a product to cart increases cart item count
2. Cart page shows correct product name(s)
3. Cart persists within the session

### Equivalence Classes

| Parameter | Valid Class | Invalid Class | Boundary |
|-----------|-------------|---------------|----------|
| Product added | 1 product | 0 (nothing added) | max cart items |
| Cart item name | matches product page name | mismatched / blank | — |

### Test Cases

| TC ID | Title | Preconditions | Steps | Expected Result | Priority | Type |
|-------|-------|---------------|-------|-----------------|----------|------|
| TC-CART-001 | Add product to cart increases item count | On home page | Hover first product → click Add to Cart → dismiss modal → go to cart | Cart shows ≥1 item | P0 | Functional |
| TC-CART-002 | Cart shows correct product name | On home page | Add first product → go to `/view_cart` | Product name in cart is not empty | P0 | Functional |
| TC-CART-003 | Add multiple products to cart | On home page | Add 2 different products → go to cart | Both products listed in cart | P1 | Functional |
| TC-CART-004 | Remove item from cart | Item in cart | Click delete/remove → confirm | Item removed; cart count decreases | P1 | Functional |
| TC-CART-005 | Cart empty after logout and re-login | Add item → logout → login | Check cart | Cart is empty (session cleared) | P2 | Functional |
| TC-CART-006 | Cart persists across page navigation | Add item → browse to home | Return to cart | Same item still in cart | P2 | Functional |

### Gherkin Scenarios

```gherkin
Scenario: Add product to cart increases cart count
  Given I am on the home page
  When I add the first visible product to cart
  And I navigate to the cart page
  Then I should see at least 1 item in the cart

Scenario: Cart shows correct product name
  Given I am on the home page
  When I add the first visible product to cart
  And I navigate to the cart page
  Then the cart item names list should not be empty
```

### Automation Status

| TC ID | Automated | Feature File / Scenario |
|-------|-----------|------------------------|
| TC-CART-001 | ✅ | `features/cart.feature` — "Add product to cart increases cart count" |
| TC-CART-002 | ✅ | `features/cart.feature` — "Cart shows correct product name" |
| TC-CART-003–006 | ❌ | Not yet automated |

---

## Feature 5: Checkout Flow

### Acceptance Criteria
1. Logged-in user can proceed to checkout from cart
2. Valid card details complete the order and show confirmation
3. Unauthenticated user is redirected to login on checkout attempt

### Equivalence Classes

| Parameter | Valid Class | Invalid Class | Boundary |
|-----------|-------------|---------------|----------|
| Card number | 4111111111111111 | 1234 / letters | 16 digits |
| Expiry | 12/2027 (future) | 01/2020 (past) | current month |
| CVC | 3 digits | 2 digits / letters | — |

### Test Cases

| TC ID | Title | Preconditions | Steps | Expected Result | Priority | Type |
|-------|-------|---------------|-------|-----------------|----------|------|
| TC-CHK-001 | Logged-in user completes checkout | Logged in; item in cart | Go to cart → Proceed to Checkout → fill card → Confirm | "Order Placed!" success message shown | P0 | Functional |
| TC-CHK-002 | Guest user checkout redirects to login | Not logged in; item in cart | Go to cart → Proceed to Checkout | Redirected to `/login` | P1 | Functional |
| TC-CHK-003 | Checkout with expired card | Logged in; item in cart | Use expiry 01/2020 | Error shown; order not placed | P1 | Negative |
| TC-CHK-004 | Checkout with invalid card number | Logged in; item in cart | Use card "1234567890123456" | Error or validation message | P2 | Negative |
| TC-CHK-005 | Checkout with empty card fields | Logged in; item in cart | Leave card fields blank → Confirm | Validation prevents submission | P2 | Negative |

### Gherkin Scenarios

```gherkin
@needs_credentials
Scenario: Logged-in user can complete checkout
  Given I am logged in as a registered user
  And I have a product in my cart
  When I proceed to checkout from cart
  And I confirm and pay for the order
  Then I should see the order placed confirmation
```

### Automation Status

| TC ID | Automated | Feature File / Scenario |
|-------|-----------|------------------------|
| TC-CHK-001 | ✅ | `features/checkout.feature` — "Logged-in user can complete checkout" |
| TC-CHK-002–005 | ❌ | Not yet automated |

---

## Feature 6: Contact Form

### Acceptance Criteria
1. All fields (name, email, subject, message) filled → submit shows success message
2. Upload field is optional
3. Alert on submit is accepted automatically

### Equivalence Classes

| Parameter | Valid Class | Invalid Class | Boundary |
|-----------|-------------|---------------|----------|
| Name | "Tresa QA" | "" (empty) | 1 char |
| Email | valid@email.com | "notanemail" | — |
| Subject | "Portfolio Test" | "" | 1 char / 255 chars |
| Message | any text | "" | 1 char |

### Test Cases

| TC ID | Title | Preconditions | Steps | Expected Result | Priority | Type |
|-------|-------|---------------|-------|-----------------|----------|------|
| TC-CONT-001 | Submit contact form with all valid fields shows success | On `/contact_us` | Fill all fields → Submit → accept alert | "Success! Your details have been submitted successfully." shown | P0 | Functional |
| TC-CONT-002 | Submit with empty name | On `/contact_us` | Leave name empty → fill others → Submit | Validation prevents submission | P1 | Negative |
| TC-CONT-003 | Submit with invalid email format | On `/contact_us` | Enter "notanemail" in email → Submit | HTML5 validation error | P1 | Negative |
| TC-CONT-004 | Submit with empty message | On `/contact_us` | Leave message empty → fill others → Submit | Validation prevents submission | P2 | Negative |
| TC-CONT-005 | XSS in subject field | On `/contact_us` | Enter `<script>alert(1)</script>` in subject → Submit | No script executes; success message shown | P1 | Security |

### Gherkin Scenarios

```gherkin
Scenario: Submit contact form with valid data
  Given I navigate to the contact page
  When I fill in the contact form with valid details
  And I submit the contact form
  Then I should see the contact success message
```

### Automation Status

| TC ID | Automated | Feature File / Scenario |
|-------|-----------|------------------------|
| TC-CONT-001 | ✅ | `features/contact.feature` — "Submit contact form with valid data" |
| TC-CONT-002–005 | ❌ | Not yet automated |

---

## Master Traceability Matrix

| TC ID | Feature | Acceptance Criterion | Automated | Priority |
|-------|---------|----------------------|-----------|----------|
| TC-LOGIN-001 | Login | Valid credentials → redirect | ✅ | P0 |
| TC-LOGIN-002 | Login | Invalid credentials → error | ✅ | P0 |
| TC-LOGIN-004 | Login | Empty form → stays on page | ✅ | P1 |
| TC-LOGIN-003, 005–009 | Login | Edge / security cases | ❌ | P1–P2 |
| TC-REG-001 | Registration | New account → confirmation | ✅ | P0 |
| TC-REG-002 | Registration | Duplicate email → error | ✅ | P0 |
| TC-REG-003–005 | Registration | Validation + security | ❌ | P1–P2 |
| TC-SRCH-001 | Search | Valid keyword → results | ✅ | P0 |
| TC-SRCH-002 | Search | Unknown keyword → 0 results | ✅ | P0 |
| TC-SRCH-003–006 | Search | Edge / security cases | ❌ | P1–P2 |
| TC-CART-001 | Cart | Add product → count increases | ✅ | P0 |
| TC-CART-002 | Cart | Cart shows product name | ✅ | P0 |
| TC-CART-003–006 | Cart | Multi-item, remove, persist | ❌ | P1–P2 |
| TC-CHK-001 | Checkout | Full purchase flow | ✅ | P0 |
| TC-CHK-002–005 | Checkout | Guest redirect, invalid card | ❌ | P1–P2 |
| TC-CONT-001 | Contact | Valid form → success | ✅ | P0 |
| TC-CONT-002–005 | Contact | Validation + security | ❌ | P1–P2 |

---

## Risk Priority Formula

```
Priority Score = (Business Impact × 0.5) + (Failure Likelihood × 0.3) + (Complexity × 0.2)

Score > 0.7  →  P0
Score 0.5–0.7  →  P1
Score 0.3–0.5  →  P2
Score < 0.3  →  P3
```

Each factor rated 0–1:
- **Business Impact:** Would failure block a user from completing a core workflow?
- **Failure Likelihood:** Is this area historically buggy or recently changed?
- **Complexity:** Number of conditions, integrations, or data combinations involved.
