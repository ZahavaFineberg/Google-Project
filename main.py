import json
from search import get_best_k_completions


def isEnglishLetter(letter):
    return ('a' <= letter <= 'z') or ('A' <= letter <= 'Z') or (letter == " ")


def isSecondSpace(subSentence):
    return len(subSentence) > 0 and subSentence[-1] == " "


def replacePunctuation(sentence):
    fixedSentence = ""
    for letter in sentence:
        if isEnglishLetter(letter):
            if letter != " ":
                fixedSentence += letter.lower()
            elif not isSecondSpace(fixedSentence):
                fixedSentence += " "
    return fixedSentence


print("loading data from \"trie.json\"...")
with open('trie.json') as trie_json:
    trie = json.load(trie_json)

print("loading data from \"completed_sentences.json\"...")
with open('completed_sentences.json') as completed_sentences_json:
    completed_sentences = json.load(completed_sentences_json)


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

term = ""
while term != "#":
    term = input("You can do a Google search or write a URL\n")
    if (len(term)) > 64:
        print(
            f"\"{term[64:70]}\" (and all the words after it) were not included in the search because we limit the "
            f"queries "
            f"to 64 letters.)")
        term = term[:64]
    if term != "#":
        lst = get_best_k_completions(trie, completed_sentences, replacePunctuation(term))
        if len(lst) > 0:
            print(f"Here are 5 suggestions for {replacePunctuation(term)}:")
            for i in lst:
                print(color.UNDERLINE+color.BLUE+color.BOLD+"sentence:"+color.END, i.completed_sentence[:i.offset]+color.RED+color.BOLD+i.completed_sentence[i.offset:i.offset+len(term)]+color.END+i.completed_sentence[i.offset+len(term):],end=" ")
                print( color.UNDERLINE+color.BLUE+color.BOLD+"source:"+color.END,color.GREEN+ i.source_text+color.END,end=" ")
                print(color.UNDERLINE+color.BLUE+color.BOLD+"offset:"+color.END, color.PURPLE+str(i.offset)+color.END,end=" ")
                print(color.UNDERLINE+color.BLUE+color.BOLD+ "score:"+color.END,color.YELLOW+str( i.score)+color.END)
                print()
        else:
            print("Sorry, We don't have a match for you :(")