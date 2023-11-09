from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import time

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
driver.maximize_window()

# TODO : url 조작(기간 조정)
url = 'https://search.naver.com/search.naver?where=blog&query=%EC%97%AC%ED%96%89&sm=tab_opt&nso=so:r,p:from20230101to20231109'
driver.get(url)

prev_height = driver.execute_script("return document.body.scrollHeight")

# 최초 창에 나타나는 게시글 개수
count = 30

while count < 210:
    print(count)

    # 스크롤을 화면 가장 아래로 내린다
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # 페이지 로딩 대기
    time.sleep(2)

    # 현재 문서 높이를 가져와서 저장
    # curr_height = driver.execute_script("return document.body.scrollHeight")

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

print(len(title_list), title_list)
print(len(des_list), des_list)