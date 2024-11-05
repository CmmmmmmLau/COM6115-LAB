"""
USE: python <PROGNAME> (options) WORDLIST-FILE INPUT-FILE OUTPUT-FILE
OPTIONS:
    -h : print this help message and exit
"""
################################################################

import sys
import binascii

################################################################

MAXWORDLEN = 4

################################################################
# Command line options handling, and help

def print_help():
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    sys.exit(0)
    
#if '-h' in sys.argv or len(sys.argv) != 4:
#    print_help()

#word_list_file = sys.argv[1]
#input_file = sys.argv[2]
#output_file = sys.argv[3]
word_list_file = "chinesetrad_wordlist.utf8"
input_file = "chinesetext.utf8"
output_file = "MYRESULTS.utf8"

################################################################

# PARTS TO COMPLETE: 

################################################################
# READ CHINESE WORD LIST
# Read words from Chinese word list file, and store in 
# a suitable data structure (e.g. a set)
word_set = set()
def read_the_word_list():
    with open(word_list_file, "r", encoding = "utf-8") as file:
        for line in file:
            word_set.add(line.rstrip('\n'))
        


################################################################
# FUNCTION TO PROCESS ONE SENTENCE
# Sentence provided as a string. Result returned as a list of strings 

def segment(sent, wordset):
    word = ""
    while sent:
        max_length = min(len(sent), MAXWORDLEN)
        for nums in range(max_length, 0, -1):
            content = sent[:nums]
            if nums == 1 or content in wordset:
                word += content + " "
                sent = sent[nums:]
                break
    
    print("Return result: " + word)
    return word


################################################################
# MAIN LOOP
# Read each line from input file, segment, and print to output file
read_the_word_list()
with open(output_file, "w", encoding = "utf-8") as output:
    with open(input_file, "r", encoding = "utf-8") as file:
        for line in file:
            newLine = segment(line, word_set)
            output.write(newLine)


################################################################
