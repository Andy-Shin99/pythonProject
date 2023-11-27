import pandas as pd
import re
from matplotlib import rc
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

    # 결과 DataFrame 저장
    title_df.to_csv(f'../results/title_dataframes/{i}.csv', sep='\t', index=True)

## todo : des 부분 그래프로 만들기 (맨 처음 여행은 빼고), 워드클라우드 만들기
for i in range(2016, 2024):
    file_path = f'../results/des_results/{i}.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 불러온 데이터 처리
    data = {}
    for line in lines:
        line = line.strip()
        key_value = line.split(' ')
        key = key_value[0]
        value = int(key_value[1])
        data[key] = value

    # 데이터를 DataFrame으로 변환
    df = pd.DataFrame(list(data.items()), columns=['Keyword', 'Count'])

    # '여행' 키워드를 제외하고 상위 20개 키워드로 DataFrame 생성
    des_df = df[df['Keyword'] != '여행'].head(20)

    # 내림차순으로 데이터 정렬
    des_df = des_df.sort_values(by=['Count'], ascending=False)

    ## todo : 차트 그리기
    rc('font', family='AppleGothic')
    plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.rcParams.update({'font.size': 10})
    plt.barh(des_df['Keyword'], des_df['Count'],height=0.5)
    plt.title(f'{i}년도 상위 20개 여행 키워드')

    plt.show()

    ## todo : des 부분 워드클라우드 만들기
    wc = df.set_index('Keyword').to_dict()['Count']
    wordCloud = WordCloud(font_path='AppleGothic', background_color='white', width=800, height=600).generate_from_frequencies(wc)

    plt.figure()
    plt.imshow(wordCloud)
    plt.axis('off')

## todo : 선그래프로 연도별로 어떤 여행지가 인기 있었는지 그리기 -> 2016~2023년까지 전체를 더한거