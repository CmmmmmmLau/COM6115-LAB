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
from overrides.typing_utils import unknown

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

stemmer = PorterStemmer().stem
def stemWord(word):
    return stemmer(word)

def parse_line(line):
    tokens = line.strip().split()
    for token in tokens:
        word, tag = re.split(r'/(?=[^/]*$)', token)
        if word not in tokenDict:
            tokenDict[word] = {tag: 1}
        else:
            if tag not in tokenDict[word]:
                tokenDict[word][tag] = 0
            tokenDict[word][tag] += 1

        if tag not in tagDict:
            tagDict[tag] = 0
        tagDict[tag] += 1


if __name__ == '__main__':
    trainingData = opts["-d"]
    tokenDict = {}
    tokenNumber = 0
    tagDict = {}
    tagNumber = 0
    print(trainingData)
    with open(trainingData, "r", encoding = "utf-8") as dataFile:
        print(dataFile)
        for line in dataFile:
            parse_line(line)

    for tag in tagDict:
        tokenNumber = tokenNumber + tagDict[tag]
    tagNumber = len(tagDict)

    ambiguousToken = 0
    ambiguousWord = 0
    correctTokens = 0
    for token in tokenDict:
        if len(tokenDict[token]) > 1:
            ambiguousToken += 1
            ambiguousWord += sum(tokenDict[token].values())
        correctTokens += max(tokenDict[token].values())

    print('Proportion of word types that are ambiguous: %5.1f%% (%d / %d)' % \
          ((100.0 * ambiguousToken) / len(tokenDict), ambiguousToken, len(tokenDict)), file=sys.stderr)
    print('Proportion of tokens that are ambiguous in data: %5.1f%% (%d / %d)' % \
          ((100.0 * ambiguousWord) / tokenNumber, ambiguousWord, tokenNumber), file=sys.stderr)
    print('Accuracy of naive tagger on training data: %5.1f%% (%d / %d)' % \
          ((100.0 * correctTokens) / tokenNumber, correctTokens, tokenNumber), file=sys.stderr)


    tags = sorted(tagDict.items(), key = lambda kv: kv[1], reverse = True)
    print("Top ten tags by count:")

    for tag in tags[:10]:
        print('   %9s %6.2f%% (%5d / %d)' % \
              (tag[0], (100.0 * tag[1]) / tokenNumber, tag[1], tokenNumber), file=sys.stderr)

    if '-t' in opts:
        applyDict = {}
        for token in tokenDict:
            applyTag = max(tokenDict[token], key=tokenDict[token].get)
            applyDict[token] = applyTag

        testData = opts["-t"]

        allTest = 0
        correctTests = 0
        unknownToken = []
        with open(testData, "r", encoding="utf-8") as testFile:
            print(dataFile)
            for line in testFile:
                tokens = line.strip().split()
                for token in tokens:
                    word, tag = re.split(r'/(?=[^/]*$)', token)
                    if word not in tokenDict:
                        unknownToken.append(word)
                    else:
                        if applyDict[word] == tag:
                            correctTests += 1
                    allTest += 1
            print("Score on test data: %5.1f%% (%5d / %5d)" % \
                  ((100.0 * correctTests) / allTest, correctTests, allTest), file=sys.stderr)