import sys
import unigramModel as unigram
import bigramModel as bigram
import baselineModel as baseline
import fileinput
import glob, os


genreList = ["history","science","crime","law","childrenslit"]
historyFiles = []
crimeFiles = []
scienceFiles = []
lawFiles = []
#testFiles = []
childrenslitFiles = []


os.chdir("history")
for file in glob.glob("*.txt"):
    historyFiles.append("history/" + file)


os.chdir("..")
os.chdir("science")
for file in glob.glob("*.txt"):
    scienceFiles.append("science/" + file)

os.chdir("..")
os.chdir("childrenslit")
for file in glob.glob("*.txt"):
    childrenslitFiles.append("childrenslit/" + file)

os.chdir("..")
os.chdir("law")
for file in glob.glob("*.txt"):
    lawFiles.append("law/" + file)

os.chdir("..")
os.chdir("crime")
for file in glob.glob("*.txt"):
    crimeFiles.append("crime/" + file)
    
os.chdir("..")
#os.chdir("testingfiles")
#for file in glob.glob("*.txt"):
#    testingFiles.append

testingFiles = []
os.chdir("testingfiles")
for file in glob.glob("*.txt"):
    string = "testingfiles/" + file
    tokens = file.split("-")
    genre = tokens[0]
    testingFiles.append((genre,string))
    
os.chdir("..")

fileList = []
#fileList.append(("test",testFiles))
fileList.append(("history",historyFiles))
fileList.append(("science",scienceFiles))
fileList.append(("crime",crimeFiles))
fileList.append(("law",lawFiles))
fileList.append(("childrenslit",childrenslitFiles))

def incorrectArgs():
    
    print "Incorrect Number of Arguments"
    print "Argument Format:"
    print "\t Argument One:"
    print "\t\t -0 : baseline probability"
    print "\t\t -1 : unigram probability (stage 1)"
    print "\t\t -2 : bigram probability (stage 2)"
    print "\t Argument Two:"
    print "\t\t -calc : Calculate the Model"
    print "\t\t -import : Import the Model"
    
    
if len(sys.argv) == 3:
    foundModel = False
    
    
    argone = str(sys.argv[1])
    argtwo = str(sys.argv[2])
    
    
    #print argone is sys.argv[1]
    #print "-0" is sys.argv[1]
    
    if argone == '-0':
        model = baseline
        foundModel = True
    elif argone == '-1':
        model = unigram
        foundModel = True
    elif argone == '-2':
        model = bigram
        foundModel = True
    else:
        incorrectArgs()
        
    if foundModel and argtwo == "-calc":
        model.calculate(fileList, genreList)
        model.test(testingFiles, genreList)
    elif foundModel and argtwo == "-import":
        model.test(testingFiles, genreList)
    else:
        incorrectArgs()
else:
    incorrectArgs()