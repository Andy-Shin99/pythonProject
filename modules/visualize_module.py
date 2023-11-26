import pandas as pd
import re
from matplotlib import rc
import matplotlib.pyplot as plt

## todo : title 부분은 표로 만들기 (연도별 표로 찍기)
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

    # 결과 DataFrame 출력
    print(title_df)

    # 결과 DataFrame 저장
    title_df.to_csv(f'../results/title_dataframes/{i}.csv', sep='\t', index=True)

## todo : des 부분은 그래프로 만들기 (맨 처음 여행은 빼고), 워드클라우드 만들기
# for i in range(2016, 2024):
#     des_df = pd.read_table(f'../results/des_results/{i}.txt', sep=' ',header=None, names=['des', 'num'])
#
#     ## todo : 차트 그리기
#     # plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
#     # plt.rcParams.update({'font.size': 8})
#     rc('font', family='AppleGothic')
#
#     des_df.plot(kind='bar', x='des', y='num', legend=True)
#     plt.show()

## todo : 선그래프로 연도별로 어떤 여행지가 인기 있었는지 그리기 -> 2016~2023년까지 전체를 더한거