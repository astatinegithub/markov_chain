from collections import Counter, defaultdict
from main import compos_hangle_ver2
import pickle
# test = defaultdict({('콘텐츠', '제작사와', '웹사이트'): Counter({'운영': 4, '제작': 3}), ('제작사와', '웹사이트', '운영'): Counter({'사들의': 1, '사': 1}), ('웹사이트', '운영', '사들의'): Counter({'경우': 1}), ('운영', '사들의', '경우'): Counter({',': 1})})
from time import time
from tqdm import tqdm
from konlpy.tag import Komoran


with open('processed_data/IT_dataset.pkl', 'rb') as f:
    matrix = pickle.load(f)

# value = []
# weight = []

# pre_token: Counter = matrix[(')', '이', '면')]
# for i in tqdm(pre_token):
#     value.append(i)
#     weight.append(pre_token[i]/sum(pre_token.values()))

# from random import choices

# rlt = choices(value, weights=weight)
# print(pre_token.most_common(1))
# print(type(rlt))
# print(rlt)

from random import choices

def select_word(pre_words: tuple):
    # m: Counter = matrix[pre_words]

    value = []
    weight = []

    pre_token: Counter = matrix[pre_words]
    for i in pre_token:
        value.append(i)
        weight.append(pre_token[i]/sum(pre_token.values()))
        
    total_sum = sum(weight)
    weight = [v/total_sum for v in weight]
    rlt = choices(value, weights=weight, k=1)
    return rlt[0]

    # return m.most_common(1)[0][0]

komoran = Komoran()

print(list(matrix.keys())[0])
text = '지난 2013년 애플이'
sentence = ['', '', '']
sentence = compos_hangle_ver2(komoran.pos(text))
print(sentence)

import time
for i in range(30):
    next = select_word((sentence[-3], sentence[-2], sentence[-1]))
    sentence.append(next)
    print(*sentence)

    time.sleep(0.1)

# import os
# dir_path = 'D:/Repositories/too_much_big_data/markov/download/라벨링데이터'
# dir_list = os.listdir(dir_path)
# path_list = [{i: len(os.listdir(dir_path+'/'+i))} for i in dir_list]

# for i in path_list:
#     print(i)