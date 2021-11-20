import os
import re
import time

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions


def get_options():
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")

    return options


def featch_page(options, url, sleep=30):
    driver = Chrome(
        executable_path=os.environ.get('chromedriver', './chromedriver'),
        options=options
    )
    driver.get(url)
    time.sleep(sleep)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    driver.close()
    return soup


def extract_num(src: str) -> int:
    r = re.match("\D*(\d+)\D*", src)
    if not r:
        return

    num = int(r.groups()[0])

    return num


def get_max_num(soup) -> int:
    elems = soup.find_all("h4")
    print(elems)
    elems_num = [extract_num(e.text.strip()) for e in elems]

    return max(elems_num)


def get_latest_date(soup):
    elems = soup.find("span", class_='series-episode-list-date')
    return elems.text
