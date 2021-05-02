class porter_stemmer:
    def __init__(self):
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


    #rule_apply: 함수 외부에서 조건 검사, 함수 내에서 suffix 변환 진행
    def rule_apply(self, token, suffix1, suffix2): #suffix1이 충족하면, suffix2로 치환
        res = token
        if len(token) > len(suffix1) and token[-len(suffix1):].lower() == suffix1:
            res = token[:-len(suffix1)] + suffix2
        return res

    def temp_stemming(self, token, suffix1):
        res = token

        if len(token) > len(suffix1) and token[-len(suffix1):].lower() == suffix1:
            return token[:-len(suffix1)]
        
        return res


    #count_m: m의 개수를 센다, m의 개수 리턴, stem을 input으로
    #stem에서 VC 발견하면 cnt+1, stem돌면서 현재 state(v인지)

    ## 모든 문자열은 알파벳임을 전제, 
    #현재 상태 v > not v 만남 = m+1, state= not v
    #현재 상태 v > v 만남 = 다음 진행
    #현재 상태 not v > v 만남 = state = v
    #현재 상태 not v > not v 만남 = 다음 진행
    # vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

    def count_m(self, temp_stem):
        is_state_v = 0
        m = 0

        for ch in temp_stem:
            if is_state_v == 1 and ch not in self.vowels:
                m += 1
                is_state_v = 0
            elif is_state_v == 1 and ch in self.vowels:
                continue
            elif is_state_v == 0 and ch in self.vowels:
                is_state_v = 1
            else:
                continue
            
        return m


    # condition *S: if len(temp_stem) >= 1 and temp_stem[-1] in ['s', 'S']:
    # condition *v*: if set(temp_stem).intersection(vowels):
    # condition *d: if len(temp_stem) >= 2 and temp_stem[-1] == temp_stem[-2]:
    # condition *o: if len(temp_stem) >= 3 and temp_stem[-3] not in vowels and temp_stem[-2] in vowels and temp_stem[-1] not in vowels and temp_stem[-1] not in ['W', 'w', 'X', 'x', 'y', 'Y']:

    #step_1a:
    def step_1a(self, token):
        stemmed = token #stemming이 적용되지 않으면 원래 토큰 리턴

        #가장 긴 조건을 먼저 검사 함으로써 logest match 가 진행되도록 한다.
        if self.temp_stemming(token, 'sses') != token:
            stemmed = self.rule_apply(token, 'sses', 'ss')

        elif self.temp_stemming(token, 'ies') != token:
            stemmed = self.rule_apply(token, 'ies', 'i')

        elif self.temp_stemming(token, 'ss') != token:
            stemmed = self.rule_apply(token, 'ss', 'ss')
        
        elif self.temp_stemming(token, 's') != token:
            stemmed = self.rule_apply(token, 's', '')

        return stemmed


    #step_1b:
    def step_1b(self, token):
        stemmed = token #stemming이 적용되지 않으면 원래 토큰 리턴
        
        #1b-1
        if self.temp_stemming(token, 'eed') != token:
            if self.count_m(self.temp_stemming(token, 'eed')) > 0:
                stemmed = self.rule_apply(token, 'eed', 'ee')
        elif self.temp_stemming(token, 'ed') != token:
            if set(self.temp_stemming(token, 'ed')).intersection(self.vowels):
                stemmed = self.rule_apply(token, 'ed', '')

        elif self.temp_stemming(token, 'ing') != token: 
            if set(self.temp_stemming(token, 'ing')).intersection(self.vowels):
                stemmed = self.rule_apply(token, 'ing', '')

        if stemmed != token: #1b-1에서 stemming이 일어난 token에 대해서만
            
        #1b-2
            if self.temp_stemming(stemmed, 'at') != stemmed:
                stemmed = self.rule_apply(stemmed, 'at', 'ate')

            elif self.temp_stemming(stemmed, 'bl') != stemmed:
                stemmed = self.rule_apply(stemmed, 'bl', 'ble')

            elif self.temp_stemming(stemmed, 'iz') != stemmed:
                stemmed = self.rule_apply(stemmed, 'iz', 'ize')

            elif len(stemmed) >= 2 and stemmed[-1] == stemmed[-2] and stemmed[-1] not in self.vowels and stemmed[-1] not in ['L', 'l', 'S', 's', 'Z', 'z']:
                stemmed = stemmed[:-1]
            
            elif self.count_m(stemmed) == 1 and len(stemmed) >= 3 and stemmed[-3] not in self.vowels and stemmed[-2] in self.vowels and stemmed[-1] not in self.vowels and stemmed[-1] not in ['W', 'w', 'X', 'x', 'y', 'Y']:
                stemmed = stemmed +'e'

        return stemmed


    #step_1c()
    def step_1c(self, token):
        stemmed = token

        if self.temp_stemming(token, 'y') != token and set(self.temp_stemming(token, 'ed')).intersection(self.vowels):
            stemmed = self.rule_apply(token, 'y', 'i')
        return stemmed



    #step_2()
    def step_2(self, token):
        stemmed = token

        if self.temp_stemming(token, 'ational') != token :
            if self.count_m(self.temp_stemming(token, 'ational')) > 0:
                stemmed = self.rule_apply(token, 'ational', 'ate')

        elif self.temp_stemming(token, 'tional') != token:
            if self.count_m(self.temp_stemming(token, 'tional')) > 0:
                stemmed = self.rule_apply(token, 'tional', 'tion')
        
        elif self.temp_stemming(token, 'enci') != token :
            if self.count_m(self.temp_stemming(token, 'enci')) > 0:
                stemmed = self.rule_apply(token, 'enci', 'ence')

        elif self.temp_stemming(token, 'anci') != token :
            if self.count_m(self.temp_stemming(token, 'anci')) > 0:
                stemmed = self.rule_apply(token, 'anci', 'ance')

        elif self.temp_stemming(token, 'izer') != token: 
            if self.count_m(self.temp_stemming(token, 'izer')) > 0:
                stemmed = self.rule_apply(token, 'izer', 'ize')

        elif self.temp_stemming(token, 'abli') != token: 
            if self.count_m(self.temp_stemming(token, 'abli')) > 0:
                stemmed = self.rule_apply(token, 'abli', 'able')

        elif self.temp_stemming(token, 'alli') != token: 
            if self.count_m(self.temp_stemming(token, 'alli')) > 0:
                stemmed = self.rule_apply(token, 'alli', 'al')

        elif self.temp_stemming(token, 'entli') != token: 
            if self.count_m(self.temp_stemming(token, 'entli')) > 0:
                stemmed = self.rule_apply(token, 'entli', 'ent')

        elif self.temp_stemming(token, 'eli') != token: 
            if self.count_m(self.temp_stemming(token, 'eli')) > 0:
                stemmed = self.rule_apply(token, 'eli', 'e')

        elif self.temp_stemming(token, 'ousli') != token: 
            if self.count_m(self.temp_stemming(token, 'ousli')) > 0:
                stemmed = self.rule_apply(token, 'ousli', 'ous')

        elif self.temp_stemming(token, 'ization') != token: 
            if self.count_m(self.temp_stemming(token, 'ization')) > 0:
                stemmed = self.rule_apply(token, 'ization', 'ize')

        elif self.temp_stemming(token, 'ation') != token: 
            if self.count_m(self.temp_stemming(token, 'ation')) > 0:
                stemmed = self.rule_apply(token, 'ation', 'ate')

        elif self.temp_stemming(token, 'ator') != token:  
            if self.count_m(self.temp_stemming(token, 'ator')) > 0:
                stemmed = self.rule_apply(token, 'ator', 'ate')
        
        elif self.temp_stemming(token, 'alism') != token: 
            if self.count_m(self.temp_stemming(token, 'alism')) > 0:
                stemmed = self.rule_apply(token, 'alism', 'al')

        elif self.temp_stemming(token, 'iveness') != token: 
            if self.count_m(self.temp_stemming(token, 'iveness')) > 0:
                stemmed = self.rule_apply(token, 'iveness', 'ive')

        elif self.temp_stemming(token, 'fulness') != token: 
            if self.count_m(self.temp_stemming(token, 'fulness')) > 0:
                stemmed = self.rule_apply(token, 'fulness', 'ful')

        elif self.temp_stemming(token, 'ousness') != token: 
            if self.count_m(self.temp_stemming(token, 'ousness')) > 0:
                stemmed = self.rule_apply(token, 'ousness', 'ous')

        elif self.temp_stemming(token, 'aliti') != token: 
            if self.count_m(self.temp_stemming(token, 'aliti')) > 0:
                stemmed = self.rule_apply(token, 'aliti', 'al')

        elif self.temp_stemming(token, 'iviti') != token: 
            if self.count_m(self.temp_stemming(token, 'iviti')) > 0:
                stemmed = self.rule_apply(token, 'iviti', 'ive')

        elif self.temp_stemming(token, 'biliti') != token: 
            if self.count_m(self.temp_stemming(token, 'biliti')) > 0:
                stemmed = self.rule_apply(token, 'biliti', 'ble')

        return stemmed



    #step3

    def step_3(self, token):
        stemmed = token

        if self.temp_stemming(token, 'icate') != token: 
            if self.count_m(self.temp_stemming(token, 'icate')) > 0:
                stemmed = self.rule_apply(token, 'icate', 'ic')
        
        elif self.temp_stemming(token, 'ative') != token: 
            if self.count_m(self.temp_stemming(token, 'ative')) > 0:
                stemmed = self.rule_apply(token, 'ative', '')

        elif self.temp_stemming(token, 'alize') != token: 
            if self.count_m(self.temp_stemming(token, 'alize')) > 0:
                stemmed = self.rule_apply(token, 'alize', 'al')

        elif self.temp_stemming(token, 'iciti') != token: 
            if self.count_m(self.temp_stemming(token, 'iciti')) > 0:
                stemmed = self.rule_apply(token, 'iciti', 'ic')

        elif self.temp_stemming(token, 'ful') != token: 
            if self.count_m(self.temp_stemming(token, 'ful')) > 0:
                stemmed = self.rule_apply(token, 'ful', '')

        elif self.temp_stemming(token, 'ness') != token: 
            if self.count_m(self.temp_stemming(token, 'ness')) > 0:
                stemmed = self.rule_apply(token, 'ness', '')

        return stemmed


    #step4

    def step_4(self, token):
        stemmed = token

        if self.temp_stemming(token, 'al') != token: 
            if self.count_m(self.temp_stemming(token, 'al')) > 1:
                stemmed = self.rule_apply(token, 'al', '')
        
        elif self.temp_stemming(token, 'ance') != token: 
            if self.count_m(self.temp_stemming(token, 'ance')) > 1:
                stemmed = self.rule_apply(token, 'ance', '')

        elif self.temp_stemming(token, 'ence') != token: 
            if self.count_m(self.temp_stemming(token, 'ence')) > 1:
                stemmed = self.rule_apply(token, 'ence', '')

        elif self.temp_stemming(token, 'er') != token: 
            if self.count_m(self.temp_stemming(token, 'er')) > 1:
                stemmed = self.rule_apply(token, 'er', '')

        elif self.temp_stemming(token, 'ic') != token: 
            if self.count_m(self.temp_stemming(token, 'ic')) > 1:
                stemmed = self.rule_apply(token, 'ic', '')

        elif self.temp_stemming(token, 'able') != token: 
            if self.count_m(self.temp_stemming(token, 'able')) > 1:
                stemmed = self.rule_apply(token, 'able', '')

        elif self.temp_stemming(token, 'ible') != token: 
            if self.count_m(self.temp_stemming(token, 'ible')) > 1:
                stemmed = self.rule_apply(token, 'ible', '')

        elif self.temp_stemming(token, 'ant') != token: 
            if self.count_m(self.temp_stemming(token, 'ant')) > 1:
                stemmed = self.rule_apply(token, 'ant', '')

        elif self.temp_stemming(token, 'ement') != token: 
            if self.count_m(self.temp_stemming(token, 'ement')) > 1:
                stemmed = self.rule_apply(token, 'ement', '')

        elif self.temp_stemming(token, 'ment') != token:
            if self.count_m(self.temp_stemming(token, 'ment')) > 1:
                stemmed = self.rule_apply(token, 'ment', '')

        elif self.temp_stemming(token, 'ent') != token: 
            if self.count_m(self.temp_stemming(token, 'ent')) > 1:
                stemmed = self.rule_apply(token, 'ent', '')

        elif self.temp_stemming(token, 'ion') != token: 
            if token[-1] in ['s', 'S', 't', 'T'] and self.count_m(temp_stemming(token, 'ion')) > 1:
                stemmed = self.rule_apply(token, 'ion', '')

        elif self.temp_stemming(token, 'ou') != token: 
            if self.count_m(self.temp_stemming(token, 'ou')) > 1:
                stemmed = self.rule_apply(token, 'ou', '')

        elif self.temp_stemming(token, 'ism') != token: 
            if self.count_m(self.temp_stemming(token, 'ism')) > 1:
                stemmed = self.rule_apply(token, 'ism', '')

        elif self.temp_stemming(token, 'ate') != token: 
            if self.count_m(self.temp_stemming(token, 'ate')) > 1:
                stemmed = self.rule_apply(token, 'ate', '')

        elif self.temp_stemming(token, 'iti') != token: 
            if self.count_m(self.temp_stemming(token, 'iti')) > 1:
                stemmed = self.rule_apply(token, 'iti', '')

        elif self.temp_stemming(token, 'ous') != token: 
            if self.count_m(self.temp_stemming(token, 'ous')) > 1:
                stemmed = self.rule_apply(token, 'ous', '')

        elif self.temp_stemming(token, 'ive') != token: 
            if self.count_m(self.temp_stemming(token, 'ive')) > 1:
                stemmed = self.rule_apply(token, 'ive', '')

        elif self.temp_stemming(token, 'ize') != token: 
            if self.count_m(self.temp_stemming(token, 'ize')) > 1:
                stemmed = self.rule_apply(token, 'ize', '')

        return stemmed


    #step5

    def step_5(self, token):
        stemmed = token

        #step 5a
        if self.temp_stemming(token, 'e') != token :
            if self.count_m(self.temp_stemming(token, 'e')) > 1:
                stemmed = self.rule_apply(token, 'e', '')

        elif self.temp_stemming(token, 'e') != token:
            if self.count_m(self.temp_stemming(token, 'e')) == 1:
                temp_stem = self.temp_stemming(token, 'e')
                if len(temp_stem) >= 3 and temp_stem[-3] not in self.vowels and temp_stem[-2] in self.vowels and temp_stem[-1] not in self.vowels and temp_stem[-1] not in ['W', 'w', 'X', 'x', 'y', 'Y']:
                    stemmed = self.rule_apply(token, 'ize', '')

        #step 5b
        if self.count_m(token) > 1 and token[-1] in ['l', 'L'] and token[-1] == token[-2]:
            stemmed = token[:-1]

        return stemmed


    def stem(self, tokens):
        res_tokens = []
        for t in tokens:
            res = ''

            print(t, end = '->')
            res = self.step_1a(t)

            # print(res, end = '(step_1b)->')
            res = self.step_1b(res)

            # print(res, end = '(step_1c)->')
            res = self.step_1c(res)

            # print(res, end = '(step_2)->')
            res = self.step_2(res)

            # print(res, end = '(step_3)->')
            res = self.step_3(res)

            # print(res, end = '(step_4)->')
            res = self.step_4(res)

            # print(res, end = '(step_5)->')
            res = self.step_5(res)

            print(res)
            res_tokens.append(res)
        return res_tokens


with open('porter_test_data.txt', 'r', encoding = 'utf8') as f:
    data = f.read()
    tokens = data.split()

ps = porter_stemmer()
res_tokens = ps.stem(tokens)

res_data = []
for i, t in enumerate(tokens):
    res_data.append(tokens[i]+' -> '+res_tokens[i])

with open('porter_stemmed_test_data.txt', 'w', encoding = 'utf8') as f:
    f.write('\n'.join(res_data))
