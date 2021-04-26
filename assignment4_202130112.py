## libraries
import re
import nltk

## load text
with open('data.txt', 'r') as f:
    data = f.read()

### 1. TOKENIZATION

## patterns for tokenization
front_punct_p = re.compile(r'(?:^|\s)([^A-Za-z\s0-9]+)([A-Za-z0-9\-]+)(?:$|\s)') #ex: "Robots 
back_punct_p = re.compile(r'(?:^|\s)([A-Za-z0-9\-]+)([^A-Za-z\s0-9]+)(?:$|\s)') #ex: the movie"
both_punct_p = re.compile(r'(?:^|\s)([^A-Za-z\s0-9]+)([A-Za-z0-9\-]+)([^A-Za-z\s0-9]+)(?:$|\s)') #ex: "nucleus"
clitics_p = re.compile(r"(?:^|\s)(\S+?)(n't|'s)(?:$|\s)") #ex: n't, 's 
puncts_p = re.compile(r"(?:^|\s)([^A-Za-z\s0-9])([^A-Za-z\s0-9]+)(?:$|\s)") #ex: )".

#완전하지 않음
numerics_with_unit_front_p = re.compile(r"(?:^|\s)([^A-Za-z\s0-9]+)([0-9][\.\,0-9]*)(?:$|\s)") #ex: $2,000
# numerics_with_unit_back_p = re.compile(r"(?:^|\s)([0-9][\.\,0-9]*)([^\s0-9]+?)(?:$|\s)") #ex: 1,000won


## pattern들을 re.sub로 띄어쓰기를 적용해준다.
## 2번 적용해 줘야 함. 띄어쓰기가 겹치기 때문

data = front_punct_p.sub(r' \1 \2 ', data)
data = back_punct_p.sub(r' \1 \2 ', data)
data = both_punct_p.sub(r' \1 \2 \3 ', data)

data = front_punct_p.sub(r' \1 \2 ', data)
data = back_punct_p.sub(r' \1 \2 ', data)
data = both_punct_p.sub(r' \1 \2 \3 ', data)

data = clitics_p.sub(r' \1 \2 ', data)

## )". 같은 punctuation 연쇄를 분리하기 위함
while True:
    if not puncts_p.findall(data): #비어있으면, 즉, punctuation 연쇄가 없으면
        break
    data = puncts_p.sub(r' \1 \2 ', data)


data = numerics_with_unit_front_p.sub(r' \1 \2 ', data)
# data = numerics_with_unit_back_p.sub(r' \1 \2 ', data)

data = re.sub('\s+', ' ', data) #띄어쓰기 1번(사실상 2번) 이상된 경우를 하나로
data = data.strip()

# data = data.split()

with open('data_tokenized.txt', 'w', encoding = 'utf8') as f:
    f.write(data)

# print(data)

##MWE 묶어주기
#대문자 2번 반복 -> 개체명 ex: San Francisco -> San_Francisco
ne_upper_case_mwe_p = re.compile(r'(?:^|\s)([A-Z]\S+)(?:\s)([A-Z]\S+)(?:$|\s)')
while True:
    if not ne_upper_case_mwe_p.findall(data):
        break
    data = ne_upper_case_mwe_p.sub(r' \1_\2 ', data)
# print(data)


### 2. WORD FREQEUNCY

word_tokens = data.split()
word_tokens_lower = list(map(lambda x: x.lower(), word_tokens)) #정규화 위해 lower case로 바꿔주기

word_freq_list = []
for w in list(set(word_tokens_lower)):
    word_freq_list.append((w,word_tokens_lower.count(w)))

word_freq_list = sorted(word_freq_list, key = lambda x: x[1], reverse = True) #빈도 리스트 고빈도순으로 정렬
word_freq_list = list(map(lambda x: x[0] + '\t' + str(x[1]), word_freq_list))
word_freq_list = '\n'.join(word_freq_list)

with open('word_freq.txt', 'w', encoding = 'utf8') as f:
    f.write(word_freq_list)

# ## 고빈도 40개 출력
# print("word_frequency_list_40")
# for w in word_freq_list[:40]:
#     print(w)


### 3. Sentence segmentation    
#'.'앞 문맥이 호칭어 종류거나 대문자+. 처럼 개체명의 일부가 아닌 경우에는 문장 종결자
#또 .으로 안 끝나고 \"로 끝날 수도 있음
with open('data.txt', 'r') as f:
    data = f.read()

sent_seg_p = re.compile(r'([\?!\.][\"\']?)(\s+)([\"\']?[A-Z])') # .!?로 끝나고 띄어쓰기 후, 대문자가 등장하는 경우, quotation mark는 optional
data = sent_seg_p.sub(r'\1\n\3', data) # re.sub로 개행문자'\n'를 넣어줌
# sent_segs = data.split('\n')

with open('sentence_segmented.txt', 'w', encoding = 'utf8') as f:
    f.write(data)



### nltk 이용
# from nltk.tokenize import word_tokenize, TreebankWordTokenizer, sent_tokenize
# import collections
# # tokenizer=TreebankWordTokenizer()
# # print(tokenizer.tokenize(text))

# with open('data.txt', 'r') as f:
#     data = f.read()

# ##tokenization
# word_tokens = word_tokenize(data)
# # print(word_tokens)

# ##word_frequency
# word_tokens_lower = list(map(lambda x: x.lower(), word_tokens)) 
# count = collections.Counter(word_tokens_lower)
# most = count.most_common() #빈도 수 순으로 추출
# print(most[:40])

# ##sentence_segmentation
# sent_segments = sent_tokenize(data)
# print(len(sent_segments))
# # print(sent_segments)