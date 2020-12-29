# TODO Documentation


def charToIndex(ch):
    if ch == ' ':
        return 26
    else:
        return ord(ch) - ord('a')


def indexToChar(index):
    return chr(index + ord('a'))


def scoreAfterSwap(score, index):
    if index < 5:
        return score - (5 - index)
    return score - 1


def scoreAfterSub(score, index):
    if index < 5:
        return score - ((5 - index) * 2)
    return score - 2


def scoreAfterAdd(score, index):
    if index < 5:
        return score - ((5 - index) * 2)
    return score - 2


def addChar(trieNode, i, term, curr, score):
    return searchCompletionsNodes(trieNode, indexToChar(i) + term[curr + 1:], False, scoreAfterAdd(score, curr))


def subChar(trieNode, term, index, score):
    return searchCompletionsNodes(trieNode, term[index + 2:], False, scoreAfterSub(score, index))


def swapChar(trieNode, swapChar, term, index, score):
    return searchCompletionsNodes(trieNode, indexToChar(swapChar) + term[index + 2:], False,
                                  scoreAfterSwap(score, index))


def searchWithOneMistake(trieNode, term, curr, score):
    result = []
    if curr == 0:
        for i in range(27):
            result += addChar(trieNode, i, term, curr - 1, score)
            result += swapChar(trieNode, i, term, curr -1, score)
        result += subChar(trieNode, term, curr -1, score)
    else:
        for i in range(27):
            result += addChar(trieNode, i, term, curr, score)
            result += swapChar(trieNode, i, term, curr, score)
        result += subChar(trieNode, term, curr, score)
    return result


def reachEnd():
    pass


# find all nodes accept the search string
def searchCompletionsNodes(trieNode, key: str, firstTime=True, score=0):
    result = []
    currNode = trieNode

    for i, ch in enumerate(key):
        index = charToIndex(ch)
        if currNode["children"][index] is not None:  # if we can continue
            if firstTime:
                result += searchWithOneMistake(currNode, key, i, score - 2)
            currNode = currNode["children"][index]
            score += 2
        else:
            if firstTime:
                result += searchWithOneMistake(currNode, key, i, score - 2)
            return result

    result += [(currNode, score)]
    return result


def findNodeMatches(trieNode):  # return all sentences begining in this node
    result = []
    if trieNode["indexesOfFullSentence"]:
        result += trieNode["indexesOfFullSentence"]
    for index in range(27):
        if trieNode["children"][index]:
            result += findNodeMatches(trieNode["children"][index])
    return result


def getNode():
    return {
        "children": [None] * 27,
        "indexesOfFullSentence": []
    }


def getTrie():
    return {"root": getNode()}


def insertTrie(trie, term, indexOfFullSentence):
    currNode = trie.get("root")

    for ch in term:
        index = charToIndex(ch)
        if not currNode["children"][index]:
            currNode["children"][index] = getNode()
        currNode = currNode["children"][index]

    currNode["indexesOfFullSentence"].append(indexOfFullSentence)