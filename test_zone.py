from collections import defaultdict, Counter
from main import matrix_save
import pickle
import os
import time
from tqdm import tqdm

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

# folder_path = 'data'
# file_list = os.listdir(folder_path)


# data = []


# for file_path in tqdm(file_list):
#     with open('data/'+file_path, 'rb') as f:
#         data.append(pickle.load(f))

# merge_matrix = defaultdict(Counter)

# for d in tqdm(data):
#     for key, counter in d.items():
#         merge_matrix[key].update(counter)

# print(merge_matrix)
# print(len(merge_matrix))

# matrix_save(merge_matrix, f'test_sum_{time.time()}.pkl')


import os
dir_path = 'D:/Repositories/too_much_big_data/markov/download/라벨링데이터'
dir_list = os.listdir(dir_path)
path_list = [{i: len(os.listdir(dir_path+'/'+i))} for i in dir_list]

for i in path_list:
    print(i)