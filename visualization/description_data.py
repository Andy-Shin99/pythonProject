import pandas as pd
import re
from matplotlib import rc
import matplotlib.pyplot as plt
from wordcloud import WordCloud

rc('font', family='AppleGothic')

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