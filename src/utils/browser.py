from seleniumbase import SB
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

def wait_for_single_window(sb, timeout=20):
    """Wait until there's only one browser window open."""
    WebDriverWait(sb.driver, timeout).until(lambda d: len(d.window_handles) == 1)
    new_window = sb.driver.window_handles[0]
    sb.driver.switch_to.window(new_window)
    sb.reconnect(3)

def scroll_to_half_page(sb):
    """Scroll to the middle of the page."""
    half_height = sb.execute_script("return document.body.scrollHeight / 2")
    sb.execute_script(f"window.scrollTo(0, {half_height});")

def save_page_html(sb, filename='page.html'):
    """Save the current page HTML to a file."""
    page_html = sb.get_page_source()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_html)
    logging.info(f'Saved page HTML to {filename}')

def click_coordinates(sb, x_ratio, y_ratio):
    """Click at coordinates based on window size ratios."""
    size = sb.driver.get_window_size()
    window_width = size['width']
    window_height = size['height']
    
    x_coordinate = (window_width / 1264) * x_ratio
    y_coordinate = (window_height / 745) * y_ratio
    
    ActionChains(sb.driver).move_by_offset(x_coordinate, y_coordinate).click().perform()

def handle_cookie_banner(sb, timeout=30):
    """Handle cookie consent banner if present."""
    try:
        sb.assert_element_present('#onetrust-banner-sdk', timeout=timeout)
        sb.click('#onetrust-reject-all-handler')
        return True
    except:
        return False

def bypass_cloudflare(sb, timeout=10):
    """Attempt to bypass Cloudflare captcha."""
    logging.info('Attempt to bypass Cloudflare captcha')
    sb.reconnect(timeout)
    sb.uc_gui_click_captcha()
    logging.info('Success Bypassing Cloudflare captcha')
    sb.reconnect(timeout) 