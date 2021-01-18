

class TurboMainPage:
    """Page Object class for main page: 'https://turbotlumaczenia.pl/'"""

    def __init__(self, webdriver_el):
        self.driver = webdriver_el
        self.accept_cookies_xpath = "//button[text()='Akceptuję']"
        self.decline_cookies_xpath = "//i[contains(@class, 'fa fa-times')]"
        self.decline_cookies_class_name = "fa-times"
        self.wycena_tlumaczenia_xpath = "//a[text()='Wycena tłumaczenia']"

    def click_decline_cookies(self):
        """Declining loading cookies method based on xpath selector."""
        self.driver.find_element_by_xpath(self.decline_cookies_xpath).click()

    def click_decline_cookies_backup(self):
        """Declining loading cookies method based on class name selector."""
        self.driver.find_element_by_class_name(self.decline_cookies_class_name).click()

    def click_accept_cookies(self):
        """Accepting loading cookies method based on xpath selector."""
        self.driver.find_element_by_xpath(self.accept_cookies_xpath).click()

    def goto_wycena_tlumaczenia(self):
        """Navigating to Order Form www page (PL: Wycena tłumaczenia)."""
        self.driver.find_element_by_xpath(self.wycena_tlumaczenia_xpath).click()
