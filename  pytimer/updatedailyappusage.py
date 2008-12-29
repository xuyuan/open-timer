# update daily app usage

import re

def update(filename):
    p = re.compile('start')
    
    f = open(filename,'r')
    line = f.readline()
    while len(line) > 0:
        if p.match(line):
            print line,
        line = f.readline()

def main():
    update('data/2008/12/28.txt')
        

if __name__=="__main__":
    main()
