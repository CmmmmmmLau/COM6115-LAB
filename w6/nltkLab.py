import nltk, re


if __name__ == "__main__":
    wordRe = re.compile(r'\w+')#
    tokenList = []
    with open("mobydick.txt") as dataFile:
        for line in dataFile:
            for token in line.split():
                tokenList.append(token)

    fd = nltk.FreqDist(tokenList)
    fd.plot(20, show=True)