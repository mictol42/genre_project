import re
import glob, os
import math
import random
import pickle



def tokenizer(inputs):
    
    for i in range(0,len(inputs)):
        inputs[i] = inputs[i].lower()
    
    abreviations = [("ph.d.", "PHDTEMP"), ("mr.","MRTEMP"), 
        ("mrs.", "MRSTEMPT"), ("ms.", "MSTEMPT")] # assume this file stores more common cases
    
    # replaces all the abbreviations with temporary values
    for abr in abreviations:
        for i in range(0,len(inputs)):
            inputs[i] = inputs[i].replace(abr[0],abr[1])
    
    # replace punctuation with punctuation surronded by spaces
    for i in range(0,len(inputs)):
        inputs[i] = re.sub(r'([^A-Za-z0-9])',' \g<1> ',inputs[i])
    
    # delete extra spaces
    for i in range(0,len(inputs)):
        inputs[i] = re.sub(r'[ ]+',' ',inputs[i])
    
    # substitute back in abbreviations
    for abr in abreviations:
        for i in range(0,len(inputs)):
            inputs[i] = inputs[i].replace(abr[1],abr[0])
    
    return inputs
    
def readFile(fileName):
    
    f = open(fileName,"r")
    
    inputs = []
    
    for line in f:
        inputs.append(line)
    
    inputs = tokenizer(inputs)
    
    return inputs
    
def calculate(fileList, genreList):

    bigramPairs = []
    
    for pair in fileList:
        
        genre = pair[0]
        list = pair[1]
    
        count = {}
        count[("<UNK>","<UNK>")] = 0
        countWords = {}
        countWords["<UNK>"] = 0
        
        for file in list:
            inputs = readFile(file)
            
            foundPrev = False
            for line in inputs:
            
                tokens = line.split()
            
                if not foundPrev:
                    if tokens:
                        prev = tokens.pop(0)
                        foundPrev = True
            
                # using the method of finding UNK as replace the first occurence
                # of any word in a training set with UNK
                for token in tokens:
                    myPair = (prev, token)
                    
                    if not (prev in countWords) and not (token in countWords):
                        count[myPair] = 1
                        count[("<UNK>","<UNK>")] += 1
                        count[(prev,"<UNK>")] = 1
                        count[("<UNK>",token)] = 1
                        countWords[prev] = 1
                        countWords[token] = 1 
                        countWords["<UNK>"] += 2
                    elif not prev in countWords:
                        countWords[prev] = 1
                        countWords[token] += 1
                        countWords["<UNK>"] += 1
                        count[myPair] = 1
                        newPair = ("<UNK>",token)
                        if newPair in count:
                            count[newPair] += 1
                        else:
                            count[newPair] = 1
                    elif not token in countWords:
                        countWords[token] = 1
                        countWords[prev] += 1
                        countWords["<UNK>"] += 1
                        count[myPair] = 1
                        newPair = (prev,"<UNK>")
                        if newPair in count:
                            count[newPair] += 1
                        else:
                            count[newPair] = 1
                    else:
                        countWords[token] += 1
                        countWords[prev] += 1
                        if myPair in count:
                            count[myPair] += 1
                        else:
                            count[myPair] = 1
                    prev = token
                        
        
        #print count
        
        #sum = 0.0
        #for token in count:
        #    sum = sum + count[token]
        
        bigram = {}
        
        #print genre
        for token in count:
            #print token
            Cpair = count[token]
            Cprev = countWords[token[0]]
            prob = 1.0 * Cpair / Cprev
            bigram[token] = prob
        
        # unigram for backup
        sum = 0.0
        for token in countWords:
            sum = sum + countWords[token]
        
        unigram = {}
        
        for token in countWords:
            prob = countWords[token] / sum    
            unigram[token] = prob
            
        bigramPairs.append((genre,bigram,unigram))
    
    pickle.dump(bigramPairs, open("bigram.p","wb"))

def test(testingFiles, genreList): 
    
    bigramPairs = pickle.load( open("bigram.p","rb"))
    
    f = open("bigramOutput.txt","w")
    
    f.write("Testfile Name \t\t\t Actual Genre \t\t Predicted Genre\n") 
    
    for test in testingFiles:
        #print "Results for " + test[1]
        #print "\tActual Genre: " + test[0]
        
        inputs = readFile(test[1])
        
        bigramResults = {}
        
        for bigram in bigramPairs:
            model = bigram[1]
            countWords = bigram[2]
            
            prob = math.log(1.0)
            foundPrev = False
            for line in inputs:
                words = line.split()
                if not foundPrev:
                    if inputs:
                        prev = words.pop(0)
                        foundPrev = True
                for word in words:
                    
                    if prev in countWords:
                        if word in countWords:
                            myPair = (prev,word)
                        else:
                            myPair = (prev,"<UNK>")
                    elif word in countWords:
                        myPair = ("<UNK>",word)
                    else:
                        myPair = ("<UNK>","<UNK>")
                    
                    if myPair in model:
                        prob = prob + math.log(model[myPair])
                    else:
                        
                        if word in countWords:
                            prob = prob + math.log(countWords[word])
                        else:
                            prob = prob + math.log(countWords["<UNK>"])
                        
                    
            bigramResults[bigram[0]] = prob
        
        max = float("-inf")
        trueResult = "none"
        for result in bigramResults:
        
            prob = bigramResults[result]
            if prob > max:
                max = prob
                trueResult = result
            
        name = test[1]
        actualGenre = test[0]
        f.write(name + "\t\t" + actualGenre + "\t\t" + trueResult + "\n")
        #print bigramResults[trueResult]

    
    