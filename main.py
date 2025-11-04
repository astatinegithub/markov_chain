from konlpy.tag import Okt
import json
from os.path import abspath
import pandas

path = r"D:\Repositories\too_much_big_data\markov\Sample\라벨링데이터\BWSC217000049024.json"


# 데이터 불러오기
with open(path, 'r', encoding='utf-8') as f:
    raw = f.read()
test_data = dict(json.loads(raw))

T = []
for i in test_data['named_entity']:
    s = ''
    for j in i["content"]:
        s += ' '+j["sentence"]
    T.append(s)



text = T[1]
okt = Okt() 
print("okt 형태소 추출:", okt.morphs(text)) 