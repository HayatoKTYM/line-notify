import os
# from datetime import datetime, timedelta, timezone
import requests

import utils
import setting


def notify(num):
    with open('setting.py', 'w') as fo:
        fo.write(f'MAX_NUM = {num}')

    url = os.environ.get('url')
    access_token = os.environ.get('access_token')
    headers = {'Authorization': 'Bearer ' + access_token}
    # JST = timezone(timedelta(hours=+9), 'JST')
    # today = datetime.now(JST).strftime('%Y/%m/%d')

    try:
        message = f'ワンパンマン最新話({num}話)が更新されたよ'
        payload = {
            'message': message,
            'stickerPackageId': 11537,
            'stickerId': 52002735
        }
        r = requests.post(url, headers=headers, params=payload)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    options = utils.get_option()
    url = 'https://tonarinoyj.jp/episode/13932016480028985383'
    try:
        soup = utils.featch_page(options, url)
        # date = get_latest_date(soup)
        num = utils.get_max_num(soup)
    except Exception as e:
        print(e)
        soup = utils.featch_page(options, url, sleep=120)
        # date = get_latest_date(soup)
        num = utils.get_max_num(soup)
    print(num)
    if setting.MAX_NUM < num:
        notify(num)
