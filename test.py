import os
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
options = Options()
options.page_load_strategy = 'normal'

def document_initialized(driver):
    return driver.find_element(By.CSS_SELECTOR, "input#single-date-picker-1.DateInput_input.DateInput_input_1")


driver = Firefox(options=options)
driver.get("https://www.recreation.gov/camping/campgrounds/232854/availability")
driver.maximize_window()
WebDriverWait(driver, timeout=5).until(document_initialized)
inputbox = driver.find_element(By.CSS_SELECTOR, "input#single-date-picker-1.DateInput_input.DateInput_input_1")
inputbox.send_keys("06/08/2020" + Keys.ENTER)
for x in range(10):
    inputbox.send_keys(Keys.ARROW_LEFT)
for x in range(10):
    inputbox.send_keys(Keys.BACKSPACE)
#driver.find_element(By.TAG_NAME, 'button').click()
#driver.quit()


     #days = driver.find_element(By.CSS_SELECTOR, "td.CalendarDay.CalendarDay_1.CalendarDay__defaultCursor.CalendarDay__defaultCursor_2.CalendarDay__default.CalendarDay__default_3.CalendarDay__blocked_calendar.CalendarDay__blocked_calendar_4")
