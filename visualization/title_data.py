import pandas as pd
import re
from matplotlib import rc
import matplotlib.pyplot as plt

rc('font', family='AppleGothic')

for i in range(2016, 2024):
    file_path = f'../results/title_results/{i}.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 불러온 데이터 처리
    data = {}
    for line in lines:
        line = line.strip()
        key_value = line.split(' : ')
        key = eval(key_value[0])  # 문자열을 튜플로 변환
        key = tuple(re.sub(r'[^\w\s,()]', '', word).strip() for word in key)  # 괄호와 쉼표를 포함한 특수문자 제거
        value = int(key_value[1])
        data[key] = value

    # DataFrame 생성
    title_df = pd.DataFrame(list(data.items()), columns=['Keywords', 'Count'])

    # '여행'을 제외한 단어만 남기는 작업
    title_df['Keywords'] = title_df['Keywords'].apply(lambda x: ' '.join([re.sub(r'[^\w\s]', '', word) for word in x if '여행' not in word]))

    # index를 1부터 시작하게 만들기
    title_df.index = title_df.index + 1

    # 결과 DataFrame 저장
    title_df.to_csv(f'../results/title_dataframes/{i}.csv', sep='\t', index=True)