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


# https://sportowefakty.wp.pl/
# skoki-narciarskie/917575/69-turniej-czterech-skoczni-pierwsza-proba-sil-dla-kamila-stocha-co-za-skok-pola

TEXT_TRANSLATE = """
69. Turniej Czterech Skoczni. Pierwsza próba sił dla Kamila Stocha! Co za skok Polaka! Sensacyjna porażka Słoweńca.
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
