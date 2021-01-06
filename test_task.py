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

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# https://sportowefakty.wp.pl/
# skoki-narciarskie/917575/69-turniej-czterech-skoczni-pierwsza-proba-sil-dla-kamila-stocha-co-za-skok-pola

TEXT_TO_TRANSLATE = """69. Turniej Czterech Skoczni. Pierwsza próba sił dla Kamila Stocha! Co za skok Polaka!
Halvor Egner Granerud postraszył na treningu, ale kwalifikacje w Bischofshofen wygrał już Kamil.
Polak zwyciężył po długim pięknym stylowo skoku. Norweg zajął 3 miejsce.
Sensacją eliminacji jest odpadnięcie Anze Laniska. Najważniejsze jednak, że Stoch wygrał próbę nerwów.
Pokazał Norwegowi, że nie robią na nim żadnego wrażenia dalekie skoki rywala z treningu.
Co więcej, to Granerud wydaje się być znacznie bardziej zdenerwowany.
Gdy zdał już sobie sprawę, że nie wygra kwalifikacji, machał zrezygnowany głową.
Widać było, że chciał we wtorek wywrzeć presję na trzykrotnym mistrzu olimpijskim, ale zupełnie mu się to nie udało.
W eliminacjach z bardzo dobrej strony pokazał się także Dawid Kubacki.
Rekordzista skoczni, z dość mocnym wiatrem w plecy, uzyskał 134,5 metra. Zajął 6. miejsce.
Zwykle Kubacki w treningach w Bischofshofen jednak nie błyszczy, a wszystko co najlepsze zostawia na konkurs.
Oby tak było także i tym razem, bo wciąż liczymy na podwójne zwycięstwo Biało-Czerwonych w turnieju.
Sensacją kwalifikacji jest dopiero 52. miejsce Anze Laniska.
W Innsbrucku Słoweniec przegrał tylko, że Stochem, od kilku konkursów skakał świetnie a w Bischofshofen spadł na bulę.
108 metrów oznaczało dla niego koniec turnieju.
Nie zakwalifikował się do pierwszej serii i nie utrzyma wysokiego 6. miejsca w całych zawodach.
Do środowego konkursu łącznie awansowało siedmiu Polaków.
Z dobrej strony pokazał się Aleksander Zniszczoł, który po próbie na 126. metr zajął 18. miejsce.
Fajerwerków nie odpalili w kwalifikacjach Andrzej Stękała i Piotr Żyła sklasyfikowani na 26. i 28. lokacie.
Żyła nie raz przyzwyczaił jednak, że w dzień kwalifikacyjny i w dzień konkursowy prezentuje zupełnie inne oblicza.
Z piątej dziesiątki do konkursu awansowali 42. Klemens Murańka i 45. Maciej Kot.
Pary, w których będą skakać Biało-Czerwoni w środę, prezentują się bardzo ciekawie.
Stękała otworzy konkurs, a jego rywalek w pierwszej parze dnia będzie sam Karl Geiger.
Niemiec jest 4ty w turnieju, ale w części austriackiej obniżył loty. W kwalifikacjach był 25. po skoku na 123,5 metra.
W eliminacjach panowały bardzo dobre warunki do skakania. Wiatr nie przekraczał 0,5 m/s.
Momentami wiało trochę mocniej w plecy, ale i tak - po raz kolejny w tym turnieju - na warunki nie można narzekać.
Wszyscy skakali z 9. belki startowej. Czekamy już na wielki finał 69. Turnieju Czterech Skoczni."""


class TimeEstimationHasBeenDone(object):
    """Custom Wait Condition for checking that an estimated time value has been recalculated.

    estimated_time_xpath - xpath used to find the estimated time value element
    initial_estimated_time_text - used to recognize that the estimated time value has changed
    returns True once estimated time value has been recalculated
    """

    def __init__(self, estimated_time_xpath):
        self.estimated_time_xpath = estimated_time_xpath
        self.initial_estimated_time_text = "godzina"

    def __call__(self, driver):
        estimated_time_value = driver.find_element_by_xpath(self.estimated_time_xpath)
        if len(estimated_time_value.text) > len(self.initial_estimated_time_text):
            return True
        else:
            return False


class CostEstimationHasBeenDone(object):
    """Custom Wait Condition for checking that an cost value has been recalculated.

    estimated_time_xpath - xpath used to find the estimated cost value element
    initial_translation_cost_text - used to recognize that the estimated cost value has changed
    returns True once estimated cost value has been recalculated
    """

    def __init__(self, translation_cost_xpath):
        self.translation_cost_xpath = translation_cost_xpath
        self.initial_translation_cost_text = "z 10 zł"

    def __call__(self, driver):
        translation_cost = driver.find_element_by_xpath(self.translation_cost_xpath)

        if len(translation_cost.text) != len(self.initial_translation_cost_text):
            return True
        else:
            return False


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


class TurboFormOrderPage:
    """Page Object class for Order Form page: 'https://panel.turbotlumaczenia.pl/pl/order/write?from=cta'"""

    def __init__(self, webdriver_el):
        self.driver = webdriver_el
        self.translateto_menu_xpath = "//div[contains(@class, 'content__input')]/span[@id='target_lang_label']"
        self.translateto_niemiecki_xpath = "//li[@data-name='Niemiecki']"
        self.proofreading_id = "proofreading"
        self.translation_text_area_xpath = "//textarea[@id='content']"
        self.estimated_time_value_xpath = "//span[@data-bind-expected-realisation-time=''][@class='content__strong']"
        self.estimated_cost_value_xpath = "//span[@data-bind-expected-price=''][@class='content__strong']"

    def click_translateto_menu(self):
        """Opening target language menu."""
        self.driver.find_element_by_xpath(self.translateto_menu_xpath).click()

    def choose_translateto_niemiecki(self):
        """Choosing target language of translation as german."""
        niemiecki_buttons = self.driver.find_elements_by_xpath(self.translateto_niemiecki_xpath)
        for niemiecki in niemiecki_buttons:
            if niemiecki.is_displayed():
                niemiecki.click()

    def choose_add_proofreading(self):
        """Choosing additional native speaker proofreading."""
        self.driver.find_element_by_id(self.proofreading_id).click()

    def provide_text_to_translation_area(self, text_input):
        """Injecting source text to be translated to translation area."""
        translation_text_area = self.driver.find_element_by_xpath(self.translation_text_area_xpath)
        translation_text_area.click()
        translation_text_area.send_keys(" ".join(text_input.split()))

    def is_estimated_time_value_visible(self) -> bool:
        """Method checks if estimated time value has been recalculated and if result is visible.
        It is done in 2 steps:
        -- 1. initial check if estimated time value is displayed
        -- 2. checking if value has been recalculated (not displaying def values) by using Custom Wait
        method returns True/False value"""
        estimated_time_value = self.driver.find_element_by_xpath(self.estimated_time_value_xpath)
        if estimated_time_value.is_displayed():
            exp_wait = WebDriverWait(self.driver, 10)
            return exp_wait.until(TimeEstimationHasBeenDone(self.estimated_time_value_xpath))
        else:
            return False

    def is_estimated_cost_value_visible(self) -> bool:
        """Method checks if estimated cost value has been recalculated and if result is visible.
        It is done in 2 steps:
        -- 1. initial check if estimated cost value is displayed
        -- 2. checking if value has been recalculated (not def values) by using Custom Wait
        method returns True/False value"""
        estimated_cost_value = \
            self.driver.find_element_by_xpath(self.estimated_cost_value_xpath)
        if estimated_cost_value.is_displayed():
            exp_wait = WebDriverWait(self.driver, 10)
            return exp_wait.until(CostEstimationHasBeenDone(self.estimated_cost_value_xpath))
        else:
            return False


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
