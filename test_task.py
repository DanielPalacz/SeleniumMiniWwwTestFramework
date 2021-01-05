"""Scenariusz testowy:
1. Wejście na stronę https://turbotlumaczenia.pl/
2. Przejście na stronę formularza zamówienia (Wycena tłumaczenia)
3. Wybranie tłumaczenia z polskiego na niemiecki
4. Wybór opcji korekty
5. Wprowadzenie tekstu o długości między 250-400 słów do pola tekstowego na treść źródłową
6. Pole na adres email ma pozostać puste
7. Sprawdzenie obecności wyceny
8. Sprawdzenie obecności szacowanego czasu wykonania
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pytest


class TurboMainPage:
    """Page Object class for main page: 'https://turbotlumaczenia.pl/'"""

    def __init__(self, webdriver):
        self.driver = webdriver
        self.accept_cookies_xpath = "//button[text()='Akceptuję']"
        self.decline_cookies_xpath = "//i[contains(@class, 'fa fa-times')]"
        self.decline_cookies_class_name = "fa-times"
        self.wycena_tlumaczenia_xpath = "//a[text()='Wycena tłumaczenia']"
        # self.order_form_xpath = "//a[text()='Wycena tłumaczenia']"

    def click_decline_cookies(self):
        """Declining loading cookies method based on xpath selector."""
        self.driver.find_element_by_xpath(self.decline_cookies_xpath).click()

    def click_decline_cookies_backup(self):
        """Declining loading cookies method based on class name selector."""
        self.driver.find_element_by_class_name(self.decline_cookies_class_name).click()

    def click_accept_cookies(self):
        self.driver.find_element_by_xpath(self.accept_cookies_xpath).click()

    def goto_wycena_tlumaczenia(self):
        self.driver.find_element_by_xpath(self.wycena_tlumaczenia_xpath).click()


class TurboFormOrderPage:
    """Page Object class for Order Form page: 'https://panel.turbotlumaczenia.pl/pl/order/write?from=cta'"""

    def __init__(self, webdriver):
        self.driver = webdriver
        self.translateto_menu_xpath = "//div[contains(@class, 'content__input')]/span[@id='target_lang_label']"
        self.translateto_niemiecki_xpath = "//li[@data-name='Niemiecki']"
        self.proofreading_id = "proofreading"

    def click_translateto_menu(self):
        self.driver.find_element_by_xpath(self.translateto_menu_xpath).click()

    def choose_translateto_niemiecki(self):
        niemiecki_buttons = self.driver.find_elements_by_xpath(self.translateto_niemiecki_xpath)
        for niemiecki in niemiecki_buttons:
            if niemiecki.is_displayed():
                niemiecki.click()

    def choose_add_proofreading(self):
        """Choosing additional native speaker proofreading."""
        self.driver.find_element_by_id(self.proofreading_id).click()


class TestDogadamyCie:

    @pytest.fixture()
    def setup(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        yield
        #self.driver.quit()

    @pytest.mark.skip()
    def test_dogadamycie1(self, setup):
        """Test1: Declined Cookies flow."""
        self.driver.get("https://turbotlumaczenia.pl/")
        main_turbo_page = TurboMainPage(self.driver)
        main_turbo_page.click_decline_cookies()
        self.driver.quit()

    def test_dogadamycie2(self, setup):
        """Test2: Aceepted Cookies flow."""
        self.driver.get("https://turbotlumaczenia.pl/")
        main_turbo_page = TurboMainPage(self.driver)
        main_turbo_page.click_accept_cookies()
        main_turbo_page.goto_wycena_tlumaczenia()
        form_order_page = TurboFormOrderPage(self.driver)
        form_order_page.click_translateto_menu()
        form_order_page.choose_translateto_niemiecki()
        form_order_page.choose_add_proofreading()
