
import os
import time
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
options = Options()
options.page_load_strategy = 'normal'

campground = "https://www.recreation.gov/camping/campgrounds/232854/availability"


class wait(object):
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self.old_page = self.driver.find_element_by_tag_name('html')

    def page_loaded(self):
        new_page = self.driver.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        start_time = time.time()
        while time.time() < start_time + 5:
            if self.page_loaded():
                return True
            else:
                time.sleep(0.1)
        raise Exception("Timeout waiting for page to load")


try:
    driver = Firefox(options=options)
    driver.implicitly_wait(10)
except Exception as e:
    print("Fail: Browser setup ", e)
    driver.quit()

print("driver version:", driver.capabilities['moz:geckodriverVersion'])
print("browser version:", driver.capabilities['browserVersion'])



try:
    with wait(driver):
        driver.get(example_campground)
    assert 'Recreation.gov' in driver.title
except Exception as e:
    print("Fail: Initial load ", e)
    driver.quit()
else:
    print("Success: Initial load")

