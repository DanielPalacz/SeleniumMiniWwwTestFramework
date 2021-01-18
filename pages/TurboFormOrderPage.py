
from selenium.webdriver.support.wait import WebDriverWait


class TimeEstimationHasBeenDone:
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


class CostEstimationHasBeenDone:
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
