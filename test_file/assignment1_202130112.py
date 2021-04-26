import re

#불러오기
with open("data.txt", 'r', encoding = 'utf8') as f:
    corpus = f.read()

#Rowbot이 포함된 토큰에 태그를 붙여줌
corpus_changed = re.sub(r'(Rowbot\S*)',r'<<<\1>>>',corpus)

#line 별로 나누어 줌, *line마다 2개 이상의 문장이 들어가 있을 수 있음= line마다 2개 이상의 Rowbots가 포함돼 있을 수 있다.
#"."으로 단순히 문장을 구분하기에는 위험성이 있다.
lines = corpus_changed.split('\n')

result = [] #여기에 결과값(concordance line)이 포함된 수정 텍스트가 들어감.
concords= re.compile(r'((?:\S+ ){0,3}<<<Rowbot\S*>>>(?: \S+){0,3})') #최대 3의 문맥을 갖는 정규 표현식 컴파일


for line in lines:
    #line을 지우는 대신 최대 3의 문맥을 갖는 concordance를 뽑아내고자 함. 
    temp = concords.findall(line)

    #Rowbot이 발견되지 않았으면 그냥 line을 넣어줌
    if len(temp) != 0:
        result += temp
    else:
        result.append(line)
    

#line을 하나의 text로, \n로 구분자를 주어 concordance들이 다른 line으로 분리되도록 하였다.
corpus_result = '\n'.join(result)

#내보내기
with open("data_result.txt", 'w', encoding = 'utf8') as f:
    f.write(corpus_result)

print(corpus_result)