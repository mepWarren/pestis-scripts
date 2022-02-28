#Author: Lizzy Porter
#Date: 5/20/2021
#This program takes MAUVE output files and assemble different genomes. 
import sys, re


numberOfFiles = 23
fastaFileName = "Mauve_chunk_1-4653775"


def main():
    print("Running...")
    divideUp()
    
def divideUp(): #Parse out each homol chunk
    headerInfo = ""
    seqInfo = ""
    try: 
        with open(fastaFileName, "r") as data:
            for line in data:
                if "#" in line: #Gets the header information
                   headerInfo = headerInfo + line
                else:   #Sequence infomation
                    seqInfo = seqInfo + line               
            parseHomolChunk(seqInfo)  
    except IOError: 
        print("Could not read file: ", fastaFileName)
    data.close() 

def parseHomolChunk(homochunk):
    #Pulls out the homologous chunks
    name = ""
    seq = ""
    endOfSeq = False
    for line in homochunk.splitlines():
        if ">" in line:
            if seq != "":
                buildFiles(name, seq)
                seq = ""
            name = line.split()[3:][0]
        elif "=" in line:
                lastLine = line [:-1]
                seq = seq + lastLine
                buildFiles(name, seq)
                name = ""
                seq = ""
        else :
            seq = seq + line
    
def cleanUpSeq(seq): #Cleans up by removing WS, and end of line char
    seq = " ".join(seq.split()) 
    seq = seq.strip() 
    seq = seq.replace(" ","") 
    return seq

def buildFiles(fileName, seq): #Builds new files 
    readySeq = cleanUpSeq(seq)
    newFile = open(fileName, "w")
    newFile.write(">" + fileName + '\n')
    newFile.write(readySeq)
    newFile.close()


#Application entry point
main()
