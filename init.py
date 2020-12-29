import os
import json
from trie import getTrie, insertTrie


def isEnglishLetter(letter):
    return ('a' <= letter <= 'z') or ('A' <= letter <= 'Z') or (letter == " ")


def isSecondSpace(subSentence):
    return (len(subSentence) > 0 and subSentence[-1] == " ") or (len(subSentence) == 0)


def replacePunctuation(sentence):
    fixedSentence = ""
    counter = 0
    howMuchReplaced = []
    for letter in sentence:
        if isEnglishLetter(letter) and letter != " ":
            fixedSentence += letter.lower()
            howMuchReplaced.append(counter)
        elif isEnglishLetter(letter) and not isSecondSpace(fixedSentence):
            fixedSentence += " "
            howMuchReplaced.append(counter)
        else:
            counter += 1
            howMuchReplaced.append(counter)
    return fixedSentence, howMuchReplaced


def getListOfFiles(dirName):
    listOfFiles = list()
    for (dirPath, dirNames, fileNames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirPath, file) for file in fileNames]
    return listOfFiles


def insertIntoList(lst, sentence, source):
    lst.append([sentence, source])


def insertIntoTrie(trie, sentence, sizeOfCompletedSentences):
    filteredSentence, howMuchReplaced = replacePunctuation(sentence)
    for offset in range(len(filteredSentence)):
        insertTrie(trie, filteredSentence[offset:(offset + 32)],
                   (sizeOfCompletedSentences, offset + howMuchReplaced[offset]))


def insertIntoDataStructure(trie, completed_sentences, sizeOfCompletedSentences, sentence, source):
    insertIntoList(completed_sentences, sentence, source)
    insertIntoTrie(trie, sentence, sizeOfCompletedSentences)


def insert():
    completed_sentences = []
    sizeOfCompletedSentences = 0
    trie = getTrie()
    listOfFiles = getListOfFiles("technology_texts")
    for file in listOfFiles:
        print("loading file", file)
        the_file = open(file)
        sentences = the_file.read().split("\n")
        for sentence in sentences:
            if sentence != "":
                insertIntoDataStructure(trie, completed_sentences, sizeOfCompletedSentences, sentence, file)
                sizeOfCompletedSentences += 1
    print("writing into file \"trie.json\"...")
    with open('trie.json', 'w') as f:
        json.dump(trie, f)
    print("writing into file \"completed_sentences.json\"...")
    with open('completed_sentences.json', 'w') as f:
        json.dump(completed_sentences, f)
    print("Done.")


insert()