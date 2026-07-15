import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.parametrize(
    "username,password,expected_success",
    [
        ("Admin", "admin123", True),       # valid
        ("wronguser", "wrongpass", False), # invalid
    ]
)
def test_orangehrm_login(page, username, password, expected_success):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.login(username, password)

    if expected_success:
        assert dashboard_page.is_loaded(), "Dashboard did not load after login"
        assert "John Cena" in dashboard_page.get_logged_in_user()
    else:
    # For invalid login, check error message instead
     error_message = page.locator("p.oxd-alert-content-text")
     error_message.wait_for(state="visible")   # <-- wait explicitly
     assert error_message.is_visible(), "Expected error message not shown"

