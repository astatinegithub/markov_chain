# print(1)
# from konlpy.tag import Okt, Hannanum, Kkma 
# print(1)
# text = "아버지가방에들어가신다." 
# okt = Okt() 
# hannanum = Hannanum() 
# kkma = Kkma() 
# print("okt 형태소 추출:", okt.morphs(text)) 
# print("Hannanum 형태소 추출:", hannanum.morphs(text)) 
# print("Kkma 형태소 추출:", kkma.morphs(text)) 

# print("okt 명사 추출:", okt.nouns(text)) 
# print("Hannanum 명사 추출:", hannanum.nouns(text)) 
# print("Kkma 명사 추출:", kkma.nouns(text)) 

import jpype
import konlpy
print("JVM started?", jpype.isJVMStarted())
import json
