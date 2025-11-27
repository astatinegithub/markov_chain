from konlpy.tag import Komoran
import json
from os.path import abspath
import os
import pandas
from jamo import h2j, j2h, j2hcj
from unicode import join_jamos
from collections import defaultdict, Counter
import pickle
import time
from tqdm import tqdm

PATH_ = r"D:\Repositories\too_much_big_data\markov\download\라벨링데이터\IT_과학\BWSC217000049024.json"
komoran = Komoran() 

# 데이터 불러오기
def data_load(PATH: str) -> dict:
    """load a data file"""
    with open(PATH, 'r', encoding='utf-8') as f:
        raw = f.read()
    return dict(json.loads(raw))


def take_content(data: list) -> list:
    """
    make a content list\
    \n
    ```return ['sentence', 'sentence', 'sentence', 'sentence', ..., 'sentence']
    """
    rlt = []
    for content in data['named_entity']:
        sentence = ''
        for j in content["content"]:
            sentence += ' ' + j["sentence"]
        rlt.append(sentence)
    return rlt


# def replace_space(text:str) -> str:
#     if text[0] == ' ':
#         text = text[1:]
#     rlt = text.replace(' ', ' ␣ ')
#     return rlt


# # 안씀
# def compose_hangle(token: list) -> list:
#     """분리된 자모 다시 결합"""
#     c_token = []
#     for idx, text in enumerate(token):
#         decompose = j2hcj(h2j(text))
#         # if decompose in ['ㄴ', 'ㄹ']:
#         if text[0] == 'ㄴ' or text[0] == 'ㄹ': # ㄴ, ㄹ 다시 병합
#             # print(decompose)
#             rlt = j2hcj(h2j((token[idx-1]))) + decompose
#             rlt = join_jamos(rlt)
#             c_token[-1] = rlt
#         elif text[0] == '아' and token[idx-1][-1] == '하': # 해 복원
#             pre = j2hcj(h2j((token[idx-1])))[:-2]
#             rlt = join_jamos(pre + "ㅎㅐ" + decompose[2:])
#             c_token[-1] = rlt
#         elif text[0] == '았' and token[idx-1][-1] == '하': # 했 복원
#             pre = j2hcj(h2j((token[idx-1])))[:-2]
#             # print(pre)
#             rlt = join_jamos(pre + "ㅎㅐㅆ" + decompose[3:])
#             c_token[-1] = rlt
#         elif text == '다': # 했 + 다 처럼 합처줌
#             rlt = c_token[-1] + text
#             c_token[-1] = rlt
#         elif text == '는' or text == '은':
#             c_token.append(text)
#         else:
#             rlt = join_jamos(decompose)
#             c_token.append(rlt)
#     return c_token


# 현재쓰는 전처리 함수
def compos_hangle_ver2(token: list) -> list:
    c_token = []
    for idx, pos in enumerate(token):
        text, tag = pos[0], pos[1]
        decompose = j2hcj(h2j(text))
        # if decompose in ['ㄴ', 'ㄹ']:
        if text[0] == 'ㄴ' or text[0] == 'ㄹ': # ㄴ, ㄹ 다시 병합
            # print(decompose)
            rlt = j2hcj(h2j((token[idx-1][0]))) + decompose
            rlt = join_jamos(rlt)
            c_token[-1] = rlt

        elif text[0] == '아' and token[idx-1][0][-1] == '하': # 해 복원
            pre = j2hcj(h2j((token[idx-1][0])))[:-2]
            rlt = join_jamos(pre + "ㅎㅐ" + decompose[2:])
            c_token[-1] = rlt

        elif text[0] == '았' and token[idx-1][0][-1] == '하': # 했 복원
            pre = j2hcj(h2j((token[idx-1][0])))[:-2]
            # print(pre)
            rlt = join_jamos(pre + "ㅎㅐㅆ" + decompose[3:])
            c_token[-1] = rlt

        elif text == '다': # 했 + 다 처럼 합처줌
            rlt = c_token[-1] + text
            c_token[-1] = rlt

        elif tag=='XSN': # 효율 + 성
            c_token[-1] = c_token[-1]+text
            # print(c_token[-1])

        elif tag in ['JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JC', 'JX', 'ETN']:
            if not token[idx-1][1] == 'SS':
                c_token[-1] = c_token[-1]+text
                # print(c_token[-1], text, tag)

        else:
            rlt = join_jamos(decompose)
            c_token.append(rlt)
    return c_token


# 파일 하나 열어서 그에 대한 전체 전이 확률 행렬 구하는 함수
def take_token_on_one_file(path: str) -> None: 
    ds = data_load(path)
    content = take_content(ds)
    tokens = []
    save_path = str(f'data/test_{int(time.time())}.pkl')

    for sentence in content:
        tokens.append(compos_hangle_ver2(komoran.pos(sentence)))
    
    Matrix = defaultdict(Counter)
    for token in tokens:
        Matrix = to_matrix(token, Matrix)
    print(len(Matrix))
    matrix_save(Matrix, save_path)
    return


def n_gram(token: list, n :int = 4):
    for i in range(len(token)):
        yield tuple(token[i:n+i])


def to_matrix(sentence: list, transitions :defaultdict[Counter] = defaultdict(Counter), n: int = 4) -> Counter:
    for ng in n_gram(sentence):
        pre = ng[:-1]
        next_token = ng[-1]
        transitions[pre][next_token] += 1
    return transitions

    
def matrix_save(matrix: defaultdict[Counter], save_path: str, n: int = 4) -> None:
    with open(save_path, 'wb') as f:
        pickle.dump(matrix, f)


# test_data = data_load(PATH_)
# t = take_content(test_data)



# text = t[-1]
# komoran = Komoran() 
# # print("okt 형태소 추출:", komoran.morphs(text)) 
# print(text)
# print('='*70)
# tokens = komoran.morphs(text)
# # tokens2 = compose_hangle(tokens)
# tokens3 = compos_hangle_ver2(komoran.pos(text))
# tokens4 = komoran.pos(text)
# print('='*70)
# print(tokens)
# print('='*70)
# print(tokens4)
# print('='*70)
# print(tokens3)



# cnt = 0
# cnt2 = 0
# for text in t:
#     k = komoran.pos(text)
#     cnt += len(compos_hangle_ver2(k))
#     cnt2 +=len(k)

# print(f'{(cnt2-cnt)/cnt2*100}%')





if __name__ == "__main__":
    dir_path = 'D:/Repositories/too_much_big_data/markov/download/라벨링데이터/건강'
    dir_list = os.listdir(dir_path)
    if 'D' in dir_list:
        print('a')
    cnt = 0
    for path in tqdm(dir_list):
        cnt += 1
        take_token_on_one_file(dir_path +'/'+ path)
        print(f'{len(dir_list)-cnt} 번 남음') # 3000개에 5시간 예상인데;; 무조건 병렬 해야할듯