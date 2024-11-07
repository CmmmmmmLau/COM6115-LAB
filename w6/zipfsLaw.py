import math
import re
import sys

import pylab as lab
from sympy.codegen.cfunctions import log10


def Tokenization(fileName):
    _wordRe = re.compile(r'\w+')
    _tokenDict = {}
    _wordTotal = 0

    with open(fileName, 'r', encoding="utf-8") as dataFile:
        for line in dataFile:
            for _token in _wordRe.findall(line.lower()):
                if _token not in _tokenDict:
                    _tokenDict[_token] = 0
                _tokenDict[_token] += 1
                _wordTotal += 1


    return sorted(_tokenDict.items(), key=lambda kv:(kv[1], kv[0]), reverse=True), _wordTotal

def WordFreqnency(targetDict, word):
    _tokenDict = dict(targetDict)
    return int(_tokenDict[word])

if __name__ == "__main__":
    tokenDict, wordTotal = Tokenization("mobydick.txt")
    print("The top 20 frequency word:")
    for token in tokenDict[:20]:
        print('   %9s %6.2f%% (%5d / %d)' % \
              (token[0], (100.0 * token[1]) / wordTotal, token[1], wordTotal), file=sys.stderr)
    wd = "distinct"
    wdF = WordFreqnency(tokenDict, wd)
    print("The frequency of word <%s> is : %d / %d" % (wd, wdF, wordTotal))

    x = []
    y = []
    for token in tokenDict[:40]:
        x.append(token[0])
        y.append(token[1])

    cumlativeX = list(range(40))
    cumlativeY = []
    acc = 0
    for token in tokenDict[:40]:
        acc += token[1]
        cumlativeY.append(acc)

    lab.subplot(2,2,1)
    lab.plot(x, y)
    lab.subplot(2,2,2)
    lab.plot(cumlativeX, cumlativeY)


    logX = []
    logY = []
    for i in range(len(cumlativeX)):
        logX.append(math.log(i+1,10))
        logY.append(math.log(y[i], 10))
    lab.subplot(2, 2, 3)
    lab.plot(logX, logY)
    lab.show()