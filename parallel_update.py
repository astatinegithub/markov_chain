"""
`main.py`로 이동함
"""

# from collections import defaultdict, Counter
# from main import matrix_save
# import pickle
# import os
# import time
# from tqdm import tqdm
# from main import *

# test_data = data_load(PATH_)
# t = take_content(test_data)

# tokens = compos_hangle_ver2(komoran.pos(text))
# # print(Counter(zip(tokens[:-1], tokens[1:])))
# print('='*60)

# def n_gram(token: list, n :int = 4):
#     for i in range(len(token)):
#         yield tuple(token[i:n+i])

# def matrix(sentence: list, n: int = 4) -> Counter:

#     transitions = defaultdict(Counter)

#     for ng in n_gram(sentence):
#         pre = ng[:-1]
#         next_token = ng[-1]
#         transitions[pre][next_token] += 1 # Counter()['key'] += number

#     return transitions

# check= list()
# for i in range(10):
#     check.append(matrix(tokens))

# x = matrix(tokens)
# print(x)
# print(type(x))
# print(len(x))

# def merge_files(folder_path:str='data'):
#     file_list = os.listdir(folder_path)

#     data = []

#     for file_path in tqdm(file_list):
#         with open(f'{folder_path}/'+file_path, 'rb') as f:
#             data.append(pickle.load(f))

#     merge_matrix = defaultdict(Counter)

#     for d in tqdm(data):
#         for key, counter in d.items():
#             merge_matrix[key].update(counter)

#     matrix_save(merge_matrix, f'processed_data/test_sum_{time.time()}.pkl')


# ===================================================================
from preprocesse import *
import multiprocessing

def load_pickle(path: str):
    with open(path, 'rb') as f:
        rlt = pickle.load(f)
    print(f'process - ({path.split('/')[-1]}) done')
    return rlt

def merge_files2(folder_path: str='data'):
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
            merge_matrix = load_pickle(f'processed_data/{NAME}_dataset.pkl')
        
        chunk_files = [f'{folder_path}/{i}' for i in file_list[start:end]]
        
        data = []
        
        # print(chunk_files)

        with multiprocessing.Pool(processes=8) as pool:
            data.append(pool.map(load_pickle, chunk_files))

        print(len(data))

        for d in data:
            for key, counter in d[0].items():
                merge_matrix[key].update(counter) # 전이 확률 업데이트
        
        matrix_save(merge_matrix, f'processed_data/{NAME}_dataset.pkl')

    # matrix_save(merge_matrix, f'processed_data/test_sum_{time.time()}.pkl')

def make_datas():
    """
    한국어 말뭉치 데이터셋에서 원하는 카테고리를 골라서 그 카테고리 파일 전부를 전처리 해서 새로운 폴더에 저장하는 코드
    저장하는 폴더는 따로 입력이 필요(매개변수x)
    """
    dir_path = f'D:/Repositories/too_much_big_data/markov/download/라벨링데이터/{NAME}'
    dir_list = os.listdir(dir_path)
    dir_list = list(map(lambda x: dir_path+'/'+x, dir_list))
    print(dir_list) # debug

    with multiprocessing.Pool(processes=6) as pool:
        list(tqdm(pool.imap_unordered(take_token_on_one_file, dir_list))) # 더 찾아보기

if __name__ == "__main__":


    merge_files2()
