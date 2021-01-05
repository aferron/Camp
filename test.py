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
cal_month = "CalendarMonth_caption"
direction_left = "div.SingleDatePicker_picker.SingleDatePicker_picker_1.SingleDatePicker_picker__directionLeft.SingleDatePicker_picker__directionLeft_2"
right_arrow = "div.sarsa-day-picker-range-controller-month-navigation-button.right"
cal_day = "CalendarDay.CalendarDay_1.CalendarDay__default.CalendarDay__default_2"
example_campground = "https://www.recreation.gov/camping/campgrounds/232854/availability"
table_scroller = "sticky-table-horizontal-scroller"



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
    return driver.find_element(By.CSS_SELECTOR, date_pick_button)


def click_to_target_month(driver):
    driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")

    open_month = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, date_pick_button))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, cal_month)))
    months = driver.find_elements_by_class_name(cal_month)

    old_month = months[1].get_attribute('innerHTML')
    new_month = old_month
    while target_month not in months[1].get_attribute('innerHTML'):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, right_arrow))).click()
        while old_month == new_month:
            months = driver.find_elements_by_class_name(cal_month)
            new_month = months[1].get_attribute('innerHTML')
        old_month = new_month

    return months[1].get_attribute('innerHTML')

def get_dates(driver):
    dates = driver.find_elements_by_class_name(cal_day)
    found = ''
    for date in dates:
        found = date.text
        # try get innerText
        if target_date in date.get_attribute('innerHTML') and date.is_displayed():
            date.click()

            break
    return found

def table_loaded(driver):
    return driver.find_element_by_xpath("//table/tbody/tr[7]/td")


def click_date_for_site(driver):
    found_site = 0
    found_row = None
    #div = driver.find_element_by_xpath("//table/tbody/tr[15]/td[2]").click()
    tbody = driver.find_element_by_xpath("//table/tbody")
    rows = driver.find_elements_by_class_name("null ")

    for row in rows:
        found_site = int(row.find_element_by_class_name("rec-availability-item").text)
        if found_site == target_site_num:
            found_row = row
            break

    try:
        selected = select_avail_dates(driver, found_row)
    except Exception as e:
        print("Fail: select available dates", e)
        driver.quit
    else:
        print("Success: select available dates")
        print("number of days selected: ", selected)
    return found_site


def select_avail_dates(driver, row):
    tds = row.find_elements_by_tag_name("td")
    tds.pop(0)
    count = 0
    for td in tds:
        # add wait here for availability
        if count == 1:
            count += 1
            continue
        # replace isEnabled with a custom staleness check
        #if td.is_enabled():
        if not_stale(driver, td):
            td.click()
            count += 1
        else:
            tds = row.find_elements_by_tag_name("td")
            tds.pop(0)
            tds[count].click()
            count += 1
            break
    return count

def not_stale(driver, element):
    try:
        element.is_enabled()
        return true
    except Exception as e:
        return false




try:
    driver = Firefox(options=options)
    driver.implicitly_wait(10)
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
    driver.maximize_window()
    month = click_to_target_month(driver)
    print("month returned:", month)
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

