import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser, pytestconfig):
    context = browser.new_context()
    page = context.new_page()
    base_url = pytestconfig.getini("base_url")
    page.goto(base_url)
    yield page
    context.close()
