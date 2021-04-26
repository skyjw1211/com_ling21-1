#필요한 것
#TRANSITION TABLE-pandas DataFrame로 해결(열이름 사용하기 위함)
#TRANSITION TABLE은 행(state number), 열(transition의 조건 alphabet)
#D-Recognize pseudo code참조.



import re
import pandas as pd

#transition table 만들기
#regex: r'baaa*!'
#열이름: b, a, !, end
#각 STATE 별 튜플
"""
('state', 'b','a','!','end')
(0, 1, '', '', '')
(1, '', 2, '', '')
(2, '', 3, '', '')
(3, '', 3, 4, '')
('accept, '', '', '', '')

"""

states = [(0, 1, '', '', ''),\
        (1, '', 2, '', ''),\
        (2, '', 3, '', ''),\
        (3, '', 3, 4, ''),\
        ('accept', '', '', '', '')] #마지막 state의 경우, 이름으로 accept를 넣어준다.

trans_table = pd.DataFrame(states, columns=('state', 'b','a','!','end'))
#state를 DataFrame으로 구성


def d_recognize(string, trans_table=trans_table): #string = tape, 
    #값 초기화
    idx = 0
    current_state = 0
    last_index = len(string)

    while True:
        
        if idx == last_index: #input을 모두 소비함
            if trans_table['state'][current_state] == 'accept': #마지막 state일 경우,
                print('accept')
                break
            else: #input 소진했는데 마지막 state가 아닌 경우
                print('reject')
                break
        elif string[idx] not in ['a', 'b', '!']: #다른 문자열 입력될 경어
            print('reject')
            break
        elif trans_table[string[idx]][current_state] == '': #다음 state로 넘어갈 수 없음
            print('reject')
            break
        else: #나머지의 경우에는 transition table에 명시된 다음 state로 이동
            current_state = trans_table[string[idx]][current_state]
            idx += 1
while True:
    string = input('인식할 문자열을 입력하세요: ')
    if string == '0': #종료 조건
        break
    d_recognize(string)