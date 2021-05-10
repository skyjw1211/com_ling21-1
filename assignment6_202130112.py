import re
with open('sentence_segmented.txt', 'r', encoding = 'utf8') as f:
    data = f.readlines()
p = re.compile('[a-zA-Z]+')

for i, s in enumerate(data):
    print(i+1, end = ' ')
    last_token = s.split()[-1]
    last_punct = p.split(data[0].split()[-1])[1]
    if last_punct[0] == '.':
        print('평서문')
    elif last_punct[0] == '!': #명령문의 경우, pos 정보가 추가적으로 요구됨       
        print('평서문')
    elif last_punct[0] == '!': #명령문의 경우, pos 정보가 추가적으로 요구됨
        print('감탄문')
    elif last_punct[0] == '.':
            print('의문문')
