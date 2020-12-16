import os
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
options = Options()
options.page_load_strategy = 'normal'

target_month = "June"
target_date = "14"
target_site_num = "011"

def document_initialized(driver):
    open_month = driver.find_element(By.CSS_SELECTOR, "button.SingleDatePickerInput_calendarIcon.SingleDatePickerInput_calendarIcon_1").click()
    return driver.find_element(By.CLASS_NAME, "CalendarMonth_caption.CalendarMonth_caption_1")

def get_month(driver):
    open_month = driver.find_element(By.CSS_SELECTOR, "button.SingleDatePickerInput_calendarIcon.SingleDatePickerInput_calendarIcon_1").click()
    month_container = driver.find_element(By.CSS_SELECTOR, "div.SingleDatePicker_picker.SingleDatePicker_picker_1.SingleDatePicker_picker__directionLeft.SingleDatePicker_picker__directionLeft_2")
    months = driver.find_elements_by_class_name("CalendarMonth_caption.CalendarMonth_caption_1")
    #monthText = month.get_attribute('innerHTML')
    return months

def click_to_target_month(driver):
    months = get_month(driver)

    while target_month not in months[1].get_attribute('innerHTML'):
        driver.find_element(By.CSS_SELECTOR, "div.sarsa-day-picker-range-controller-month-navigation-button.right").click()
        months = get_month(driver)
    return months[1]


def get_dates(driver):
    dates = driver.find_elements_by_class_name("CalendarDay.CalendarDay_1.CalendarDay__default.CalendarDay__default_2")
    for date in dates:
        if target_date in date.get_attribute('innerHTML') and date.is_displayed():
            date.click()
        dates = driver.find_elements_by_class_name("CalendarDay.CalendarDay_1.CalendarDay__default.CalendarDay__default_2")

#def click_date_for_site(driver):
#    avail_dates = driver.find_elements_by_class_name("rec-availability-date")
#    for adate in avail_dates:
#        if "Site 015 is available" in adate.get_attribute('aria-label'):
#            print(adate.get_attribute('aria-label'))

driver = Firefox(options=options)
driver.get("https://www.recreation.gov/camping/campgrounds/232854/availability")
driver.maximize_window()
WebDriverWait(driver, timeout=5).until(document_initialized)
month = click_to_target_month(driver)
get_dates(driver)




#inputbox = driver.find_element(By.CSS_SELECTOR, "input#single-date-picker-1.DateInput_input.DateInput_input_1")
#inputbox.send_keys("06/08/2020" + Keys.ENTER)
#for x in range(10):
#    inputbox.send_keys(Keys.ARROW_LEFT)
#for x in range(10):
#    inputbox.send_keys(Keys.BACKSPACE)
#driver.find_element(By.TAG_NAME, 'button').click()
driver.quit()


     #days = driver.find_element(By.CSS_SELECTOR, "td.CalendarDay.CalendarDay_1.CalendarDay__defaultCursor.CalendarDay__defaultCursor_2.CalendarDay__default.CalendarDay__default_3.CalendarDay__blocked_calendar.CalendarDay__blocked_calendar_4")
