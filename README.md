# Selenium E2E Suite — Automation Exercise

[![CI](https://github.com/tresajohn/selenium-e2e-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/tresajohn/selenium-e2e-suite/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Report](https://img.shields.io/badge/HTML-Report-4a8e56)](https://tresajohn.github.io/selenium-e2e-suite)

A Selenium WebDriver framework targeting [automationexercise.com](https://automationexercise.com), built as a QA portfolio project. Demonstrates the Page Object Model, BDD with Behave, HTML test reporting, GitHub Actions CI/CD, and automatic Jira bug creation on failure.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Language |
| Selenium 4.25+ | Browser automation |
| webdriver-manager | Auto-manages ChromeDriver — no manual driver setup |
| Behave 1.3.3 | BDD / Gherkin feature files |
| behave-html-formatter | Generates a self-contained HTML report after each run |
| GitHub Actions | CI — headless run on every push to `main` |
| Jira REST API v3 | Auto-creates bug tickets with screenshot on failure |
| python-dotenv | Credential and config management via `.env` |

---

## Project Structure

```
selenium-e2e-suite/
├── .github/
│   └── workflows/ci.yml        # GitHub Actions CI pipeline
├── config/
│   ├── config.py               # Config dataclass, reads env vars + config.json
│   └── config.json             # Base URL, browser defaults, timeout
├── features/
│   ├── steps/
│   │   ├── login_steps.py      # Step definitions for login/registration
│   │   └── product_steps.py    # Step definitions for search, cart, checkout, contact
│   ├── environment.py          # Driver lifecycle, screenshot on failure, Jira hook
│   ├── login.feature
│   ├── registration.feature
│   ├── product_search.feature
│   ├── cart.feature
│   ├── checkout.feature
│   └── contact.feature
├── pages/
│   ├── base_page.py            # BasePage with Selenium helpers (click, type, wait)
│   ├── login_page.py
│   ├── registration_page.py
│   ├── home_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── contact_page.py
├── utils/
│   ├── driver_factory.py       # Chrome / Firefox factory via webdriver-manager
│   ├── wait_helper.py          # Explicit wait wrappers
│   ├── screenshot_helper.py    # Saves PNG to logs/screenshots/ on failure
│   └── jira_helper.py          # Creates Jira bug + attaches screenshot
├── tests/                      # Unit tests for framework utilities
├── logs/screenshots/           # Failure screenshots (git-ignored)
├── reports/                    # HTML report output (git-ignored)
├── Makefile
├── behave.ini
└── pyproject.toml
```

---

## Setup

**Prerequisites:** Python 3.11+, Google Chrome installed.

```bash
git clone https://github.com/tresajohn/selenium-e2e-suite
cd selenium-e2e-suite
cp .env.example .env      # fill in your credentials (see below)
make install              # pip install -e ".[dev]"
```

---

## Running Tests

```bash
# Run all scenarios headed (browser visible)
make test

# Run all scenarios headless (no browser window)
make test-headless

# Open the HTML report after a run
make report

# Delete reports and screenshots
make clean
```

The HTML report is written to `reports/report.html` after every run. Open it in any browser — no server needed.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in what you need.

| Variable | Required | Description |
|----------|----------|-------------|
| `TEST_EMAIL` | For login/checkout scenarios | Registered automationexercise.com account email |
| `TEST_PASSWORD` | For login/checkout scenarios | Account password |
| `HEADLESS` | No | Set `true` for headless Chrome. Default: `false` |
| `BROWSER` | No | `chrome` or `firefox`. Default: `chrome` |
| `JIRA_BASE_URL` | No | e.g. `https://yoursite.atlassian.net` |
| `JIRA_EMAIL` | No | Your Atlassian account email |
| `JIRA_API_TOKEN` | No | Jira API token — Jira integration is disabled if not set |
| `JIRA_PROJECT_KEY` | No | Project key for new bugs. Default: `SES` |

Scenarios that need credentials are tagged `@needs_credentials` and are automatically skipped if `TEST_EMAIL` / `TEST_PASSWORD` are not set.

---

## BDD Scenarios

11 scenarios across 6 feature files:

| Feature | Scenario | Tag |
|---------|----------|-----|
| User Login | Login with valid credentials | `@needs_credentials` |
| User Login | Login with invalid credentials | — |
| User Login | Empty credentials stays on login page | — |
| User Registration | Register new account with unique email | — |
| User Registration | Register with already-used email shows error | — |
| Product Search | Search returns results for valid keyword | — |
| Product Search | Search returns no results for unknown keyword | — |
| Shopping Cart | Add product to cart increases cart count | — |
| Shopping Cart | Cart shows correct product name | — |
| Checkout Flow | Logged-in user can complete checkout | `@needs_credentials` |
| Contact Form | Submit contact form with valid data | — |

---

## HTML Test Report

After each run `reports/report.html` is generated — a single self-contained file with no dependencies. It lists every feature, scenario, and step with pass/fail status and duration.

The CI pipeline uploads this file as a downloadable artifact and deploys it to GitHub Pages:
[tresajohn.github.io/selenium-e2e-suite](https://tresajohn.github.io/selenium-e2e-suite)

---

## Failure Handling

When a scenario fails or throws an exception, `environment.py` does two things automatically:

1. **Screenshot** — saves a timestamped PNG to `logs/screenshots/` and attaches it to the report.
2. **Jira bug** — if `JIRA_API_TOKEN` is set, creates a bug in the configured Jira project with the scenario name as the summary and the screenshot attached. Duplicate prevention: a new ticket is only created if no open issue with the same summary already exists.

Both behaviours are silent — a failure in screenshot capture or Jira API never causes the test run itself to error.

---

## CI/CD

GitHub Actions runs the full suite headless on every push to `main`:

1. Check out the repo and set up Python 3.12
2. `make install` — installs all dependencies
3. `make test-headless` — runs Behave with the HTML formatter, writes `reports/report.html`
4. Uploads `reports/report.html` as a downloadable artifact (available even if tests fail)
5. Deploys the report to **GitHub Pages** on successful `main` pushes

Jira credentials are stored as GitHub repository secrets (`TEST_EMAIL`, `TEST_PASSWORD`, and optionally the Jira variables).

---

**Tresa John** — QA Automation Engineer · [github.com/tresajohn](https://github.com/tresajohn)
