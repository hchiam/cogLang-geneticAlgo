from random import randint, sample
from operator import itemgetter
import ast # to convert string of list to actual list
import collections
import re

#------------------------
# shared variables:
#------------------------

outputFilename = 'output.txt'

allophones = {
    'aeiou' : 'a',
    'bp' : 'b',
    'cjsz' : 'z',
    'dt' : 'd',
    'fv' : 'v',
    'gkq' : 'g',
    'hx' : 'h',
    'lr' : 'l',
    'mn' : 'm',
    'w' : 'w',
    'y' : 'y'
}

possibleInstructions = [0,1,2,3,4,'+','+','x'] # make '+' more likely (heuristically seems good)

popSize = 10
numGenerations = 1000
epochMilestone = numGenerations//10
population = []
scoreHistory = []
scoreHistory2 = []
wordHistory = []

debugOn = False

count = 0
countNew = 0
scoreImprovements = 0

creatingFromScratch = True

if debugOn:
    import matplotlib.pyplot as plt

#------------------------
# functions:
#------------------------


def getFirstSyllable(string):
    syll = re.search(r'[^aeiou]+[aeiou][^aeiou]?',string)
    if syll:
        return syll.group() # CV, CVC, CCVC, ...
    return string # in case word only has vowels (V or VV...)


def respellWithAllophones(word):
    for char in word:
        for allo in allophones:
            if char in allo:
                word = word.replace(char,allophones[allo])
    return word


def encourage_LettersFromEachSource(word,originalWords):
    score = 0
    lettersAlreadyUsed = []
    for letter in word:
        # avoid using the same letter again anywhere in the same word:
        if letter not in lettersAlreadyUsed:
            lettersAlreadyUsed.append(letter)
            # encourage using words with letters found in all source words:
            for srcWord in originalWords:
                score += 1 if letter in srcWord else 0
    return score


def encourage_UsesFirstSyllablesAllophones(word, originalWords):
    score = 0
    word_allo = respellWithAllophones(word)
    srcSyllables_allo = [respellWithAllophones(getFirstSyllable(srcWord)) for srcWord in originalWords if srcWord!=None]
    for syllable in srcSyllables_allo:
        if syllable in word_allo:
            score += len(syllable)
    return score


def encourage_First3LetterAllosInOrderAndWithin1Space(word, originalWords):
    score = 0
    newWord = respellWithAllophones(word)

    first3letterAllos = [respellWithAllophones(srcWord[:3]) for srcWord in originalWords]

    # test each 3-letter initial (allophone) letters
    for test in first3letterAllos:
        # set up regex based on number of letters available in test
        # (account for source words shorter than 3 letters)
        if len(test) == 3:
            regex = test[0] + r'(\w?)' + test[1] + r'(\w?)' + test[2]
        elif len(test) == 2:
            regex = test[0] + r'(\w?)' + test[1]
        elif len(test) == 1:
            regex = test[0]
        else:
            break # 0 characters, word translation does not exist in that source language

        matches = re.search(regex,newWord)
        if matches:

            # score up by number of letters allo word
            # (account for source words shorter than 3 letters)
            score += len(test) # print(word,test,score)

            # score down by number of interspersed letters between
            # (account for source words shorter than 3 letters)
            try:
                score -= len(matches.group(1))
                try:
                    score -= len(matches.group(2))
                except Exception as e:
                    pass
            except Exception as e:
                pass

    return score


def penalize_ConsonantClusters(word):
    score = 0
    consonantClusterLength = 0
    for letter in word:
        if letter not in 'aeiou':
            consonantClusterLength += 1
        else:
            if consonantClusterLength > 2: # CC is ok (esp. from src words and may favour shorter words)
                score -= consonantClusterLength
            consonantClusterLength = 0
    # in case the word ends with a consonant:
    score -= consonantClusterLength
    return score


def penalize_Length(word):
    return -len(word)


def evaluate(line):
    newWord = line.split(',')[0]
    originalWords = line.split(',')[2:]
    score = 0
    # encourage using letters from ALL src words, but avoid repeating letters like in "mmmmmmommmmmmm":
    score += encourage_LettersFromEachSource(newWord, originalWords)
    score += encourage_UsesFirstSyllablesAllophones(newWord, originalWords)
    score += encourage_First3LetterAllosInOrderAndWithin1Space(newWord, originalWords)
    # avoid consonant clusters like in "htkyowaz" or "kdyspgunwa"
    score += penalize_ConsonantClusters(newWord)
    score += penalize_Length(newWord)
    return score


def getSourceWords(data):
    return data.split(',')[2:][:-1]


def random_insert_seq(lst, seq): # O(n+m)
    # https://stackoverflow.com/questions/2475518/python-how-to-append-elements-to-a-list-randomly
    insert_locations = sample(xrange(len(lst) + len(seq)), len(seq))
    inserts = dict(zip(insert_locations, seq))
    input = iter(lst)
    lst[:] = [inserts[pos] if pos in inserts else next(input)
        for pos in xrange(len(lst) + len(seq))]


def trackSourceLanguagesUsed(instruction, sourcesUsed):
    # tracking source language used: 0b11111 if used all
    langID = 0b00000
    if instruction == 0:
        return 0b10000 # 10000
    elif instruction == 1:
        return 0b01000 # 01000
    elif instruction == 2:
        return 0b00100 # 00100
    elif instruction == 3:
        return 0b00010 # 00010
    elif instruction == 4:
        return 0b00001 # 00001
    # finally, combine:
    return langID | sourcesUsed


def generateNewIndividual():
    outputInstructions = []
    sourcesUsed = 0b00000 # tracks source languages used: 0b11111 if used all
    # possibleInstructions = [0,1,2,3,4,'+','+','x'] # make '+' more likely (heuristically seems good)
    for i in range(25):
        index = randint(0,len(possibleInstructions)-1)
        instruction = possibleInstructions[index]
        if instruction == 'x':
            if outputInstructions != '':
                break
        else:
            outputInstructions.append(instruction)
        sourcesUsed = trackSourceLanguagesUsed(instruction, sourcesUsed)
    # insert other source languages if missing
    if sourcesUsed != 0b11111:
        random_insert_seq(outputInstructions,[0,1,2,3,4])
    return outputInstructions


def justTwoInitSylls_CVC(word):
    beforeThisIndex = 0
    afterThisIndex = 0
    for vowel1 in word:
        if vowel1 in 'aeiou':
            afterThisIndex = word.index(vowel1)
            break
    for vowel2 in word[afterThisIndex+1:]:
        if vowel2 in 'aeiou':
            beforeThisIndex = word[afterThisIndex+1:].index(vowel2)+1 + afterThisIndex+1
            # if second syllable has two vowels, then ignore that final vowel to preserve two vowels/syllables per word
            if beforeThisIndex < len(word) and word[beforeThisIndex] in 'aeiou':
                beforeThisIndex -= 1
            break
    if beforeThisIndex!=0:
        word = word[:beforeThisIndex+1]
    return word


def constructWord(sourceWords, instructions):
    newWord = []
    i = 0
    lang = 0
    wordIndices = [0] * len(sourceWords)
    for instruction in instructions:
        if instruction == 'x':
            break
        elif instruction == '+':
            # make '+' per language, so don't lose out on initial letters in different words
            wordIndices[lang] += 1
        else: # instruction = lang 0,1,2,3,4
            lang = instruction
            sourceWord = justTwoInitSylls_CVC(sourceWords[lang]) # only use letters from first 2 "syllables"
            i = wordIndices[lang]
            if i < len(sourceWord):
                newWord.append(sourceWord[i])
    newWord = ''.join(newWord)
    return newWord


def sortByScore(population):
    population.sort(key=itemgetter(0), reverse=True)


def getBestAlgo():
    # assumes first one is best
    bestSoFar = population[0]
    return bestSoFar


def printOnSepLines(arr):
    if debugOn:
        for line in arr:
            print(line)


def updateScoreHistory():
    # assumes first one is best
    currentBestScore = population[0][0]
    secondBestScore = population[2][0]
    scoreHistory.append(currentBestScore)
    scoreHistory2.append(secondBestScore)


def updateWordHistory():
    wordHistory.append(population[0][1].split(',',1)[0])


def getEntryIdentifier(entry):
    return str(entry).split(',')[2]
    # parts = str(entry).split(', ')
    # sourceWordsListStr = parts[1]
    # justSrcWords = sourceWordsListStr.split(',',1)[1]
    # removedFinalApostrophe = justSrcWords[:-1]
    # identifier = removedFinalApostrophe
    # return identifier


def getEntryScore(entry):
    return int(str(entry).split(', ',1)[0][1:]) # [1:] to remove initial '['


def printDebug(*args):
    if debugOn:
        print(' '.join([str(arg) for arg in args]))

#------------------------
# main part of the program:
#------------------------

def createWord(inputLineEntry, scorers, scorersFile):
    global population
    global scoreHistory
    global scoreHistory2
    global wordHistory
    global count
    global countNew
    global scoreImprovements
    global creatingFromScratch

    printDebug('\n...Running...')
    count += 1
    print(count)

    # data = '+,long,tcan,largo,lamba,towil,dlini,' # tcanlartowdlam
    # data = '0,use,yun,usa,istemal,istemal,potrebi,' # yunsastempot
    data = inputLineEntry
    srcWords = getSourceWords(data)
    engWord = data.split(',')[1]

    population = []
    scoreHistory = []
    scoreHistory2 = []
    wordHistory = []

    # initialize population
    for i in range(popSize):
        instructions = generateNewIndividual()
        newWord = constructWord(srcWords, instructions)
        entry = newWord + ',' + engWord + ',' + ','.join(srcWords) + ',' # should have 7 commas
        score = evaluate(entry)
        individual = [score, entry, instructions]
        population.append(individual)

    creatingFromScratch = False # initialize for random decision

    # randomize whether initialization includes previous best-scorer in this session's population
    # (later will still compare to it anyways to check for improved score)
    cointoss = randint(0,1)
    if cointoss == 0:
        creatingFromScratch = True
    elif cointoss == 1:
        # make use of preexisting best-scorer saved externally
        if scorers != {}:
            generatedBestScorer = population[0]
            bestScorerKey = getEntryIdentifier(generatedBestScorer)
            if bestScorerKey in scorers:
                scorer = scorers[bestScorerKey]
                # prevBestScore = int(float(scorer.split(', ')[0].replace('[','')))
                prevBestEntry = scorer.split(', ')[1].replace('\'','')
                prevBestScore = evaluate(prevBestEntry)
                prevBestInstruction = ast.literal_eval(scorer.replace('\n','').split(', ',2)[2][:-1]) # [:-1] to remove final ']'
                prevBest = [prevBestScore,prevBestEntry,prevBestInstruction]
                # include preexisting best-scorer saved externally
                population.append(prevBest)

    # starting "from scratch"? allow more generations before comparing with best scorer
    adjustForFromScratch = 1
    if creatingFromScratch:
        adjustForFromScratch = 2

    # train
    for i in range(numGenerations * adjustForFromScratch):
        # sort by score
        sortByScore(population)
        # printOnSepLines(population)

        # update score history after sorting by score
        updateScoreHistory()

        # update word history after sorting by score
        if i%epochMilestone == 0:
            updateWordHistory()

        # remove lower scorers
        halfOfPop = popSize//2
        for i in range(halfOfPop):
            population.pop()

        # add new random individuals to population
        halfOfHalf = halfOfPop//2
        for i in range(halfOfHalf):
            instructions = generateNewIndividual()
            newWord = constructWord(srcWords, instructions)
            entry = newWord + ',' + engWord + ',' + ','.join(srcWords) + ',' # should have 7 commas
            score = evaluate(entry)
            individual = [score, entry, instructions]
            population.append(individual)

        # remove duplicate individuals
        mySet = []
        for indiv in population:
            if indiv not in mySet:
                mySet.append(indiv)
        duplicatesToReplace = len(population) - len(mySet)
        population = list(mySet)

        # add variations of existing individuals in population
        restOfPop = halfOfPop - halfOfHalf + duplicatesToReplace
        for i in range(restOfPop):
            index = randint(0,len(population)-1) # 0 to len(population)-1 includes top scorer
            instructions_toMutate = list(population[index][2]) # hacky: use list() to make an actual copy, not a reference
            if len(instructions_toMutate) == 0:
                instructions_toMutate = ''
            else:
                for mutation in range(3):
                    # mutate instructions (replace/add/delete) at index_toMutate:
                    decide1replace2add3delete = randint(1,3)
                    index_toMutate = randint(0,len(instructions_toMutate)) # not -1 so that can add at end
                    atEnd = index_toMutate == len(instructions_toMutate)
                    if decide1replace2add3delete == 1 and instructions_toMutate:
                        if atEnd: # check if 1 out of range
                            index_toMutate -= 1
                        # replace instruction at index_toMutate
                        instruction_toReplace = possibleInstructions[ randint(0,len(possibleInstructions)-1) ]
                        instructions_toMutate[index_toMutate] = instruction_toReplace
                    elif decide1replace2add3delete == 2:
                        # add instruction at index_toMutate
                        instruction_toAdd = possibleInstructions[ randint(0,len(possibleInstructions)-1) ]
                        instructions_toMutate.insert(index_toMutate, instruction_toAdd)
                    elif decide1replace2add3delete == 3 and instructions_toMutate:
                        if atEnd: # check if 1 out of range
                            index_toMutate -= 1
                        # delete instruction at index_toMutate
                        del instructions_toMutate[index_toMutate]
            instructions = instructions_toMutate
            newWord = constructWord(srcWords, instructions)
            entry = newWord + ',' + engWord + ',' + ','.join(srcWords) + ',' # should have 7 commas
            score = evaluate(entry)
            individual = [score, entry, instructions]
            population.append(individual)

    # sort by score
    sortByScore(population)

    # get the best so far
    bestSoFar = getBestAlgo()
    scoreBestSoFar, entryBestSoFar, instructionsBestSoFar = bestSoFar

    if debugOn: # suppress debug output, especially if other python file is calling this function
        printDebug('\nFINAL CANDIDATES:')
        printOnSepLines(population)

        printDebug('\nBEST SO FAR:')
        printDebug(bestSoFar)

        printDebug('\nORIGINALLY:')
        original = 'yunsastempot,use,yun,usa,istemal,istemal,potrebi,'
        # original = 'tcanlartowdlam,long,tcan,largo,lamba,towil,dlini,'
        printDebug(evaluate(original), original)

        printDebug('\nIF USE BEST SO FAR ON DIFFERENT INPUT:')
        data = '+,long,tcan,largo,lamba,towil,dlini,' # can use this to check still outputs same newWord
        # data = '0,use,yun,usa,istemal,istemal,potrebi,'
        srcWords = getSourceWords(data)
        engWord = data.split(',')[1]
        newWord = constructWord(srcWords, instructionsBestSoFar)
        entry = newWord + ',' + engWord + ',' + ','.join(srcWords) + ',' # should have 7 commas
        score = evaluate(entry)
        individual = [score, entry, instructionsBestSoFar]
        printDebug(individual)

        original = 'tcanlartowdlam,long,tcan,largo,lamba,towil,dlini,'
        printDebug('vs')
        printDebug(evaluate(original), original)

        # show word history
        printDebug('\nBEST SCORERS AT EVERY '+str(epochMilestone)+' GENERATIONS:')
        printDebug(wordHistory)

    # store best scorer in scorers dictionary, to save externally (ctrl+f "with open" and "'a'" in the calling .py file)
    bestSoFar_id = getEntryIdentifier(bestSoFar)
    bestSoFar_scr = getEntryScore(bestSoFar)
    bestSoFar_word = entryBestSoFar.split(',')[0].replace('\'','')

    if bestSoFar_id not in scorers: #or scorers == {}
        # add new entry
        scorers[bestSoFar_id] = str(bestSoFar)
        countNew += 1
        print('NEW WORDS:',countNew,bestSoFar_word)
    else:
        # replace with better scorer out of previous or just generated one
        scorer = scorers[bestSoFar_id]
        prevScorer_scr = getEntryScore(scorer)
        prevScorer_word = scorer.split(',')[1].replace(' \'','')
        # include only better scorer
        if bestSoFar_scr > prevScorer_scr:
            scorers[bestSoFar_id] = str(bestSoFar)
            print(prevScorer_word + ' -> ')
            print(bestSoFar)
            countNew += 1
            print('NEW WORDS:',countNew) # ,bestSoFar_word)
            scoreImprovements += bestSoFar_scr - prevScorer_scr
            print('SCORE IMPROVEMENT SUM:',scoreImprovements)
        else: # prevScorer_scr > bestSoFar_scr
            # will return, whether or not actually scored better than before
            bestSoFar_word = prevScorer_word
    # return bestSoFar_word whether or not actually scored better than before
    # but always return updated scorers dictionary too
    return [bestSoFar_word, scorers]

if __name__ == '__main__': # run the following if running this .py file directly:
    inputLineEntry = '0,use,yun,usa,istemal,istemal,potrebi,' # yunsastempot
    # get the so far best scorers into a dictionary, in case we need to update it
    scorersFile = 'best-scorers.txt'
    scorers = {}
    with open(scorersFile,'r') as f:
        for entry in f:
            if entry != '\n': # ignore empty lines (some editors automatically add them)
                keyEng = entry.split(',')[2]
                scorers[keyEng] = entry

    wordCreated = createWord( inputLineEntry, scorers, scorersFile )
    # inputLineEntry = '0,be,ca,esta,ho,kana,bi,' # castahokanbi
    # wordCreated = createWord(inputLineEntry)
    print('\nCREATED WORD:')
    print(wordCreated)
    # print(wordCreated + ' ' + str(evaluate(wordCreated + inputLineEntry[1:])))
    if debugOn:
        title = 'Score History'
        # plot score over generations:
        plt.plot(scoreHistory)
        # show second-bests if external scorer was put in population
        if not creatingFromScratch:
            title += ' - USING PREVIOUS BEST SCORER'
            plt.plot(scoreHistory2)
        plt.title(title)
        plt.show()
