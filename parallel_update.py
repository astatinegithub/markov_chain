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


# ===================================================================
from main import *
def merge_files(folder_path:str='data-국제'):
    file_list = os.listdir(folder_path)

    data = []

    for file_path in tqdm(file_list):
        with open(f'{folder_path}/'+file_path, 'rb') as f:
            data.append(pickle.load(f))

    merge_matrix = defaultdict(Counter)

    for d in tqdm(data):
        for key, counter in d.items():
            merge_matrix[key].update(counter)

    matrix_save(merge_matrix, f'processsed_data/test_sum_{time.time()}.pkl')

import multiprocessing

if __name__ == "__main__":
    dir_path = f'D:/Repositories/too_much_big_data/markov/download/라벨링데이터/{NAME}'
    dir_list = os.listdir(dir_path)
    dir_list = list(map(lambda x: dir_path+'/'+x, dir_list))
    print(dir_list)

    with multiprocessing.Pool(processes=8) as pool:
        list(tqdm(pool.imap_unordered(take_token_on_one_file, dir_list))) # 더 찾아보기

    # proc = []
    # for path in tqdm(dir_list):
    #     p = multiprocessing.Process(target=take_token_on_one_file, args=(path, ))
    #     p.start()
    #     proc.append(p)

    # for p in proc:
    #     p.join()
    try:
        merge_files()
    except:
        print('병합 실패')