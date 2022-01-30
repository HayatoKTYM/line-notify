import requests
import utils
import setting


def notify(num: int, url: str) -> None:
    """
    メッセージをLINE に投稿
    """
    with open('setting.py', 'w') as fo:
        fo.write(f'MAX_NUM = {num}')

    access_token = utils.access_token
    line_post_url = utils.line_post_url
    headers = {'Authorization': 'Bearer ' + access_token}

    try:
        message = f'ワンパンマン最新話({num}話)が更新されたよ\n {url}'
        payload = {'message': message}
        requests.post(line_post_url, headers=headers, params=payload)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    options = utils.get_options()
    base_url = 'https://tonarinoyj.jp/episode/13932016480028985383'
    try:
        soup = utils.featch_page(options, base_url)
        num = utils.get_max_num(soup)
        url = utils.get_url(soup)
        print(num)
        print(url)
    except Exception as e:
        print(e)
        soup = utils.featch_page(options, base_url, sleep=120)
        num = utils.get_max_num(soup)
        url = utils.get_url(soup)
    if setting.MAX_NUM < num:
        notify(num, url)
