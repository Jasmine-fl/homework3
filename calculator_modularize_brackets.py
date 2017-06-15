
# coding: UTF-8

def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index



def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readMultiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def readBracket_Left(line, index):
    token = {'type': '('}
    return token, index + 1

def readBracket_Right(line, index):
    token = {'type': ')'}
    return token, index + 1




def tokenize(line): #tokenize
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit(): #readNumber
            (token, index) = readNumber(line, index)
        elif line[index] == '+': #readPlus
            (token, index) = readPlus(line, index)
        elif line[index] == '-': #readMinus
            (token, index) = readMinus(line, index)
        elif line[index] == '*': #readMultiply
            (token, index) = readMultiply(line, index)
        elif line[index] == '/': #readDivide
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readBracket_Left(line, index)
        elif line[index] == ')':
            (token, index) = readBracket_Right(line, index)
        else: #エラー
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_multiply_divide(tokens):  #1.calculate "x", "÷"
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER': #if number
            if tokens[index - 1]['type'] == 'MULTIPLY': #× before number(ex:4×2 → 8)
                tokens[index]['number'] *= tokens[index - 2]['number']
                del tokens[index - 1]
                del tokens[index - 2]
                index -= 2
            if tokens[index - 1]['type'] == 'DIVIDE': #÷ before number(ex:4÷2 → 2)
                tokens[index - 2]['number'] /= tokens[index]['number']*1.0
                del tokens[index]
                del tokens[index - 1]
                index -= 2
            # else:
            #     print 'Invalid syntax'
        index += 1
    return tokens


def evaluate_plus_minus(tokens): #2.calculate "+", "-"
    final_answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER': #if number
            if tokens[index - 1]['type'] == 'PLUS': #+ before number
                final_answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS': #- before number
                final_answer -= tokens[index]['number']
            # else:
            #     print 'Invalid syntax'
        index += 1
    return final_answer

def evaluate(tokens): #1,2 calculate "+","-","×","÷" をまとめた
    tokens = evaluate_multiply_divide(tokens)  #1.calculate "x", "÷"
    answer = evaluate_plus_minus(tokens)   #2.calculate "+", "-"
    return answer


def find_tokens_inside_bracket(tokens): #1番内側の()内にあるtokensを取り出す
    index = 0
    bracket_left_index = 0
    bracket_right_index = 0
    while index < len(tokens):
        if tokens[index]['type'] == '(': #(の位置
            bracket_left_index = index
        elif tokens[index]['type'] == ')': #)の位置
            bracket_right_index = index
            break
        index += 1
    tokens_inside_bracket = tokens[bracket_left_index + 1:bracket_right_index] #()の中身
    return [tokens_inside_bracket, bracket_left_index, bracket_right_index]

def test(line, expectedAnswer):  #test
    tokens = tokenize(line)
    while(1):
        list_tokensInsideBracket = find_tokens_inside_bracket(tokens) #[()の中身, (の位置, )の位置]
        tokens_inside_bracket = list_tokensInsideBracket[0]
        bracket_left_index = list_tokensInsideBracket[1]
        bracket_right_index = list_tokensInsideBracket[2]
        if bracket_right_index == 0:
            # ()がないのでbreak
            break
        else:
            tokens[bracket_left_index]['type'] = 'NUMBER' #()内を計算した結果を'('の位置に代入
            tokens[bracket_left_index]['number'] = evaluate(tokens_inside_bracket)
            for i in range(bracket_left_index + 1, bracket_right_index + 1): #()内の計算後にいらないtokenを削除
                del tokens[bracket_left_index + 1]
    actualAnswer = evaluate(tokens)  #かっこがなくなったら普通に計算
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    print "整数のみ"
    test("1",1) #整数
    test("1+2", 3)
    test("-1+2-3", -2)
    test("2*3*4", 24)
    test("2*3*4+2", 26)
    test("-3-2*3*4", -27)
    test("-3/4",-0.75)
    test("3/4/5", 0.15)
    test("3/4*6",4.5)
    test("3/4*6*2/3",3.0)
    print "小数含む"
    test("2.0",2.0) #小数点
    test("1.0+2.1-3", 0.1)
    test("3.0+4*2-1/5",10.8)
    test("4*2.0*1.5", 12.0)
    test("-2.0+4*2.0*2.0",14.0)
    test("2/4/2",0.25)
    test("-1-2/4/2", -1.25)
    test("3.0/4*6*2/3*4.2",12.6)
    print "==== Test finished! ====\n"
    print "()含む"
    test("3+(1+2)", 6)
    test("3*(2+1)", 9)
    test("3.0/(2+1)", 1.0)
    test("(-3+2)/5/2", -0.1)
    test("(3.0+4*(2-1))/5", 1.4)
    test("(2-(3*1.0))/5+1", 0.8)
    test("((2/4)-(3/10+0.1))/(2*3+2)", 0.0125)


runTest()


#mainの処理
while True:
    print '> ',
    line = raw_input() #read line
    tokens = tokenize(line)  #tokenize
    print "first_tokenized_tokens ="
    print tokens
    #最も内側の()の中身を計算 をかっこがなくなるまで繰り返す
    while(1):
        list_tokensInsideBracket = find_tokens_inside_bracket(tokens) #[()の中身, (の位置, )の位置]
        print "[tokens_inside_bracket, bracket_left_index, bracket_right_index] = "
        print list_tokensInsideBracket #debug後に削除
        tokens_inside_bracket = list_tokensInsideBracket[0]
        bracket_left_index = list_tokensInsideBracket[1]
        bracket_right_index = list_tokensInsideBracket[2]
        if bracket_right_index == 0:
            # print "bracketがないのでbreak"
            break
        else:
            tokens[bracket_left_index]['type'] = 'NUMBER' #かっこ内を計算した結果を'('の位置に代入
            tokens[bracket_left_index]['number'] = evaluate(tokens_inside_bracket)
            print "()内の計算結果 = "
            print tokens[bracket_left_index]['number']
            for i in range(bracket_left_index + 1, bracket_right_index + 1): #かっこ内の計算後にいらないtokenを削除
                del tokens[bracket_left_index + 1]
            # print  "()内を計算した後のtokens = "
            # print tokens
    answer = evaluate(tokens)  #かっこがなくなったら普通に計算
    print "answer = %f\n" % answer
