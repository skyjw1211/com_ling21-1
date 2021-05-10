import re
from nltk import word_tokenize, pos_tag

with open('sentence_segmented.txt', 'r', encoding = 'utf8') as f:
    data = f.readlines()

def sentence_type_classifier(data):
    p = re.compile('[a-zA-Z]+')

    #평서문
    decl = 0
    #의문문
    inte = 0
    #명령문
    impe = 0
    #감탄문
    excl = 0

    for i, s in enumerate(data):
        print(i+1, end = ' ')
        last_token = s.split()[-1]
        
        tokenized = word_tokenize(s)
        sent_pos = pos_tag(tokenized)

        first_pos = sent_pos[0][1]
        if not first_pos.isalpha(): #문장부호 인 경우
            first_pos = sent_pos[1]

        last_punct = p.split(data[0].split()[-1])[1] #어절 내 문장 부호 분리 위함
        if first_pos == 'VB': # 첫번째 pos 가 동사 원형
            if last_punct[0] != '?':
                impe += 1
                print('명령문') 

        elif last_punct[0] == '.':
            decl += 1
            print('평서문')

        elif last_punct[0] == '!': #명령문의 경우, pos 정보가 추가적으로 요구됨
            excl += 1
            print('감탄문')

        elif last_punct[0] == '?':
            inte += 1
            print('의문문')

    return decl, inte, impe, excl

decl, inte, impe, excl = sentence_type_classifier(data)

print('\n\n-----Sentence Types-------')

print('평서문: ', decl)

print('의문문: ', inte)

print('명령문: ', impe)

print('감탄문: ', excl)