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

target_month = "June"
target_date = "14"
target_site_num = 11
date_pick_button = "button.SingleDatePickerInput_calendarIcon.SingleDatePickerInput_calendarIcon_1"
cal_month = "CalendarMonth_caption.CalendarMonth_caption_1"
direction_left = "div.SingleDatePicker_picker.SingleDatePicker_picker_1.SingleDatePicker_picker__directionLeft.SingleDatePicker_picker__directionLeft_2"
right_arrow = "div.sarsa-day-picker-range-controller-month-navigation-button.right"
cal_day = "CalendarDay.CalendarDay_1.CalendarDay__default.CalendarDay__default_2"
example_campground = "https://www.recreation.gov/camping/campgrounds/232854/availability"



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



def document_initialized(driver):
    open_month = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, date_pick_button)))
    #open_month.find_element(By.CSS_SELECTOR, date_pick_button).click()
    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((open_month.find_element(By.CSS_SELECTOR, date_pick_button)))).click()

    #return driver.find_element(By.CLASS_NAME, cal_month)
    return driver.find_element(By.CSS_SELECTOR, date_pick_button)


def click_to_target_month(driver):
    #need to scroll up if the date pick button isn't visible. how to scroll up??
    #use webdriver wait from here?https://selenium-python.readthedocs.io/waits.html
    table = WebDriverWait(driver, 20).until(EC.element_to_be
    while not driver.find_element(By.CSS_SELECTOR, date_pick_button).is_displayed()
        driver.send_keys(Keys.ARROWUP)

    open_month = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, date_pick_button))).click()
    #open_month = driver.find_element(By.CSS_SELECTOR, date_pick_button).click()
    months = driver.find_elements_by_class_name(cal_month)

    while target_month not in months[1].get_attribute('innerHTML'):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, right_arrow))).click()
        #driver.find_element(By.CSS_SELECTOR, right_arrow).click()
        months = driver.find_elements_by_class_name(cal_month)
    print("returning from click to target month:", months[1].text)
    return months[1].text


def get_dates(driver):
    dates = driver.find_elements_by_class_name(cal_day)
    found = ''
    for date in dates:
        found = date.text
        if target_date in date.get_attribute('innerHTML') and date.is_displayed():
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(date)).click()
            break
    return dates


def table_loaded(driver):
    return driver.find_element_by_xpath("//table/tbody/tr[7]/td")


def click_date_for_site(driver):
    trs = driver.find_elements_by_xpath("//table/tbody/tr")
    row = None

    for tr in trs:
        row = tr
        site = tr.find_element_by_class_name("rec-availability-item")
        found_site = int(site.text)
        if found_site == target_site_num:
            print("site", found_site, "found")
            break
    return found_site



try:
    driver = Firefox(options=options)
except Exception as e:
    print("Fail: Browser setup ", e)
    driver.quit

print("driver version:", driver.capabilities['moz:geckodriverVersion'])
print("browser version:", driver.capabilities['browserVersion'])

try:
    with wait(driver):
        driver.get(example_campground)
    assert 'Recreation.gov' in driver.title
except Exception as e:
    print("Fail: Initial load ", e)
    driver.quit
else:
    print("Success: Initial load")

try:
    #driver.maximize_window()
    month = click_to_target_month(driver)
    assert target_month in month
except Exception as e:
    print("Fail: nav to target month", e)
    driver.quit
else:
    print("Success: nav to target month")

try:
    clicked_date = get_dates(driver)
except Exception as e:
    print("Fail: get dates", e)
    driver.quit
else:
    print("Success: get dates returned", clicked_date)

try:
    found_site = click_date_for_site(driver)
    assert target_site_num == found_site
except Exception as e:
    print("Fail: nav to site number", e)
    driver.quit
else:
    print("Success: nav to site number returned", found_site)

driver.quit()


    #div = driver.find_element_by_xpath("//table/tbody/tr[15]/td[2]").click()
    #aria_label = div.find_element_by_css_selector('button').click()
    #avail_dates = driver.find_elements_by_class_name("rec-availability-date")
    #for adate in avail_dates:
        #print(adate)
        #if "Site 015 is available" in adate.get_attribute('aria-label'):
            #print(adate.get_attribute('aria-label'))

#inputbox = driver.find_element(By.CSS_SELECTOR, "input#single-date-picker-1.DateInput_input.DateInput_input_1")
#inputbox.send_keys("06/08/2020" + Keys.ENTER)
#for x in range(10):
#    inputbox.send_keys(Keys.ARROW_LEFT)
#for x in range(10):
#    inputbox.send_keys(Keys.BACKSPACE)
#driver.find_element(By.TAG_NAME, 'button').click()


     #days = driver.find_element(By.CSS_SELECTOR, "td.CalendarDay.CalendarDay_1.CalendarDay__defaultCursor.CalendarDay__defaultCursor_2.CalendarDay__default.CalendarDay__default_3.CalendarDay__blocked_calendar.CalendarDay__blocked_calendar_4")
