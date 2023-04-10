# -*- coding: utf-8 -*-
import configparser
import requests
import argparse


# 設定ファイルのセクション名
USER_SECTION = 'USER'
AIRCON_SECTION = 'AIRCON'
# 設定ファイルのパス
CONFIG_FILE_NAME = 'setting.ini'
# switchbotのアクセストークンのファイル名
ACCESS_TOKEN = 'switchbot_access_token'


def update_config(temperature, power, mode):
    """
    設定ファイルを読み込み、更新を行う。
    Parameters
    ----------
    temperature : int
        温度の上下を指定
    power : int
        電源のオンオフを指定
    mode : int
        エアコンのモードを指定
        TODO: エアコンモードの切り替えは未実装
    Returns
    -------
    config_dict : dict
        最新化された設定内容の辞書型
    """

    #  TODO: 設定している内容をDB管理にする。
    # DB管理していないため、設定ファイルを用いてエアコンの設定を記憶する
    config = configparser.RawConfigParser()
    config.read('setting.ini')

    # 設定ファイルの値を取得
    config_temp = int(config.get(AIRCON_SECTION, 'Temperature'))
    config_power = config.get(AIRCON_SECTION, 'Power')

    # 1は温度を上げ、2は温度を下げる
    if temperature:
        if temperature == 1 and config_temp > 16:
            config.set(AIRCON_SECTION, 'Temperature', str(int(config_temp) - 1))
        elif temperature == 2 and config_temp < 30:
            config.set(AIRCON_SECTION, 'Temperature', str(int(config_temp) + 1))

    # 1はon、2はoff、3はonとoffの切り替え
    if power:
        if power == 1:
            config.set(AIRCON_SECTION, 'Power', 'on')
        elif power == 2:
            config.set(AIRCON_SECTION, 'Power', 'off')
        elif power == 3:
            if config_power == 'off':
                config.set(AIRCON_SECTION, 'Power', 'on')
            else:
                config.set(AIRCON_SECTION, 'Power', 'off')

    # エアコンのモード
    # 1:自動, 2:冷房, 3:ドライ, 4:送風, 5:暖房
    if mode:
        if mode >= 1 and mode <= 5:
            config.set(AIRCON_SECTION, 'AirMode', str(int(mode)))


    # 設定ファイルを更新
    with open(CONFIG_FILE_NAME, 'w') as file:
        config.write(file)

    return dict(config)


# TODO: utilとして別ファイル化したい
def open_access_token(file_path):
    """
    アクセストークンが保管されているファイルを読み込み内容を返す。
    Parameters
    ----------
    file_path : string
        アクセストークンが記述されているファイルのパス
    Returns
    -------
    access_token : string
        アクセストークン
    """
    with open(file_path, 'r') as file:
        access_token = file.read()
    return access_token


def request_for_air_conditioner(config_dict):
    """
    エアコンの設定をswitchbotへ反映する。
    Parameters
    ----------
    config_dict : dict
        エアコンの設定する情報のdict型
    Returns
    -------
    response : Response
        responseデータ
    """

    # アクセストークンを取得
    access_token = open_access_token(ACCESS_TOKEN)

    # リクエストヘッダ
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json; charset=utf8',
    }

    #  リクエストデータ
    json_data = {
        'command': 'setAll',
        'parameter': config_dict[AIRCON_SECTION]['Temperature'] + ',' + config_dict[AIRCON_SECTION]['AirMode'] + ',' + config_dict[AIRCON_SECTION]['Fan'] + ',' + config_dict[AIRCON_SECTION]['Power'],
        'commandType': 'command',
    }
    # 設定をswitchbotへ反映
    response = requests.post('https://api.switch-bot.com/v1.0/devices/' + config_dict[USER_SECTION]['Device'] + '/commands', headers=headers, json=json_data)

    return response


if __name__ == '__main__':
    # コマンドライン引数
    parser = argparse.ArgumentParser(description='Operate switch-bot devices')
    parser.add_argument('-t', '--up-or-down-temperature', help='Up or down the temperature (Up = 1, Down = 2)', type=int)
    parser.add_argument('-p', '--power', help='Up or down the temperature (ON = 1, OFF = 2, Switch = 3)', type=int)
    parser.add_argument('-m', '--mode', help='Change air conditioner mode (Auto = 1, Cooling = 2, Dry = 3, Fan = 4, Heating = 5)', type=int)
    args = parser.parse_args()

    # 設定ファイルを更新
    latest_config_dict = update_config(args.up_or_down_temperature, args.power, args.mode)
    # switchbotへ設定を反映
    response = request_for_air_conditioner(latest_config_dict)
    print(response.status_code)
