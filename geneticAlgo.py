from collections import OrderedDict
import time
import re
import os

import geneticAlgo_just1_v2 as geneticAlgo_just1 # use version 2, but make the code here look the same
import sortByEng

#------------------------
# shared variables:
#------------------------

words = OrderedDict()
words['Eng'] = ''
words['Chi'] = ''
words['Spa'] = ''
words['Hin'] = ''
words['Ara'] = ''
words['Rus'] = ''

localtime = time.asctime(time.localtime(time.time()))

inputFileName = 'data.txt'

# get best scorers so far into a dictionary, in case we need to update it
scorersFileName = 'best-scorers.txt'
scorers = {}

outputFileName = 'output.txt'

#------------------------
# functions:
#------------------------

def createWord_GeneticAlgo(entry):
    global scorers, scorersFileName
    [bestSoFar_word, scorers] = geneticAlgo_just1.createWord( entry, scorers, scorersFileName )
    return bestSoFar_word

#------------------------
# main part of the program:
#------------------------

# get lines of file into a list:
with open(inputFileName,'r') as f1:
    data = f1.readlines()

# get the so far best scorers into a dictionary, in case we need to update it:
with open(scorersFileName,'r') as f:
    for line in f:
        if line != '\n': # ignore empty lines (some editors automatically add them)
            keyEng = str(line.replace('\n','').split(',')[2])
            scorers[keyEng] = line

# mark out beginning of new run in output file:
with open(outputFileName,'a') as f2:
    f2.write('____________________\n')
    f2.write(localtime + '\n')

# fill arrays:
for line in data:
    words['Eng'] = line.split(',')[1]
    words['Chi'] = line.split(',')[2]
    words['Spa'] = line.split(',')[3]
    words['Hin'] = line.split(',')[4]
    words['Ara'] = line.split(',')[5]
    words['Rus'] = line.split(',')[6]
    originalWords = words.copy()
    originalWords_Alt = words.copy()

    if words['Eng'] != 'Eng':
        newWord = createWord_GeneticAlgo(line) # here is the major function call!
        with open(outputFileName,'a') as f2:
            f2.write(newWord + ',' + originalWords['Eng'] + ',' + originalWords['Chi'] + ',' + originalWords['Spa'] + ',' + originalWords['Hin'] + ',' + originalWords['Ara'] + ',' + originalWords['Rus'] + ',\n')

    time.sleep(0.5) # give computer a quick rest to avoid overheating

# update file to track best scorers:
with open(scorersFileName,'w') as f:
    for key in scorers:
        scorer = scorers[key]
        if scorer != '':
            f.write(str(scorer).replace('\n','')+'\n')
    f.close()

# mark out end of new run in output file:
with open(outputFileName,'a') as f2:
    f2.write('____________________\n')

# sort file:
sortByEng.main(scorersFileName)
