#Author: Lizzy Porter
#Date: 7/8/2021
#This program takes GFF file, parses out cdRegions, and  
import sys, re, os


gffFileName = "genomic.gff"

def main():
    print("Running...") 
    starts = []
    ends = []
    myData = openFile()   
    regions = mapAnnotationFile(myData)
    starts = regions[0]
    ends = regions[1]
    whichHomolMatch(starts, ends)
     

def openFile():
    print("Open files...")
    myData = ""
    try: 
        with open(gffFileName, "r") as data: 
            for line in data:
                myData = myData + line
            data.close() #When do I want to close this file?
    except IOError: 
        print("Could not read file: ", gffFileName)
    return(myData)

def mapAnnotationFile(data):
    cdMap = []
    starts = []
    ends = []
    print("Mapping annotation files...")
    cdMap = re.findall('Homology'+ '\s' +"CDS" +'\s'+'[0-9]*'+ '\s'+'[0-9]*', data)
    for i in cdMap:
        cdNum = i.split()
        regions = forwardReverse(cdNum[2], cdNum[3])
        starts.append(regions[0])
        ends.append(regions[1])
    return(starts, ends)
    

def forwardReverse(one, two):
    numOne = int(one)
    numTwo = int(two)
    if numOne < numTwo:
        return(numOne, int(numTwo)-3)
    elif numOne > numTwo:
        return(numTwo, int(numOne)-3)
    else:
        return (numOne, numTwo)     


def whichHomolMatch(starts, ends):
    print("Which files do I want...")
    start = starts
    end = ends    
    for filename in os.listdir('homFiles'):
        mauveFiles = re.findall('[0-9]+', filename) 
        mauveStart = mauveFiles[0]
        mauveEnd = mauveFiles[1]
        for (cdStart, cdEnd) in zip(start, end):
            if int(mauveStart) < int(cdStart) and (int(mauveEnd) > int(cdEnd)):
                geneStart = int(cdStart) - int(mauveStart)
                geneLength = int(cdEnd) - int(cdStart)
                geneEnd = geneStart + geneLength
                nucDiff(filename, geneStart, geneEnd)
              

def nucDiff(fileName, geneStart, geneEnd):
    cdChunk = ""
    header = ""
    seq = ""
    with open("homFiles/" + fileName, "r") as data: 
        for line in data:
            if ">" in line:
                if seq != "":
                    tempSeq = seq[geneStart:geneEnd]
                    cdChunk =  cdChunk + header + "\n" + tempSeq + "\n"
                    seq = ""
                    header = ""
                header = line.strip()
            elif "=" in line:
                seq = seq + line.strip()
                tempSeq = seq[geneStart:geneEnd]
                cdChunk =  cdChunk + header + "\n" + tempSeq
                seq = ""
                header = ""
            else :
                seq = seq + line.strip()
        fileName = str(geneStart) + "_" + str(geneEnd)
        buildFiles(fileName, cdChunk)


def buildFiles(Name, cdChunk): #Builds new files 
    fileName = "CDRegion_CO92_" + str(Name)
    newFile = open(fileName, "w")
    newFile.write(cdChunk)
    newFile.close()


#Application entry point
main()
