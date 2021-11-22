# from datetime import datetime, timedelta, timezone
import requests

import utils
import setting


def notify(num):
    with open('setting.py', 'w') as fo:
        fo.write(f'MAX_NUM = {num}')

    access_token = utils.access_token
    url = utils.url
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
        print(f'status code:{r.status_code}')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    options = utils.get_options()
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
