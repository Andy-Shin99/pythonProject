from utils import infinite_scroll_data
import pandas as pd

# url 조작(기간 조정)
duration_list = ['20160101to20161231', '20170101to20171231', '20180101to20181231', '20190101to20191231', '20200101to20201231', '20210101to20211231', '20220101to20221231', '20230101to20231110']


post_data = infinite_scroll_data.get_post_datas(duration_list)

# csv 파일로 저장
df = pd.DataFrame(post_data)
# 행과 열을 바꾸기
df = df.transpose()

df.to_csv('post_datas.csv', encoding='utf-8-sig')
