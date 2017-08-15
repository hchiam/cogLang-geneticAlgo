from collections import OrderedDict
import time
import re

import geneticAlgo_just1

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

outputFilename = 'output.txt'

filename1 = 'data.txt'

localtime = time.asctime(time.localtime(time.time()))

#------------------------
# functions:
#------------------------

def createWord_GeneticAlgo(entry):
    # use geneticAlgo_just1.py
    return geneticAlgo_just1.createWord(str(entry))

#------------------------
# main part of the program:
#------------------------

# get lines of file into a list:
with open(filename1,'r') as f1:
    data = f1.readlines()

with open(outputFilename,'a') as f2:
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
        with open(outputFilename,'a') as f2:
            f2.write(newWord + ',' + originalWords['Eng'] + ',' + originalWords['Chi'] + ',' + originalWords['Spa'] + ',' + originalWords['Hin'] + ',' + originalWords['Ara'] + ',' + originalWords['Rus'] + ',\n')

    time.sleep(0.5) # give computer a quick rest to avoid overheating

with open(outputFilename,'a') as f2:
    f2.write('____________________\n')
