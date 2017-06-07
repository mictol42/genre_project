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
    
    unigramPairs = []
    
    for pair in fileList:
        
        genre = pair[0]
        list = pair[1]
    
        count = {}
        count["<UNK>"] = 0
    
        for file in list:
            inputs = readFile(file)
            
            for line in inputs:
                tokens = line.split()
            
                # using the method of finding UNK as replace the first occurence
                # of any word in a training set with UNK
                for token in tokens:
                    if not token in count:
                        count[token] = 1
                        count["<UNK>"] += 1
                    else:
                        count[token] += 1
        
        sum = 0.0

        #for token in count:
        #    if not token is "<UNK>":
        #        count[token] -= 1
            
        
        for token in count:
            sum = sum + count[token]
        
        unigram = {}
        
        #print genre
        for token in count:
            #if count[token] > 0:
            prob = count[token] / sum
            
            unigram[token] = prob
            
            #if token is "<UNK>":
            #    print unigram[token]
        
        unigramPairs.append((genre,unigram))
    
    pickle.dump(unigramPairs, open("unigram.p","wb"))
    return True

def test(testingFiles, genreList): 
    
    #unigramPairs = unigramCounter()
    unigramPairs = pickle.load( open("unigram.p","rb"))
    
    f = open("unigramOutput.txt","w")
    
    f.write("Testfile Name \t\t\t Actual Genre \t\t Predicted Genre\n")
    
    for test in testingFiles:
        #print "Results for " + test[1]
        #print "\tActual Genre: " + test[0]
        
        inputs = readFile(test[1])
        
        unigramResults = {}
        
        for unigram in unigramPairs:
            model = unigram[1]
            
            prob = math.log(1.0)
            for line in inputs:
                words = line.split()
                for word in words:
                    if word in model:
                        prob = prob + math.log(model[word])
                    #elif "<UNK>" in model:
                    #    prob = prob + math.log(model["<UNK>"])
                    #else:
                    #    prob = 0
            unigramResults[unigram[0]] = prob
        
        
        
        max = float("-inf")
        trueResult = "none"
        for result in unigramResults:
        
            prob = unigramResults[result]
            #print result
            #print str(prob) + " > " + str(max)
            #print prob
            #print prob > max
            if prob > max:
                max = prob
                trueResult = result
                #print "here"
            #print "\t" + result + " log probability: " + str(unigramResults[result]) 
            #print "\t" + result + " \t\t " + str(unigramResults[result]) 
            
        name = test[1]
        actualGenre = test[0]
        f.write(name + "\t\t" + actualGenre + "\t\t" + trueResult + "\n")
        
        #print "\tPredicted Genre: " + trueResult
        #print "\tLog Probability: " + str(unigramResults[trueResult])
            
