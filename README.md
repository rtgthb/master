# SwitchBotに登録されているデバイスを操作するpythonスクリプト

## 概要

SwichBot に登録されているデバイスを用意されているAPIを実行するpythonスクリプトです。
こちらでは LoupeDeck など外部サービスから呼び出されることを想定しています。

## 利用手順

1. pythonスクリプトをダウンロードし、同階層に 'switchbot_access_token' というファイル名を作成する。
2. 利用するSwitchBotのアクセストークンを記載する。取得方法は[こちら](https://support.switch-bot.com/hc/ja/articles/12822710195351-%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%81%AE%E5%8F%96%E5%BE%97%E6%96%B9%E6%B3%95)を参照。
3. SwitchBot に登録されている操作の対象デバイスのデバイスIDを取得する。デバイスIDの確認方法は以下のcurlを実行する。

curlコマンド
 ```
curl "https://api.switch-bot.com/v1.0/devices" -H "Authorization: <アクセストークン>"
 ```

 Responseの抜粋
 ```
"infraredRemoteList": [
    {
        "deviceId": "xx-yyyyyyyyyyyy-zzzzzzzz", ★必要なID
        "deviceName": "エアコン01",
        "remoteType": "Air Conditioner",
        "hubDeviceId": "AAAAAAAAAAAA"
    },
    {
        "deviceId": "xx-yyyyyyyyyyyy-zzzzzzzz",
        "deviceName": "テレビ01",
        "remoteType": "TV",
        "hubDeviceId": "AAAAAAAAAAAA"
    },
    {
        "deviceId": "xx-yyyyyyyyyyyy-zzzzzzzz",
        "deviceName": "エアコン02",
        "remoteType": "Air Conditioner",
        "hubDeviceId": "AAAAAAAAAAAA"
    },
    ・
    ・
    ・
 ```

4. setting.ini の USER セクションのdeviceに設定する。

## 利用方法

```
usage: switchbot.py [-h] [-t UP_OR_DOWN_TEMPERATURE] [-p POWER] [-m MODE]

Operate switch-bot devices

options:
  -h, --help            show this help message and exit
  -t UP_OR_DOWN_TEMPERATURE, --up-or-down-temperature UP_OR_DOWN_TEMPERATURE
                        Up or down the temperature (Up = 1, Down = 2)
  -p POWER, --power POWER
                        Up or down the temperature (ON = 1, OFF = 2, Switch =
                        3)
  -m MODE, --mode MODE  Change air conditioner mode (Auto = 1, Cooling = 2,
                        Dry = 3, Fan = 4, Heating = 5)
```