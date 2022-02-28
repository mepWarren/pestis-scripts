#Author: Lizzy Porter
#Date: 11/29/2021
#This program takes homol chunk and parses out char that are different
#This was used to parse MetaCATS
import sys, re, os


faFile = "cdPlasmid.fa"
output = "output"

def main():
    print("Running...") 
    names = []
    seqInfo = []
    locRet = []
    newSeq = ""
    dataReturn = createMap()
    names = dataReturn[0]
    seqInfo = dataReturn[1]
    locRet = parseOutLoc(seqInfo)
    for i in range(len(seqInfo)):
        #print(names[i])
        newSeq = newSeq + '\n' + str(names[i])+ '\n' 
        for j in range(len(locRet)):         
            pos = int(locRet[j])
            newSeq = newSeq + str(seqInfo[i][pos-1])
    buildFiles("metaOutput", newSeq)


def parseOutLoc(seqInfo):
    print("Parsing out characters that show patterns")
    #160
    tempSeq = ""
    locReturn = []
    for j in range (len(seqInfo[1])):
        for i in range(len(seqInfo)): 
            tempSeq = tempSeq + seqInfo[i][j]
        tempSeqUp = tempSeq.upper()
        seqCount = 0
        if tempSeqUp.count('A') > 2:
            seqCount = seqCount + 1
        if tempSeqUp.count('T') > 2:
            seqCount = seqCount + 1
        if tempSeqUp.count('C') > 2:
            seqCount = seqCount + 1
        if tempSeqUp.count('G') > 2:
            seqCount = seqCount + 1
        if tempSeqUp.count('-') > 2:
            seqCount = seqCount + 1

        if seqCount > 1:
            locReturn.append(j+1)
        tempSeq = ''

    buildFiles("Locations", str(locReturn))
    return(locReturn)


def createMap():
    mapNames = []
    mapSeqs = []
    tempMap = []
    seqInfo = ""
    #Seqs [ [[name][seq info]], [[name][seq info]] ]
    with open(faFile, "r") as data:
        for line in data: 
            if ">" in line or "=" in line:
                if len(seqInfo) > 0:        
                    for char in seqInfo.strip():
                        tempMap.append(char)
                    mapSeqs.append(tempMap) 
                tempMap = []
                seqInfo = ""
                mapNames.append(line.strip())
               # tempMap.append(line.strip())
            else:
                seqInfo = seqInfo + line.strip()
    return(mapNames, mapSeqs)


def buildFiles(Name, seqInfo): #Builds new files 
   # newFile = open(Name)
    newFile = open(output + "/" + Name, "w")
    newFile.write(Name + " pCD plasmid" + '\n')
    newFile.write(seqInfo)
    newFile.close() 



#Application entry point
main()
