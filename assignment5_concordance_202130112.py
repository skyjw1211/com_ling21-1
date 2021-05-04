import re

token = ''
left_context_leng = ''
right_context_leng = ''

#input
while token == '':
    token = input('찾을 토큰을 입력해주세요: ') #token값 입력 받기

while left_context_leng == '':
    try:
        left_context_leng = int(input('왼쪽 문맥의 범위을 입력해주세요.(숫자): ')) #context 범위 입력받기
    except: #숫자 아닌 입력이 들어왔을 때 계속됨
        continue

while right_context_leng == '':
    try:
        right_context_leng = int(input('오른쪽 문맥의 범위을 입력해주세요.(숫자): ')) #context 범위 입력받기
    except:
        continue


#불러오기
with open("data.txt", 'r', encoding = 'utf8') as f:
    corpus = f.read()

#입력받은 토큰이 포함된 어절에 태그를 붙여줌
corpus_changed = re.sub(r'({tok}\S*)'.format(tok = token),r'<<<\1>>>',corpus)

#line 별로 나누어 줌, *line마다 2개 이상의 문장이 들어가 있을 수 있음= line마다 2개 이상의 토큰이 포함돼 있을 수 있다.
#"."으로 단순히 문장을 구분하기에는 위험성이 있다.
lines = corpus_changed.split('\n')

result = [] #여기에 결과값(concordance line)이 포함된 텍스트가 들어감.
regex_str = r'((?:\S+ ){0,%d}<<<%s\S*>>>(?: \S+){0,%d})'% (left_context_leng, token, right_context_leng) #입력값으로 포매팅
concords= re.compile(regex_str) #최대 n의 문맥을 갖는 정규 표현식 컴파일


for line in lines:
    #line을 지우는 대신 최대 n의 문맥을 갖는 concordance를 뽑아내고자 함. 
    temp = concords.findall(line)

    if len(temp) != 0: #발견된 게 있으면 결과 값에 넣어줌
        result += temp

#left context, token, right context list로 만든 후 가장 긴 길이의 context를 기준으로 각각 alignment? 혹은 포매팅으로 빈 문자열 넣어줌
left_context_ls = [] #왼쪽 문맥
search_token_ls = [] #검색할 토큰, 리스트로 만들어주는 이유는 토큰 기준으로 나누었기에 뒤에 문장부호가 결합된 형식으로 토큰이 전부 상이할 수 있다.
right_context_ls = [] #오른쪽 문맥


for sent in result:
    p_split_context = re.compile(r'((?:\S+ ){0,%d})(<<<%s\S*>>>)((?: \S+){0,%d})'% (left_context_leng, token, right_context_leng)) # 양 옆 문맥과 가운데 토큰으로 나눔

    left, center, right = p_split_context.findall(sent)[0] #리스트 내에 튜플 형식으로 되어 있음
    
    left_context_ls.append(left)
    search_token_ls.append(center)
    right_context_ls.append(right)
    
#각 문맥별 최대 길이
left_max_len = max(list(map(lambda x: len(x), left_context_ls)))
right_max_len = max(list(map(lambda x: len(x), right_context_ls)))
all_max = max(left_max_len, right_max_len)

#토큰 최대 길이
token_max_len = max(list(map(lambda x: len(x), search_token_ls)))

#최대 문맥 길이로 포맷팅 형식에 넣어준다.
left_format = "%{max_len}s".format(max_len = all_max)
right_format = "%-{max_len}s".format(max_len = all_max)

#최대 토큰 길이로 포맷팅 형식에 넣어주기
center_format = "%-{max_len}s".format(max_len = token_max_len)

#가장 긴 문맥의 길이를 기준으로 포맷팅 해준다. 
left_contexts = list(map(lambda x: left_format % x, left_context_ls))
search_tokens = list(map(lambda x: center_format % x, search_token_ls))
right_contexts = list(map(lambda x: right_format % x, right_context_ls))

res = []
for i in range(len(search_token_ls)):
    res.append(left_contexts[i] + ' ' + search_tokens[i] + '\t' + right_contexts[i])

#line을 하나의 text로, \n로 구분자를 주어 concordance들이 다른 line으로 분리되도록 하였다.
corpus_result = '\n'.join(res)

#내보내기
with open("data_concor_result.txt", 'w', encoding = 'utf8') as f:
    f.write(corpus_result)

# print(corpus_result)