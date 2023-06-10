# line-notify
LINEへ通知するためのスクリプト

## 環境変数
```text
line_post_url ... LINE Notify時のURL
access_token  ... LINE Notify使用時のアクセストークン
chromedriver  ... Chromedriverのパス
```

## 参考
* [LINE Notify API Document](https://notify-bot.line.me/doc/ja/)

アクセストークンが有効であるかを確認するコマンド

```sh=
curl -H "Authorization: Bearer ${access_token}" \
https://notify-api.line.me/api/status
```

メッセージが遅れるかを検証するコマンド

```sh=
curl -X POST -H "Authorization: Bearer ${access_token}" -F 'message=TEST RUN from kata***' \
https://notify-api.line.me/api/notify
```

