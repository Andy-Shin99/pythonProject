from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import time

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
driver.maximize_window()

# url 조작(기간 조정)
duration_list = ['20160101to20161231', '20170101to20171231', '20180101to20181231', '20190101to20191231', '20200101to20201231', '20210101to20211231', '20220101to20221231', '20230101to20231110']

base_url = 'https://search.naver.com/search.naver?where=blog&query=%EC%97%AC%ED%96%89&sm=tab_opt&nso=so:r,p:from'

# post 제목, desc 저장할 dict type 변수
post_dict = {}

for duration in duration_list:
    url = base_url + duration

    driver.get(url)

    prev_height = driver.execute_script("return document.body.scrollHeight")

    # 최초 창에 나타나는 게시글 개수
    count = 30

    while count <= 1020:
        # 스크롤을 화면 가장 아래로 내린다
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 페이지 로딩 대기
        time.sleep(2)

        # 스크롤 시 추가 30개 게시글 로딩, 개수 추가
        count += 30


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title_tag_list = soup.select('.lst_view > .bx > .view_wrap > .detail_box > .title_area > a')
    des_tag_list = soup.select('.lst_view > .bx > .view_wrap > .detail_box > .dsc_area > a')

    # title_tag_list의 a 태그 사이에 있는 content만 뽑아내기
    title_list = []
    des_list = []

    # title_tag_list의 a 태그 사이에 있는 content만 뽑아내기
    for title_tag in title_tag_list:
        title_list.append(title_tag.text)

    # des_tag_list의 a 태그 사이에 있는 content만 뽑아내기
    for des_tag in des_tag_list:
        des_list.append(des_tag.text)

    # post_dict에 저장
    post_dict[duration] = {'title': title_list, 'description': des_list}

# csv 파일로 저장
import pandas as pd

df = pd.DataFrame(post_dict)
# 행과 열을 바꾸기
df = df.transpose()

df.to_csv('post_datas.csv', encoding='utf-8-sig')