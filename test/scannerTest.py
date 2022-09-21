import sys

sys.path.append('..')

from scanner import scanner

def test():

    inputs = (
        #Test 1
        'print "Hello World";',
        #Test 2
        'var language = "lox";',
        #Test 3
        'var x = 0.2431 + 4.1353;',
        #Test 4
        'if(2+2!=4) {       \
            var i = 4;      \
        else {              \
            var i = 5;      \
        }',
        #Test 5
        'while(x == 5){             \
            z = x + 1;              \
            var test = "Hello Lox"; \
            x= x + 1;               \
        '
    )

    outputs = (
        #Test 1 expected output
        [
            'Identifier: tokenTypes.PRINT Lexeme: print Literal Value: None',
            'Identifier: tokenTypes.STRING Lexeme: "Hello World" Literal Value: Hello World',
            'Identifier: tokenTypes.SEMICOLON Lexeme: ; Literal Value: None',
            'Identifier: tokenTypes.EOF Lexeme:  Literal Value: None'
        ],
        #Test 2 expected output
        [
            'Identifier: tokenTypes.VAR Lexeme: var Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: language Literal Value: None',
            'Identifier: tokenTypes.EQUAL Lexeme: = Literal Value: None',
            'Identifier: tokenTypes.STRING Lexeme: "lox" Literal Value: lox',
            'Identifier: tokenTypes.SEMICOLON Lexeme: ; Literal Value: None',
            'Identifier: tokenTypes.EOF Lexeme:  Literal Value: None'
        ],
        #Test 3 expected output
        [
            'Identifier: tokenTypes.VAR Lexeme: var Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: x Literal Value: None',
            'Identifier: tokenTypes.EQUAL Lexeme: = Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 0.2431 Literal Value: 0.2431',
            'Identifier: tokenTypes.PLUS Lexeme: + Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 4.1353 Literal Value: 4.1353',
            'Identifier: tokenTypes.SEMICOLON Lexeme: ; Literal Value: None',
            'Identifier: tokenTypes.EOF Lexeme:  Literal Value: None'
        ],
        #Test 4 expected output
        [
            'Identifier: tokenTypes.IF Lexeme: if Literal Value: None',
            'Identifier: tokenTypes.LEFT_PAREN Lexeme: ( Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 2 Literal Value: 2.0',
            'Identifier: tokenTypes.PLUS Lexeme: + Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 2 Literal Value: 2.0',
            'Identifier: tokenTypes.BANG_EQUAL Lexeme: != Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 4 Literal Value: 4.0',
            'Identifier: tokenTypes.RIGHT_PAREN Lexeme: ) Literal Value: None',
            'Identifier: tokenTypes.LEFT_BRACE Lexeme: { Literal Value: None',
            'Identifier: tokenTypes.VAR Lexeme: var Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: i Literal Value: None',
            'Identifier: tokenTypes.EQUAL Lexeme: = Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 4 Literal Value: 4.0',
            'Identifier: tokenTypes.SEMICOLON Lexeme: ; Literal Value: None',
            'Identifier: tokenTypes.ELSE Lexeme: else Literal Value: None',
            'Identifier: tokenTypes.LEFT_BRACE Lexeme: { Literal Value: None',
            'Identifier: tokenTypes.VAR Lexeme: var Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: i Literal Value: None',
            'Identifier: tokenTypes.EQUAL Lexeme: = Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 5 Literal Value: 5.0',
            'Identifier: tokenTypes.SEMICOLON Lexeme: ; Literal Value: None',
            'Identifier: tokenTypes.RIGHT_BRACE Lexeme: } Literal Value: None',
            'Identifier: tokenTypes.EOF Lexeme:  Literal Value: None'
        ],
        #Test 5 expected output
        [
            'Identifier: tokenTypes.WHILE Lexeme: while Literal Value: None',
            'Identifier: tokenTypes.LEFT_PAREN Lexeme: ( Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: x Literal Value: None',
            'Identifier: tokenTypes.EQUAL_EQUAL Lexeme: == Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 5 Literal Value: 5.0',
            'Identifier: tokenTypes.RIGHT_PAREN Lexeme: ) Literal Value: None',
            'Identifier: tokenTypes.LEFT_BRACE Lexeme: { Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: z Literal Value: None',
            'Identifier: tokenTypes.EQUAL Lexeme: = Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: x Literal Value: None',
            'Identifier: tokenTypes.PLUS Lexeme: + Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 1 Literal Value: 1.0',
            'Identifier: tokenTypes.SEMICOLON Lexeme: ; Literal Value: None',
            'Identifier: tokenTypes.VAR Lexeme: var Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: test Literal Value: None',
            'Identifier: tokenTypes.EQUAL Lexeme: = Literal Value: None',
            'Identifier: tokenTypes.STRING Lexeme: "Hello Lox" Literal Value: Hello Lox',
            'Identifier: tokenTypes.SEMICOLON Lexeme: ; Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: x Literal Value: None',
            'Identifier: tokenTypes.EQUAL Lexeme: = Literal Value: None',
            'Identifier: tokenTypes.IDENTIFIER Lexeme: x Literal Value: None',
            'Identifier: tokenTypes.PLUS Lexeme: + Literal Value: None',
            'Identifier: tokenTypes.NUMBER Lexeme: 1 Literal Value: 1.0',
            'Identifier: tokenTypes.SEMICOLON Lexeme: ; Literal Value: None',
            'Identifier: tokenTypes.EOF Lexeme:  Literal Value: None'
        ]
    )

    runTests(inputs, outputs)

def runTests(inputs, outputs):
    for i, testString in enumerate(inputs):
        print(f"Running Test #{i+1}")
        result = scanner(testString).scanTokens()
        print(f"Test #{i+1} passed: {verifyResult(result, outputs[i])}")
    for i, testString in enumerate(inputs):
        print()
        print(f"Test #{i+1} input:")
        print(testString)
        print(f"Test #{i+1} full output:")
        result = scanner(testString).scanTokens()
        printResult(result)

def printResult(arr):
    for item in arr:
        print(item)

def verifyResult(inputArr, outputArr):
    for i,item in enumerate(inputArr):
        if(str(item) != outputArr[i]):
            print(f'FAILURE CONDITION: {str(item)} does not equal {outputArr[i]}')
            return False
    return True

test()