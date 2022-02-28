#Author: Lizzy Porter
#Date: 7/8/2021
#This program parses out the slurm for MEME/FEL
import sys, re, os

slurmFile = "slurm_fel.out"
filePath = "/zhome/izy003/runthrough/cdTextFiles/bob/"

def main():
    names = []
    resultPos = []
    resultNeg = []
    pvalue = []

    myData = openFile()
    names = mapFile(myData)
    resultPos = mapResultPos(myData)
    resultNeg = mapResultNeg (myData)
    pvalue = mapPvalue (myData)
    check = dataCheck(len(names), len(resultPos), len(resultNeg), len(pvalue))
    if dataCheck:   
        posRes = parseResultPos(resultPos)
        negRes = parseResulsNeg(resultNeg)
        pVRes = parsePvalue(pvalue)
        parseAll (posRes[1], negRes[1], pVRes[1],names)


def parseAll (posRes, negRes, pVRes, names):
    print("Parsing all...")
    finalPosRes= "No results"
    finalNegRes= "No results"
    finalPValRes= "No results"
    if len(posRes) != 1:
        finalPosRes = getName(posRes, names)
    if len(negRes) != 1:
        finalNegRes = getName(negRes, names)
    if len(pVRes) != 1:
        finalPValRes = getName(pVRes, names)
    buildFiles("Pos_Selection.txt", finalPosRes)
    buildFiles("Neg_Selection.txt", finalNegRes)
    buildFiles("P_Val_Selection.txt", finalPValRes)


def getName(loc, names):
    output = ["File Name, location"]
    for i in loc:
        if i != "Location:":
            output.append(names[i])
            output.append(i)
           # output.append(change[i])
    return(output)
    #Grab name of file that matches 



def parsePvalue(pvalue):
    loc= ["Location:"]
    result = ["Results:"]
    for i in range(len(pvalue)):
        if pvalue[i] != str(0.1):
            loc.append(i)
            result.append(pvalue[i])
    return(result, loc)

def parseResulsNeg(resultNeg):
    loc= ["Location:"]
    result = ["Results:"]
    for i in range(len(resultNeg)):
        if (resultNeg[i]) != 0:
            loc.append(i)
            result.append(resultNeg[i])
    return(result, loc)

def parseResultPos(resultPos):
    loc= ["Location:"]
    result = ["Results:"]
    for i in range(len(resultPos)):
        if (resultPos[i]) != 0:
            loc.append(i)
            result.append(resultPos[i])
    return(result,loc)
            

def dataCheck(namesLen, resultPosLen, resultNegLen, pvalueLen):
    print("Checking length...")
    valid = False   
    totalLen = namesLen + resultPosLen + resultNegLen + pvalueLen
    if totalLen/4 == namesLen:
        valid = True
    else:
        valid = False
    return (valid)
                 

def openFile():
    print("Open files...")
    myData = ""
    try: 
        with open(slurmFile, "r") as data: 
            for line in data:
                myData = myData + line
            data.close() #When do I want to close this file?
    except IOError: 
        print("Could not read file: ", slurmFile)
    return(myData)

def mapFile(data):
    print("Mapping files...")
    names = []
    nameMap = re.findall(filePath + '[a-z]*[A-Z]*' + '_' + '[0-9]*', data)
    for i in nameMap:
        nameOnly = i.replace(filePath, "")
        names.append(nameOnly)  
    return(names)


def mapResultPos(data):
    print("Mapping pos results...")
    posResult = []
    results = []
    posResult = re.findall("Found"+"\s"+"_"+ "[0-9]*"+"_" +"\s"+"sites under pervasive positive diversifying", data)
    for i in posResult:
        result1 = i.replace("Found _", "")
        result = result1.replace("_ sites under pervasive positive diversifying", "")
        results.append(int(result))  
    return(results)


def mapResultNeg(data):
    print("Mapping neg results...")
    posResult = []
    results = []
    posResult = re.findall("[0-9]*"+"_" +"\s"+"sites under negative selection", data)
    for i in posResult:
        result = i.replace("_ sites under negative selection", "")
        results.append(int(result))  
    return(results)
   

def mapPvalue(data):
    print("Mapping pvalue results...")
    pvalueString = []
    pvalue = []
    pvalueString = re.findall("sites under negative selection at p"+"\s" +"<=" +"\s"+ "[0-9]*.[0-9*]", data)
    for i in pvalueString:
        result = i.replace("sites under negative selection at p <= ", "")
        pvalue.append(str(result))  
    return(pvalue)


def buildFiles(name, info): #Builds new files 
    newFile = open(name, "w")
    newFile.write(str(info))
    newFile.close() 

#Application entry point

main() 
