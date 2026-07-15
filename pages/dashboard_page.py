class DashboardPage:
    def __init__(self, page):
        self.page = page
        self.welcome_banner = page.locator("h6.oxd-text--h6")
        self.user_dropdown = page.locator("p.oxd-userdropdown-name")
    def is_loaded(self) -> bool:     
       try:
          self.welcome_banner.wait_for(state="visible", timeout=5000)
          return True
       except:
        return False
    def get_logged_in_user(self) -> str:
        return self.user_dropdown.inner_text()
