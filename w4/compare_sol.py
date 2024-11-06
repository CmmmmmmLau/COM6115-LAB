"""\
------------------------------------------------------------
USE: python  (options) file1...fileN
OPTIONS:
    -h : print this help message
    -s FILE : use stoplist file FILE
    -p : use Porter stemming (default: no stemming)
    -b : use BINARY weights (default: count weighting)
------------------------------------------------------------\
"""

import sys, re, getopt
import glob
from nltk.stem import PorterStemmer

opts, args = getopt.getopt(sys.argv[1:], 'hs:pbI:')
opts = dict(opts)

##############################
# HELP option

if '-h' in opts:
    progname = sys.argv[0]
    progname = progname.split('/')[-1]  # strip out extended path
    help = __doc__.replace('', progname, 1)
    print(help, file=sys.stderr)
    sys.exit()

##############################
# Identify input files, when "-I" option used

if '-I' in opts:
    filenames = glob.glob(opts['-I'])
else:
    filenames = args

# Check if filenames are being found 
# (comment out after checking)
print('INPUT-FILES:', filenames, file=sys.stderr)

##############################
# STOPLIST option

stops = set()
if '-s' in opts:
    with open(opts['-s'], 'r') as stop_fs:
        for line in stop_fs:
            stops.add(line.strip())

##############################
# Stemming function

stemmer = PorterStemmer().stem


def stem_word(word):
    return stemmer(word)


##############################
# COUNT-WORDS function. 
# Takes 2 inputs: 1= FILE-NAME, 2= stoplist
# Returns a dictionary of word counts

def count_words(filename, stops):
    wordRE = re.compile('[A-Za-z]+')
    counts = {}
    with open(filename, 'r') as infile:
        for line in infile:
            for word in wordRE.findall(line.lower()):
                if word not in stops:
                    if '-p' in opts:
                        word = stem_word(word)
                    if word in counts:
                        counts[word] += 1
                    else:
                        counts[word] = 1
    return counts


##############################
# Compute counts for individual documents

docs = []

for infile in filenames:
    docs.append(count_words(infile, stops))


##############################
# Compute similarity score for document pair

def jaccard(doc1, doc2):
    wds1 = set(doc1)
    wds2 = set(doc2)
    if '-b' in opts:
        over = len(wds1 & wds2)  # where '&' is set intersection op
        under = len(wds1 | wds2)  # where '|' is set union op
    else:
        over = under = 0
        for wd in (wds1 | wds2):

            if wd in doc1 and wd in doc2:
                over += min(doc1[wd], doc2[wd])

            wmax = 0
            if wd in doc1:
                wmax = doc1[wd]
            if wd in doc2:
                wmax = max(doc2[wd], wmax)
            under += wmax

    if under > 0:
        return over / under
    else:
        return 0.0


##############################
# Compute scores for all document pairs

results = {}
for i in range(len(docs) - 1):
    for j in range(i + 1, len(docs)):
        pair_name = '%s <> %s' % (filenames[i], filenames[j])
        results[pair_name] = jaccard(docs[i], docs[j])

##############################
# Sort, and print top N results

top_N = 20
pairs = sorted(results, key=lambda v: results[v], reverse=True)
if top_N > 0:
    pairs = pairs[:top_N]
c = 0
for pair in pairs:
    c += 1
    print('[%d] %s = %.3f' % (c, pair, results[pair]), file=sys.stdout)

##############################
