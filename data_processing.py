import re
import nltk
from nltk import word_tokenize
from hanspell import spell_checker
from konlpy.tag import Komoran
import collections
from itertools import combinations

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

def pairwise(arr):
    toks = list(dict.fromkeys(arr))
    pair = list(combinations(sorted(toks), 2))
    return pair

def preprocessing_data(duration) :
    title_data = []
    des_data = []
    data = [title_data, des_data]

    filename = str(duration) + '.txt'
    f = open(filename, 'r', encoding='utf-8')
    for line in f:
        title_data.append(line.strip())
        if len(title_data) >= 1000 :
            break
    for line in f :
        des_data.append(line.strip())
    f.close()

    title_corpus = []
    des_corpus = []
               
    for title in title_data :
        corpus = text_clean(title)
        title_corpus.append(corpus)

    for des in des_data :
        corpus = text_clean(des)
        des_corpus.append(corpus)

    title_corpus = list(map(lambda x : spell_checker.check(x).checked, title_corpus))
    des_corpus = list(map(lambda x : spell_checker.check(x).checked, des_corpus))
 
    return title_corpus, des_corpus

def get_title_result(duration, corpus):
    title_tokens = []

    for sentence in corpus:
        words = komoran.nouns(sentence)
        tokens = []
        for word in words :
            if word not in stopwords :
                tokens.append(word)
        title_tokens.append(tokens)

    title_pairs = []

    for token in title_tokens :
        pair = pairwise(token)
        title_pairs += pair

    count = collections.Counter(list(title_pairs))
    count = {k: v for k, v in count.items() if v >= 20} #threshold

    scount = sorted(count.items(), key=lambda x:x[1], reverse=True)
    
    filename = str(duration)[:4] + 'title.txt'
    with open(filename, 'w', encoding='utf-8') as f:    
        for k, v in scount:
            f.write(f'{k} : {v}\n')
    f.close()

    return

duration_list = ['20160101to20161231', '20170101to20171231', '20180101to20181231', '20190101to20191231', '20200101to20201231', '20210101to20211231', '20220101to20221231', '20230101to20231110']

stopwords = []
stopwords = stopwords + [line.strip() for line in open('stopwordsKor.txt', encoding='utf-8')]

komoran = Komoran(userdic='user_dic.txt')

for duration in duration_list :
    title_corpus, des_corpus = preprocessing_data(duration)
    get_title_result(duration, title_corpus)