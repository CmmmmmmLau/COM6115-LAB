"""
USE: python <PROGNAME> (options) 
OPTIONS:
    -h : print this help message and exit
    -d FILE : use FILE as data to create a new lexicon file
    -t FILE : apply lexicon to test data in FILE
"""
################################################################

import sys, re, getopt

from nltk.stem import PorterStemmer

################################################################
# Command line options handling, and help

opts, args = getopt.getopt(sys.argv[1:], 'hd:t:')
opts = dict(opts)

def printHelp():
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    sys.exit()
    
if '-h' in opts:
    printHelp()

if '-d' not in opts:
    print("\n** ERROR: must specify training data file (opt: -d FILE) **", file=sys.stderr)
    printHelp()

if len(args) > 0:
    print("\n** ERROR: no arg files - only options! **", file=sys.stderr)
    printHelp()

################################################################

def parse_line(line):
    token = line.split(" ")
    word, tag = re.split(r'/(?=[^/]*$)', token)



if __name__ == '__main':
    trainingData = opts["-d"]
    termDict = {}
    print(trainingData)
    with open(trainingData, "r", encoding = "utf-8") as dataFile:
        print(dataFile)
        for line in dataFile:
            parse_line(line)


'''
if __name__ == '__main__':
    trainingData = opts["-d"]
    termDict = {}
    print(trainingData)
    with open(trainingData, "r", encoding = "utf-8") as dataFile:
        print(dataFile)
        for line in dataFile:
            splitList = line.split(" ")
            
            for token in splitList:
                word, tag = re.split(r'/(?=[^/]*$)', token)
                word = stemmingWord(word)

                if word not in termDict:
                    termDict[word] = dict.fromkeys([tag], 1)
                else:
                    
                    if tag not in termDict[word]:
                        termDict[word] = dict.fromkeys([tag], 1)
                    else:
                        tagDict = termDict[word]
                        tagDict[tag] += 1
'''