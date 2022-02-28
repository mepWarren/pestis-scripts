#Author: Lizzy Porter
#Date: 7/8/2021
#This program parses out the slurm for MEME/FEL
import sys, re, os

slurmFile = "slurm_meme.out"
filePath = "/zhome/izy003/runthrough/cdTextFiles/for/bobMeme/"

def main():
    names = []
    resultPos = []
    resultNeg = []
    pvalue = []
    myData = openFile()
    names = mapFile(myData)
    resultEpi = mapResult(myData)
    if len(names) == len(resultEpi):
        epiRes = parseResult(resultEpi)
        parseAll (epiRes[1],names)
    else:
        print("The name and results didn't match in length'")


def parseAll (epiRes, names):
    print("Parsing all...")
    finalEpiRes= "No results"
    if len(epiRes) != 1:
        finalEpiRes = getName(epiRes, names)
    buildFiles("episodic_Selection.txt", finalEpiRes)

def getName(loc, names):
    output = ["File Name, location"]
    for i in loc:
        if i != "Location:":
            output.append(names[i])
            output.append(i)
    return(output)

def parseResult (resultEpi):
    loc= ["Location:"]
    result = ["Results:"]
    for i in range(len(resultEpi)):
        if (resultEpi[i]) != 0:
            loc.append(i)
            result.append(resultEpi[i])
    return(result, loc)


def mapResult(data):
    print("Mapping results...")
    posResult = []
    results = []
    epiResult = re.findall("Found"+"\s"+"_"+ "[0-9]*"+"_" +"\s"+"sites under episodic diversifying positive selection at", data)
    for i in epiResult:
        result1 = i.replace("Found _", "")
        result = result1.replace("_ sites under episodic diversifying positive selection at", "")
        results.append(int(result)) 
    return(results)



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


def buildFiles(name, info): #Builds new files 
    newFile = open(name, "w")
    newFile.write(str(info))
    newFile.close()


#Application entry point

main() 
