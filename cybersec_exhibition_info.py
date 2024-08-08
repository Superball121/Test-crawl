import requests
import time
from bs4 import BeautifulSoup
from test01 import (get_detail,create_webdriver)
import pandas as pd


def get_cybersec_exd_info(is_export_to_csv=True):
    
    # 只抓2024
    url = "https://cybersec.ithome.com.tw/2024/exhibitionDirectory"

    # 1. 先去取得資訊: 回傳一份完整的html + js 字串
    response = requests.get(url)

    # 2. 把剛剛得到的字串，丟給beautifulsoup處理
    # 3. 找出所有的<div class='exd-card'>
    soup = BeautifulSoup(response.text, "html.parser")
    exd_cards = soup.find_all("div", attrs={"class": "exd-card"})

    driver = create_webdriver()
    url_prefix = "https://cybersec.ithome.com.tw"
    exd_cards_info = list()

    for exd_card in exd_cards:
        # 找連結
        href = url_prefix + exd_card.a["href"]
        # 展攤名稱
        exd_name = exd_card.h5.text
        # 展攤位置編號
        if exd_card.h6: # 判斷是否為None
            exd_id = exd_card.h6.text.split("：")[1]
        else:
            exd_id = ""
        # 使用動態爬蟲抓聯絡資訊
        exd_data = get_detail(href,driver)
        # 廠商資料
        exd_data_intro = {
            'exd_link': href,
            'exd_name': exd_name,
            'exd_id': exd_id
        }
        exd_data.update(exd_data_intro)
        exd_cards_info.append(exd_data)
        time.sleep(1.5)
    driver.close()

    if is_export_to_csv:
        data = pd.DataFrame(exd_cards_info) # 轉換成DataFrame
        data.to_csv('cybersec_exd.csv')

    return exd_cards_info


if __name__ == '__main__':
   data = get_cybersec_exd_info(is_export_to_csv=False)
   print(data[:5])