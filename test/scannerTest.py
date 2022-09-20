import sys

sys.path.append('..')

from scanner import scanner

def runTests():

    print("Running Test #1")
    input1 = 'print "Hello World" 2 + 2 = 4'
    output1 = scanner(input1).scanTokens()
    output1 = buildOutput(output1)
    print("Input:", input1)
    print("Output:", output1)

def buildOutput(output):
    res = []
    for token in output:
        res.append(f'{token}')
    return res
    
runTests()