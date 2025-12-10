from konlpy.tag import Komoran
import json
from os.path import abspath
import os
import pandas
from unicode import join_jamos
from collections import defaultdict, Counter
import pickle
import time
from tqdm import tqdm
from jamo import h2j, j2h, j2hcj

komoran = Komoran() 

# 데이터 불러오기 (json)
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

# 이것도 안씀
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


def compos_hangle_ver2(token: list) -> list:
    """
    현재 사용중인 전처리 보강 함수
    """
    c_token = []
    temp = None
    for idx, pos in enumerate(token):
        text, tag = pos[0], pos[1]
        decompose = j2hcj(h2j(text))
        # if decompose in ['ㄴ', 'ㄹ']:
        if temp != None:
            text = text + temp
            temp = None

        if text[0] == 'ㄴ' or text[0] == 'ㄹ' and len(c_token) >= 1: # ㄴ, ㄹ 다시 병합
            # print(decompose)
            rlt = j2hcj(h2j((token[idx-1][0]))) + decompose
            rlt = join_jamos(rlt)
            c_token[-1] = rlt
        
        elif text[-1] == 'ㄴ':
            temp = text

        elif text[0] == '아' and token[idx-1][0][-1] == '하' and len(c_token) >= 1: # 해 복원
            pre = j2hcj(h2j((token[idx-1][0])))[:-2]
            rlt = join_jamos(pre + "ㅎㅐ" + decompose[2:])
            c_token[-1] = rlt

        elif text[0] == '았' and token[idx-1][0][-1] == '하' and len(c_token) >= 1: # 했 복원
            pre = j2hcj(h2j((token[idx-1][0])))[:-2]
            # print(pre)
            rlt = join_jamos(pre + "ㅎㅐㅆ" + decompose[3:])
            c_token[-1] = rlt

        elif text[-1] == '다' and len(text) == 1 and len(c_token) >= 1: # 했 + 다 처럼 합처줌 # 케나다 같은 예외 주의
            rlt = c_token[-1] + text
            c_token[-1] = rlt

        elif tag=='XSN' and len(c_token) >= 1: # 효율 + 성
            c_token[-1] = c_token[-1]+text
            # print(c_token[-1])

        elif tag in ['JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JC', 'JX', 'ETN'] and len(c_token) >= 1:
            if not token[idx-1][1] == 'SS':
                c_token[-1] = c_token[-1]+text
                # print(c_token[-1], text, tag)

        else:
            rlt = join_jamos(decompose)
            c_token.append(rlt)
    return c_token


def take_token_on_one_file(path: str, root_name: str='data', n: int=4) -> None: 
    """
    파일 하나 열어서 그에 대한 전체 전이 확률 행렬 구하는 함수
    """
    ds = data_load(path)
    content = take_content(ds)
    tokens = []
    path_content = path.split('/')
    path_name = path_content[-1].split('.')[0]
    save_path = str(f'{root_name}/test_{path_name}.pkl')

    for i, sentence in enumerate(content):
        try:
            tokens.append(compos_hangle_ver2(komoran.pos(sentence)))
        except:
            print(i, sentence)
            raise 'stop'
    
    Matrix = defaultdict(Counter)
    for token in tokens:
        Matrix = to_matrix(token, Matrix, n)
    # print(len(Matrix))
    matrix_save(Matrix, save_path)
    print(f'process - ({path_name}) done')


def n_gram(token: list, n :int = 4): # (n-1)-gram으로 생각해야함, 앞n개와 현재 토큰 1개를 포함한 n+1개가 필요해서 이렇게 된 것임
    for i in range(len(token)):
        yield tuple(token[i:n+i])


def to_matrix(sentence: list, transitions :defaultdict[Counter] = defaultdict(Counter), n: int = 4) -> Counter:
    for ng in n_gram(sentence, n):
        pre = ng[:-1]
        next_token = ng[-1]
        transitions[pre][next_token] += 1
    return transitions

    
def matrix_save(matrix: defaultdict[Counter], save_path: str, n: int = 4) -> None:
    with open(save_path, 'wb') as f:
        pickle.dump(matrix, f)


# ===================================================================
from preprocesse import *
import multiprocessing

# 데이터 불러오기 (pickle)
def load_pickle(path: str) -> defaultdict[Counter]:
    with open(path, 'rb') as f:
        rlt = pickle.load(f)
    print(f'process - ({path.split('/')[-1]}) done')
    return rlt


def merge_files2(folder_path: str='data') -> None : 
    file_list = os.listdir(folder_path)

    data = []
    size = 64
    n = len(file_list)
    chunk_idx = 0 

    for start in tqdm(range(0, n, size)):
        end = min(start + size, n)

        if start==0:
            print('!')
            merge_matrix = defaultdict(Counter)
        else:
            merge_matrix = load_pickle(f'processed_data_n=1/{NAME}_dataset.pkl')
        
        chunk_files = [f'{folder_path}/{i}' for i in file_list[start:end]]
        
        data = []
    
        with multiprocessing.Pool(processes=8) as pool:
            data.append(pool.map(load_pickle, chunk_files))

        for d in data:
            for key, counter in d[0].items():
                merge_matrix[key].update(counter) # 전이 확률 업데이트
        
        matrix_save(merge_matrix, f'processed_data/{NAME}_dataset.pkl')


def make_datas():
    """
    한국어 말뭉치 데이터셋에서 원하는 카테고리를 골라서 그 카테고리 파일 전부를 전처리 해서 새로운 폴더에 저장하는 코드
    저장하는 폴더는 따로 입력이 필요(매개변수x)
    """
    dir_path = f'D:/Repositories/too_much_big_data/markov/download/라벨링데이터/{NAME}'
    dir_list = os.listdir(dir_path)
    dir_list = list(map(lambda x: dir_path+'/'+x, dir_list))
    print(dir_list) # debug

    with multiprocessing.Pool(processes=8) as pool:
        list(tqdm(pool.imap_unordered(take_token_on_one_file, dir_list))) # 더 찾아보기

NAME = 'IT_과학'

if __name__ == "__main__":

    # dir_path = f'D:/Repositories/too_much_big_data/markov/download/라벨링데이터/{NAME}'
    # dir_list = os.listdir(dir_path)
    # take_token_on_one_file(dir_path +'/'+ dir_list[9], root_name='data')

    make_datas()
    merge_files2()


