""" Program for text replacement of Notion """
import time
import os
import logging
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium_helper import SeleniumBrowser
import replace_parameters


def notion_text_replace() -> None:
    """
    Replace function for Notion
    """
    # logging definition
    logging.basicConfig(level=logging.INFO, format=" %(asctime)s - %(levelname)s - %(message)s")
    # load parameters
    load_dotenv()

    page_url = replace_parameters.NOTION_PAGE_URL
    before_text = replace_parameters.BEFORE_TEXT
    after_text = replace_parameters.AFTER_TEXT

    # browser for selenium
    # browser = GetSeleniumBrowser()
    browser = SeleniumBrowser(
        headless=False,
        geckodriver_path=os.getenv("GECKODRIVER_PATH"),
        browser_setting={
            "browser_path": os.getenv("FIREFOX_BINARY_PATH"),
            "browser_profile": os.getenv("FIREFOX_PROFILE_PATH"),
        },
    )

    # Access to Notion
    browser.browser.get(page_url)
    WebDriverWait(browser.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "notion-login")))
    time.sleep(1)
    # ID入力
    notion_login_form_input(browser, "notion-email-input-", os.getenv("NOTION_MAIL"))
    notion_login_button(browser, "メールアドレスでログインする")
    notion_login_form_input(browser, "notion-password-input-", os.getenv("NOTION_PASS"))
    notion_login_button(browser, "ログイン")
    WebDriverWait(browser.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "notion-page-content")))
    time.sleep(5)

    contents = browser.browser.find_elements(
        By.CSS_SELECTOR, ".notion-page-content .notion-text-block div div .notranslate"
    )
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


def notion_login_form_input(browser: classmethod, partial_id: str, form_value: str) -> None:
    """
    Input form value function during login phase of Notion.
    Args:
        browser: selenium-helper class,
        partial_id: search ID without number,
        form_value: value to input to the form.
    """
    for email_num in range(1, 5):
        logging.info(f"Try: {email_num}")
        search_text = partial_id + str(email_num)
        try:
            clmn = browser.browser.find_element(By.ID, search_text)
        except NoSuchElementException:
            continue
        clmn.send_keys(form_value)
        break
    if clmn is None:
        raise Exception


def notion_login_button(browser: classmethod, text: str) -> None:
    """
    Press button function during login phase of Notion.
    Args:
        browser: selenium-helper class,
        text: Button text.
    """
    for login_btn in browser.browser.find_elements(By.TAG_NAME, "div"):
        if login_btn.text == text:
            login_btn.click()
            break


if __name__ == "__main__":
    notion_text_replace()
