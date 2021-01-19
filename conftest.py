import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def setup(request):
    chrome_options = Options()
    chrome_options.add_argument("--lang=pl")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # self.driver.implicitly_wait(10)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()
