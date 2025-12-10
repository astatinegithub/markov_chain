from collections import Counter, defaultdict
from preprocesse import compos_hangle_ver2
import pickle
from time import time
import math
from random import choices
from konlpy.tag import Komoran
import os
komoran = Komoran() 


def load_martrix(file_name: str='processed_data/IT_dataset.pkl') -> defaultdict[Counter]:
    print('데이터 로드중 ...')
    T = time()
    with open(file_name, 'rb') as f:
        matrix = pickle.load(f)
    print(f'데이터 로드 완료 {time()-T}초 걸림')
    
    return matrix


def logit(P: float) -> float:
    """probability to float"""
    return math.log(P/(1-P))


def Temperature_normalization(P_list: list, T: float = 0.35) -> list:
    temp = []
    for P in P_list:
        if P==0:
            temp.append(0)
        elif P ==1:
            temp.append(1)
        else:
            temp.append(math.e**(logit(P)/T))
    temp_all  = sum(temp)
    rlt = []
    for i in temp:
        rlt.append(i/temp_all)
    return rlt


def select_word(matrix, pre_words: tuple, T=0.35):
    value = []
    weight = []

    pre_token: Counter = matrix[pre_words]
    for i in pre_token:
        value.append(i)
        weight.append(pre_token[i]/sum(pre_token.values()))
        
    total_sum = sum(weight)
    weight = Temperature_normalization([v/total_sum for v in weight], T)
    # weight = Temperature_normalization(weight)
    rlt = choices(value, weights=weight, k=1)
    print(dict(zip(value, weight)))
    return rlt[0]



if __name__ == "__main__":
    Matrix = load_martrix(file_name='processed_data/취미_dataset.pkl')
    Matrix_n1 = load_martrix(file_name='processed_data_n=1/IT_과학_dataset.pkl')
    # for i in matrix.keys():
    #     if i in '새롭ㄴ':
    #         print(i)


    # # 새롭ㄴ
    # print(list(Matrix.keys()))
    text = '애플'
    sentence = ['', '', '']
    sentence = compos_hangle_ver2(komoran.pos(text))
    print(Matrix_n1[('워렌',)])

    # try:
    import time
    for i in range(200):
        if len(sentence) <= 2:
            next = select_word(Matrix_n1, (sentence[-1],))
        else:
            try:
                next = select_word(Matrix, (sentence[-3], sentence[-2], sentence[-1]))
            except:
                next = select_word(Matrix_n1, (sentence[-1],))
                
        sentence.append(next)
        print()
        print(*sentence)

        time.sleep(0.1)
    # except:
    #     print('행렬에 없는 데이터')

# import os
# dir_path = 'D:/Repositories/too_much_big_data/markov/download/라벨링데이터'
# dir_list = os.listdir(dir_path)
# path_list = [{i: len(os.listdir(dir_path+'/'+i))} for i in dir_list]

# for i in path_list:
#     print(i)