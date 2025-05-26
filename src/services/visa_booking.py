from seleniumbase import SB
from selenium.webdriver.common.by import By
import logging
import time

from src.config.settings import (
    AUTH_EMAIL, AUTH_PASSWORD, USER_FIRST_NAME, USER_LAST_NAME,
    USER_BIRTHDAY, USER_PASSPORT_NUMBER, USER_EXPIRE_DATA,
    USER_PHONE_HEADER, USER_PHONE_BODY, USER_ADDRESS_LINE,
    LOGIN_URL
)
from src.utils.browser import (
    wait_for_single_window, scroll_to_half_page, save_page_html,
    click_coordinates, handle_cookie_banner, bypass_cloudflare
)

logger = logging.getLogger(__name__)

def login(sb: SB) -> None:
    """Log into the visa application website."""
    logging.info(f'Login into {LOGIN_URL}')    
    sb.uc_open_with_reconnect(LOGIN_URL, 30)

    # Handle cookie banner if present
    handle_cookie_banner(sb)
    
    # Bypass Cloudflare captcha
    bypass_cloudflare(sb)

    # Login form
    sb.assert_element_present('#email', timeout=30)
    sb.type('#email', AUTH_EMAIL)
    sb.type('#password', AUTH_PASSWORD)

    sb.reconnect(1)
    sb.assert_element_present("/html/body/app-root/div/main/div/app-login/section/div/div/mat-card/form/button", timeout=30)    
    sb.click("/html/body/app-root/div/main/div/app-login/section/div/div/mat-card/form/button")
    logging.info('Successfully logged in')

    sb.reconnect(10)

    # Handle potential re-login scenario
    if sb.driver.current_url == LOGIN_URL:
        sb.reconnect(10)
        sb.uc_gui_click_captcha()
        sb.reconnect(10)
        sb.click("/html/body/app-root/div/main/div/app-login/section/div/div/mat-card/form/button")

def book_appointment(sb: SB) -> None:
    """Navigate to booking appointment page."""
    logging.info('Booking appointment')

    wait_for_single_window(sb, 20)
    
    # Click on appointment booking button (using coordinates)
    click_coordinates(sb, 965, 155)
    
    wait_for_single_window(sb, 10)

    # Fill out appointment criteria
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

def your_details(sb: SB) -> None:
    """Fill out personal details form."""
    logging.info('Fill out your details')
    wait_for_single_window(sb, 20)
    sb.reconnect(40)

    # Personal information
    sb.assert_element_present('input[placeholder="Enter your first name"]', timeout=30)
    sb.type('input[placeholder="Enter your first name"]', USER_FIRST_NAME)
    
    sb.assert_element_present('input[placeholder="Please enter last name."]', timeout=30)
    sb.type('input[placeholder="Please enter last name."]', USER_LAST_NAME)

    # Gender selection
    sb.assert_element_present("/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[8]/div/div[1]/div/app-dropdown/div/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]", timeout=30)
    sb.click("/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[8]/div/div[1]/div/app-dropdown/div/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]")
    sb.click('/html/body/div[4]/div[2]/div/div/mat-option[2]')

    # Date of birth
    sb.assert_element_present('input[placeholder="Please select the date"]', timeout=30)
    sb.type('input[placeholder="Please select the date"]', USER_BIRTHDAY)

    # Nationality
    sb.assert_element_present("/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[9]/div/div/div/app-dropdown/div/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]", timeout=30)
    sb.click("/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[9]/div/div/div/app-dropdown/div/mat-form-field/div[1]/div/div[2]/mat-select/div/div[2]")
    sb.reconnect(2)
    sb.assert_element_present('/html/body/div[4]/div[2]/div/div/mat-option[232]', timeout=30)
    sb.click('/html/body/div[4]/div[2]/div/div/mat-option[232]')
    sb.reconnect(2)

    # Passport details
    sb.assert_element_present('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[10]/div/div/div/app-input-control/div/mat-form-field/div[1]/div/div[2]/input', timeout=30)
    sb.type('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[10]/div/div/div/app-input-control/div/mat-form-field/div[1]/div/div[2]/input', USER_PASSPORT_NUMBER)
    
    sb.assert_element_present('input[placeholder="Please select the date"]', timeout=30)
    sb.type('#passportExpirtyDate', USER_EXPIRE_DATA)

    # Contact information
    sb.assert_element_present('input[placeholder="44"]', timeout=30)        
    sb.type('input[placeholder="44"]', USER_PHONE_HEADER)

    sb.assert_element_present('input[placeholder="012345648382"]', timeout=30)
    sb.type('input[placeholder="012345648382"]', USER_PHONE_BODY)

    sb.assert_element_present('input[placeholder="Enter Email Address"]', timeout=30)
    sb.type('input[placeholder="Enter Email Address"]', AUTH_EMAIL)

    sb.assert_element_present('input[placeholder="Enter Address line 1"]', timeout=30)
    sb.type('input[placeholder="Enter Address line 1"]', USER_ADDRESS_LINE)

    # Submit form
    sb.assert_element_present('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button')

    wait_for_single_window(sb, 20)
    sb.reconnect(3)

    sb.assert_element_present('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[2]/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-applicant-details/section/mat-card[2]/div/div[2]/button')
    logging.info('Successfully filled out your details')

def book_appointment_data(sb: SB) -> None:
    """Select appointment date and time."""
    logging.info('Booking appointment data')
    wait_for_single_window(sb, 20)
    sb.reconnect(10)
    
    # Find available dates
    calendar_days = sb.find_elements(By.CSS_SELECTOR, 'td.fc-day-future.fc-daygrid-day.date-availiable')
    calender_day = calendar_days[0].find_element(By.CSS_SELECTOR, 'a[class="fc-daygrid-day-number"]')
    day_id = calender_day.get_attribute('id')
    print(day_id)

    # Scroll to see calendar
    scroll_to_half_page(sb)
    
    # Select date
    sb.sleep(1)
    sb.click(By.CSS_SELECTOR, f'td[aria-labelledby="{day_id}"]')
    
    # Select time
    sb.reconnect(10)
    sb.assert_element_present("/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[1]/div[4]/table/tbody/tr[3]/td[2]/div[2]", timeout=30)
    sb.click("/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[1]/div[4]/table/tbody/tr[3]/td[2]/div[2]")

    # Continue
    sb.assert_element_present('/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[2]/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-book-appointment-split-slot/section/mat-card[2]/div/div[2]/button')
    logging.info('Successfully selected appointment time')

def services(sb: SB) -> None:
    """Configure services for the appointment."""
    logging.info('Configure Services')
    wait_for_single_window(sb, 20)
    sb.reconnect(5)

    # Continue with default services
    sb.assert_element_present('/html/body/app-root/div/main/div/app-manage-service/section/mat-card[2]/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-manage-service/section/mat-card[2]/div/div[2]/button')
    logging.info('Successfully Configure Services')

def review(sb: SB) -> None:
    """Review application and accept terms."""
    logging.info('Review')
    
    # Accept terms
    sb.sleep(1)
    sb.click('label[for="mat-mdc-checkbox-1-input"]')
    sb.sleep(1)
    sb.click('label[for="mat-mdc-checkbox-2-input"]')
    sb.sleep(1)
    sb.click('label[for="mat-mdc-checkbox-3-input"]')

    # Continue
    sb.assert_element_present('/html/body/app-root/div/main/div/app-review-and-payment/section/form/mat-card[2]/div/div[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-review-and-payment/section/form/mat-card[2]/div/div[2]/button')
    logging.info('Successfully Review')

def confirmation(sb: SB) -> None:
    """Confirm booking and save receipt."""
    logging.info('Confirmation')
    wait_for_single_window(sb, 20)

    # Save page for receipt
    save_page_html(sb)

    # Finalize booking
    sb.assert_element_present('/html/body/app-root/div/main/div/app-payment-confirmation/section/mat-card[2]/button', timeout=30)
    sb.click('/html/body/app-root/div/main/div/app-payment-confirmation/section/mat-card[2]/button')
    logging.info('Successfully Confirmation')

def dashboard(sb: SB) -> None:
    """Navigate to dashboard and wait for user."""
    logging.info('Dashboard')
    wait_for_single_window(sb, 20)
    sb.reconnect(300) 