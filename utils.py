import os
import re
import time

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions

line_post_url = os.environ['line_post_url']
access_token = os.environ['access_token']
chromedriver_path = os.environ['chromedriver']


def get_options() -> ChromeOptions:
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


def featch_page(
        options: ChromeOptions,
        url: str,
        sleep: int = 30
) -> BeautifulSoup:
    """
    webページをスクレイピング
    """
    driver = Chrome(
        executable_path=chromedriver_path,
        options=options
    )
    driver.get(url)
    time.sleep(sleep)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    soup.find_all("ul",
                  class_="test-readable_product-list series-episode-list ")
    driver.close()
    return soup


def extract_num(src: str) -> int:
    """
    正規表現で数字部分を抽出
    """
    r = re.match("\D*(\d+)\D*", src)
    if not r:
        return 0  # intで返したいため

    num = int(r.groups()[0])
    return num


def get_max_num(soup: BeautifulSoup) -> int:
    """
    最新話の数値を抽出
    """
    elem = soup.find("h4", class_="series-episode-list-title")
    num = extract_num(elem.text.strip())

    return num


def get_url(soup: BeautifulSoup) -> str:
    """
    最新話のurlを抽出
    """
    url = soup.find("a", class_='series-episode-list-container').get("href")
    return url


def get_latest_date(soup: BeautifulSoup) -> str:
    """
    最新話の日付を抽出(unused)
    """
    elems = soup.find("span", class_='series-episode-list-date')
    return elems.text
