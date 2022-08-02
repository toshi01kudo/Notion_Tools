""" Program for text replacement of Notion """
import time, gc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import parameter

## Parameters - To Be Changed manually: 
NOTION_PAGE_URL = "https://www.notion.so/your_notion_page"
BEFORE_TEXT = "AAA"
AFTER_TEXT = "ZZZ"

def notion_text_replace(page_url = NOTION_PAGE_URL, before_text = BEFORE_TEXT, after_text = AFTER_TEXT):
    """ Main function """
    ## browser for selenium
    browser = GetSeleniumBrowser()
    
    ## Access to Notion
    browser.browser.get(page_url)
    element = WebDriverWait(browser.browser, 10).until(
        EC.presence_of_element_located((By.ID, "notion-email-input-1")) 
    )
    time.sleep(1)
    ## ID入力
    adrs_clmn = browser.browser.find_element_by_id("notion-email-input-1")
    adrs_clmn.send_keys(parameter.Notion_mail)
    for login_btn in browser.browser.find_elements_by_class_name('notion-focusable'):
        if login_btn.text == 'メールアドレスでログインする':
            login_btn.click()
            break
    pass_clmn = browser.browser.find_element_by_id("notion-password-input-2")
    pass_clmn.send_keys(parameter.Notion_pass)
    for login_btn in browser.browser.find_elements_by_class_name('notion-focusable'):
        if login_btn.text == 'ログイン':
            login_btn.click()
            break
    element = WebDriverWait(browser.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "notion-page-content")) 
    )
    time.sleep(5)

    contents = browser.browser.find_elements_by_css_selector('.notion-page-content .notion-text-block div div .notranslate')
    for line in contents:
        if before_text in line.text:
            print(line.text)
            replace_text = line.text.replace(before_text, after_text)
            print(replace_text)
            line.click()
            line.send_keys(Keys.CONTROL + "a")
            line.send_keys(Keys.DELETE)
            line.send_keys(replace_text)

    time.sleep(1)
    browser.close_selenium()

class GetSeleniumBrowser:
    def __init__(self, headless=False):
        # Option for headless mode
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        self.browser = webdriver.Firefox(executable_path=parameter.gekodriver_path, options=options)
        self.browser.implicitly_wait(10) # implicit wait time (secs)

    def close_selenium(self):
        self.browser.quit()
        time.sleep(1)
        del self.browser
        gc.collect()

if __name__ == "__main__":
    notion_text_replace()
