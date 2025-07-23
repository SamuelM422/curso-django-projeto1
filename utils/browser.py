from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import os

ROOT_PATH = Path(__file__).parent.parent
WEBDRIVER_NAME = 'msedgedriver.exe'
WEBDRIVER_PATH = ROOT_PATH / 'bin' /WEBDRIVER_NAME

def make_webdriver(*options):

    if not WEBDRIVER_PATH.exists():
        raise FileNotFoundError(f'File {WEBDRIVER_NAME} not found')

    webdriver_options = webdriver.EdgeOptions()

    if options is not None:
        for option in options:
            webdriver_options.add_argument(option)

    if os.getenv('SELENIUM_HEADLESS') == '1':
        webdriver_options.add_argument('--headless')

    webdriver_service = Service(WEBDRIVER_PATH.__str__())
    webdriver_browser = webdriver.Edge(service=webdriver_service, options=webdriver_options)

    return webdriver_browser

if __name__ == '__main__':
    browser = make_webdriver()
    browser.get('https://www.google.com.br/')
    sleep(5)
    browser.quit()