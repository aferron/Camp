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


# Hard code the date, site number, and time to make the reservation
target_month = "July"
target_date = "19"
target_site_num = 1
target_min = 55
target_hour = 7


# Hard code email and password
email = "you@host.com"
password = "00000"


# Some variables to make the code easier to read
home = "https://www.recreation.gov/"
date_pick_button = "button.SingleDatePickerInput_calendarIcon.SingleDatePickerInput_calendarIcon_1"
cal_month = "CalendarMonth_caption"
direction_left = "div.SingleDatePicker_picker.SingleDatePicker_picker_1.SingleDatePicker_picker__directionLeft.SingleDatePicker_picker__directionLeft_2"
right_arrow = "div.sarsa-day-picker-range-controller-month-navigation-button.right"
cal_day = "CalendarDay.CalendarDay_1.CalendarDay__default.CalendarDay__default_2"
campground = "https://www.recreation.gov/camping/campgrounds/232000/availability"
table_scroller = "sticky-table-horizontal-scroller"
next_days = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div[3]/div[2]/div[2]/div/div[1]/div/div/div[2]/div/button[3]"
next_days_class = "sarsa-button.sarsa-button-link.sarsa-button-sm"
next_five_xpath = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div[3]/div[2]/div[2]/div/div[1]/div/div/div[2]/div/button[3]"
book_now_xpath = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div[3]/div[3]/div/div/div/div/div[2]/button"
login_xpath = "/html/body/div[2]/div/div/div/header/div/nav/div/div[2]/div/div/button[2]"
continue_xpath = "/html/body/div[13]/div/div/div[2]/button[1]"


# wait until a page loads
class wait(object):
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self.old_page = self.driver.find_element_by_tag_name('html')

    # check if the page is loaded
    def page_loaded(self):
        new_page = self.driver.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    # give a time limit for the page to load
    def __exit__(self, *_):
        start_time = time.time()
        while time.time() < start_time + 5:
            if self.page_loaded():
                return True
            else:
                time.sleep(0.1)
        raise Exception("Timeout waiting for page to load")


# check that the page elements have loaded, using the date pick button as the test element
def document_initialized(driver):
    open_month = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, date_pick_button)))
    return driver.find_element(By.CSS_SELECTOR, date_pick_button)


# log in to Recreation.gov account
def login(driver):
    nhbs = driver.find_elements(By.CLASS_NAME, "nav-header-button")
    length = len(nhbs)

    nhbs[1].click()

    email_input = driver.find_element(By.ID, "rec-acct-sign-in-email-address").send_keys(email + Keys.ENTER)
    pwd_input = driver.find_element(By.ID, "rec-acct-sign-in-password").send_keys(password + Keys.ENTER)


    #login = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, login_xpath))).click()


# navigate to the month that you want to make the reservation
def click_to_target_month(driver):
    time.sleep(2)
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


# click on the date you want
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


# load the table
def table_loaded(driver):
    return driver.find_element_by_xpath("//table/tbody/tr[7]/td")


# navigate to the site number, select all the available dates
def click_date_for_site(driver):
    found_site = 0
    found_row = None
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
        driver.quit()
    else:
        print("Success: select available dates")
        print("number of days selected: ", selected)

    return found_site


# select all the available dates
def select_avail_dates(driver, row):
    tds = row.find_elements_by_tag_name("td")

    # click the first available date
    tds[1].click()
    tds = row.find_elements_by_tag_name("td")

    # wait until the hour is reached
    x = 0
    while time.localtime().tm_hour != target_hour:
        x += 1

    # click the last date shown
    tds[10].click()

    # click "book now" to get it
    book_now = driver.find_element_by_xpath(book_now_xpath)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, book_now_xpath))).click()

    # if it's too early then try again, just once. Still would be better written recursively
    if driver.find_element_by_class_name("booking-notification-block"):
        print("blocked")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, continue_xpath))).click()

        tds = row.find_elements_by_tag_name("td")

        tds[1].click()
        tds = row.find_elements_by_tag_name("td")
        tds[10].click()

        book_now = driver.find_element_by_xpath(book_now_xpath)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, book_now_xpath))).click()

    return 10


# check that an element is not stale
def not_stale(driver, element):
    try:
        element.is_enabled()
        return True
    except Exception as e:
        return False


# used to select five days at a time to reserve
def get_next_five(driver):
    next_five = driver.find_element_by_xpath(next_five_xpath)

    print(next_five.get_attribute("aria-label"))

    time.sleep(3)
    return True


# open recreation.gov page
def open_rec_gov(driver):
    try:
        with wait(driver):
            driver.get(home)
        assert 'Recreation.gov' in driver.title
    except Exception as e:
        print("Fail: Initial load ", e)
        driver.quit()
    else:
        print("Success: Initial load")


# click through to the next available dates for the site
def click_next_days(driver):
    try:
        driver.find_element_by_xpath(next_days).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, next_days))).click()
    except Exception as e:
        print("Fail: click next days", e)
        driver.quit
    else:
    print("Success: click next days", e)


# set up browser
try:
    driver = Firefox(options=options)
    driver.implicitly_wait(10)
except Exception as e:
    print("Fail: Browser setup ", e)
    driver.quit()

print("driver version:", driver.capabilities['moz:geckodriverVersion'])
print("browser version:", driver.capabilities['browserVersion'])


# nav to campground reservation page
try:
    with wait(driver):
        driver.get(campground)
    assert 'Recreation.gov' in driver.title
except Exception as e:
    print("Fail: Initial load ", e)
    driver.quit()
else:
    print("Success: Initial load")


# login
try:
    driver.maximize_window()
    login(driver)
except Exception as e:
    print("Fail: login", e)
    driver.quit()
else:
    print("Success: login")


# navigate to the month 
try:
    month = click_to_target_month(driver)
    print("month returned:", month)
    assert target_month in month
except Exception as e:
    print("Fail: nav to target month", e)
    driver.quit()
else:
    print("Success: nav to target month")


# click on the start date for the reservation 
try:
    clicked_date = get_dates(driver)
except Exception as e:
    print("Fail: get dates", e)
    driver.quit()
else:
    print("Success: get dates returned", clicked_date)


# navigate to the site and click on the first available date
try:
    found_site = click_date_for_site(driver)
    assert target_site_num == found_site
except Exception as e:
    print("Fail: nav to site number", e)
    driver.quit()
else:
    print("Success: nav to site number returned", found_site)

#driver.quit()
