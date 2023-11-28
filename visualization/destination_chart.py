from matplotlib import rc
import matplotlib.pyplot as plt

rc('font', family='AppleGothic')

# 각 연도별로 유럽, 동남아, 동북아, 국내, 대양주 키워드 개수를 저장할 리스트 생성

years = []
europe_counts = []
southeast_asia_counts = []
east_asia_counts = []
domestic_counts = []
oceania_counts = []

# 각 연도별 des_results 파일을 읽어서 데이터를 처리하고, 그래프로 그리기

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

    # 유럽 : 유럽
    # 미주 : 미국, 캐나다, 북미, 남미
    # 동남아 : 동남아, 베트남, 태국, 필리핀, 인도네시아, 말레이시아, 싱가포르, 브루나이, 라오스, 캄보디아, 미얀마, 홍콩
    # 동북아 : 중국, 일본
    # 국내 : 국내, 한국
    # 대양주 : 호주, 뉴질랜드, 괌

    # 각 연도별로 위에 정리된 카테고리별 키워드가 있으면 모두 더해서 하나의 값으로 만들기
    europe = 0
    southeast_asia = 0
    east_asia = 0
    domestic = 0
    oceania = 0

    for key, value in data.items():
        if key in ['유럽']:
            europe += value

        elif key in ['동남아', '베트남', '태국', '필리핀', '인도네시아', '말레이시아', '싱가포르', '브루나이', '라오스', '캄보디아', '미얀마', '홍콩']:
            southeast_asia += value
        elif key in ['중국', '일본']:
            east_asia += value
        elif key in ['국내', '한국', '제주도']:
            domestic += value
        elif key in ['호주', '뉴질랜드', '괌']:
            oceania += value

    years.append(i)
    europe_counts.append(europe)
    southeast_asia_counts.append(southeast_asia)
    east_asia_counts.append(east_asia)
    domestic_counts.append(domestic)
    oceania_counts.append(oceania)

# 선 그래프 그리기
# x축 : 연도, y축 : 키워드 개수
# 각 키워드마다 색깔 다르게
# 범례 추가
# 제목 추가

plt.plot(years, europe_counts, label='유럽')
plt.plot(years, southeast_asia_counts, label='동남아')
plt.plot(years, east_asia_counts, label='동북아')
plt.plot(years, domestic_counts, label='국내')
plt.plot(years, oceania_counts, label='대양주')

plt.legend()

plt.show()