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
    """Page Object class for 'https://turbotlumaczenia.pl/'"""

    def __init__(self, webdriver):
        self.driver = webdriver
        self.accept_cookies_xpath = ""
        self.decline_cookies_xpath = "//i[contains(@class, 'fa fa-times')]"
        self.decline_cookies_class_name = "fa-times"

    def click_decline_cookies1(self):
        """Declining loading cookies method based on class name selector."""
        self.driver.find_element_by_class_name(self.decline_cookies_class_name).click()

    def click_decline_cookies2(self):
        """Declining loading cookies method based on xpath selector."""
        self.driver.find_element_by_xpath(self.decline_cookies_xpath).click()

    def accept_cookies(self):
        # self.driver.find_element_by_class_name(self.accept_cookies_class_name).click()
        return self.driver.find_elements_by_class_name(self.accept_cookies_class_name)


class TestDogadamyCie:

    @pytest.fixture()
    def setup(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        yield
        #self.driver.quit()

    def test_dogadamycie1(self, setup):
        """Test description."""
        self.driver.get("https://turbotlumaczenia.pl/")
        # assert 1 == len(self.driver.find_elements_by_class_name("fa-times"))
        main_turbo_page = TurboMainPage(self.driver)
        main_turbo_page.click_decline_cookies2()
