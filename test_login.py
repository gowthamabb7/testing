import pytest
from playwright.sync_api import Playwright, sync_playwright, Page, expect

# Constants
BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless= False)  # Set headless=True for headless mode
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser) -> Page:
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.mark.parametrize("username,password,should_succeed", [
    (VALID_USERNAME, VALID_PASSWORD, True),          # valid credentials
    ("wronguser", "wrongpass", False),               # invalid credentials
])
def test_orangehrm_login(page: Page, username, password, should_succeed):
    # Navigate to login page
    page.goto(BASE_URL)

    # Fill login form
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')

    if should_succeed:
        # Expect dashboard URL after successful login
        page.wait_for_url("**/dashboard/index", timeout=5000)
        assert "/dashboard/index" in page.url, "Login failed unexpectedly"
    else:
        # Expect error box with 'Invalid credentials'
        error_locator = page.locator(".oxd-alert-content-text")
        expect(error_locator).to_be_visible(timeout=5000)
        assert "Invalid credentials" in error_locator.inner_text(), \
            f"Unexpected error message: {error_locator.inner_text()}"
