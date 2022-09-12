import string

def scanner(fileName):
    #open a file for reading, for now we will just do an example.lox file
    inputFile = open(fileName, 'r')

    rawText = inputFile.read()
    print(rawText)