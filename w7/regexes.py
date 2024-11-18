
# COM6115: Text Processing
# Regular Expressions Lab Class

import sys, re

#------------------------------

testRE = re.compile('(logic|sicstus)', re.I)

part1RE = re.compile('<.*>')

#------------------------------

with open('RGX_DATA.html') as infs: 
    linenum = 0
    for line in infs:
        linenum += 1
        if line.strip() == '':
            continue
        print('  ', '-' * 100, '[%d]' % linenum, '\n   TEXT:', line, end='')

        mm = testRE.finditer(line)
        for m in mm:
            print('** TEST-RE(Finder):', m.group(1))
        print('** Tag:', part1RE.findall(line))