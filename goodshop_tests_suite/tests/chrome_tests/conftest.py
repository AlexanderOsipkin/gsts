import pytest
from selene import browser
from selenium import webdriver


@pytest.fixture(scope='function', autouse=True)
def browser_cfg():
    driver_options = webdriver.ChromeOptions()
    browser.config.driver_options = driver_options
    browser.config.timeout = 15
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield

    browser.quit()