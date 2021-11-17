import os
import re
import time
from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions

# import setting


def initialize_options():
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


def extract_num(src):
    r = re.match("\D*(\d+)\D*", src)
    if not r:
        return

    num = int(r.groups()[0])

    return num


def get_max_num(soup):
    elems = soup.find_all("h4")
    print(elems)
    elems_num = [extract_num(e.text.strip()) for e in elems]

    return max(elems_num)


def get_latest_date(soup):
    elems = soup.find("span", class_='series-episode-list-date')
    return elems.text


if __name__ == '__main__':
    options = initialize_options()
    url = 'https://tonarinoyj.jp/episode/13932016480028985383'
    try:
        soup = featch_page(options, url)
        date = get_latest_date(soup)
        # num = get_max_num(soup)
    except:
        soup = featch_page(options, url, sleep=120)
        date = get_latest_date(soup)
        # num = get_max_num(soup)
    print(date)
    # TO DO: num で 通知を判断するようにする
    # その際，MAX_NUM setting.pyで保持するなど何かしら処理が必要
    # if setting.MAX_NUM < num:
    #     with open('setting.py','w') as fo:
    #         fo.write(f'MAX_NUM = {num}')

    url = os.environ.get('url')
    access_token = os.environ.get('access_token')
    headers = {'Authorization': 'Bearer ' + access_token}
    JST = timezone(timedelta(hours=+9), 'JST')
    today = datetime.now(JST).strftime('%Y/%m/%d')
    try:
        if today == date:
            message = 'ワンパンマン最新話が更新されたよ'
            payload = {
                'message': message,
                'stickerPackageId': 11537,
                'stickerId': 52002735
            }
            r = requests.post(url, headers=headers, params=payload)
            print(r.status_code)
    except Exception as e:
        print(e)
