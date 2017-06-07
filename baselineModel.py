import random

def calculate(fileList, genreList):
    return True

def test(testingFiles, genreList):

    f = open("baselineOutput.txt","w")
    # Baseline - Random Assignment of Genre
    print "Baseline Model"
    f.write("Testfile Name \t\t\t Actual Genre \t\t Predicted Genre\n") 
    for test in testingFiles:
        #print "Results for " + test[1]
        #print "\tActual Genre: " + test[0]    
        val = random.randrange(0,5)
        predicted = genreList[val]
        #print "\tPredicted Genre: " + predicted
        f.write(test[1] + "\t\t" + test[0] + "\t\t" + predicted + "\n")