#Author: Lizzy Porter
#Date: 5/20/2021
#This program takes MAUVE output files and separates the homologous sequence. 
import sys, re


numberOfFiles = 24
fastaFileName = "NMsamples.xmfa"

def main():
    print("testing main")
    divideUp()
    
def divideUp(): #Parse out each homol chunk
    #print("Tesing divide Up")

    countOfNewFiles = 0
    headerInfo = ""
    seqInfo = ""
    try: 
        with open(fastaFileName, "r") as data: 
            for line in data:#Gets the header information
                if "#" in line: 
                   headerInfo = headerInfo + line
                else: 
                    seqInfo = seqInfo + line
            parseTileInfo(headerInfo.strip())
            parseSeqInfo(seqInfo.strip())
    except IOError: 
        print("Could not read file:", fastaFileName)
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
        print("Error message: you build the wrong number of files, skipped")
           
def parseSeqInfo(seqInfo):#seperates = by =
   # print("Parsing seq info")
    homolChunk = ""
    for line in seqInfo.splitlines():
        if "=" not in line: 
            homolChunk = homolChunk + line + "\n"               
        else:   
            countCheck(homolChunk.strip())
            homolChunk = ""

def countCheck(chunk): 
#Counts how many sequences are in each homol chunk
    #print("Count Check")
    if (chunk.count(">") == numberOfFiles): 
        parseHomolChunk(chunk + "=")  
    else:    
        print("Error message: you don't have the right number of files")

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
                addToFile(name, seq)
                name = ""
                seq = ""
        else :
            seq = seq + line
            

def addToFile(name, seq): #Adds homol chunks to the specific file
  #  print("Add chunk to files")
    tempFile = open(name, "a") #Open the right file
    cleanSeq = cleanUpSeq(seq)
    tempFile.write(cleanSeq)
    tempFile.close()
  
def cleanUpSeq(seq):
    seq = " ".join(seq.split()) #Cleans up by removing WS and NL
    seq = seq.strip() #Removes end of line char
    seq = seq.replace(" ","") #Removes White space
    return seq


def buildFiles(fileName): #Builds new files 
    #print("Build the files")
    newFile = open(fileName, "w")
    newFile.write(">" + fileName + '\n')
    newFile.close()


#Application entry point
main()
