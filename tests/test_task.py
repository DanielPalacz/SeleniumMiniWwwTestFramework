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

import pathmagic  # noqa Pep8 uncheck

from pages.TurboMainPage import TurboMainPage
from pages.TurboFormOrderPage import TurboFormOrderPage

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from texts_as_py_modules.text1 import TEXT_TO_TRANSLATE


class TestDogadamyCie:
    """Pytest test class implementing test cases for the given scenario."""

    @pytest.fixture()
    def setup(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--lang=pl")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)
        # self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        yield
        self.driver.quit()

    @pytest.mark.skip()
    def test_dogadamycie1(self, setup):
        """Test1: Declined initial Cookies flow."""
        self.driver.get("https://turbotlumaczenia.pl/")
        main_turbo_page = TurboMainPage(self.driver)
        main_turbo_page.click_decline_cookies()
        main_turbo_page.goto_wycena_tlumaczenia()
        form_order_page = TurboFormOrderPage(self.driver)
        form_order_page.click_translateto_menu()
        form_order_page.choose_translateto_niemiecki()
        form_order_page.choose_add_proofreading()
        form_order_page.provide_text_to_translation_area(TEXT_TO_TRANSLATE)
        assert form_order_page.is_estimated_time_value_visible(), \
            "Estimated time is not properly displayed"
        assert form_order_page.is_estimated_cost_value_visible(), \
            "Estimated cost is not properly displayed"

    def test_dogadamycie2(self, setup):
        """Test1: Declined initial Cookies flow."""
        self.driver.get("https://turbotlumaczenia.pl/")
        main_turbo_page = TurboMainPage(self.driver)
        main_turbo_page.click_accept_cookies()
        main_turbo_page.goto_wycena_tlumaczenia()
        form_order_page = TurboFormOrderPage(self.driver)
        form_order_page.click_translateto_menu()
        form_order_page.choose_translateto_niemiecki()
        form_order_page.choose_add_proofreading()
        form_order_page.provide_text_to_translation_area(TEXT_TO_TRANSLATE)
        assert form_order_page.is_estimated_time_value_visible(), \
            "Estimated time is not properly displayed"
        assert form_order_page.is_estimated_cost_value_visible(), \
            "Estimated cost is not properly displayed"


if __name__ == "__main__":
    print("Main Test case definition is as following:\n")
    print(__doc__)
    print()
    all_test_variants = [name_el for name_el in dir(TestDogadamyCie) if "test_" in name_el]
    print("Below variants of Main Test test are implemented:")
    for i, v in enumerate(all_test_variants):
        print("Var_", i + 1, ". ", v, sep="")
