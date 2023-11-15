import re
import nltk
from nltk import word_tokenize
from hanspell import spell_checker
from konlpy.tag import Komoran
#pip install git+https://github.com/ssut/py-hanspell.git
#pip install konlpy
#https://m.blog.naver.com/j7youngh/222824588851
#https://github.com/ssut/py-hanspell
#hanspell 오류수정 : https://www.codeit.kr/community/questions/UXVlc3Rpb246NjQyMjdiNTZiNThiNmIxODFjNmYyMGVk, https://github.com/ssut/py-hanspell/issues/41

def text_clean(text):
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern, '', text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern, '', text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거    
    text = re.sub(pattern, '', text)
    pattern = '([a-zA-Z0-9]+)'   # 알파벳, 숫자 제거  
    text = re.sub(pattern, '', text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern, '', text)
    pattern = '[^\w\s]'         # 특수기호제거
    text = re.sub(pattern, '', text)
    return text  

title_list = ['동유럽여행 일정 및 경비(엑셀파일첨부)', '마요르카<섬> 여행에 궁금한 점들 있으세요?', '나디아가 정리한 세부여행팁 총정리',
'스페인여행] 스페인 신혼여행 다녀왔어요~', '여행은 살아보는거야', '일본여행 준비물 체크리스트, 여행시 챙길 것',
'호주여행 얌바(Yamba) 보석 같은 곳', '여행계획서 만들기! 일본 홋카이도 여행계획표','강릉여행 안목해변 커피거리',
'엄마와 함께 대만 여행기 01.여행준비'] 

des_list = ['여행을 다녀온지 2주가 지났다. 사진정리는 하나도 못했음 ㅋㅋㅋㅋㅋㅋㅋ 막상 지우려니깐.. 초점이 안맞은 사진까지도 지울수가 없;;ㅠㅠ 난 이래서 다른 정리도 잘 못하나봐 ㅋㅋㅋ 버리는걸 잘 못한다 ㅋㅋㅋㅋ 암튼, 그동안 여행다녀올때마다 일정은 상세히 기록해뒀지만',
'여행을 위해서는 패케지 여행은 그런대로 별 사전 정보 없이 다니실수 있으시겠지만. 개인적으로 여행을 떠나시는 여행객들에게는 정보가 많이 필요할 것이라는 생각입니다. 저 역시 다른 나라를 여행 할 때는 실수를 하지 않나 두렵고, 먼저 그곳을 여행 해 보신 분들에게',
'이웃님들 그리고 이 글을 보고 계시는 세부 여행객들^^ 평상시 여행을 추천하는 나디아에요. 여행이라는 건 큰 비용 없이도 갈 수 있기 때문에 좋은 여행을 하길 바라며 세부여행팁을 엑셀로 정리해봤어요. 나디아도 3박 5일만 있던 사람이라... 사실 필리핀 세부를 잘 몰라요..',
'비어버렸네용 여행중에 폰까지 망가졌어서 블로그는 들어가보지도 못하고 지냈어요 ~ 우리 멋진 여봉봉이 한땀한땀 정성들여 만들어준 가죽여권지갑을 들고 요렇게 총총총 여행길을 떠났답니다 ㅎㅎㅎ 신혼여행이다보니 블로그 포스팅을 다 잘 할 수 있을지는 모르지만 틈틈히',
'부모님들이 불편할 때엔 바로바로 해결해줄것 등등의 생각 + 그리고 세가족이 움직이고 긴 여행이라 물가비싼 북유럽에서 아낄 수 있는 부분은 숙박비밖에 없더라구요 뭐 신혼여행도아니고.. 북유럽이 호텔컨디션 빈익빈부익부가 심한 편이라 괜찮은데로 찾다보니 숙박비에서만 몇',
'일본여행 준비물 체크리스트, 여행시 챙길 것 이번 일본 삿포로, 오타루 여행을 하면서 내가 생각보다 준비를 많이 못하고 나왔구나 라는 생각을 몇 번이나 했는지... 앞으로 그런 일이 없기를 바라면서 일본여행 준비물 체크리스트 표를 또 만들어봤다. 예전에 유럽여행 관련해서',
'호주여행 얌바(Yamba) 느림의 미학여행을 준비할 때 구체적인 계획은 세우지 않아도 어디에 무엇이 있는지 정도는 알아보고 매체나 이야기로 들었던 장면들을 상상하면서 보통 그렇게 여행을 하곤 했어요 허나, 이번 호주여행은 조금 달랐어요 잠은 자야 하니까 목적지는 있으나']

title_corpus = []
des_corpus = []

for title in title_list :
    corpus = text_clean(title)
    title_corpus.append(corpus)

for des in des_list :
    corpus = text_clean(des)
    des_corpus.append(corpus)

title_corpus = list(map(lambda x : spell_checker.check(x).checked, title_corpus))
des_corpus = list(map(lambda x : spell_checker.check(x).checked, des_corpus))

stopwords = []
stopwords = stopwords + [line.strip() for line in open('stopwordsKor.txt', encoding='utf-8')]


komoran = Komoran()
#1
for title in title_corpus:
    tokens = komoran.nouns(title)
    for token in tokens :
        if token not in stopwords :
            print(token, end= ' ')

#2
title_token = []
for title in title_corpus:
    tokens = komoran.pos(title)
    for token in tokens :
        if token[1] not in ['JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JX', 'JC', 'EP', 'EF', 'EC', 'ETN', 'ETM', 'XSN', 'XSV', 'XSA'] :
            title_token.append(token[0])

print('#2')
print(title_token)