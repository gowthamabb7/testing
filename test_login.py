import pytest
from playwright.sync_api import Playwright, sync_playwright, Page, expect

BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser) -> Page:
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.mark.parametrize("username,password,should_succeed", [
    (VALID_USERNAME, VALID_PASSWORD, True),
    ("wronguser", "wrongpass", False),
])
def test_orangehrm_login(page: Page, username, password, should_succeed):
    page.goto(BASE_URL)

    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Login").click()

    if should_succeed:
        # Success: wait for URL change instead of breadcrumb
        page.wait_for_url("**/dashboard/index")
        assert "/dashboard/index" in page.url, "Login failed unexpectedly"
    else:
        # Failure: wait for error box
        error_locator = page.locator(".oxd-alert-content-text")
        expect(error_locator).to_be_visible()
        assert "Invalid credentials" in error_locator.inner_text()
