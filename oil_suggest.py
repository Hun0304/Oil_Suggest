# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 21:57:23 2022

@author: Hun
"""

import requests
from bs4 import BeautifulSoup
from math import floor


def get_oil_price() -> float:
    # Go to web get 92 oil price.
    oil_price = 0  # initialize
    url = 'https://gas.goodlife.tw/'          # Data Source Web
    myweb = requests.get(url)
    myweb.encoding = 'utf-8'
    sp = BeautifulSoup(myweb.text, 'lxml')
    cpc_oil_price = sp.find('div', id='cpc')  # Only Get CPC oil price.
    while True:
        oil_type = input('請輸入要加的油種(92, 95, 98)：')
        if oil_type == '92':    # Get 92 oil price.
            oil_price = float(cpc_oil_price.find_all('li')[0].text[-4:])
        elif oil_type == '95':  # Get 95 oil price.
            oil_price = float(cpc_oil_price.find_all('li')[1].text[-4:])
        elif oil_type == '98':  # Get 98 oil price.
            oil_price = float(cpc_oil_price.find_all('li')[2].text[-4:])

        if oil_price == 0:
            print('請重新輸入無鉛汽油的種類')
        else:
            print(f'今日 {oil_type} 無鉛汽油的金額：{oil_price}')
            break
    return oil_price


def calculator(oil_price) -> None:
    discount = oil_price - float(input('請輸入自助加油折扣：'))
    ori_oil_list = []     # Origin oil list.
    max_oil_list = []     # Suggest interval maximum oil's liter list.
    gap_oil_list = []     # Origin and suggest oil's liter gap list.
    pay_list = []         # You need to pay list.
    ori_price_list = []   # Origin pay list.
    save_money_list = []  # Origin and suggest oil's price gap list.

    while True:
        choice = int(input('請選擇公升為主(0)or價格為主(1)：'))
        if choice == 0:  # Follow the litre.
            oil = float(input('請輸入欲加的公升數：'))
            pay_price = round(discount * oil)

            for i in range(5):  # Give you five suggests.
                pay_list.append(pay_price)
                # Data processing. Ex: 15.* -> 15.XX
                max_oil = floor(((pay_price + 0.5) / discount) * 100) / 100
                ori_price = round(oil_price * max_oil)
                gap_price = ori_price - pay_price

                max_oil_list.append(max_oil)
                ori_price_list.append(ori_price)
                save_money_list.append(gap_price)
                pay_price += 1

            print(f'自助最多可加多少公升的油：{max_oil_list}')
            print(f'原始花費金額：{ori_price_list}')
            print(f'自助花費金額：{pay_list}')
            print(f'可以省下金額：{save_money_list}')
            break

        elif choice == 1:  # Follow the price.
            pay_price = int(input('請輸入欲花費的金額：'))
            pay_price = float(pay_price) + 0.5
            for i in range(5):
                pay_list.append(int(pay_price))
                # Data processing. Ex: 15.* -> 15.XX
                ori_max_oil = floor((pay_price / price) * 100) / 100
                max_oil = floor((pay_price / discount) * 100) / 100
                gap_oil = floor((max_oil - ori_max_oil) * 100) / 100

                ori_oil_list.append(ori_max_oil)
                max_oil_list.append(max_oil)
                gap_oil_list.append(gap_oil)
                pay_price += 1

            print(f'原始花費金額：{pay_list}')
            print(f'原始油費可加多少公升的油：{ori_oil_list}')
            print(f'自助最多可加多少公升的油：{max_oil_list}')
            print(f'相差多少公升的油：{gap_oil_list}')
            break
        else:
            print('請重新選擇')
    return None


if __name__ == '__main__':
    price = get_oil_price()
    # To compute my suggestion: oil's type or oil's price.
    calculator(price)
