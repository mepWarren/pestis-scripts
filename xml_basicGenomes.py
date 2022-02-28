#Author: Lizzy Porter
#Date: 5/20/2021
#This program takes MAUVE output files and assemble different genomes. 
import sys, re


numberOfFiles = 2
fastaFileName = "bobChunk"


def main():
    print("Running...")
    divideUp()
    
def divideUp(): #Parse out each homol chunk
    #print("Tesing divide Up")

    countOfNewFiles = 0
    headerInfo = ""
    seqInfo = ""
    try: 
        with open(fastaFileName, "r") as data: 
            for line in data:
                if "#" in line: #Gets the header information
                   headerInfo = headerInfo + line
                else:   #Or sequence infomation
                    seqInfo = seqInfo + line
            parseTileInfo(headerInfo.strip())
            parseSeqInfo(seqInfo.strip())
    except IOError: 
        print("Could not read file: ", fastaFileName)
    data.close() #When do I want to close this file?

def parseTileInfo(titleInfo): #gets the names of all the files to build
    count = 0
    filesBuild = 0  
    for line in titleInfo.splitlines():
        count += 1
        if (count % 2 == 0) & (count < numberOfFiles * 2 + 2):  #Get names
            portion_of_line = re.split(' +', line)
            sequenceInfo = line.split()
            name = sequenceInfo[1]
            buildFiles(name)
            filesBuild += 1
    if(filesBuild != numberOfFiles):
        print("Error message: you built the wrong number of files")
           
def parseSeqInfo(seqInfo):#seperates = by =
    print("Parsed info")
    homolChunk = ""
    for line in seqInfo.splitlines():
        if "=" not in line: 
            homolChunk = homolChunk + line + "\n"               
        else:   
            countCheck(homolChunk.strip())
            homolChunk = ""

def countCheck(chunk): 
#Counts how many sequences are in each homol chunk
    if (chunk.count(">") == numberOfFiles): 
        parseHomolChunk(chunk + "=")  
    else:    
        print("Error message: homol chunk not in all files, not saved")

def parseHomolChunk(homochunk):
    name = ""
    seq = ""
    endOfSeq = False
    for line in homochunk.splitlines():
        if ">" in line:
            if seq != "":
                addToFile(name, seq)
                seq = ""
            name = line.split()[3:][0] #1 is the location 3 is the name
            
        elif "=" in line:
                lastLine = line [:-1]
                seq = seq + lastLine
                addToFile(name, seq)
                name = ""
                seq = ""
        else :
            seq = seq + line
            

def addToFile(name, seq): #Adds homol chunks to the specific file
    tempFile = open(name, "a") #Open the right file
    readySeq = cleanUpSeq(seq)
    tempFile.write(readySeq)
    tempFile.close()
  
def cleanUpSeq(seq):
    seq = " ".join(seq.split()) #Cleans up by removing WS and NL
    seq = seq.strip() #Removes end of line char
    seq = seq.replace(" ","") #Removes White space
    return seq


def buildFiles(fileName): #Builds new files 
    newFile = open(fileName, "w")
    newFile.write(">" + fileName + '\n')
    newFile.close()


#Application entry point
main()
