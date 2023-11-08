from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

#selenium 창 꺼짐 방지 
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#browser 열기
browser = webdriver.Chrome(options=chrome_options)
url = 'https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword=%EC%97%AC%ED%96%89'
browser.get(url)

#기간 선택 총 8쌍 
period_list = [['2016-01-01', '2016-12-31'], ['2017-01-01', '2017-12-31'], ['2018-01-01', '2018-12-31'], ['2019-01-01', '2019-12-31'], 
               ['2020-01-01', '2020-12-31'], ['2021-01-01', '2021-12-31'], ['2022-01-01', '2022-12-31'], ['2023-01-01', '2023-11-07']]
title_list = []

for period in period_list :
    browser.get(url)
    try :
        button = browser.find_element(By.XPATH, '/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/div/div/a/strong')
    except :
        button = browser.find_element(By.XPATH, '/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/div/div/a')
    button.click()

    browser.find_element(By.XPATH, '//*[@id="search_start_date"]').click()
    browser.find_element(By.XPATH, '//*[@id="search_start_date"]').send_keys(period[0])
    browser.find_element(By.XPATH, '//*[@id="search_start_date"]').send_keys(Keys.ENTER)

    browser.find_element(By.XPATH, '//*[@id="search_end_date"]').click()
    browser.find_element(By.XPATH, '//*[@id="search_end_date"]').send_keys(period[1])
    browser.find_element(By.XPATH, '//*[@id="search_end_date"]').send_keys(Keys.ENTER)

    browser.find_element(By.XPATH, '//*[@id="periodSearch"]').click()

    time.sleep(1)

    html = browser.page_source 
    soup = BeautifulSoup(html, 'html.parser')
    post = soup.select('.desc')[2:]
    print("기간:", period[0], period[1])
    print(post)