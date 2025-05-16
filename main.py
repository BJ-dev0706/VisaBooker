import logging
import os
import sys

from dotenv import load_dotenv
from seleniumbase import SB
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

REQUIRED_ENV_VARS = [
    'AUTH_EMAIL',
    'AUTH_PASSWORD',
    # 'COUNTRY_SELECT_SITE_URL',
    'USER_FIRST_NAME',
    'USER_LAST_NAME',
    'USER_BIRTHDAY',
    'USER_PASSPORT_NUMBER',
    'USER_EXPIRE_DATA',
    'USER_PHONE_HEADER',
    'USER_PHONE_BODY',
    'USER_ADDRESS_LINE',
    'DEFAULT_APPLYING_FROM',
    'DEFAULT_GOING_TO',
    'PROXY'
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logging.getLogger(__name__)

load_dotenv()
 
missing_vars = [var for var in REQUIRED_ENV_VARS if os.getenv(var) is None]
if missing_vars:
    raise EnvironmentError(f"Missing environment variables: {missing_vars}")

AUTH_EMAIL=os.getenv("AUTH_EMAIL")
AUTH_PASSWORD=os.getenv("AUTH_PASSWORD")
# COUNTRY_SELECT_SITE_URL=os.getenv("COUNTRY_SELECT_SITE_URL")

USER_FIRST_NAME=os.getenv("USER_FIRST_NAME")
USER_LAST_NAME=os.getenv("USER_LAST_NAME")
USER_BIRTHDAY=os.getenv("USER_BIRTHDAY")
USER_PASSPORT_NUMBER=os.getenv("USER_PASSPORT_NUMBER")
USER_EXPIRE_DATA=os.getenv("USER_EXPIRE_DATA")
USER_PHONE_HEADER=os.getenv("USER_PHONE_HEADER")
USER_PHONE_BODY=os.getenv("USER_PHONE_BODY")
USER_ADDRESS_LINE=os.getenv("USER_ADDRESS_LINE")

DEFAULT_APPLYING_FROM=os.getenv("DEFAULT_APPLYING_FROM")
DEFAULT_GOING_TO=os.getenv("DEFAULT_GOING_TO")

PROXY = os.getenv("PROXY")

def login(
    sb:SB,
)-> None:
    login_url = 'https://visa.vfsglobal.com/usa/en/aut/login'
    # login_url = 'https://visa.vfsglobal.com/cpv/en/prt/login'
    logging.info(f'Login into {login_url}')    
    sb.uc_open_with_reconnect(login_url, 30)

    try:
        sb.assert_element_present('#onetrust-banner-sdk', timeout=30)
        sb.click('#onetrust-reject-all-handler')
    except:
        pass

    sb.reconnect(10)
    logging.info('Attempt to bypass Cloudflare captcha')
    sb.uc_gui_click_captcha()
    logging.info('Success Bypassing Cloudflare captcha')

    sb.reconnect(10)
    sb.assert_element_present('#email', timeout=30)
    sb.type('#email', AUTH_EMAIL)
    sb.type('#password', AUTH_PASSWORD)

    sb.reconnect(1)
    sb.assert_element_present("/html/body/app-root/div/main/div/app-login/section/div/div/mat-card/form/button", timeout=30)    
    sb.click("/html/body/app-root/div/main/div/app-login/section/div/div/mat-card/form/button")
    logging.info('Successfully logged in')

    sb.reconnect(10)

    if sb.driver.current_url == 'https://visa.vfsglobal.com/usa/en/aut/login':
        sb.reconnect(10)
        sb.uc_gui_click_captcha()
        sb.reconnect(10)
        sb.click("/html/body/app-root/div/main/div/app-login/section/div/div/mat-card/form/button")

def book_appointment(
    sb:SB,
)-> None:

    logging.info('Booking appointment')

    WebDriverWait(sb.driver, 20).until(lambda d: len(d.window_handles) == 1)
    new_window = sb.driver.window_handles[0]
    sb.driver.switch_to.window(new_window)
    sb.reconnect(10)

    size = sb.driver.get_window_size()
    window_width = size['width']
    window_height = size['height']
    
    x_coodinate = (window_width / 1264) * 965
    y_coodinate = (window_height / 745) * 155

    ActionChains(sb.driver).move_by_offset(x_coodinate, y_coodinate).click().perform()
    
    WebDriverWait(sb.driver, 10).until(lambda d: len(d.window_handles) == 1)
    new_window = sb.driver.window_handles[0]
    sb.driver.switch_to.window(new_window)
    sb.reconnect(10)

    sb.assert_element_present('/html/body/app-root/div/main/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[1]/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]/div', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[1]/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]/div')
    sb.click('//mat-option//span[text()=" Austria Visa Application Center - New York "]')
    sb.reconnect(5)

    sb.assert_element_present('/html/body/app-root/div/main/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[2]/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]/div', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[2]/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]/div')
    sb.click('//mat-option//span[text()=" Austria Visa Application "]')

    sb.assert_element_present('/html/body/app-root/div/main/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[3]/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]/div', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[3]/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]/div')
    sb.click('//mat-option//span[text()=" Visa - D "]')
    sb.reconnect(5)

    sb.assert_element_present('.btn.mat-btn-lg.btn-block.btn-brand-orange.mdc-button.mdc-button--raised.mat-mdc-raised-button.mat-unthemed.mat-mdc-button-base.ng-star-inserted', timeout=30)
    sb.click('.btn.mat-btn-lg.btn-block.btn-brand-orange.mdc-button.mdc-button--raised.mat-mdc-raised-button.mat-unthemed.mat-mdc-button-base.ng-star-inserted')
    
    logging.info('Successfully booked appointment')

def your_details(
    sb:SB
)-> None:

    logging.info('Fill out your details')
    WebDriverWait(sb.driver, 20).until(lambda d: len(d.window_handles) == 1)
    new_web_window = sb.driver.window_handles[0]
    sb.driver.switch_to.window(new_web_window)
    
    sb.reconnect(40)

    sb.assert_element_present('input[placeholder="Enter your first name"]', timeout=30)
    sb.type('input[placeholder="Enter your first name"]', USER_FIRST_NAME)
    
    sb.assert_element_present('input[placeholder="Please enter last name."]', timeout=30)
    sb.type('input[placeholder="Please enter last name."]', USER_LAST_NAME)

    sb.assert_element_present("/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[8]/div/div[1]/div/app-dropdown/div/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]", timeout=30)
    sb.click("/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[8]/div/div[1]/div/app-dropdown/div/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]")
    sb.click('/html/body/div[4]/div[2]/div/div/mat-option[2]')

    sb.assert_element_present('input[placeholder="Please select the date"]', timeout=30)
    sb.type('input[placeholder="Please select the date"]', USER_BIRTHDAY)

    sb.assert_element_present("/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[9]/div/div/div/app-dropdown/div/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]", timeout=30)
    sb.click("/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[9]/div/div/div/app-dropdown/div/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]")
    sb.reconnect(2)

    sb.assert_element_present('/html/body/div[4]/div[2]/div/div/mat-option[232]', timeout=30)
    sb.click('/html/body/div[4]/div[2]/div/div/mat-option[232]')
    sb.reconnect(2)

    sb.assert_element_present('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[10]/div/div/div/app-input-control/div/mat-form-field/div[1]/div/div[2]/input', timeout=30)
    sb.type('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[10]/div/div/div/app-input-control/div/mat-form-field/div[1]/div/div[2]/input', USER_PASSPORT_NUMBER)
    
    sb.assert_element_present('input[placeholder="Please select the date"]', timeout=30)
    sb.type('#passportExpirtyDate', USER_EXPIRE_DATA)

    sb.assert_element_present('input[placeholder="44"]', timeout=30)        
    sb.type('input[placeholder="44"]', USER_PHONE_HEADER)

    sb.assert_element_present('input[placeholder="012345648382"]', timeout=30)
    sb.type('input[placeholder="012345648382"]', USER_PHONE_BODY)

    sb.assert_element_present('input[placeholder="Enter Email Address"]', timeout=30)
    sb.type('input[placeholder="Enter Email Address"]', AUTH_EMAIL)

    sb.assert_element_present('input[placeholder="Enter Address line 1"]', timeout=30)
    sb.type('input[placeholder="Enter Address line 1"]', USER_ADDRESS_LINE)

    sb.assert_element_present('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button')

    
    WebDriverWait(sb.driver, 20).until(lambda d: len(d.window_handles) == 1)
    new_web_window = sb.driver.window_handles[0]
    sb.driver.switch_to.window(new_web_window)
    sb.reconnect(3)

    sb.assert_element_present('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[2]/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[2]/div/div[2]/button')
    logging.info('Successfully filled out your details')

    
def book_appointment_data(
    sb:SB
)-> None:
    # WebDriverWait(sb.driver, 20).until(lambda d: len(d.window_handles) == 1)
    # new_web_window = sb.driver.window_handles[0]
    # sb.driver.switch_to.window(new_web_window)
    # sb.reconnect(3)

    # sb.assert_element_present('/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[1]/div[2]/div/div/full-calendar/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[5]/td[5]', timeout=30)
    # sb.click('/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[1]/div[2]/div/div/full-calendar/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[5]/td[5]')
    logging.info('Booking appointment data')
    WebDriverWait(sb.driver, 20).until(lambda d: len(d.window_handles) == 1)
    new_web_window = sb.driver.window_handles[0]
    sb.driver.switch_to.window(new_web_window)
    sb.reconnect(10)
    
    #danger
    calendar_days = sb.find_elements(By.CSS_SELECTOR, 'td.fc-day-future.fc-daygrid-day.date-availiable')
    calender_day = calendar_days[0].find_element(By.CSS_SELECTOR, 'a[class="fc-daygrid-day-number"]')
    day_id = calender_day.get_attribute('id')
    print(day_id)

    half_height = sb.execute_script("return document.body.scrollHeight / 2")
    sb.execute_script(f"window.scrollTo(0, {half_height});")
    
    sb.sleep(1)
    sb.click(By.CSS_SELECTOR, f'td[aria-labelledby="{day_id}"]')
    
    sb.reconnect(10)
    sb.assert_element_present("/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[1]/div[4]/table/tbody/tr[3]/td[2]/div[2]", timeout=30)
    sb.click("/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[1]/div[4]/table/tbody/tr[3]/td[2]/div[2]")

    sb.assert_element_present('/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[2]/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[2]/div/div[2]/button')
    logging.info('complete All process')

def services(
    sb:SB
)->None:

    logging.info('Configure Services')
    WebDriverWait(sb.driver, 20).until(lambda d: len(d.window_handles) == 1)
    new_web_window = sb.driver.window_handles[0]
    sb.driver.switch_to.window(new_web_window)
    sb.reconnect(5)

    sb.assert_element_present('/html/body/app-root/div/main/div/app-manage-service/section/mat-card[2]/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-manage-service/section/mat-card[2]/div/div[2]/button')
    logging.info('Successfully Configure Services')

def review(
    sb:SB
)->None:
    logging.info('Review')
    # WebDriverWait(sb.driver, 20).until(lambda d: len(d.window_handles) == 1)
    # new_web_window = sb.driver.window_handles[0]
    # sb.driver.switch_to.window(new_web_window)
    sb.sleep(1)
    sb.click('label[for="mat-mdc-checkbox-1-input"]')
    sb.sleep(1)
    sb.click('label[for="mat-mdc-checkbox-2-input"]')
    sb.sleep(1)
    sb.click('label[for="mat-mdc-checkbox-3-input"]')
    # sb.assert_element_present('/html/body/app-root/div/main/div/app-review-and-payment/section/form/mat-card[1]/div[9]/mat-checkbox/div/div/input', timeout=30)
    # sb.click('/html/body/app-root/div/main/div/app-review-and-payment/section/form/mat-card[1]/div[9]/mat-checkbox/div/div/input')

    # sb.assert_element_present('/html/body/app-root/div/main/div/app-review-and-payment/section/form/mat-card[1]/div[10]/mat-checkbox/div/div/input', timeout=30)
    # sb.click('/html/body/app-root/div/main/div/app-review-and-payment/section/form/mat-card[1]/div[10]/mat-checkbox/div/div/input')

    sb.assert_element_present('/html/body/app-root/div/main/div/app-review-and-payment/section/form/mat-card[2]/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-review-and-payment/section/form/mat-card[2]/div/div[2]/button')
    logging.info('Successfully Review')

def confirmation(
    sb:SB
)->None:
    logging.info('Confirmation')
    WebDriverWait(sb.driver, 20).until(lambda d: len(d.window_handles) == 1)
    new_web_window = sb.driver.window_handles[0]

    # Save the current page HTML
    page_html = sb.get_page_source()
    with open('page.html', 'w', encoding='utf-8') as f:
        f.write(page_html)
    logging.info('Saved page HTML to page.html')

    sb.driver.switch_to.window(new_web_window)
    sb.reconnect(5)

    sb.assert_element_present('/html/body/app-root/div/main/div/app-payment-confirmation/section/mat-card[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-payment-confirmation/section/mat-card[2]/button')
    logging.info('Successfully Confirmation')

def dashboard(
    sb:SB
)->None:
    logging.info('Dashboard')
    WebDriverWait(sb.driver, 20).until(lambda d: len(d.window_handles) == 1)
    new_web_window = sb.driver.window_handles[0]
    sb.driver.switch_to.window(new_web_window)
    sb.reconnect(300)


def main() -> None:
    # with SB(uc=True, incognito=True) as sb:
    with SB(uc=True, incognito=True) as sb:
        login(sb)
        book_appointment(sb)
        your_details(sb)
        book_appointment_data(sb)
        services(sb)
        review(sb)
        confirmation(sb)
        dashboard(sb)

if __name__ == "__main__":
    main()












