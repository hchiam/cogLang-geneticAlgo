import sys # so you can get terminal argument using print sys.argv[1]
import collections # so you can do dictionary manipulations

scorers = {}

def readScorers(scorersFilename):
    with open(scorersFilename,'r') as f:
        for entry in f:
            keyEng = entry.replace('\n','').split(',')[2]
            scorers[keyEng] = entry

def sortByEng():
    global scorers
    scorers = collections.OrderedDict(sorted(scorers.items()))

def writeScorers(scorersFilename):
    with open(scorersFilename,'w') as f:
        for key in scorers:
            scorer = scorers[key]
            f.write(scorer)

def main(scorersFilename):
    readScorers(scorersFilename)
    sortByEng()
    writeScorers(scorersFilename)

if __name__ == '__main__':
    scorersFilename = sys.argv[1] # so in terminal: python sortByEng.py best-scorers.txt
    main(scorersFilename)
