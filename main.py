#main.py
#this will be the program that is called to start the process of py
#USAGE: python3 main.py (optional filename)
#with no fileName, this will act as a bash script
#with fileName, this will act as an interpreter for the passed .lox file

import sys
import scanner 

if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")

    argv = sys.argv
    argc = len(argv)

    if argc == 1:
        #cli() work in progress
        print('Not complete yet')
    elif argc == 2:
        scanner.scanner(argv[1])
    else:
        print('Error, incorrect number of arguements')